
# This class allow to transform the string that come from a checkbox form field to a boolean
class CheckboxValueToBoolTransformer:

    def transform(self, string: str) -> bool :
        if string == 'on': return True
        return False
