class CombinationModel:
    def __init__(self, numbers, index):
        """Initializes the CombinationModel with a list of numbers and an index.
        :param numbers: List of numbers to be used in the model."""
        self.index = index
        self.numbers = sorted(numbers)
        self.properties = {}

    def calculate_properties(self, properties_functions, **kwargs):
        """Calculates properties of the numbers using provided functions.
        :param properties_functions: List of functions that take a list of numbers and return a key-value pair.
        """
        for func in properties_functions:
            if (
                func.__name__ in ("level_key", "level_members")
                and "population_size" in kwargs
            ):
                key, value = func(
                    self.numbers, population_size=kwargs["population_size"]
                )
            elif func.__name__ == "generate_boxes" and "index" in kwargs:
                key, value = func(self.numbers, kwargs["index"])
            else:
                key, value = func(self.numbers)
            self.properties[key] = value

    def to_dict(self):
        """Converts the model to a dictionary representation."""
        return {
            "index": self.index,
            "numbers": self.numbers,
            **self.properties,
        }
