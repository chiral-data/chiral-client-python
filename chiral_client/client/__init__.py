import typing
import grpc
import json
import ftplib
import pathlib

from . import end_user_pb2
from . import end_user_pb2_grpc
from ..types import TransferFile

class Client:
    def __init__(self, email: str, token_api: str, computing_server_addr: str, computing_server_port: str, file_server_addr: str, file_server_port: int):
        self.channel = grpc.insecure_channel(f'{computing_server_addr}:{computing_server_port}')
        self.stub = end_user_pb2_grpc.ChiralEndUserStub(self.channel)
        self.metadata = (
            ('user_email', email),
            ('token_api', token_api)
        )
        self.user = email
        self.token_api = token_api
        self.ftp_addr = file_server_addr
        self.ftp_port = file_server_port
        self.ftp_root = None

    def connect_file_server(self):
        self.ftp = ftplib.FTP()
        self.ftp.connect(self.ftp_addr, self.ftp_port)
        self.ftp.login(self.user, self.token_api)
        self.ftp.cwd(self.user)
        self.ftp_root = self.ftp.pwd()

    def disconnect_file_server(self):
        self.ftp.quit()

    def reconnect(self):
        try:
            self.ftp.cwd(self.ftp_root)
        except Exception:
            self.connect_file_server()

    def upload_files(self, files: typing.List[TransferFile]):
        self.reconnect()
        for (fn, local_dir, remote_dir) in files:
            self.ftp.cwd(self.ftp_root)
            self.ftp.cwd(remote_dir)
            with open(pathlib.Path(local_dir).joinpath(fn), 'rb') as file:
                self.ftp.storbinary(f'STOR {fn}', file)

    def download_files(self, files: typing.List[TransferFile]):
        self.reconnect()
        for (fn, local_dir, remote_dir) in files:
            self.ftp.cwd(self.ftp_root)
            self.ftp.cwd(remote_dir)
            with open(pathlib.Path(local_dir).joinpath(fn), 'wb') as file:
                self.ftp.retrbinary(f'RETR {fn}', file.write)

    def remove_files(self, files: typing.List[TransferFile]):
        self.reconnect()
        for (fn, _, remote_dir) in files:
            self.ftp.cwd(self.ftp_root)
            self.ftp.cwd(remote_dir)
            self.ftp.delete(fn)

    def is_remote_file(self, file: TransferFile) -> bool:
        filename, _, remote_dir = file
        self.ftp.cwd(self.ftp_root)
        self.ftp.cwd(remote_dir)
        try:
            file_size = self.ftp.size(filename)
            return bool(file_size)
        except Exception:
            return False
        
    def is_remote_dir(self, parent_dir: str, dir: str) -> bool:
        self.ftp.cwd(self.ftp_root)
        self.ftp.cwd(parent_dir)
        return dir in self.ftp.nlst()
    
    def create_remote_dir(self, dir_name: str):
        self.ftp.cwd(self.ftp_root)
        self.ftp.mkd(dir_name)

    def remove_remote_dir(self, parent_dir: str, dir: str):
        # will remove all the files inside
        self.ftp.cwd(self.ftp_root)
        self.ftp.cwd(parent_dir)
        self.ftp.cwd(dir)
        for filename in self.ftp.nlst():
            self.ftp.delete(filename)
        self.ftp.cwd('..')
        self.ftp.rmd(dir)

    def __del__(self):
        self.channel.close()

    def submit_job(self, job_req: str, divisor: int) -> str:
        reply = self.stub.AcceptJob(end_user_pb2.RequestAcceptJob(requirement=job_req, divisor=divisor), metadata=self.metadata)
        if reply.error:
            raise Exception(f'Submit job error: {reply.error}')
        else:
            return reply.job_id
    
    def check_job_status(self, job_ids: typing.List[str]) -> typing.Dict[str, typing.Any]:
        return self.stub.JobStatus(end_user_pb2.RequestJobStatus(job_ids=job_ids), metadata=self.metadata).statuses
    
    def get_job_result(self, job_id: str) -> (typing.List[str], str):
        reply = self.stub.JobResult(end_user_pb2.RequestJobResult(job_id=job_id), metadata=self.metadata)
        if reply.error:
            return ([], f'Get job result error: {reply.error}')
        else:
            job_result = json.loads(reply.job_result)
            if job_result['error']:
                return ([], f'Job running error in cloud: {job_result["error"]}')
            else:
                return (job_result["outputs"], "")



