import argparse
from openai import OpenAI
with open("../../drums_llm.key") as f:
    key = f.read().strip()
client = OpenAI(api_key = key)
import json
from parse import parse_drum_notation, parse_response
from unit_tests import *
from notation_to_midi import notation_to_midi
from midi_to_audio import midi_to_audio

# Argument parsing
parser = argparse.ArgumentParser(description="Evaluate drum LLM requests or instructions.")
parser.add_argument('--type', choices=['initialize', 'edit'], required=True, help="Type: 'instruction' or 'request'")
parser.add_argument('--id', nargs='+', required=True, help="List of IDs to process")
args = parser.parse_args()

DEFAULT_INITIALIZE_REQUEST = "Now generate one bar of any reasonable drum groove."

with open("../prompts/notation.txt") as f:
    notation = f.read()

with open("../prompts/requests.json") as f:
    data = json.load(f)
    requests = data[args.type]

DEFAULT_FIRST_RESPONSE = "Certainly! Based on your instructions and the rules provided, here’s a reasonable one-bar drum beat using the notation style you described:\n\n@@@\nK: O---|----|O---|----  \nS: ----|O---|----|O---  \nH: x---|x---|x---|x---  \nT: ----|----|----|----  \nC: ----|----|----|----  \nR: ----|----|----|----  \n@@@\n\n**Explanation:**  \n- Kick (K) is played on the first 16th note of beat 1 and 3.\n- Snare (S) is played on the first 16th note of beats 2 and 4 (typical backbeat).\n- HiHat (H) is played every first 16th note of each beat (steady).\n- No Toms or Cymbals, leaving hands free for Snare and HiHat and obeying all rules."

def run_unit_test(drum_dict, unit_test_name, unit_test_args):
    # Get the function from the unit_tests module by name
    unit_test_func = globals()[unit_test_name]
    # Call the function with drum_dict as the first argument, then unpack the rest
    return unit_test_func(drum_dict, *unit_test_args)

def diff(drum_dict_original, drum_dict_edited):
    for inst in drum_dict_original.keys():
        if inst not in drum_dict_edited:
            print(f"Instrument {inst} is missing in the edited version.")
            continue
        original_measures = drum_dict_original[inst]
        edited_measures = drum_dict_edited[inst]
        for i, (original_measure, edited_measure) in enumerate(zip(original_measures, edited_measures)):
            for j, (original_note, edited_note) in enumerate(zip(original_measure, edited_measure)):
                if original_note != edited_note:
                    print(f"At measure {i+1}, note {j+1}: {original_note} -> {edited_note}")
                    return False
    return True

for id in args.id:
    id = str(id)
    request_block = requests[id]
    request = request_block["request"]
    unit_test_name = request_block["unit_test_name"]
    unit_test_args = request_block["unit_test_args"]

    print("Request: ", request)
    if args.type == "initialize":
        prompt = notation + "\n" + request
        input=[
            {
                "role": "user",
                "content": [
                    {
                    "type": "input_text",
                    "text": prompt
                    }
                ]
            }
        ]
    elif args.type == "edit":
        prompt = notation + "\n" + DEFAULT_INITIALIZE_REQUEST 
        input=[
            {
                "role": "user",
                "content": [
                    {
                    "type": "input_text",
                    "text": prompt
                    }
                ]
                },
                {
                "role": "assistant",
                "content": [
                    {
                        "type": "output_text",
                        "text": DEFAULT_FIRST_RESPONSE
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
        ]

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
                    "text": DEFAULT_FIRST_RESPONSE
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
    # Print
    print("Response:\n" + drum_notation)
    # Unit Test
    drum_dict = parse_drum_notation(drum_notation)
    if unit_test_name:
        print("\nRunning unit test: ", unit_test_name)
        unit_test_result = run_unit_test(drum_dict, unit_test_name, unit_test_args)
        if unit_test_result:
            print("Unit test passed.")
        else:
            print("Unit test failed.")
    else:
        print("No unit test provided.")
    # Diff TODO
    # Convert to MIDI
    notation_to_midi(drum_notation)
    # Convert to audio
    midi_to_audio()
    
    print("\n")