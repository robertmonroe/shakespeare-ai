
class EditorAgentPatched:
    def rewrite_with_review(self, text:str, review:dict):
        return text + "\n# Edited using review"
