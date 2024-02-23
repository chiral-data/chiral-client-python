# import json
# import typing
# from .. import Client
# from . import JobRequirement, OperatorKind, DatasetKind

# class Input:
#     temperature: float
#     prompt: str

#     def __init__(self, temperature: float, prompt: str):
#         self.temperature = temperature
#         self.prompt = prompt

# class JobManager:
#     def submit_job(self, client: Client, temperature: float, prompt: str):
#         input = Input(temperature, prompt)
#         jr = JobRequirement(json.dumps(input.__dict__), OperatorKind.CandleLLaMA2, DatasetKind.Empty)
#         return client.submit_job(json.dumps(jr.__dict__), 1)

#     def get_output(self, client: Client, job_id: str) -> (typing.List[str], str):
#         (outputs, error) = client.get_job_result(job_id)
#         if error:
#             return ({}, error)
#         else:
#             return (json.loads(outputs[0]), "")
