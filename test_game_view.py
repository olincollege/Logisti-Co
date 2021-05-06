"""
Test functions
"""

import pytest

from file import (
    functions
)


# Define sets of test cases.
sample_cases = [
    # case 1
    (input, output),
]
@pytest.mark.parametrize("inputs",sample_cases)
def test_function(inputs):
    """
    Description goes here
    Args:
        inputs: the inputs of the function
    """
    assert function(input) == output