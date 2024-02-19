import typing
import os
import json
import pathlib
from . import Client
from .types import TransferFile

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
        self.client = Client(user_email, user_token_api, chiral_computing_host, chiral_computing_port)

    def create_remote_dir(self, remote_dir: str):
        self.client.reconnect()
        if not remote_dir in self.client.ftp.nlst():
            self.client.ftp.mkd(remote_dir)

    def set_remote_dir(self, remote_dir: str):
        self.remote_dir = remote_dir

    def set_local_dir(self, local_dir: str):
        self.local_dir = local_dir

    def set_project_name(self, project_name: str):
        self.project_name = project_name
        self.client.reconnect()
        self.client.ftp.cwd(self.remote_dir)
        if not project_name in self.client.ftp.nlst():
            self.client.ftp.mkd(project_name)

    def upload_files(self, files: typing.List[str]):
        # files: list of file names, without directory
        remote_project_dir = f'{self.remote_dir}/{self.project_name}'
        self.client.reconnect()
        self.client.ftp.cwd(remote_project_dir)
        for fn in files:
            try:
                self.client.ftp.size(fn)
                self.client.ftp.delete(fn)
            except Exception:
                pass

            with open(pathlib.Path(self.local_dir).joinpath(fn), 'rb') as file:
                self.client.ftp.storbinary(f'STOR {fn}', file)

    def download_files(self, client: Client, files: typing.List[str]):
        remote_dir = f'{self.remote_dir}/{self.project_name}'
        files_transfer: typing.List[TransferFile] = list(map(lambda f: (f, self.local_dir, remote_dir), files))
        client.download_files(files_transfer)

    # def clear_files(self, client: Client):
    #     if client.is_remote_dir('.', self.remote_dir):
    #         client.remove_remote_dir('.', self.remote_dir)
    #     client.create_remote_dir(self.remote_dir)

    # def submit_job(self, client: Client, work_dir: str, is_long: bool, arguments: str, prompts: str, files_input: typing.List[str], files_output: typing.List[str], files_checkpoint: typing.List[str], files_log: typing.List[str]) -> str:
    #     return client.submit_gromacs_job(is_long, arguments.split(' '), prompts.split(' '), work_dir, files_input, files_output, files_checkpoint, files_log)

    # def get_output(self, client: Client, job_id: str) -> (str, str):
    #     (outputs, error) = client.get_job_result(job_id)
    #     if error:
    #         return ({}, error)
    #     else:
    #         return (json.loads(outputs[0]), "")
