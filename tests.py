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
    job_id = job_mgr.submit_job(c, 'pdb2gmx', '-f 1AKI_clean.pdb -o 1AKI_processed.gro -water spce', '15 0', 'gromacs', ['1AKI_clean.pdb'], ["1AKI_processed.gro", "topol.top", "posre.itp"])
    print(job_id)


    # remote_parent_dir = "python_test/subfolder"
    # remote_dir = "python_test/subfolder/lysozyme"
    # if c.is_remote_dir(remote_parent_dir, 'lysozyme'):
    #     c.remove_remote_dir(remote_parent_dir, 'lysozyme')
    # c.create_remote_dir(remote_dir)
    # c.upload_files([("1AKI_clean.pdb", "examples/files/lysozyme", remote_dir)])
    # # submit jobs
    # gromacs_job = chiral_client.GromacsJob(client=c)
    # gromacs_job.set_input('lysozyme', 'pdb2gmx', ["-f", "1AKI_clean.pdb", "-o", "1AKI_processed.gro", "-water", "spce"], ["15 0"], 'python_test/subfolder', ["1AKI_clean.pdb"], ["1AKI_processed.gro", "topol.top", "posre.itp"])
    # assert gromacs_job.requirement == r'{"ji":"{\"simulation_id\":\"lysozyme\",\"sub_command\":\"pdb2gmx\",\"arguments\":[\"-f\",\"1AKI_clean.pdb\",\"-o\",\"1AKI_processed.gro\",\"-water\",\"spce\"],\"prompts\":[\"15 0\"],\"files_dir\":\"python_test/subfolder\",\"files_input\":[\"1AKI_clean.pdb\"],\"files_output\":[\"1AKI_processed.gro\",\"topol.top\",\"posre.itp\"]}","opk":"GromacsRunGMXCommand","dsk":"Empty"}'
    # assert gromacs_job.id == None
    # gromacs_job.submit()
    # assert len(gromacs_job.id) == 32
    # assert gromacs_job.status_label == None
    # gromacs_job.check_status()
    # assert gromacs_job.status_label == "Processing"
    # while gromacs_job.status_label == "Processing":
    #     time.sleep(1.0)
    #     gromacs_job.check_status()
    # gromacs_job.get_output()
    # assert gromacs_job.status_label == 'Completed'
    # assert gromacs_job.output.success

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