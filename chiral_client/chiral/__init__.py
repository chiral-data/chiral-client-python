"""
Chiral gRPC client using UserCommunicate protocol.
"""
import typing
import time
import os
import grpc

from . import chiral_client_pb2
from . import chiral_client_pb2_grpc
from ..api_types import Request, Reply, AppKind
from ..ftp import FtpClient, ftp_connect


class ChiralClient:
    """
    Client for Chiral Cloud API using the UserCommunicate protocol.

    All requests are serialized as JSON and sent via a single gRPC method.
    """

    def __init__(self, email: str, token_auth: str, chiral_computing_url: str,
                 options: typing.List[typing.Tuple[str, int]] = [],
                 ftp_port: int = None, user_id: str = None):
        self.channel = grpc.insecure_channel(chiral_computing_url, options=options)
        self.stub = chiral_client_pb2_grpc.ChiralStub(self.channel)
        self.metadata = (
            ('user_id', email),
            ('auth_token', token_auth)
        )
        self.user_email = email
        self.token_auth = token_auth

        # FTP settings - addr is same as gRPC host, user_id is email
        self.ftp_addr = chiral_computing_url.split(':')[0]
        self.ftp_port = ftp_port or int(os.environ.get('CHIRAL_FTP_PORT', '2025'))
        self.user_id = user_id or email

    def __del__(self):
        self.channel.close()

    def create_ftp_client(self) -> FtpClient:
        """Create an FTP client for file uploads/downloads."""
        if not self.user_id:
            raise ValueError('User ID not configured. Set CHIRAL_USER_ID or pass user_id.')
        return FtpClient(
            ftp_addr=self.ftp_addr,
            ftp_port=self.ftp_port,
            user_email=self.user_email,
            token_api=self.token_auth,
            user_id=self.user_id
        )

    def _communicate(self, serialized_request: str) -> str:
        """
        Send a request via UserCommunicate and return the serialized reply.

        Raises:
            Exception: If the request fails
        """
        request = chiral_client_pb2.RequestUserCommunicate(
            serialized_request=serialized_request
        )
        reply = self.stub.UserCommunicate(request, metadata=self.metadata)

        if not reply.success:
            raise Exception(f'API error: {reply.error}')

        return reply.serialized_reply

    # Credit Points
    def get_credit_points(self) -> float:
        """Get the credit points balance for the current user."""
        req = Request.get_credit_points()
        reply = self._communicate(req)
        return Reply.get_credit_points(reply)

    # Token API
    def get_token_api(self) -> str:
        """Get the API token for the current user."""
        req = Request.get_token_api()
        reply = self._communicate(req)
        return Reply.get_token_api(reply)

    def refresh_token_api(self) -> str:
        """Refresh and get a new API token."""
        req = Request.refresh_token_api()
        reply = self._communicate(req)
        return Reply.refresh_token_api(reply)

    # Jobs
    def submit_test_job(self, job_type_name: str, index: int) -> str:
        """Submit a test job and return the job ID."""
        req = Request.submit_test_job(job_type_name, index)
        reply = self._communicate(req)
        return Reply.submit_test_job(reply)

    def get_jobs(self, offset: int = 0, count_per_page: int = 20) -> typing.List[typing.Dict]:
        """Get a list of jobs for the current user."""
        req = Request.get_jobs(offset, count_per_page)
        reply = self._communicate(req)
        return Reply.get_jobs(reply)

    def get_job(self, job_id: str) -> typing.Dict:
        """Get details of a specific job."""
        req = Request.get_job(job_id)
        reply = self._communicate(req)
        return Reply.get_job(reply)

    def submit_job(self, app: AppKind, command_str: str, project_name: str,
                   input_files: typing.List[str], output_files: typing.List[str]) -> str:
        """
        Submit a job and return the job ID.

        Args:
            app: The application to run (e.g., AppKind.Gromacs)
            command_str: The command string to execute
            project_name: Name of the project
            input_files: List of input file names
            output_files: List of output file names

        Returns:
            The job ID
        """
        req = Request.submit_job(app, command_str, project_name, input_files, output_files)
        reply = self._communicate(req)
        return Reply.submit_job(reply)

    def cancel_job(self, job_id: str):
        """Cancel a job."""
        req = Request.cancel_job(job_id)
        self._communicate(req)

    def submit_job_from_potter(self, config_json_str: str) -> str:
        """Submit a job using Potter configuration."""
        req = Request.submit_job_from_potter(config_json_str)
        reply = self._communicate(req)
        return Reply.submit_job_from_potter(reply)

    def wait_until_completion(self, job_id: str, poll_interval: float = 1.0):
        """
        Wait until a job completes.

        Args:
            job_id: The job ID to wait for
            poll_interval: Seconds between status checks
        """
        while True:
            job = self.get_job(job_id)
            status = job.get('status', '')
            if status in ['Completed', 'CompletedWithError', 'Canceled']:
                break
            time.sleep(poll_interval)

    # Projects
    def list_projects(self) -> typing.List[str]:
        """List all projects for the current user."""
        req = Request.list_of_projects()
        reply = self._communicate(req)
        return Reply.list_of_projects(reply)

    def create_project(self, project_name: str):
        """Create a new project."""
        req = Request.create_project(project_name)
        self._communicate(req)

    def delete_project(self, project_name: str):
        """Delete a project."""
        req = Request.delete_project(project_name)
        self._communicate(req)

    def list_example_projects(self) -> typing.List[str]:
        """List available example projects."""
        req = Request.list_of_example_projects()
        reply = self._communicate(req)
        return Reply.list_of_example_projects(reply)

    def import_example_project(self, project_name: str):
        """Import an example project."""
        req = Request.import_example_project(project_name)
        self._communicate(req)

    def import_example_files(self, project_name: str):
        """Import example files into a project."""
        req = Request.import_example_files(project_name)
        self._communicate(req)

    # Project Files
    def list_project_files(self, project_name: str) -> typing.List[str]:
        """List files in a project."""
        req = Request.list_of_project_files(project_name)
        reply = self._communicate(req)
        return Reply.list_of_project_files(reply)

    def list_files_and_folders(self, project_name: str,
                                child_folders: typing.List[str] = []) -> typing.List[typing.Tuple[str, str]]:
        """
        List files and folders in a project directory.

        Returns:
            List of (name, type) tuples where type is 'file' or 'folder'
        """
        req = Request.list_files_and_folders(project_name, child_folders)
        reply = self._communicate(req)
        return Reply.list_files_and_folders(reply)

    def get_project_file(self, project_name: str, file_name: str) -> bytes:
        """Get the contents of a project file."""
        req = Request.get_project_file(project_name, file_name)
        reply = self._communicate(req)
        return Reply.get_project_file(reply)

    def write_project_file(self, project_name: str, file_name: str, content: str):
        """Write content to a project file."""
        req = Request.write_project_file(project_name, file_name, content)
        self._communicate(req)

    def delete_project_file_or_folder(self, project_name: str, name: str):
        """Delete a file or folder from a project."""
        req = Request.delete_project_file_or_folder(project_name, name)
        self._communicate(req)

    # Payment
    def confirm_payment(self, order_id: str, access_id: str, amount: int):
        """Confirm a payment."""
        req = Request.confirm_payment(order_id, access_id, amount)
        self._communicate(req)
