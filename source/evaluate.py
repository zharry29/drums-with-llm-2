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
import os

# Argument parsing
parser = argparse.ArgumentParser(description="")
parser.add_argument('--data', choices=['instantiated', 'unrolled'], required=True, help="")
parser.add_argument('--model', default="gpt-4.1-mini", help="")
args = parser.parse_args()

DEFAULT_INITIALIZE_REQUEST = "Now generate one bar of any reasonable drum groove."

with open("../prompts/prompt.json") as f:
    prompt_structure = json.load(f)

with open("../prompts/initial_prompt.txt") as f:
    initial_prompt = f.read()

with open(f"../prompts/requests_{args.data}.json") as f:
    requests = json.load(f)

def run_unit_test(drum_dict, unit_test_name, unit_test_args):
    # Get the function from the unit_tests module by name
    unit_test_func = globals()[unit_test_name]
    # Call the function with drum_dict as the first argument, then unpack the rest
    return unit_test_func(drum_dict, *unit_test_args)

def diff(drum_dict_original, drum_dict_edited):
    output = []
    for inst in drum_dict_original.keys():
        if inst not in drum_dict_edited:
            msg = f"Instrument {inst} is missing in the edited version."
            output.append(msg)
            continue
        original_measures = drum_dict_original[inst]
        edited_measures = drum_dict_edited[inst]
        for i, (original_measure, edited_measure) in enumerate(zip(original_measures, edited_measures)):
            for j, (original_note, edited_note) in enumerate(zip(original_measure, edited_measure)):
                if original_note != edited_note:
                    msg = f"{inst}: At measure {i+1}, note {j+1}: {original_note} -> {edited_note}"
                    output.append(msg)
    if not output:
        return "No differences found."
    return "\n".join(output)

def build_prompt(prompt_structure, request_block):
    prompt = ""
    for component in prompt_structure["prompt0"]:
        if component == "@initial_prompt":
            prompt += initial_prompt
        elif component == "@original_groove":
            prompt += "\n" + request_block["original_groove"]
        elif component == "@request":
            prompt += "\n" + request_block["request"]
        else:
            prompt += "\n" + component
    return prompt

for id, request_block in requests.items():
    request = request_block["request"]

    print("Request: ", request)
    prompt = build_prompt(prompt_structure, request_block)
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

    response = client.responses.create(
        model=args.model,
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

    output_dir = f"../outputs/{args.data}-{args.model}"
    os.makedirs(output_dir, exist_ok=True)
    # Create output subdirectories if they don't exist
    for subdir in ["raw", "notation", "test_results", "midi", "audio"]:
        os.makedirs(os.path.join(output_dir, subdir), exist_ok=True)
    # Save raw response text
    raw_output_path = os.path.join(output_dir, "raw", f"{id}.txt")
    with open(raw_output_path, "w") as f:
        f.write(response_txt)
    # Save drum notation
    notation_output_path = os.path.join(output_dir, "notation", f"{id}.txt")
    with open(notation_output_path, "w") as f:
        f.write(drum_notation)

    # Print
    # print("Response:\n" + drum_notation)
    # Unit Test
    drum_dict = parse_drum_notation(drum_notation)

    
    test_results_path = os.path.join(output_dir, "test_results", f"{id}.txt")
    # Clear previous results for this id
    open(test_results_path, "w").close()

    passed_universal_checks = universal_checks(drum_dict)
    def log(msg):
        print(msg)
        with open(test_results_path, "a") as f:
            f.write(str(msg) + "\n")
    if not passed_universal_checks:
        log("Universal checks failed.")
        continue
    original_drum_notation = parse_response(request_block["original_groove"])
    original_drum_dict = parse_drum_notation(original_drum_notation)

    unit_tests = request_block["unit_tests"]
    if unit_tests:
        pass_all = True
        conjuction = "and" if "and" in unit_tests else "or"
        for unit_test_and in unit_tests[conjuction]:
            unit_test_name = unit_test_and["unit_test_name"]
            unit_test_args = unit_test_and["unit_test_args"]
            log(f"Running unit test: {unit_test_name}")
            unit_test_result = run_unit_test(drum_dict, unit_test_name, unit_test_args)
            if unit_test_result:
                log("Unit test passed.")
                if conjuction == "or":
                    pass_all = True
            else:
                log("Unit test failed.")
                if conjuction == "and":
                    pass_all = False
        if pass_all:
            log("All unit tests passed.")
        else:
            log("Some unit tests failed.")
    else:
        log("No unit tests provided.")
    # Diff
    log(diff(original_drum_dict, drum_dict))
    # Convert to MIDI
    out_midi_fname = os.path.join(output_dir, "midi", f"{id}.mid")
    notation_to_midi(drum_notation, out_midi_fname)
    out_midi_original_fname = os.path.join(output_dir, "midi", f"{id}_original.mid")
    notation_to_midi(original_drum_notation, out_midi_original_fname)
    # Convert to audio
    out_audio_fname = os.path.join(output_dir, "audio", f"{id}.wav")
    midi_to_audio(out_midi_fname, out_audio_fname)
    out_audio_original_fname = os.path.join(output_dir, "audio", f"{id}_original.wav")
    midi_to_audio(out_midi_original_fname, out_audio_original_fname)
    


    print("\n")