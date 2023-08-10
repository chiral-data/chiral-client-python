import time
import os
import json
import chiral_client

user_email = 'new_user_2@gmail.com'
user_token_api = "i7oqcut9lw828uq6xv1cb1kqupllol0u"
chiral_computing_host = 'localhost'
chiral_computing_port = '20001'
chiral_file_host = '127.0.0.1' 
chiral_file_port = 2121

def test_gromacs(c: chiral_client.client.Client = chiral_client.client.Client(user_email, user_token_api, chiral_computing_host, chiral_computing_port, chiral_file_host, chiral_file_port)):
    print("-------------- Testing Gromacs Job --------------")
    c.connect_file_server()
    simulation_id = 'lysozyme'
    c.remove_remote_dir('gromacs', simulation_id)
    job_mgr = chiral_client.GromacsJobManager(simulation_id, 'examples/lysozyme/files', c)
    # upload input files
    job_mgr.upload_files(c, ['1AKI_clean.pdb'])
    # submit a job
    job_id = job_mgr.submit_job(c, 'pdb2gmx', '-f 1AKI_clean.pdb -o 1AKI_processed.gro -water spce', '15 0', 'gromacs', ['1AKI_clean.pdb'], ["1AKI_processed.gro", "topol.top", "posre.itp"])
    assert len(job_id) > 0
    job_mgr.wait_until_completion(c, job_id)
    (output, error) = job_mgr.get_output(c, job_id)
    assert output['success']
    assert error == ''
    # submit a job with wrong input
    job_id = job_mgr.submit_job(c, 'pdb2gmx', '-f 1AKI_clean.pdb -o 1AKI_processed.gro -water spce', '15 0', 'gromacs', '1AKI_clean.pdb', ["1AKI_processed.gro", "topol.top", "posre.itp"])
    job_mgr.wait_until_completion(c, job_id)
    (output, error) = job_mgr.get_output(c, job_id)
    assert output == {} 
    assert error != ''

def create_file(filename: str, local_dir: str):
    with open(f'{local_dir}/{filename}', 'w') as f:
        f.writelines(f'this is file {filename}')
        f.close()

def remove_file(filename: str, local_dir: str):
    full_path =  f'{local_dir}/{filename}'
    if os.path.exists(full_path):
        os.remove(full_path)
    
def test_file_transfer(c: chiral_client.client.Client = chiral_client.client.Client(user_email, user_token_api, chiral_computing_host, chiral_computing_port, chiral_file_host, chiral_file_port)):
    print("-------------- Testing File Transfer --------------")
    c.connect_file_server()

    # file list
    for remote_dir in ['gromacs_test_1', 'gromacs_test_2']:
        if not c.is_remote_dir('.', remote_dir):
            c.create_remote_dir(remote_dir)
    files = [
        ('1.txt', '.', 'gromacs_test_1'),
        ('2.txt', '.', 'gromacs_test_2')
    ]
    # file does not exist in remote server
    for f in files:
        assert not c.is_remote_file(f)

    # create local files and upload it
    for (fn, local_dir, _) in files:
        create_file(fn, local_dir)
    c.upload_files(files)

    # now files on remote servers
    for f in files:
        assert c.is_remote_file(f)

    # test remote dirs
    assert c.is_remote_dir('.', 'gromacs_test_1')
    assert c.is_remote_dir('.', 'gromacs_test_2')
    assert not c.is_remote_dir('.', 'gromacs_test_3')
    c.create_remote_dir('gromacs_test_3')
    assert c.is_remote_dir('.', 'gromacs_test_3')
    c.remove_remote_dir('.', 'gromacs_test_3')
    assert not c.is_remote_dir('.', 'gromacs_test_3')

    c.remove_files(files)
    for remote_dir in ['gromacs_test_1', 'gromacs_test_2']:
        c.remove_remote_dir('.', remote_dir)
    c.disconnect_file_server()
    for (fn, local_dir, _) in files:
        remove_file(fn, local_dir)


if __name__ == '__main__':
    test_gromacs()
    # test_file_transfer()