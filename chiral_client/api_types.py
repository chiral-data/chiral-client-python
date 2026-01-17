"""
API types for the Chiral UserCommunicate protocol.
These match the Rust Request/Reply enums in chiral-backend.
"""
import json
from enum import Enum
from typing import List, Tuple, Optional, Any, Dict
from dataclasses import dataclass


class AppKind(Enum):
    """Application types supported by Chiral Cloud."""
    Unknown = "Unknown"
    Gromacs = "Gromacs"
    Boltz2 = "Boltz2"
    BoltzGen = "BoltzGen"
    LightDock = "LightDock"
    Haddock3 = "Haddock3"
    DiffDockPP = "DiffDockPP"
    AutoDockVina = "AutoDockVina"
    Smina = "Smina"
    DockingReport = "DockingReport"
    BoltzReport = "BoltzReport"
    RNAFold = "RNAFold"
    RNACofold = "RNACofold"
    RNAEval = "RNAEval"
    RNAUp = "RNAUp"
    Blast = "Blast"
    RNAHybrid = "RNAHybrid"
    IntaRNA = "IntaRNA"


# Request types - match Rust Request enum
class Request:
    """Base class for API requests. Serializes to JSON matching Rust serde format."""

    @staticmethod
    def get_user_id() -> str:
        return json.dumps("GetUserId")

    @staticmethod
    def get_credit_points() -> str:
        return json.dumps("GetCreditPoints")

    @staticmethod
    def get_token_api() -> str:
        return json.dumps("GetTokenAPI")

    @staticmethod
    def refresh_token_api() -> str:
        return json.dumps("RefreshTokenAPI")

    @staticmethod
    def submit_test_job(job_type_name: str, index: int) -> str:
        return json.dumps({"SubmitTestJob": [job_type_name, index]})

    @staticmethod
    def get_jobs(offset: int, count_per_page: int) -> str:
        return json.dumps({"GetJobs": [offset, count_per_page]})

    @staticmethod
    def get_job(job_id: str) -> str:
        return json.dumps({"GetJob": job_id})

    @staticmethod
    def confirm_payment(order_id: str, access_id: str, amount: int) -> str:
        return json.dumps({"ConfirmPayment": [order_id, access_id, amount]})

    @staticmethod
    def list_of_projects() -> str:
        return json.dumps("ListOfProjects")

    @staticmethod
    def list_of_project_files(project_name: str) -> str:
        return json.dumps({"ListOfProjectFiles": project_name})

    @staticmethod
    def import_example_project(project_name: str) -> str:
        return json.dumps({"ImportExampleProject": project_name})

    @staticmethod
    def create_project(project_name: str) -> str:
        return json.dumps({"CreateProject": project_name})

    @staticmethod
    def delete_project(project_name: str) -> str:
        return json.dumps({"DeleteProject": project_name})

    @staticmethod
    def list_of_example_projects() -> str:
        return json.dumps("ListOfExampleProjects")

    @staticmethod
    def get_project_file(project_name: str, file_name: str) -> str:
        return json.dumps({"GetProjectFile": [project_name, file_name]})

    @staticmethod
    def write_project_file(project_name: str, file_name: str, file_content: str) -> str:
        return json.dumps({"WriteProjectFile": [project_name, file_name, file_content]})

    @staticmethod
    def delete_project_file_or_folder(project_name: str, name: str) -> str:
        return json.dumps({"DeleteProjectFileOrFolder": [project_name, name]})

    @staticmethod
    def submit_job(app: AppKind, command_str: str, project_name: str,
                   input_files: List[str], output_files: List[str]) -> str:
        return json.dumps({"SubmitJob": [app.value, command_str, project_name, input_files, output_files]})

    @staticmethod
    def cancel_job(job_id: str) -> str:
        return json.dumps({"CancelJob": job_id})

    @staticmethod
    def submit_job_from_potter(config_json_str: str) -> str:
        return json.dumps({"SubmitJobFromPotter": config_json_str})

    @staticmethod
    def list_files_and_folders(project_name: str, child_folders: List[str]) -> str:
        return json.dumps({"ListFilesAndFolders": [project_name, child_folders]})

    @staticmethod
    def import_example_files(project_name: str) -> str:
        return json.dumps({"ImportExampleFiles": project_name})


