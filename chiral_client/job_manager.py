import typing
import os
import json
import pathlib
import tarfile
from .client import ChiralClient
from .ftp import FtpClient
from .app_type import AppType

class JobManager:
    project_name: str
    local_dir: str
    remote_dir: str

    def __init__(self) -> None:
        self.project_name = '.'
        self.local_dir = '.'
        self.remote_dir = '.'

        user_email = os.environ['CHIRAL_USER_EMAIL']
        user_token_api = os.environ['CHIRAL_TOKEN_API']
        chiral_computing_host = os.environ['CHIRAL_DATABASE_ADDR']
        chiral_computing_port = os.environ['CHIRAL_DATABASE_PORT']
        self.chiral = ChiralClient(user_email, user_token_api, chiral_computing_host, chiral_computing_port)
        self.ftp = self.chiral.create_ftp_client()

    def create_remote_dir(self, parent_dir: str, dirname: str):
        self.ftp.cwd_root()
        self.ftp.ftp.cwd(parent_dir)
        if not dirname in self.ftp.ftp.nlst():
            self.ftp.ftp.mkd(dirname)
        self.ftp.cwd_root()

    def remove_remote_dir_all(self, parent_dir: str, dirname: str):
        self.ftp.cwd_root()
        self.ftp.ftp.cwd(parent_dir)
        self.ftp.remove_dir_all(dirname)
        self.ftp.cwd_root()

    def set_remote_dir(self, parent_dir: str, dirname: str):
        self.remote_dir = os.path.join(parent_dir, dirname)

    def set_local_dir(self, local_dir: str):
        self.local_dir = local_dir

    def set_project_name(self, project_name: str):
        self.project_name = project_name

    def upload_files(self, files: typing.List[str]):
        # files: list of file names, without directory
        remote_project_dir = f'{self.remote_dir}/{self.project_name}'
        self.ftp.cwd_root()
        self.ftp.ftp.cwd(remote_project_dir)
        for filename in files:
            self.ftp.upload_file(self.local_dir, filename)
        self.ftp.cwd_root()

    def download_files(self, files: typing.List[str]):
        remote_project_dir = f'{self.remote_dir}/{self.project_name}'
        self.ftp.cwd_root()
        self.ftp.ftp.cwd(remote_project_dir)
        for filename in files:
            self.ftp.download_file(self.local_dir, filename)
        self.ftp.cwd_root()

    def upload_directory(self):
        local_dir = pathlib.Path(self.local_dir).parent.absolute()
        filename = f'{self.project_name}.tar.chiral'
        file_to_upload = os.path.join(local_dir, filename)
        current_local_dir = pathlib.Path(os.curdir).absolute()
        os.chdir(self.local_dir)
        with tarfile.open(file_to_upload, 'w') as tar:
            for fn in os.listdir('.'):
                if os.path.isfile(fn):
                    tar.add(fn)
        self.ftp.cwd_root()
        self.ftp.ftp.cwd(self.remote_dir)
        self.ftp.upload_file(str(local_dir), filename)
        self.ftp.ftp.cwd(self.project_name)
        os.chdir(local_dir)
        os.remove(filename)
        os.chdir(current_local_dir)

    def submit_job_gromacs(self,
        args: str,
        prompts: str,
        input_files: typing.List[str],
        output_files: typing.List[str],
        checkpoint_files: typing.List[str],
        log_files: typing.List[str]
    ) -> str:
        job_id = self.chiral.submit_gromacs_job(work_dir=self.remote_dir, proj_name=self.project_name, is_long=True, args=args.split(' '), prompts=prompts.split(' '), input_files=input_files, output_files=output_files, checkpoint_files=checkpoint_files, log_files=log_files)
        return job_id

    def submit_job_script(self,
        script_file: str,
        apps: typing.List[AppType],
        input_files: typing.List[str],
        output_files: typing.List[str],
        checkpoint_files: typing.List[str],
        log_files: typing.List[str]
    ) -> str:
        apps_grpc = list(map(lambda x: x.to_grpc_type(), apps))
        job_id = self.chiral.submit_job_shell_scripts(work_dir=self.remote_dir, proj_name=self.project_name, script_file=script_file, apps=apps_grpc, prompts=[], input_files=input_files, output_files=output_files, checkpoint_files=checkpoint_files, log_files=log_files)
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
