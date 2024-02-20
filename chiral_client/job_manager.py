import typing
import os
import json
import pathlib
from .client import ChiralClient
from .ftp import FtpClient

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

    def ensure_connection(self):
        self.ftp.cwd_root()

    def create_remote_dir(self, remote_dir: str):
        self.ftp.cwd_root()
        if not remote_dir in self.ftp.ftp.nlst():
            self.ftp.ftp.mkd(remote_dir)

    def set_remote_dir(self, remote_dir: str):
        self.remote_dir = remote_dir

    def set_local_dir(self, local_dir: str):
        self.local_dir = local_dir

    def set_project_name(self, project_name: str):
        self.project_name = project_name
        self.ftp.cwd_root()
        self.ftp.ftp.cwd(self.remote_dir)
        if not project_name in self.ftp.ftp.nlst():
            self.ftp.ftp.mkd(project_name)

    def upload_files(self, files: typing.List[str]):
        # files: list of file names, without directory
        remote_project_dir = f'{self.remote_dir}/{self.project_name}'
        self.ftp.cwd_root()
        self.ftp.ftp.cwd(remote_project_dir)
        for filename in files:
            self.ftp.upload_file(self.local_dir, filename)

    def download_files(self, files: typing.List[str]):
        remote_project_dir = f'{self.remote_dir}/{self.project_name}'
        self.ftp.ftp.cwd(remote_project_dir)
        for filename in files:
            self.ftp.download_file(self.local_dir, filename)

    def submit_job_gromacs(self,
        args: str,
        prompts: str,
        input_files: typing.List[str],
        output_files: typing.List[str],
        checkpoint_files: typing.List[str],
        log_files: typing.List[str]
    ) -> str:
        self.upload_files(input_files)
        job_id = self.chiral.submit_gromacs_job(is_long=True, args=args.split(' '), prompts=prompts.split(' '), work_dir=self.project_name, input_files=input_files, output_files=output_files, checkpoint_files=checkpoint_files, log_files=log_files)
        return job_id

    def submit_job_script(self
    ) -> str:
        return ''

    def wait_until_completion(self, job_id: str):
        self.chiral.wait_until_completion(job_id=job_id)



    # def clear_files(self, client: Client):
    #     if client.is_remote_dir('.', self.remote_dir):
    #         client.remove_remote_dir('.', self.remote_dir)
    #     client.create_remote_dir(self.remote_dir)

    # def get_output(self, client: Client, job_id: str) -> (str, str):
    #     (outputs, error) = client.get_job_result(job_id)
    #     if error:
    #         return ({}, error)
    #     else:
    #         return (json.loads(outputs[0]), "")
