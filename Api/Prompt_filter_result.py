from Content_filer_result import ContentFilterResults

class PromptFilterResults:
    def __init__(self, prompt_index: int, content_filter_results: ContentFilterResults):
        self.prompt_index = prompt_index
        self.content_filter_results = content_filter_results