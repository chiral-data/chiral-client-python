import typing
import time
import grpc
import pathlib
from google.protobuf.internal.enum_type_wrapper import EnumTypeWrapper

from . import chiral_pb2
from . import chiral_pb2_grpc
from ..ftp import FtpClient

class ChiralClient:
    def __init__(self, email: str, token_api: str, chiral_computing_url: str, options: typing.List[typing.Tuple[str, int]] = []):
        self.channel = grpc.insecure_channel(chiral_computing_url, options = options)
        self.stub = chiral_pb2_grpc.ChiralStub(self.channel)
        self.metadata = (
            ('user_id', email),
            ('auth_token', token_api)
        )
        self.user_email = email
        self.token_api = token_api

    def create_ftp_client(self) -> FtpClient:
        reply = self.stub.UserInitialize(chiral_pb2.RequestUserInitialize(), metadata=self.metadata)
        if reply.error:
            raise Exception(f'Client auth error: {reply.error}')
        else:
            ftp_addr = reply.settings['ftp_addr']
            ftp_port = int(reply.settings['ftp_port'])
            user_id = reply.settings['user_id']
            ftp = FtpClient(ftp_addr=ftp_addr, ftp_port=ftp_port, user_email=self.user_email, token_api=self.token_api, user_id=user_id)
            ftp.connect()
            return ftp

    def __del__(self):
        self.channel.close()

    def submit_job_shell_scripts(self,
        work_dir: str,
        proj_name: str,
        script_file: str,
        apps: typing.List[chiral_pb2.AppType],
        prompts: typing.List[str],
        input_files: typing.List[str],
        output_files: typing.List[str],
        checkpoint_files: typing.List[str],
        log_files: typing.List[str]
    ) -> str:
        job_command = chiral_pb2.JobCommand(work_dir=work_dir, proj_name=proj_name, is_long=True, args=[script_file], prompts=prompts, input_files=input_files, output_files=output_files, checkpoint_files=checkpoint_files, log_files=log_files)
        job_scripts = chiral_pb2.JobScript(command=job_command, script_file=script_file, apps=apps)
        request = chiral_pb2.RequestUserSubmitAppJob(script=job_scripts)
        reply = self.stub.UserSubmitAppJob(request, metadata = self.metadata)

        if reply.success:
            return reply.job_id
        else:
            raise Exception(f'submit shell scripts job error: {reply.error}')

    def submit_gromacs_job(self, is_long: bool,
        work_dir: str,
        proj_name: str,
        args: typing.List[str],
        prompts: typing.List[str],
        input_files: typing.List[str],
        output_files: typing.List[str],
        checkpoint_files: typing.List[str],
        log_files: typing.List[str]
    ) -> str:
        job_gromacs = chiral_pb2.JobCommand(work_dir=work_dir, proj_name=proj_name, is_long=is_long, args=args, prompts=prompts, input_files=input_files, output_files=output_files, checkpoint_files=checkpoint_files, log_files=log_files)
        reply = self.stub.UserSubmitAppJob(chiral_pb2.RequestUserSubmitAppJob(gromacs=job_gromacs), metadata = self.metadata)

        if reply.success:
            return reply.job_id
        else:
            raise Exception(f'submit gromacs job error: {reply.error}')

    def send_monitor_action(self,
        job_id: str,
        monitor_action_type: chiral_pb2.MonitorActionType
    ) -> chiral_pb2.MonitorActionReply:
        request = chiral_pb2.RequestUserSendMonitorAction(job_id, monitor_action_type)
        reply = self.stub.UserSendMonitorAction(request, metadata = self.metadata)
        if reply.success:
            return reply.reply
        else:
            raise Exception(f'send monitor action error: {reply.error}')

    def cancel_job(self, job_id: str):
        reply = self.stub.UserSendMonitorAction(chiral_pb2.RequestUserSendMonitorAction(job_id=job_id, action_type=chiral_pb2.MAT_CANCEL), metadata=self.metadata)
        if not reply.success:
            raise Exception(f'cancel job error: {reply.error}')

    def get_log_files(self, job_id: str):
        reply = self.stub.UserSendMonitorAction(chiral_pb2.RequestUserSendMonitorAction(job_id=job_id, action_type=chiral_pb2.MAT_GET_DETAILS), metadata=self.metadata)
        if not reply.success:
            raise Exception(f'cancel job error: {reply.error}')

    def get_job_status(self, job_ids: typing.List[str]) -> typing.Dict[str, typing.Any]:
        return self.stub.UserGetJobStatus(chiral_pb2.RequestUserGetJobStatus(job_ids=job_ids), metadata=self.metadata).statuses

    def wait_until_completion(self, job_id: str):
        while True:
            job_statuses = self.get_job_status([job_id])
            if job_id in job_statuses and job_statuses[job_id] in ['"Completed"', '"CompletedWithError"', '"Canceled"']:
                break
            time.sleep(0.5)

    def check_credit_points(self) -> float:
        reply = self.stub.UserGetCreditPoints(chiral_pb2.RequestUserGetCreditPoints(), metadata = self.metadata)
        if reply.success:
            return reply.points
        else:
            raise Exception(f'check user credit points error: {reply.error}')
