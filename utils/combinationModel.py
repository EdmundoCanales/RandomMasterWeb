class CombinationModel:
    def __init__(self, numbers, index):
        """Initializes the CombinationModel with a list of numbers and an index.
        :param numbers: List of numbers to be used in the model."""
        self.index = index
        self.numbers = sorted(numbers)
        self.properties = {}

    def calculate_properties(self, properties_functions):
        """Calculates properties of the numbers using provided functions.
        :param properties_functions: List of functions that take a list of numbers and return a key-value pair.
        """
        for func in properties_functions:
            key, value = func(self.numbers)
            self.properties[key] = value

    def to_dict(self):
        """Converts the model to a dictionary representation."""
        return {
            "index": self.index,
            "numbers": self.numbers,
            **self.properties,
        }
