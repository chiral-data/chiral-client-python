# Documentation for Client API

```python
class Client:
    def __init__(self, user_email: str, token_api: str, remote_dir: str, local_dir: str, chiral_computing_url: str = 'api.chiral.one') -> None:
        """
        Initialize a Client instance

        Parameters:
        - user_email: Email address of the user account registered at https://cloud.chiral.one.
        - token_api: Token obtained from the "Profile" page after logging into https://cloud.chiral.one.
        - remote_dir: Directory of the remote storage. It will be created if it does not exist.
        - local_dir: Directory of the local storage. The user is responsible for ensuring its existence.
        """

    def set_remote_dir(self, remote_dir: str):
        """
        Change the remote directory of the Client.

        Parameters:
        - remote_dir: Directory of the remote storage.
        """

    def set_local_dir(self, local_dir: str):
        """
        Change the local directory of the Client.

        Parameters:
        - local_dir: Directory of the local storage.
        """

    def remove_remote_dir(self, parent_dir: str, dirname: str):
        """
        Removes a directory from the remote storage.

        Parameters:
        - parent_dir (str): The directory path where the directory to be removed exists.
        - dirname (str): The name of the directory to be removed.
        """

    def set_project(self, project: str):
        """
        Set the current project.
        The remote directory for the project will be remote_dir/project,
        and the local directory for the project will be local_dir/project.
        Parameters:
          project (str): The name of the current project.
        """

    def create_project_remote(self):
        """
        Create the remote directory for the current project.
        The directory will be remote_dir/project.
        """

    def remove_project_remote(self):
        """
        Remove the remote directory for the current project
        """

    def upload_files(self, files: typing.List[str]):
        """
        Upload files from the local project directory to the remote project directory.
        Parameters:
          files (list of str): List of file names without directory prefix.
        """

    def download_files(self, files: typing.List[str]):
        """
        Download files from the remote project directory to the local project directory.
        Parameters:
          files (list of str): List of file names without directory prefix.
        """

    def upload_directory(self):
        """
        Upload the entire local project directory to the remote storage space.
        If the remote project directory exists, it will be renamed with a sequential number.
        """

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

    def cancel_job(self, job_id: str):
        """
        Cancel a job.
        Parameters:
          job_id (str): The ID of the job to be canceled.
        """

    def get_job_status(self, job_id: str) -> str:
        """
        Get the status of a job.
        Parameters:
          job_id (str): The ID of the job.
        Returns:
          str: The status of the job.
        """

    def request_log_files(self, job_id: str):
        """
        Ask for the latest log files of a job.
        The log files will be ready within 2 seconds in the remote storage
        after the computing server receives the request and uploads the log files.
        Parameters:
            job_id (str): The ID of the job.
        """

    def wait_until_completion(self, job_id: str):
        """
        Check the job status and wait until the job is completed, either with success or with error.
        Parameters:
          job_id (str): The ID of the job.
        """

    def check_credit_points(self) -> float:
        """
        Check the point balance of the current user.
        """
```