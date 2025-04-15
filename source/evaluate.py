from openai import OpenAI
with open("../../drums_llm.key") as f:
    key = f.read().strip()
client = OpenAI(api_key = key)
import json
from parse import parse_drum_notation, parse_response
from unit_tests import *

with open("../prompts/notation.txt") as f:
    notation = f.read()

with open("../prompts/requests.json") as f:
    data = json.load(f)
    requests = data["requests"]

example_first_response = "Certainly! Based on your instructions and the rules provided, here’s a reasonable one-bar drum beat using the notation style you described:\n\n@@@\nK: O---|----|O---|----  \nS: ----|O---|----|O---  \nH: x---|x---|x---|x---  \nT: ----|----|----|----  \nC: ----|----|----|----  \n@@@\n\n**Explanation:**  \n- Kick (K) is played on the first 16th note of beat 1 and 3.\n- Snare (S) is played on the first 16th note of beats 2 and 4 (typical backbeat).\n- HiHat (H) is played every first 16th note of each beat (steady).\n- No Toms or Cymbals, leaving hands free for Snare and HiHat and obeying all rules."

def run_unit_test(drum_dict, unit_test_name, unit_test_args):
    # Get the function from the unit_tests module by name
    unit_test_func = globals()[unit_test_name]
    # Call the function with drum_dict as the first argument, then unpack the rest
    return unit_test_func(drum_dict, *unit_test_args)

for request_block in requests:
    request = request_block["request"]
    unit_test_name = request_block["unit_test_name"]
    unit_test_args = request_block["unit_test_args"]

    print("Request: ", request)

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
            "role": "user",
            "content": [
                {
                "type": "input_text",
                "text": notation
                }
            ]
            },
            {
            "role": "assistant",
            "content": [
                {
                    "type": "output_text",
                    "text": example_first_response
                }
            ]
            },
            {
            "role": "user",
            "content": [
                {
                "type": "input_text",
                "text": request
                }
            ]
            }
        ],
        text={
            "format": {
            "type": "text"
            }
        },
        reasoning={},
        tools=[],
        temperature=1,
        max_output_tokens=2048,
        top_p=1,
        store=True
    )
    response_txt = response.output[0].content[0].text
    drum_notation = parse_response(response_txt)
    print("Response:\n" + drum_notation)
    drum_dict = parse_drum_notation(drum_notation)
    unit_test_result = run_unit_test(drum_dict, unit_test_name, unit_test_args)
    if unit_test_result:
        print("Unit test passed.")
    else:
        print("Unit test failed.")
    
    print("\n")