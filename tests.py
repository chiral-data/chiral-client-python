import sys
import os
import shutil 
import chiral_client

CURSOR_UP_ONE = '\x1b[1A' 
ERASE_LINE = '\x1b[2K' 

USE_REMOTE = True

def _create_client_for_local_server() -> chiral_client.client.Client:
    user_email = 'new_user@gmail.com'
    user_token_api = "ocgr295kqvtxvxpzjdcgemxf0hda7axpaunwjnl5k4dum1f26tdzlplk01ya38gz"
    chiral_computing_host = 'localhost'
    chiral_computing_port = '20001'
    return chiral_client.client.Client(user_email, user_token_api, chiral_computing_host, chiral_computing_port)

def _create_client_for_remote_server() -> chiral_client.client.Client:
    user_email = os.environ['CHIRAL_USER_EMAIL']
    token_api = os.environ['CHIRAL_TOKEN_API']
    chiral_computing_host = '133.242.237.70'
    chiral_computing_port = '20000'
    return chiral_client.client.Client(user_email, token_api, chiral_computing_host, chiral_computing_port)

def _create_client() -> chiral_client.client.Client:
    if USE_REMOTE:
        return _create_client_for_remote_server()
    else:
        return _create_client_for_local_server()

def test_gromacs(c: chiral_client.client.Client = _create_client()):
    test_dir = 'test_gromacs'
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.mkdir(test_dir)
    shutil.copyfile(f'{os.environ["CHIRAL_DATA_DIR"]}/gromacs/lysozyme/1AKI_clean.pdb', f'{test_dir}/1AKI_clean.pdb')
    print("-------------- Testing Gromacs Job --------------")
    c.connect_file_server()
    simulation_id = 'lysozyme'
    if c.is_remote_dir('gromacs', simulation_id):
        c.remove_remote_dir('gromacs', simulation_id)
    job_mgr = chiral_client.GromacsJobManager(simulation_id, test_dir, c)
    # upload input files
    job_mgr.upload_files(c, ['1AKI_clean.pdb'])
    # submit a job
    job_id = job_mgr.submit_job(c, 'pdb2gmx', '-f 1AKI_clean.pdb -o 1AKI_processed.gro -water spce', '15 0', ['1AKI_clean.pdb'], ["1AKI_processed.gro", "topol.top", "posre.itp"])
    assert len(job_id) > 0
    c.wait_until_completion(job_id)
    (output, error) = job_mgr.get_output(c, job_id)
    assert len(output['stdout']) > 0
    assert len(output['stderr']) == 0
    assert error == ''
    # submit a job with wrong input
    job_id = job_mgr.submit_job(c, 'pdb2gmx', '-f 1AKI_clean.pdb -o 1AKI_processed.gro -water spce', '15 0', '1AKI_clean.pdb', ["1AKI_processed.gro", "topol.top", "posre.itp"])
    c.wait_until_completion(job_id)
    (output, error) = job_mgr.get_output(c, job_id)
    assert output == {} 
    assert error != ''
    sys.stdout.write(CURSOR_UP_ONE) 
    sys.stdout.write(ERASE_LINE) 
    print("-------------- Testing Gromacs Job Done --------------")
    shutil.rmtree(test_dir)

def test_recgen(c: chiral_client.client.Client = _create_client()): 
    test_dir = 'test_recgen'
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.mkdir(test_dir)
    for sample in ['sample1', 'sample4']:
        shutil.copyfile(f'{os.environ["CHIRAL_DATA_DIR"]}/recgen/inputs/{sample}.mol', f'{test_dir}/{sample}.mol')
    print("-------------- Testing ReCGen Job --------------")
    job_mgr = chiral_client.RecGenJobManager()

    for (mol_file, result_count) in [
        ('sample1', 1117), 
        ('sample4', 33),
    ]:
        with open(f'{test_dir}/{mol_file}.mol') as f:
            input_mol = f.read()
            f.close()
        job_id = job_mgr.submit_job(c, input_mol)
        c.wait_until_completion(job_id)
        (output, error) = job_mgr.get_output(c, job_id)
        assert len(output) == result_count
        assert error == ''
    sys.stdout.write(CURSOR_UP_ONE) 
    sys.stdout.write(ERASE_LINE) 
    print("-------------- Testing ReCGen Job Done --------------")
    shutil.rmtree(test_dir)

def test_llama2(c: chiral_client.client.Client = _create_client()): 
    print("-------------- Testing LLaMA2 Job --------------")
    job_mgr = chiral_client.Llma2JobManager()
    job_id = job_mgr.submit_job(c, 0.0, "I am so tired today after work")
    c.wait_until_completion(job_id)
    (output, error) = job_mgr.get_output(c, job_id)
    # print(output['text'])
    assert len(output['text']) > 0
    assert error == ''
    sys.stdout.write(CURSOR_UP_ONE) 
    sys.stdout.write(ERASE_LINE) 
    print("-------------- Testing LLaMA2 Job Done --------------")

def create_file(filename: str, local_dir: str):
    with open(f'{local_dir}/{filename}', 'w') as f:
        f.writelines(f'this is file {filename}')
        f.close()

def remove_file(filename: str, local_dir: str):
    full_path =  f'{local_dir}/{filename}'
    if os.path.exists(full_path):
        os.remove(full_path)
    
def test_file_transfer(c: chiral_client.client.Client = _create_client()): 
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
    test_recgen()
    test_llama2()
    # test_file_transfer()