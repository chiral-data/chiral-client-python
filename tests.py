from logging import shutdown
import sys
import os
import shutil
import chiral_client
from chiral_client.client import ChiralClient
from chiral_client.ftp import PathType, FtpClient
from chiral_client import JobManager

CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'

USE_REMOTE = True

def create_client_for_local_server() -> ChiralClient:
    user_email = os.environ['CHIRAL_USER_EMAIL']
    user_token_api = os.environ['CHIRAL_TOKEN_API']
    chiral_computing_host = 'localhost'
    chiral_computing_port = '30001'
    return ChiralClient(user_email, user_token_api, chiral_computing_host, chiral_computing_port)

def create_client_for_remote_server() -> ChiralClient:
    user_email = os.environ['CHIRAL_USER_EMAIL']
    token_api = os.environ['CHIRAL_TOKEN_API']
    chiral_computing_host = 'api.chira.one'
    chiral_computing_port = '20000'
    return ChiralClient(user_email, token_api, chiral_computing_host, chiral_computing_port)

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

    client = create_client_for_local_server()
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
    ftp.remove_dir_all(parent_dir)
    assert ftp.path_exist(parent_dir) == PathType.NotExist
    print_ftp_client(f'remove_dir_all ... test pass')

def test_chiral_client():
    # setup
    test_dir = 'test_chiral_client'
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.mkdir(test_dir)
    client = create_client_for_local_server()
    # shell_scripts
    # gromacs_job
    # clean
    shutil.rmtree(test_dir)


def test_gromacs(jm: JobManager, parent_dir: str):
    # set up
    test_dir = os.path.join(parent_dir, 'test_gromacs')
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.mkdir(test_dir)
    #
    data_dir = os.environ["CHIRAL_DATA_DIR"]
    shutil.copyfile(f'{data_dir}/gromacs/lysozyme/1AKI_clean.pdb', f'{test_dir}/1AKI_clean.pdb')
    print("-------------- Testing Gromacs Job --------------")
    project_name = 'lysozyme'
    jm.ensure_connection()
    jm.create_remote_dir('gromacs')
    jm.set_remote_dir('gromacs')
    jm.set_project_name(project_name)
    jm.set_local_dir(test_dir)
    input_files = ['1AKI_clean.pdb']
    output_files = ["1AKI_processed.gro", "topol.top", "posre.itp"]
    job_id = jm.submit_job_gromacs('pdb2gmx -f 1AKI_clean.pdb -o 1AKI_processed.gro -water spce', '15 0', input_files, output_files, [], [])
    assert len(job_id) > 0
    jm.wait_until_completion(job_id)
    jm.download_files(output_files)
    for filename in output_files:
        assert os.path.exists(os.path.join(test_dir, filename))

    # submit a job with wrong input
    # job_id = job_mgr.submit_job(c, 'pdb2gmx', '-f 1AKI_clean.pdb -o 1AKI_processed.gro -water spce', '15 0', '1AKI_clean.pdb', ["1AKI_processed.gro", "topol.top", "posre.itp"])
    # c.wait_until_completion(job_id)
    # (output, error) = job_mgr.get_output(c, job_id)
    # assert output == {}
    # assert error != ''
    # sys.stdout.write(CURSOR_UP_ONE)
    # sys.stdout.write(ERASE_LINE)
    print("-------------- Testing Gromacs Job Done --------------")
    # clean
    shutil.rmtree(test_dir)

def test_job_manager():
    # setup
    test_dir = 'test_job_manager'
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.mkdir(test_dir)
    #
    jm = JobManager()
    test_gromacs(jm, test_dir)
    # clean
    # shutil.rmtree(test_dir)

# def test_recgen(c: chiral_client.client.Client = _create_client()):
#     test_dir = 'test_recgen'
#     if os.path.exists(test_dir):
#         shutil.rmtree(test_dir)
#     os.mkdir(test_dir)
#     for sample in ['sample1', 'sample4']:
#         shutil.copyfile(f'{os.environ["CHIRAL_DATA_DIR"]}/recgen/inputs/{sample}.mol', f'{test_dir}/{sample}.mol')
#     print("-------------- Testing ReCGen Job --------------")
#     job_mgr = chiral_client.RecGenJobManager()

#     for (mol_file, result_count) in [
#         ('sample1', 1117),
#         ('sample4', 33),
#     ]:
#         with open(f'{test_dir}/{mol_file}.mol') as f:
#             input_mol = f.read()
#             f.close()
#         job_id = job_mgr.submit_job(c, input_mol)
#         c.wait_until_completion(job_id)
#         (output, error) = job_mgr.get_output(c, job_id)
#         assert len(output) == result_count
#         assert error == ''
#     sys.stdout.write(CURSOR_UP_ONE)
#     sys.stdout.write(ERASE_LINE)
#     print("-------------- Testing ReCGen Job Done --------------")
#     shutil.rmtree(test_dir)

# def test_llama2(c: chiral_client.client.Client = _create_client()):
#     print("-------------- Testing LLaMA2 Job --------------")
#     job_mgr = chiral_client.Llma2JobManager()
#     job_id = job_mgr.submit_job(c, 0.0, "I am so tired today after work")
#     c.wait_until_completion(job_id)
#     (output, error) = job_mgr.get_output(c, job_id)
#     # print(output['text'])
#     assert len(output['text']) > 0
#     assert error == ''
#     sys.stdout.write(CURSOR_UP_ONE)
#     sys.stdout.write(ERASE_LINE)
#     print("-------------- Testing LLaMA2 Job Done --------------")

if __name__ == '__main__':
    test_ftp_client()
    test_chiral_client()
    test_job_manager()
