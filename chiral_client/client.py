import shutil
import typing
import os
import pathlib
import tarfile
from .chiral import ChiralClient
from .app_type import AppType
from .ftp import ftp_connect

def require_project(func):
    def wrapper_func(self, *args, **kwargs) -> typing.Any:
        if not self.project:
            raise Exception(f'project is required for JobManager')
        return func(self, *args, **kwargs)
    return wrapper_func

class Client:
    project: str
    local_dir: str
    remote_dir: str

    def __init__(
        self,
        user_email: str,
        token_api: str,
        remote_dir: str,
        local_dir: str,
        chiral_computing_url: str = 'api.chiral.one',
    ) -> None:
        """
        Initialize a Client instance

        Parameters:
        - user_email: Email address of the user account registered at https://cloud.chiral.one.
        - token_api: Token obtained from the "Profile" page after logging into https://cloud.chiral.one.
        - remote_dir: Directory of the remote storage. It will be created if it does not exist.
        - local_dir: Directory of the local storage. The user is responsible for ensuring its existence.
        """
        self.chiral = ChiralClient(user_email, token_api, chiral_computing_url)
        self.ftp = self.chiral.create_ftp_client()

        self.set_remote_dir(remote_dir)
        self.set_local_dir(local_dir)
        self.project = ''

    def _create_remote_dir(self):
        parent = pathlib.Path(self.remote_dir).parent
        basename = os.path.basename(self.remote_dir)
        with ftp_connect(self.ftp) as ftp:
            ftp.create_dir(str(parent), basename)

    def set_remote_dir(self, remote_dir: str):
        """
        Change the remote directory of the Client.

        Parameters:
        - remote_dir: Directory of the remote storage.
        """
        self.remote_dir = remote_dir
        self._create_remote_dir()

    def set_local_dir(self, local_dir: str):
        """
        Change the local directory of the Client.

        Parameters:
        - local_dir: Directory of the local storage.
        """
        self.local_dir = pathlib.Path(local_dir).absolute()

    def remove_remote_dir(self, parent_dir: str, dirname: str):
        """
        Removes a directory from the remote storage.

        Parameters:
        - parent_dir (str): The directory path where the directory to be removed exists.
        - dirname (str): The name of the directory to be removed.
        """
        with ftp_connect(self.ftp) as ftp:
            ftp.remove_dir(parent_dir, dirname)

    def set_project(self, project: str):
        """
        Set the current project.
        The remote directory for the project will be remote_dir/project,
        and the local directory for the project will be local_dir/project.
        Parameters:
          project (str): The name of the current project.
        """
        self.project = project

    @require_project
    def create_project_remote(self):
        """
        Create the remote directory for the current project.
        The directory will be remote_dir/project.
        """
        with ftp_connect(self.ftp) as ftp:
            ftp.create_dir(self.remote_dir, self.project)

    @require_project
    def remove_project_remote(self):
        """
        Remove the remote directory for the current project
        """
        with ftp_connect(self.ftp) as ftp:
            ftp.remove_dir(self.remote_dir, self.project)

    @require_project
    def remove_project_local(self):
        if os.path.exists(os.path.join(self.local_dir, self.project)):
            shutil.rmtree(os.path.join(self.local_dir, self.project))

    @require_project
    def upload_files(self, files: typing.List[str]):
        """
        Upload files from the local project directory to the remote project directory.
        Parameters:
          files (list of str): List of file names without directory prefix.
        """
        with ftp_connect(self.ftp) as ftp:
            remote_project_dir = os.path.join(self.remote_dir, self.project).replace('\\', '/')
            ftp.ftp.cwd(remote_project_dir)
            local_project_dir = os.path.join(self.local_dir, self.project)
            for filename in files:
                ftp.upload_file(local_project_dir, filename)

    @require_project
    def download_files(self, files: typing.List[str]):
        """
        Download files from the remote project directory to the local project directory.
        Parameters:
          files (list of str): List of file names without directory prefix.
        """
        with ftp_connect(self.ftp) as ftp:
            remote_project_dir = os.path.join(self.remote_dir, self.project).replace('\\', '/')
            ftp.ftp.cwd(remote_project_dir)
            local_project_dir = os.path.join(self.local_dir, self.project)
            for filename in files:
                ftp.download_file(local_project_dir, filename)

    @require_project
    def upload_directory(self):
        """
        Upload the entire local project directory to the remote storage space.
        If the remote project directory exists, it will be renamed with a sequential number.
        """
        current_local_dir = pathlib.Path(os.curdir).absolute()
        filename = f'{self.project}.tar.chiral'
        os.chdir(self.local_dir)
        with tarfile.open(filename, 'w') as tar:
            os.chdir(self.project)
            for fn in os.listdir("."):
                if os.path.isfile(fn):
                    tar.add(fn)

        with ftp_connect(self.ftp) as ftp:
            ftp.cwd_root()
            ftp.ftp.cwd(self.remote_dir)
            ftp.upload_file(self.local_dir, filename)
            ftp.ftp.cwd(self.project) # trigger extraction

        # self.ftp.ftp.cwd(current_remote_dir)
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
        """
        Submit a job of a Gromacs command.
        Parameters:
          args (str): The argument string.
          prompts (str): The prompts to be input, separated by space in a string.
          input_files (list of str): Files to be downloaded by the computing server before starting the computation.
          output_files (list of str): Files to be uploaded to the remote storage after the completion of the computation.
          checkpoint_files (list of str): Files to be uploaded to the remote storage every 1 hour.
          log_files (list of str): Extra log files in addition to job_id.out and job_id.err.
        Returns:
          str: A string representing the ID of the job.
        """
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
        """
        Submit a job to run a script file.
        Parameters:
          script_file (str): The name of the script file.
          apps (str): Applications required by the script file.
          input_files (list of str): Files to be downloaded by the computing server before starting the computation.
          output_files (list of str): Files to be uploaded to the remote storage after the completion of the computation.
          checkpoint_files (list of str): Files to be uploaded to the remote storage every 1 hour.
          log_files (list of str): Extra log files in addition to job_id.out and job_id.err.
        Returns:
          str: A string representing the ID of the job.
        """
        apps_grpc = list(map(lambda x: x.to_grpc_type(), apps))
        job_id = self.chiral.submit_job_shell_scripts(work_dir=self.remote_dir, proj_name=self.project, script_file=script_file, apps=apps_grpc, prompts=[], input_files=input_files, output_files=output_files, checkpoint_files=checkpoint_files, log_files=log_files)
        return job_id

    def cancel_job(self, job_id: str):
        """
        Cancel a job.
        Parameters:
          job_id (str): The ID of the job to be canceled.
        """
        self.chiral.cancel_job(job_id)

    def get_job_status(self, job_id: str) -> str:
        """
        Get the status of a job.
        Parameters:
          job_id (str): The ID of the job.
        Returns:
          str: The status of the job.
        """
        status = self.chiral.get_job_status([job_id])
        return status[job_id][1:-1] # remove quote char ""

    def request_log_files(self, job_id: str):
        """
        Ask for the latest log files of a job.
        The log files will be ready within 2 seconds in the remote storage
        after the computing server receives the request and uploads the log files.
        Parameters:
            job_id (str): The ID of the job.
        """
        self.chiral.get_log_files(job_id)

    def wait_until_completion(self, job_id: str):
        """
        Check the job status and wait until the job is completed, either with success or with error.
        Parameters:
          job_id (str): The ID of the job.
        """
        self.chiral.wait_until_completion(job_id=job_id)

    def check_credit_points(self) -> float:
        """
        Check the point balance of the current user.
        """
        return self.chiral.check_credit_points()
