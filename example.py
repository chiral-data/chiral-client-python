#!/usr/bin/python
#

import os
import shutil
import time
from chiral_client import JobManager, AppType

data_dir = os.environ["CHIRAL_DATA_DIR"]

def copy_input_files(local_dir: str, project_name: str):
    example_data_dir = os.path.join(data_dir, 'gromacs', project_name)
    for filename in os.listdir(example_data_dir):
        shutil.copyfile(f'{example_data_dir}/{filename}', f'{local_dir}/{filename}')

def create_job_manager() -> JobManager:
    user_email = os.environ['CHIRAL_USER_EMAIL']
    token_api = os.environ['CHIRAL_TOKEN_API']
    chiral_computing_url = os.environ['CHIRAL_CLOUD_URL']
    return JobManager(user_email, token_api, chiral_computing_url)

def run_example_job_management(jm: JobManager):
    # JobManager settings
    jm.create_remote_dir('.', 'gromacs')
    jm.set_remote_dir('.', 'gromacs')
    project_name = 'Mg_Ion_310d'
    jm.set_project_name(project_name)
    os.mkdir(os.path.join(project_name))
    jm.set_local_dir(os.path.join(project_name))
    # Prepare input files
    copy_input_files(jm.local_dir, project_name)
    output_files = ['em1_psr1000.tpr', 'em1_psr1000.tng']
    checkpoint_files = ['npt_eq2.cpt']
    for filename in output_files:
        os.remove(os.path.join(jm.local_dir, filename))
    # Submit the job
    jm.upload_directory()
    script_file = '310d.sh'
    job_id = jm.submit_job_script(script_file=script_file, apps=[AppType.Gromacs], input_files=[], output_files=output_files, checkpoint_files=checkpoint_files, log_files=[])
    time.sleep(1.0)
    # Check the job status
    assert jm.get_job_status(job_id) == 'Processing'
    # Get log files
    jm.get_log_files(job_id)
    time.sleep(2.0)
    log_files = [f'{job_id}.out', f'{job_id}.err']
    jm.download_files(log_files)
    for log_file in log_files:
        log_file_path = os.path.join(jm.local_dir, log_file)
        assert os.path.isfile(log_file_path)
    # Cancel the job
    jm.cancel_job(job_id)
    time.sleep(1.0)
    assert jm.get_job_status(job_id) == 'Cancelled'
    # clean the storage
    jm.remove_remote_dir_all('gromacs', project_name)


    # another script job
    script_file = '310d.sh'
    output_files = ['em1_psr1000.tpr', 'em1_psr1000.tng']
    checkpoint_files = ['npt_eq2.cpt']
    # as a demonstration, reduce the number of commands in the scripts to 2 in order to get the result quickly
    with open(os.path.join(jm.local_dir, script_file), 'r') as f:
        lines = f.readlines()
        f.close()
    with open(os.path.join(jm.local_dir, script_file), 'w') as f:
        f.write(''.join(lines[:2]))
        f.close()
    jm.upload_directory()
    job_id = jm.submit_job_script(script_file=script_file, apps=[AppType.Gromacs], input_files=[], output_files=output_files, checkpoint_files=checkpoint_files, log_files=[])
    jm.wait_until_completion(job_id)
    for file_output in output_files:
        assert not os.path.exists(os.path.join(jm.local_dir, file_output))
    jm.download_files(output_files)
    for file_output in output_files:
        assert os.path.exists(os.path.join(jm.local_dir, file_output))
    shutil.rmtree(os.path.join(project_name))
    # Clean directories
    jm.remove_remote_dir_all('.', 'gromacs')
    shutil.rmtree(project_name)

def run_script_job(jm: JobManager, protein: str, mg_ion: str):
    project_name = f'{mg_ion}_{protein}'
    jm.set_project_name(project_name)
    os.mkdir(os.path.join(project_name))
    jm.set_local_dir(os.path.join(project_name))
    copy_input_files('rna_ol3', project_name)

    example_data_dir = os.path.join(data_dir, 'gromacs', project_name)
    for filename in os.listdir(example_data_dir):
        shutil.copyfile(f'{example_data_dir}/{filename}', f'{jm.local_dir}/{filename}')
    jm.upload_directory()
    script_file = f'{protein}.sh'
    job_id = jm.submit_job_script(script_file=script_file, apps=[AppType.Gromacs], input_files=[], output_files=[], checkpoint_files=[], log_files=[])


proteins = ['1i7j', '1yn2', '2q1r', '3ftm', '3gvn', '3ssf', '310d']
mg_ions = ['Mg_Ion', 'No_Mg_Ion']

def main():
    jm = create_job_manager()
    job_management(jm)

if __name__ == '__main__':
    main()
