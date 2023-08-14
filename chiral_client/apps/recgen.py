import json
import typing
import functools
from .. import Client 
from . import JobRequirement, OperatorKind, DatasetKind

class Input:
    mol: str

    def __init__(self, mol: str):
        self.mol = mol

class JobManager:
    def submit_job(self, client: Client, mol: str, divisor: int):
        input = Input(mol)
        jr = JobRequirement(json.dumps(input.__dict__), OperatorKind.ReCGenBuild, DatasetKind.Empty)
        return client.submit_job(json.dumps(jr.__dict__), divisor)
    
    def get_output(self, client: Client, job_id: str) -> (typing.List[str], str):
        def map_func(output):
            return json.loads(output)['results']
        def reduce_func(vec_1: typing.List[str], vec_2: typing.List[str]):
            for smiles in vec_2:
                if smiles not in vec_1:
                    vec_1.append(smiles)
            return vec_1

        (outputs, error) = client.get_job_result(job_id)
        if error:
            return ({}, error)
        else:
            return (functools.reduce(reduce_func, map(map_func, outputs), []), error)

