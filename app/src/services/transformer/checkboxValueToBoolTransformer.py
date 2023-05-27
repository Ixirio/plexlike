class CheckboxValueToBoolTransformer:

    def transform(self, string: str) -> bool :
        if string == 'on': return True
        return False
