import shutil
import typing
import os
import pathlib
import tarfile
from .client import ChiralClient
from .app_type import AppType

def require_project(func):
    def wrapper_func(self, *args, **kwargs) -> typing.Any:
        if not self.project:
            raise Exception(f'project is required for JobManager')
        return func(self, *args, **kwargs)
    return wrapper_func

class JobManager:
    project_name: str
    local_dir: str
    remote_dir: str

    def __init__(
        self,
        user_email: str,
        token_api: str,
        chiral_computing_url: str,
        remote_dir: str,
        local_dir: str,
    ) -> None:
        self.chiral = ChiralClient(user_email, token_api, chiral_computing_url)
        self.ftp = self.chiral.create_ftp_client()

        self.remote_dir = remote_dir
        self.create_remote_dir(remote_dir)

        self.local_dir = pathlib.Path(local_dir).absolute()

        self.project = ''

    def create_remote_dir(self, remote_dir: str):
        parent = pathlib.Path(remote_dir).parent
        basename = os.path.basename(remote_dir)
        self.ftp.create_dir(str(parent), basename)

    def remove_remote_dir(self):
        parent = pathlib.Path(self.remote_dir).parent
        basename = os.path.basename(self.remote_dir)
        self.ftp.remove_dir(str(parent), basename)

    def set_project(self, project: str):
        self.project = project
        # create the project directories remotely and locally
        self.ftp.create_dir(self.remote_dir, project)
        if not os.path.exists(os.path.join(self.local_dir, project)):
            os.mkdir(os.path.join(self.local_dir, project))

    @require_project
    def remove_project_remote(self):
        self.ftp.remove_dir(self.remote_dir, self.project)

    @require_project
    def remove_project_local(self):
        if os.path.exists(os.path.join(self.local_dir, self.project)):
            shutil.rmtree(os.path.join(self.local_dir, self.project))

    @require_project
    def upload_files(self, files: typing.List[str]):
        # files: list of file names, without directory
        remote_project_dir = os.path.join(self.remote_dir, self.project)
        self.ftp.cwd_root()
        self.ftp.ftp.cwd(remote_project_dir)
        local_project_dir = os.path.join(self.local_dir, self.project)
        for filename in files:
            self.ftp.upload_file(local_project_dir, filename)
        self.ftp.cwd_root()

    @require_project
    def download_files(self, files: typing.List[str]):
        remote_project_dir = os.path.join(self.remote_dir, self.project)
        self.ftp.cwd_root()
        self.ftp.ftp.cwd(remote_project_dir)
        local_project_dir = os.path.join(self.local_dir, self.project)
        for filename in files:
            self.ftp.download_file(local_project_dir, filename)
        self.ftp.cwd_root()

    @require_project
    def upload_directory(self):
        current_local_dir = pathlib.Path(os.curdir).absolute()
        current_remote_dir = self.ftp.ftp.pwd()

        filename = f'{self.project}.tar.chiral'
        os.chdir(self.local_dir)
        with tarfile.open(filename, 'w') as tar:
            os.chdir(self.project)
            for fn in os.listdir("."):
                if os.path.isfile(fn):
                    tar.add(fn)
        self.ftp.cwd_root()
        self.ftp.ftp.cwd(self.remote_dir)
        self.ftp.upload_file(self.local_dir, filename)
        self.ftp.ftp.cwd(self.project) # trigger extraction

        self.ftp.ftp.cwd(current_remote_dir)
        os.chdir(self.local_dir)
        os.remove(filename)
        os.chdir(current_local_dir)

    @require_project
    def submit_job_gromacs(self,
        args: str,
        prompts: str,
        input_files: typing.List[str],
        output_files: typing.List[str],
        checkpoint_files: typing.List[str],
        log_files: typing.List[str]
    ) -> str:
        job_id = self.chiral.submit_gromacs_job(work_dir=self.remote_dir, proj_name=self.project, is_long=True, args=args.split(' '), prompts=prompts.split(' '), input_files=input_files, output_files=output_files, checkpoint_files=checkpoint_files, log_files=log_files)
        return job_id

    @require_project
    def submit_job_script(self,
        script_file: str,
        apps: typing.List[AppType],
        input_files: typing.List[str],
        output_files: typing.List[str],
        checkpoint_files: typing.List[str],
        log_files: typing.List[str]
    ) -> str:
        apps_grpc = list(map(lambda x: x.to_grpc_type(), apps))
        job_id = self.chiral.submit_job_shell_scripts(work_dir=self.remote_dir, proj_name=self.project, script_file=script_file, apps=apps_grpc, prompts=[], input_files=input_files, output_files=output_files, checkpoint_files=checkpoint_files, log_files=log_files)
        return job_id

    def cancel_job(self, job_id: str):
        self.chiral.cancel_job(job_id)

    def get_job_status(self, job_id: str) -> str:
        status = self.chiral.get_job_status([job_id])
        return status[job_id][1:-1] # remove quote

    def get_log_files(self, job_id: str):
        self.chiral.get_log_files(job_id)

    def wait_until_completion(self, job_id: str):
        self.chiral.wait_until_completion(job_id=job_id)

    def check_credit_points(self) -> float:
        return self.chiral.check_credit_points()
