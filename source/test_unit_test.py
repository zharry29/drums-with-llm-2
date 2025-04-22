from parse import parse_drum_notation
from unit_tests import *

def run_unit_test(drum_dict, unit_test_name, unit_test_args):
    # Get the function from the unit_tests module by name
    unit_test_func = globals()[unit_test_name]
    # Call the function with drum_dict as the first argument, then unpack the rest
    return unit_test_func(drum_dict, *unit_test_args)

drum_notation = """
    K: O---|----|O---|----
    S: ----|S--o|----|O---
    H: x---|x---|x---|x---
    T: ----|----|-O--|---o
    C: O---|----|----|----
    R: ----|----|----|----
    """

drum_dict = parse_drum_notation(drum_notation)

unit_test_name = "no_inst_on_beat"
unit_test_args = ["K", 3]

if unit_test_name:
    print("\nRunning unit test: ", unit_test_name)
    unit_test_result = run_unit_test(drum_dict, unit_test_name, unit_test_args)
    if unit_test_result:
        print("Unit test passed.")
    else:
        print("Unit test failed.")
else:
    print("No unit test provided.")