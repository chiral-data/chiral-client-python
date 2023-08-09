import typing
import json
from .. import Client
from ..types import TransferFile
from . import JobRequirement, OperatorKind, DatasetKind

class Input:
    simulation_id: str
    sub_command: str
    arguments: typing.List[str]
    prompts: typing.List[str]
    files_dir: str 
    files_input: typing.List[str]
    files_output: typing.List[str]

    def __init__(self, simulation_id: str, sub_command: str, arguments: typing.List[str], prompts: typing.List[str], files_dir: str, files_input: typing.List[str], files_output: typing.List[str]):
        self.simulation_id = simulation_id
        self.sub_command = sub_command
        self.arguments = arguments
        self.prompts = prompts
        self.files_dir = files_dir
        self.files_input = files_input
        self.files_output = files_output

class JobManager:
    simulation_id: str
    local_dir: str
    remote_dir: str

    def __init__(self, simulation_id: str, local_dir: str, client: Client) -> None:
        self.simulation_id = simulation_id
        self.local_dir = local_dir 
        self.remote_dir = f'gromacs/{simulation_id}'
        if not client.is_remote_dir('.', 'gromacs'):
            client.create_remote_dir('gromacs')
        client.create_remote_dir(self.remote_dir)

    def upload_files(self, client: Client, files: typing.List[str]):
        files_transfer: typing.List[TransferFile] = list(map(lambda f: (f, self.local_dir, self.remote_dir), files))
        client.upload_files(files_transfer)

    def download_files(self, client: Client, files: typing.List[str]):
        files_transfer: typing.List[TransferFile] = list(map(lambda f: (f, self.local_dir, self.remote_dir), files))
        client.download_files(files_transfer)

    def clear_files(self, client: Client):
        client.remove_remote_dir(self.remote_dir)

    def submit_job(self, client: Client, sub_command: str, arguments: str, prompts: str, files_dir: str, files_input: typing.List[str], files_output: typing.List[str]) -> str:
        input = Input(self.simulation_id, sub_command, arguments.split(' '), prompts.split(' '), files_dir, files_input, files_output)
        jr = JobRequirement(json.dumps(input.__dict__), OperatorKind.GromacsRunGMXCommand, DatasetKind.Empty)
        print(json.dumps(jr.__dict__))
        job_id = client.submit_job(json.dumps(jr.__dict__), 1)
        return job_id

