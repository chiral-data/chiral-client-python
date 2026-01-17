"""
Tests for Chiral Python SDK using UserCommunicate API.
"""

import os

from chiral_client import AppKind, ChiralClient


def create_client() -> ChiralClient:
    """Create a ChiralClient from environment variables."""
    user_email = os.environ["CHIRAL_USER_EMAIL"]
    token_auth = os.environ["CHIRAL_TOKEN_API"]
    chiral_cloud_url = os.environ.get("CHIRAL_CLOUD_URL", "api.chiral.one:20000")
    print(f"Connecting to {chiral_cloud_url} as {user_email}")
    return ChiralClient(user_email, token_auth, chiral_cloud_url)


def test_get_user_id():
    """Test getting user ID."""
    print("Testing get_user_id...")
    client = create_client()
    user_id = client.get_user_id()
    print(f"User ID: {user_id}")
    assert isinstance(user_id, str)
    assert len(user_id) > 0
    print("test_get_user_id ... pass")


def test_get_credit_points():
    """Test getting credit points."""
    print("Testing get_credit_points...")
    client = create_client()
    points = client.get_credit_points()
    print(f"Credit points: {points}")
    assert isinstance(points, float)
    print("test_get_credit_points ... pass")


def test_list_projects():
    """Test listing projects."""
    print("Testing list_projects...")
    client = create_client()
    projects = client.list_projects()
    print(f"Projects: {projects}")
    assert isinstance(projects, list)
    print("test_list_projects ... pass")


def test_list_example_projects():
    """Test listing example projects."""
    print("Testing list_example_projects...")
    client = create_client()
    projects = client.list_example_projects()
    print(f"Example projects: {projects}")
    assert isinstance(projects, list)
    print("test_list_example_projects ... pass")


def test_get_jobs():
    """Test getting jobs."""
    print("Testing get_jobs...")
    client = create_client()
    jobs = client.get_jobs()
    print(f"Found {len(jobs)} jobs")
    assert isinstance(jobs, list)
    print("test_get_jobs ... pass")


def test_submit_job():
    """Test submitting a simple job."""
    print("Testing submit_job...")
    client = create_client()

    # First, ensure we have a project
    projects = client.list_projects()
    if not projects:
        print("Creating test project...")
        client.create_project("test_sdk")
        projects = ["test_sdk"]

    project_name = projects[0]
    print(f"Using project: {project_name}")

    # Submit a simple gromacs job
    job_id = client.submit_job(
        app=AppKind.Gromacs,
        command_str="gmx --version",
        project_name=project_name,
        input_files=[],
        output_files=[],
    )
    print(f"Submitted job: {job_id}")
    assert len(job_id) > 0

    # Get job status
    job = client.get_job(job_id)
    print(f"Job status: {job.get('status')}")

    # Wait for completion (with timeout)
    print("Waiting for job completion...")
    client.wait_until_completion(job_id)

    job = client.get_job(job_id)
    print(f"Final job status: {job.get('status')}")
    print("test_submit_job ... pass")


def test_gromacs_pdb2gmx():
    """Test gromacs pdb2gmx command job."""
    print("Testing gromacs pdb2gmx...")
    client = create_client()
    data_dir = os.environ.get("CHIRAL_DATA_DIR", "")

    project_name = "test_gromacs_sdk"

    # Create or use existing project
    projects = client.list_projects()
    if project_name not in projects:
        print(f"Creating project: {project_name}")
        client.create_project(project_name)

    # Upload input file via FTP
    input_file = "1AKI_clean.pdb"
    input_path = os.path.join(data_dir, "lysozyme", input_file)

    ftp = client.create_ftp_client()
    ftp.connect()
    print(f"FTP connected to {client.ftp_addr}:{client.ftp_port}")

    # Create project directory if needed
    if ftp.path_exist(project_name).value == 0:  # NotExist
        ftp.ftp.mkd(project_name)
    ftp.ftp.cwd(project_name)

    # Upload input file
    if os.path.exists(input_path):
        print(f"Uploading {input_file} via FTP...")
        ftp.upload_file(os.path.join(data_dir, "lysozyme"), input_file)
    else:
        print(f"Warning: {input_path} not found, using existing file in project")

    ftp.disconnect()

    # Submit gromacs pdb2gmx job
    input_files = [input_file]
    output_files = ["1AKI_processed.gro", "topol.top", "posre.itp"]

    job_id = client.submit_job(
        app=AppKind.Gromacs,
        command_str="gmx pdb2gmx -f 1AKI_clean.pdb -o 1AKI_processed.gro -water spce -ff oplsaa",
        project_name=project_name,
        input_files=input_files,
        output_files=output_files,
    )
    print(f"Gromacs pdb2gmx job ID: {job_id}")
    assert len(job_id) > 0

    # Wait for completion
    print("Waiting for job completion...")
    client.wait_until_completion(job_id, verbose=True)
    print("job completed ...")

    # Check final status
    job = client.get_job(job_id)
    status = job.get("status", "")
    print(f"Job {job_id} completed with status: {status}")

    if status == "Completed":
        # List project files to verify outputs
        files = client.list_project_files(project_name)
        print(f"Project files: {files}")
        for out_file in output_files:
            if out_file in files:
                print(f"  ✓ {out_file} exists")
            else:
                print(f"  ✗ {out_file} missing")
        print("test_gromacs_pdb2gmx ... pass")
    else:
        assert False, f"test_gromacs_pdb2gmx ... job completed with status: {status}"


def run_all_tests():
    """Run all tests."""
    print("=" * 50)
    print("Chiral SDK Tests (UserCommunicate API)")
    print("=" * 50)

    test_get_user_id()
    print()

    test_get_credit_points()
    print()

    test_list_projects()
    print()

    test_list_example_projects()
    print()

    test_get_jobs()
    print()

    # Gromacs job test (requires worker and CHIRAL_DATA_DIR)
    test_gromacs_pdb2gmx()
    print()

    print("=" * 50)
    print("All tests passed!")
    print("=" * 50)


if __name__ == "__main__":
    run_all_tests()
