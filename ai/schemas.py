class ExplainRequest:
    def __init__(self, text, context=""):
        self.text = text
        self.context = context


class ExplainResponse:
    def __init__(self, definition, steps=None, example=""):
        self.definition = definition
        self.steps = steps or []
        self.example = example