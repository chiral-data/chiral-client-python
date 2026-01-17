"""
Tests for Chiral Python SDK using UserCommunicate API.
"""
import os
from chiral_client import ChiralClient, AppKind


def create_client() -> ChiralClient:
    """Create a ChiralClient from environment variables."""
    user_email = os.environ['CHIRAL_USER_EMAIL']
    token_auth = os.environ['CHIRAL_TOKEN_API']
    chiral_cloud_url = os.environ.get('CHIRAL_CLOUD_URL', 'api.chiral.one:20000')
    print(f'Connecting to {chiral_cloud_url} as {user_email}')
    return ChiralClient(user_email, token_auth, chiral_cloud_url)


def test_get_credit_points():
    """Test getting credit points."""
    print('Testing get_credit_points...')
    client = create_client()
    points = client.get_credit_points()
    print(f'Credit points: {points}')
    assert isinstance(points, float)
    print('test_get_credit_points ... pass')


def test_list_projects():
    """Test listing projects."""
    print('Testing list_projects...')
    client = create_client()
    projects = client.list_projects()
    print(f'Projects: {projects}')
    assert isinstance(projects, list)
    print('test_list_projects ... pass')


def test_list_example_projects():
    """Test listing example projects."""
    print('Testing list_example_projects...')
    client = create_client()
    projects = client.list_example_projects()
    print(f'Example projects: {projects}')
    assert isinstance(projects, list)
    print('test_list_example_projects ... pass')


def test_get_jobs():
    """Test getting jobs."""
    print('Testing get_jobs...')
    client = create_client()
    jobs = client.get_jobs()
    print(f'Found {len(jobs)} jobs')
    assert isinstance(jobs, list)
    print('test_get_jobs ... pass')


def test_submit_job():
    """Test submitting a job."""
    print('Testing submit_job...')
    client = create_client()

    # First, ensure we have a project
    projects = client.list_projects()
    if not projects:
        print('Creating test project...')
        client.create_project('test_sdk')
        projects = ['test_sdk']

    project_name = projects[0]
    print(f'Using project: {project_name}')

    # Submit a simple gromacs job
    job_id = client.submit_job(
        app=AppKind.Gromacs,
        command_str='gmx --version',
        project_name=project_name,
        input_files=[],
        output_files=[]
    )
    print(f'Submitted job: {job_id}')
    assert len(job_id) > 0

    # Get job status
    job = client.get_job(job_id)
    print(f'Job status: {job.get("status")}')

    # Wait for completion (with timeout)
    print('Waiting for job completion...')
    client.wait_until_completion(job_id)

    job = client.get_job(job_id)
    print(f'Final job status: {job.get("status")}')
    print('test_submit_job ... pass')


def run_all_tests():
    """Run all tests."""
    print('=' * 50)
    print('Chiral SDK Tests (UserCommunicate API)')
    print('=' * 50)

    test_get_credit_points()
    print()

    test_list_projects()
    print()

    test_list_example_projects()
    print()

    test_get_jobs()
    print()

    # Uncomment to test job submission (requires worker)
    # test_submit_job()
    # print()

    print('=' * 50)
    print('All tests passed!')
    print('=' * 50)


if __name__ == '__main__':
    run_all_tests()
