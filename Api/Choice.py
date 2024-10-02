from Content_filer_result import ContentFilterResults
from typing import Optional
from Message import Message
class Choice:
    def __init__(self, content_filter_results: ContentFilterResults, finish_reason: str, index: int, logprobs: Optional[str], message: Message):
        self.content_filter_results = content_filter_results
        self.finish_reason = finish_reason
        self.index = index
        self.logprobs = logprobs
        self.message = message