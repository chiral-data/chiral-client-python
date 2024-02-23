# import json
# import typing
# import functools
# from .. import Client
# from . import JobRequirement, OperatorKind, DatasetKind

# class Input:
#     db_file: str
#     mol: str

#     def __init__(self, db_file: str, mol: str):
#         self.db_file = db_file
#         self.mol = mol

# class JobManager:
#     def submit_job(self, client: Client, mol: str):
#         fragment_db = "DrugBank_M.db"
#         # fragment_db = "kegg_drug220912.db"
#         divisor = 40
#         print(f'using fragment db {fragment_db} and divisor {divisor}')
#         input = Input(fragment_db, mol)
#         jr = JobRequirement(json.dumps(input.__dict__), OperatorKind.ReCGenBuild, DatasetKind.Empty)
#         return client.submit_job(json.dumps(jr.__dict__), divisor)

#     def get_output(self, client: Client, job_id: str) -> (typing.List[str], str):
#         def map_func(output):
#             return json.loads(output)['smiles']
#         def reduce_func(vec_1: typing.List[str], vec_2: typing.List[str]):
#             for smiles in vec_2:
#                 if smiles not in vec_1:
#                     vec_1.append(smiles)
#             return vec_1

#         (outputs, error) = client.get_job_result(job_id)
#         if error:
#             return ({}, error)
#         else:
#             return (functools.reduce(reduce_func, map(map_func, outputs), []), error)