class Reply:
    """Parser for API replies. Deserializes from JSON matching Rust serde format."""

    @staticmethod
    def parse(serialized_reply: str) -> Tuple[str, Any]:
        """
        Parse a serialized reply and return (reply_type, data).

        Returns:
            Tuple of (reply_type_name, reply_data)
        """
        data = json.loads(serialized_reply)

        # Simple unit variants are just strings
        if isinstance(data, str):
            return (data, None)

        # Variants with data are dicts with single key
        if isinstance(data, dict) and len(data) == 1:
            key = list(data.keys())[0]
            return (key, data[key])

        raise ValueError(f"Unknown reply format: {data}")

    @staticmethod
    def get_user_id(serialized_reply: str) -> str:
        reply_type, data = Reply.parse(serialized_reply)
        if reply_type != "GetUserId":
            raise ValueError(f"Expected GetUserId reply, got {reply_type}")
        return str(data)

    @staticmethod
    def get_credit_points(serialized_reply: str) -> float:
        reply_type, data = Reply.parse(serialized_reply)
        if reply_type != "GetCreditPoints":
            raise ValueError(f"Expected GetCreditPoints reply, got {reply_type}")
        return float(data)

    @staticmethod
    def get_token_api(serialized_reply: str) -> str:
        reply_type, data = Reply.parse(serialized_reply)
        if reply_type != "GetTokenAPI":
            raise ValueError(f"Expected GetTokenAPI reply, got {reply_type}")
        return str(data)

    @staticmethod
    def refresh_token_api(serialized_reply: str) -> str:
        reply_type, data = Reply.parse(serialized_reply)
        if reply_type != "RefreshTokenAPI":
            raise ValueError(f"Expected RefreshTokenAPI reply, got {reply_type}")
        return str(data)

    @staticmethod
    def submit_test_job(serialized_reply: str) -> str:
        reply_type, data = Reply.parse(serialized_reply)
        if reply_type != "SubmitTestJob":
            raise ValueError(f"Expected SubmitTestJob reply, got {reply_type}")
        return str(data)

    @staticmethod
    def get_jobs(serialized_reply: str) -> List[Dict]:
        reply_type, data = Reply.parse(serialized_reply)
        if reply_type != "GetJobs":
            raise ValueError(f"Expected GetJobs reply, got {reply_type}")
        return data

    @staticmethod
    def get_job(serialized_reply: str) -> Dict:
        reply_type, data = Reply.parse(serialized_reply)
        if reply_type != "GetJob":
            raise ValueError(f"Expected GetJob reply, got {reply_type}")
        return data

    @staticmethod
    def list_of_projects(serialized_reply: str) -> List[str]:
        reply_type, data = Reply.parse(serialized_reply)
        if reply_type != "ListOfProjects":
            raise ValueError(f"Expected ListOfProjects reply, got {reply_type}")
        return data

    @staticmethod
    def list_of_project_files(serialized_reply: str) -> List[str]:
        reply_type, data = Reply.parse(serialized_reply)
        if reply_type != "ListOfProjectFiles":
            raise ValueError(f"Expected ListOfProjectFiles reply, got {reply_type}")
        return data

    @staticmethod
    def list_of_example_projects(serialized_reply: str) -> List[str]:
        reply_type, data = Reply.parse(serialized_reply)
        if reply_type != "ListOfExampleProjects":
            raise ValueError(f"Expected ListOfExampleProjects reply, got {reply_type}")
        return data

    @staticmethod
    def get_project_file(serialized_reply: str) -> bytes:
        reply_type, data = Reply.parse(serialized_reply)
        if reply_type != "GetProjectFile":
            raise ValueError(f"Expected GetProjectFile reply, got {reply_type}")
        # data is a list of bytes
        return bytes(data)

    @staticmethod
    def submit_job(serialized_reply: str) -> str:
        reply_type, data = Reply.parse(serialized_reply)
        if reply_type != "SubmitJob":
            raise ValueError(f"Expected SubmitJob reply, got {reply_type}")
        return str(data)

    @staticmethod
    def submit_job_from_potter(serialized_reply: str) -> str:
        reply_type, data = Reply.parse(serialized_reply)
        if reply_type != "SubmitJobFromPotter":
            raise ValueError(f"Expected SubmitJobFromPotter reply, got {reply_type}")
        return str(data)

    @staticmethod
    def list_files_and_folders(serialized_reply: str) -> List[Tuple[str, str]]:
        reply_type, data = Reply.parse(serialized_reply)
        if reply_type != "ListFilesAndFolders":
            raise ValueError(f"Expected ListFilesAndFolders reply, got {reply_type}")
        return [(item[0], item[1]) for item in data]
