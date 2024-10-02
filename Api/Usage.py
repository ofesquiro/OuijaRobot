class Usage:
    def __init__(self, completion_tokens: int, prompt_tokens: int, total_tokens: int):
        self.completion_tokens = completion_tokens
        self.prompt_tokens = prompt_tokens
        self.total_tokens = total_tokens