import os
import shutil
from time import sleep

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


def create_client(remote_dir: str, local_dir: str) -> Client:
    user_email = os.environ['CHIRAL_USER_EMAIL']
    token_api = os.environ['CHIRAL_TOKEN_API']
    chiral_computing_url = os.environ['CHIRAL_CLOUD_URL']
    return Client(
        user_email, token_api, remote_dir,
        local_dir, chiral_computing_url
    )


def create_file(filename: str, local_dir: str):
    with open(f'{local_dir}/{filename}', 'w') as f:
        f.writelines(f'this is file {filename}')
        f.close()


def remove_file(filename: str, local_dir: str):
    full_path = f'{local_dir}/{filename}'
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
    print_ftp_client('connect ... test pass')
    ftp.disconnect()
    print_ftp_client('disonnect ... test pass')
    # assert ftp.root_dir == None
    # ftp.cwd_root()
    # assert ftp.root_dir == f'/{ftp.user_id}'
    # print_ftp_client(f'cwd_root ... test pass')
    ftp.connect()
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
    print_ftp_client('path_exist ... test pass')
    assert not os.path.exists(test_filename_1)
    ftp.cwd_root()
    ftp.ftp.cwd(parent_dir)
    ftp.download_file('.', test_filename_1)
    assert os.path.exists(test_filename_1)
    os.remove(test_filename_1)
    print_ftp_client('download_file ... test pass')
    ftp.cwd_root()
    ftp.remove_dir_recursively(parent_dir)
    assert ftp.path_exist(parent_dir) == PathType.NotExist
    print_ftp_client('remove_dir_all ... test pass')


def test_gromacs(local_dir: str):
    def print_test_gromacs(msg: str):
        print(f'testing Gromacs {msg}')

    remote_dir = 'gromacs'
    client = create_client(remote_dir, local_dir)
    data_dir = os.environ["CHIRAL_DATA_DIR"]

    # test submit gromacs job
    project = 'lysozyme'
    client.set_project(project)
    client.create_project_remote()
    if not os.path.exists(os.path.join(client.local_dir, project)):
        os.mkdir(os.path.join(client.local_dir, project))
    shutil.copyfile(
        os.path.join(data_dir, project, '1AKI_clean.pdb'),
        os.path.join(client.local_dir, project, '1AKI_clean.pdb')
    )
    input_files = ['1AKI_clean.pdb']
    output_files = ["1AKI_processed.gro", "topol.top", "posre.itp"]
    client.upload_files(input_files)
    job_id = client.submit_job_gromacs(
        'pdb2gmx -f 1AKI_clean.pdb -o 1AKI_processed.gro -water spce',
        '15 0', input_files, output_files, [], []
    )
    assert len(job_id) > 0
    client.wait_until_completion(job_id)
    client.download_files(output_files)
    for filename in output_files:
        assert os.path.exists(
            os.path.join(client.local_dir, project, filename)
        )
    client.remove_project_remote()
    client.remove_project_local()
    client.remove_remote_dir('.', remote_dir)
    print_test_gromacs('submit gromacs job ... pass')


def test_long_idle(local_dir: str):
    print('Testing long idle ...')
    # setup
    remote_dir = 'gromacs'
    test_project = 'long_idle'
    test_files = ['1.txt', '2.txt']
    curdir = os.getcwd()
    os.chdir(local_dir)
    os.mkdir(test_project)
    os.chdir(test_project)
    for f in test_files:
        create_file(f, '.')
    os.chdir(curdir)

    # test starts
    client = create_client(remote_dir, local_dir)
    client.set_project(test_project)
    client.create_project_remote()
    client.upload_files(test_files)
    for f in test_files:
        os.remove(os.path.join(local_dir, test_project, f))

    for i in range(5):
        # sleep(3600)
        sleep(3)
        client.download_files(test_files)
        for f in test_files:
            local_file = os.path.join(local_dir, test_project, f)
            assert os.path.exists(local_file)
            os.remove(local_file)
        print(f'Testing long idle {i} hour(s) ... pass')

    client.remove_project_remote()
    client.remove_project_local()
    print('Testing long idle ... pass')


def test_client():
    # setup
    test_dir = 'test_client'
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.mkdir(test_dir)

    # test
    test_gromacs(test_dir)
    test_long_idle(test_dir)

    # clean
    shutil.rmtree(test_dir)


if __name__ == '__main__':
    test_ftp_client()
    test_client()
