import json
import os
import copy
import itertools
import random

def load_json_file(filepath):
    """Load a JSON file and return its contents"""
    with open(filepath, 'r') as f:
        return json.load(f)

def main():
    global INSTANTIATED
    for INSTANTIATED in [True, False]:
        # Define file paths
        requests_path = '../prompts/requests.json'
        grooves_path = '../prompts/grooves.json'
        output_path = '../prompts/requests_unrolled.json' if not INSTANTIATED else '../prompts/requests_instantiated.json'
        
        # Load the input files
        requests = load_json_file(requests_path)
        grooves = load_json_file(grooves_path)
        
        # Define instrument mappings (name to code)
        instruments = [
            {"name": "kick", "code": "K"},
            {"name": "snare", "code": "S"},
            {"name": "tom", "code": "T"},
            {"name": "hihat", "code": "H"},
            {"name": "cymbal", "code": "C"},
            {"name": "ride", "code": "R"}
        ]
        
        # Initialize the output dictionary and ID counter
        unrolled_requests = {}
        next_id = 0
        
        # Process each section of requests
        for section_key in requests.keys():
            if section_key == "edit":
                # Process each request in the "edit" section
                for request_id, request_data in requests[section_key].items():
                    next_id = process_request(request_data, instruments, grooves, next_id, unrolled_requests)
            else:
                # Process standalone items (like "20")
                next_id = process_request(requests[section_key], instruments, grooves, next_id, unrolled_requests)
        
        # Write the output file
        with open(output_path, 'w') as f:
            json.dump(unrolled_requests, f, indent=4)
        
        print(f"Created {output_path} with {next_id} entries")

def process_request(request_data, instruments, grooves, current_id, output_dict):
    """Process a single request, generating all combinations and adding them to the output dictionary"""
    start_id = current_id
    
    # Store the original request with placeholders
    templated_request = request_data.get("request", "")
    
    # Determine which instrument placeholders need to be replaced
    has_inst0 = "@inst0@" in templated_request or "@i0@" in templated_request
    has_inst1 = "@inst1@" in templated_request or "@i1@" in templated_request or "@ii@" in templated_request or "@ins1t@" in templated_request
    
    # Generate all possible instrument combinations
    if has_inst0 and has_inst1:
        # Need two different instruments (permutations where order matters)
        instrument_combinations = list(itertools.permutations(instruments, 2))
    elif has_inst0:
        # Need only one instrument
        instrument_combinations = [(inst, None) for inst in instruments]
    else:
        # No instrument placeholders
        instrument_combinations = [(None, None)]
    
    # Determine which grooves to use
    if request_data.get("original_groove_name") == "any":
        grooves_to_use = grooves["base_grooves"]
    else:
        # Use the specific groove already in the request
        grooves_to_use = [{
            "name": request_data.get("original_groove_name", ""),
            "groove": request_data.get("original_groove", "")
        }]
    
    # Generate all combinations of instruments and grooves
    random.shuffle(instrument_combinations)
    for inst_combo in instrument_combinations:
        random.shuffle(grooves_to_use)
        for groove in grooves_to_use:
            # Create a copy of the original request
            new_request = copy.deepcopy(request_data)
            
            # Add the templated request field
            new_request["templated_request"] = templated_request
            
            # Apply instrument replacements
            new_request["request"] = templated_request
            
            if inst_combo[0]:
                new_request["request"] = new_request["request"].replace("@inst0@", inst_combo[0]["name"])
                new_request["request"] = new_request["request"].replace("@i0@", inst_combo[0]["code"])
            
            if inst_combo[1]:
                new_request["request"] = new_request["request"].replace("@inst1@", inst_combo[1]["name"])
                new_request["request"] = new_request["request"].replace("@i1@", inst_combo[1]["code"])
                new_request["request"] = new_request["request"].replace("@ii@", inst_combo[1]["code"])
                new_request["request"] = new_request["request"].replace("@ins1t@", inst_combo[1]["name"])
            
            # Apply groove replacements if needed
            if request_data.get("original_groove_name") == "any":
                new_request["original_groove_name"] = groove["name"]
                new_request["original_groove"] = groove["groove"]
            
            # Update unit tests if needed
            if "unit_tests" in new_request:
                update_unit_tests(new_request["unit_tests"], inst_combo)
            
            # Add the new request to the output with an incremental ID
            output_dict[str(current_id)] = new_request
            current_id += 1

            if INSTANTIATED:
                break  # Only instantiate once, no need for multiple combinations
    
        if INSTANTIATED:
            break  # Only instantiate once, no need for multiple combinations
    return current_id

def update_unit_tests(unit_tests, inst_combo):
    """Recursively update instrument references in unit tests"""
    if isinstance(unit_tests, dict):
        for key, value in unit_tests.items():
            if key in ["and", "or"]:
                # Recursively process nested conditions
                for item in value:
                    update_unit_tests(item, inst_combo)
            elif key == "unit_test_args" and isinstance(value, list):
                # Replace instrument codes in test arguments
                for i, arg in enumerate(value):
                    if isinstance(arg, str):
                        if arg == "@i0@" and inst_combo[0]:
                            value[i] = inst_combo[0]["code"]
                        elif arg in ["@i1@", "@ii@"] and inst_combo[1]:
                            value[i] = inst_combo[1]["code"]

if __name__ == "__main__":
    main()