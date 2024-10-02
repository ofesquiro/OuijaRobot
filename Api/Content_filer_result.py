from Filter_results import FilterResults
class ContentFilterResults:
    def __init__(self, hate: FilterResults, protected_material_code: FilterResults, protected_material_text: FilterResults,
                 self_harm: FilterResults, sexual: FilterResults, violence: FilterResults):
        self.hate = hate
        self.protected_material_code = protected_material_code
        self.protected_material_text = protected_material_text
        self.self_harm = self_harm
        self.sexual = sexual
        self.violence = violence
