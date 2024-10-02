from typing import List 
from Choice import Choice
from Prompt_filter_result import PromptFilterResults
from Usage import Usage

class Response:
    def __init__(self, choices: List[Choice], created: int, response_id: str, model: str, object_type: str, 
                 prompt_filter_results: List[PromptFilterResults], system_fingerprint: str, usage: Usage):
        self.choices = choices
        self.created = created
        self.id = response_id
        self.model = model
        self.object = object_type
        self.prompt_filter_results = prompt_filter_results
        self.system_fingerprint = system_fingerprint
        self.usage = usage