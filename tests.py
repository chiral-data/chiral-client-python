import os
import shutil

from chiral_client.chiral import ChiralClient
from chiral_client.ftp import PathType
from chiral_client import Client

def create_client_for_local_server() -> ChiralClient:
    user_email = os.environ['CHIRAL_USER_EMAIL']
    user_token_api = os.environ['CHIRAL_TOKEN_API']
    chiral_cloud_url = os.environ['CHIRAL_CLOUD_URL']
    return ChiralClient(user_email, user_token_api, chiral_cloud_url)

def create_client_for_remote_server() -> ChiralClient:
    user_email = os.environ['CHIRAL_USER_EMAIL']
    token_api = os.environ['CHIRAL_TOKEN_API']
    return ChiralClient(user_email, token_api, 'api.chiral.one:20000')

def create_file(filename: str, local_dir: str):
    with open(f'{local_dir}/{filename}', 'w') as f:
        f.writelines(f'this is file {filename}')
        f.close()

def remove_file(filename: str, local_dir: str):
    full_path =  f'{local_dir}/{filename}'
    if os.path.exists(full_path):
        os.remove(full_path)

def test_ftp_client():
    def print_ftp_client(msg: str):
        print(f'testing FtpClient {msg}')

    # client = create_client_for_local_server()
    client = create_client_for_remote_server()
    ftp = client.create_ftp_client()
    ftp.connect()
    assert ftp.root_dir == f'/{ftp.user_id}'
    print_ftp_client(f'connect ... test pass')
    ftp.disconnect()
    assert ftp.root_dir == None
    print_ftp_client(f'disonnect ... test pass')
    ftp.cwd_root()
    assert ftp.root_dir == f'/{ftp.user_id}'
    print_ftp_client(f'cwd_root ... test pass')
    parent_dir = 'parent_dir'
    child_dir = 'child_dir'
    test_filename_1 = '1.txt'
    test_filename_2 = '2.txt'
    create_file(test_filename_1, '.')
    ftp.ftp.mkd(parent_dir)
    ftp.ftp.cwd(parent_dir)
    ftp.upload_file('.', test_filename_1)
    ftp.ftp.mkd(child_dir)
    ftp.ftp.cwd(child_dir)
    ftp.upload_file('.', test_filename_1)
    ftp.cwd_root()
    assert ftp.path_exist(parent_dir) == PathType.Directory
    assert ftp.path_exist(child_dir) == PathType.NotExist
    assert ftp.path_exist(test_filename_1) == PathType.NotExist
    assert ftp.path_exist(test_filename_2) == PathType.NotExist
    ftp.ftp.cwd(parent_dir)
    assert ftp.path_exist(parent_dir) == PathType.NotExist
    assert ftp.path_exist(child_dir) == PathType.Directory
    assert ftp.path_exist(test_filename_1) == PathType.File
    assert ftp.path_exist(test_filename_2) == PathType.NotExist
    os.remove(test_filename_1)
    print_ftp_client(f'path_exist ... test pass')
    assert not os.path.exists(test_filename_1)
    ftp.cwd_root()
    ftp.ftp.cwd(parent_dir)
    ftp.download_file('.', test_filename_1)
    assert os.path.exists(test_filename_1)
    os.remove(test_filename_1)
    print_ftp_client(f'download_file ... test pass')
    ftp.cwd_root()
    ftp.remove_dir_recursively(parent_dir)
    assert ftp.path_exist(parent_dir) == PathType.NotExist
    print_ftp_client(f'remove_dir_all ... test pass')

def test_gromacs(client: Client, parent_dir: str):
    def print_test_gromacs(msg: str):
        print(f'testing Gromacs Jobs {msg}')
    data_dir = os.environ["CHIRAL_DATA_DIR"]
    # test submit gromacs job
    project = 'lysozyme'
    client.set_project(project)
    client.create_project_remote()
    if not os.path.exists(os.path.join(client.local_dir, project)):
        os.mkdir(os.path.join(client.local_dir, project))
    shutil.copyfile(
        os.path.join(data_dir, 'gromacs', project, '1AKI_clean.pdb'),
        os.path.join(client.local_dir, project, '1AKI_clean.pdb')
    )
    input_files = ['1AKI_clean.pdb']
    output_files = ["1AKI_processed.gro", "topol.top", "posre.itp"]
    client.upload_files(input_files)
    job_id = client.submit_job_gromacs('pdb2gmx -f 1AKI_clean.pdb -o 1AKI_processed.gro -water spce', '15 0', input_files, output_files, [], [])
    assert len(job_id) > 0
    client.wait_until_completion(job_id)
    client.download_files(output_files)
    for filename in output_files:
        assert os.path.exists(os.path.join(client.local_dir, project, filename))
    client.remove_project_remote()
    client.remove_project_local()
    print_test_gromacs('submit gromacs job ... pass')

def test_client():
    # setup
    test_dir = 'test_job_manager'
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.mkdir(test_dir)
    #
    user_email = os.environ['CHIRAL_USER_EMAIL']
    token_api = os.environ['CHIRAL_TOKEN_API']
    chiral_computing_url = os.environ['CHIRAL_CLOUD_URL']
    remote_dir = 'gromacs'
    local_dir = test_dir
    client= Client(user_email, token_api, remote_dir, local_dir, chiral_computing_url)
    test_gromacs(client, test_dir)
    # clean
    client.remove_remote_dir('.', 'gromacs')
    shutil.rmtree(test_dir)

if __name__ == '__main__':
    test_ftp_client()
    # test_client()
