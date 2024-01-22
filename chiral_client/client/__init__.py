import typing
import time
import grpc
import ftplib
import pathlib

from . import chiral_pb2 
from . import chiral_pb2_grpc 
from ..types import TransferFile

class Client:
    # def __init__(self, email: str, token_api: str, computing_server_addr: str, computing_server_port: str, file_server_addr: str, file_server_port: int):
    def __init__(self, email: str, token_api: str, computing_server_addr: str, computing_server_port: str, options: typing.List[typing.Tuple[str, int]] = None):
        self.channel = grpc.insecure_channel(f'{computing_server_addr}:{computing_server_port}', options = options)
        self.stub = chiral_pb2_grpc.ChiralStub(self.channel)
        self.metadata = (
            ('user_id', email),
            ('auth_token', token_api)
        )
        self.user_email = email
        self.token_api = token_api
        reply = self.stub.UserInitialize(chiral_pb2.RequestUserInitialize(), metadata=self.metadata)
        if reply.error:
            raise Exception(f'Client auth error: {reply.error}')
        else:
            self.ftp_addr = reply.settings['ftp_addr'] 
            self.ftp_port = int(reply.settings['ftp_port'])
            self.user_id = reply.settings['user_id']
            self.ftp_root = None
            self.connect_file_server()

    def connect_file_server(self):
        self.ftp = ftplib.FTP()
        self.ftp.connect(self.ftp_addr, self.ftp_port)
        self.ftp.login(self.user_email, self.token_api)
        self.ftp.cwd(self.user_id)
        self.ftp_root = self.ftp.pwd()

    def disconnect_file_server(self):
        self.ftp.quit()

    def reconnect(self):
        try:
            self.ftp.cwd(self.ftp_root)
        except Exception:
            print('reconnecting ...')
            self.connect_file_server()

    def upload_files(self, files: typing.List[TransferFile]):
        self.reconnect()
        for (fn, local_dir, remote_dir) in files:
            self.ftp.cwd(self.ftp_root)
            self.ftp.cwd(remote_dir)
            # if file exists remotely, skip uploading
            try: 
                self.ftp.size(fn)
            except Exception:
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
        self.reconnect()
        filename, _, remote_dir = file
        self.ftp.cwd(self.ftp_root)
        self.ftp.cwd(remote_dir)
        try:
            file_size = self.ftp.size(filename)
            return bool(file_size)
        except Exception:
            return False
        
    def is_remote_dir(self, parent_dir: str, dir: str) -> bool:
        self.reconnect()
        self.ftp.cwd(self.ftp_root)
        self.ftp.cwd(parent_dir)
        return dir in self.ftp.nlst()
    
    def create_remote_dir(self, dir_name: str):
        self.reconnect()
        self.ftp.cwd(self.ftp_root)
        self.ftp.mkd(dir_name)

    def remove_remote_dir(self, parent_dir: str, dir: str):
        self.reconnect()
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

    # def submit_job(self, job_req: str, divisor: int) -> str:
    #     reply = self.stub.UserSubmitJob(chiral_pb2.RequestAcceptJob(requirement=job_req, divisor=divisor), metadata=self.metadata)
    #     if reply.error:
    #         raise Exception(f'Submit job error: {reply.error}')
    #     else:
    #         return reply.job_id
        
    def cancel_job(self, job_id: str):
        reply = self.stub.UserSendMonitorAction(chiral_pb2.RequestUserSendMonitorAction(job_id=job_id, action_type=chiral_pb2.MAT_CANCEL), metadata=self.metadata)
        if not reply.success:
            raise Exception(f'cancel job error: {reply.error}')

    def request_log_files(self, job_id: str):
        reply = self.stub.UserSendMonitorAction(chiral_pb2.RequestUserSendMonitorAction(job_id=job_id, action_type=chiral_pb2.MAT_GET_DETAILS), metadata=self.metadata)
        if not reply.success:
            raise Exception(f'cancel job error: {reply.error}')
        
    def check_job_status(self, job_ids: typing.List[str]) -> typing.Dict[str, typing.Any]:
        return self.stub.UserGetJobStatus(chiral_pb2.RequestUserGetJobStatus(job_ids=job_ids), metadata=self.metadata).statuses
    
    # def get_job_result(self, job_id: str) -> (typing.List[str], str):
    #     reply = self.stub.JobResult(chiral_pb2.RequestJobResult(job_id=job_id), metadata=self.metadata)
    #     if reply.error:
    #         return ([], f'Get job result error: {reply.error}')
    #     else:
    #         job_result = json.loads(reply.job_result)
    #         if job_result['error']:
    #             return ([], f'Job running error in cloud: {job_result["error"]}')
    #         else:
    #             return (job_result["outputs"], "")

    def wait_until_completion(self, job_id: str):
        while True:
            job_statuses = self.check_job_status([job_id])
            if job_id in job_statuses and job_statuses[job_id] in ['"Completed"', '"Cancelled"']:
                break
            time.sleep(0.5)

    def submit_gromacs_job(self, is_long: bool, args: typing.List[str], prompts: typing.List[str], work_dir: str, input_files: typing.List[str], output_files: typing.List[str], checkpoint_files: typing.List[str], log_files: typing.List[str]) -> str:
        job_gromacs = chiral_pb2.JobGromacs(is_long=is_long, args=args, prompts=prompts, work_dir=work_dir, input_files=input_files, output_files=output_files, checkpoint_files=checkpoint_files, log_files=log_files) 
        reply = self.stub.UserSubmitAppJob(chiral_pb2.RequestUserSubmitAppJob(app_type=chiral_pb2.APP_GROMACS, gromacs=job_gromacs), metadata = self.metadata)

        if reply.success:
            return reply.job_id
        else:
            raise Exception(f'submit gromacs job error: {reply.error}')


