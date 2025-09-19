What utils.access_nested_map Is
access_nested_map is a helper function used to retrieve values from nested dictionaries (maps) using a sequence of keys.

->an example
nested_map = {"a": {"b": {"c": 1}}}
path = ("a", "b", "c")

# This should return 1

utils.access_nested_map is a small utility function that retrieves values from a deeply nested dictionary using a tuple of keys. It’s typically implemented using a simple loop and raises KeyError on invalid paths. Unit testing involves checking both correct outputs and error handling.

Why is it Useful
Encapsulates repeated nested dict access logic.
Easy to unit test because it’s deterministic and pure (no side effects).
Raises built-in KeyError naturally — consistent with Python dict behavior.

Parameterized testing
This is running the same test logic with different sets of input and expected output automatically.

Instead of writing separate test methods for each case, you define one test and pass it multiple data sets. This:
Reduces duplication.
Makes tests easier to maintain.
Ensures consistency.

In Python’s unittest world, you can achieve this using the parameterized library.
pip install parameterized

How to Use parameterized
You import the decorator @parameterized.expand and supply a list of tuples — each tuple is one test case.
from parameterized import parameterized

class MyTests(unittest.TestCase):
    @parameterized.expand([
        ("case1", input1, expected1),
        ("case2", input2, expected2),
    ])
    def test_something(self, name, input_value, expected_value):
        self.assertEqual(my_function(input_value), expected_value)

Benefits
Cleaner tests — less copy-paste.
Scalable — easily add new cases.
Each case shows up separately in test output.

in conclusion
parameterized allows you to write one test function but run it over many input-output combinations.
With access_nested_map, you can parameterize both successful and error cases to keep your tests compact and clear.
