import json
import os
import copy
import itertools

def load_json_file(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)

def main():
    # Load the input files
    requests_path = os.path.join('drums-with-llm-2', 'prompts', 'requests.json')
    grooves_path = os.path.join('drums-with-llm-2', 'prompts', 'grooves.json')
    
    requests_data = load_json_file(requests_path)
    grooves_data = load_json_file(grooves_path)
    
    # Define instrument mappings
    instruments = [
        {"name": "kick", "code": "K"},
        {"name": "snare", "code": "S"},
        {"name": "tom", "code": "T"},
        {"name": "hihat", "code": "H"},
        {"name": "cymbal", "code": "C"},
        {"name": "ride", "code": "R"}
    ]
    
    # Initialize output data
    unrolled_data = {}
    next_id = 0
    
    # Process edit requests
    for section_key in ["edit", "20"]:  # Process both "edit" and "20" sections
        if section_key not in requests_data:
            continue
            
        if section_key == "edit":
            section = requests_data[section_key]
        else:
            # Handle the "20" section (which is a single item, not a dict of items)
            section = {section_key: requests_data[section_key]}
            
        for request_id, request in section.items():
            # Store original request with placeholders
            templated_request = request["request"] if "request" in request else ""
            
            # Determine which instrument combinations to use
            if "@inst0@" in templated_request or "@i0@" in templated_request:
                # We need to substitute instruments
                if "@inst1@" in templated_request or "@i1@" in templated_request or "@ii@" in templated_request or "@ins1t@" in templated_request:
                    # Need two different instruments
                    instrument_combinations = list(itertools.permutations(instruments, 2))
                else:
                    # Need just one instrument
                    instrument_combinations = [(inst, None) for inst in instruments]
            else:
                # No substitution needed
                instrument_combinations = [(None, None)]
            
            # Determine which grooves to use
            original_groove_name = request.get("original_groove_name", "")
            if original_groove_name == "any":
                grooves_to_use = grooves_data["base_grooves"]
            else:
                # Use the specified groove
                grooves_to_use = [{"name": original_groove_name, "groove": request.get("original_groove", "")}]
            
            # Create unrolled entries
            for inst_combo in instrument_combinations:
                for groove in grooves_to_use:
                    new_request = copy.deepcopy(request)
                    
                    # Set original templated request
                    new_request["templated_request"] = templated_request
                    
                    # Replace instrument placeholders
                    new_request["request"] = templated_request
                    
                    if inst_combo[0]:
                        new_request["request"] = new_request["request"].replace("@inst0@", inst_combo[0]["name"])
                        new_request["request"] = new_request["request"].replace("@i0@", inst_combo[0]["code"])
                    
                    if inst_combo[1]:
                        new_request["request"] = new_request["request"].replace("@inst1@", inst_combo[1]["name"])
                        new_request["request"] = new_request["request"].replace("@i1@", inst_combo[1]["code"])
                        new_request["request"] = new_request["request"].replace("@ii@", inst_combo[1]["code"])
                        new_request["request"] = new_request["request"].replace("@ins1t@", inst_combo[1]["name"])
                    
                    # Replace groove information
                    if original_groove_name == "any":
                        new_request["original_groove_name"] = groove["name"]
                        new_request["original_groove"] = groove["groove"]
                    
                    # Update unit tests if needed
                    if "unit_tests" in new_request:
                        update_unit_tests(new_request["unit_tests"], inst_combo)
                    
                    # Add to output data with new ID
                    unrolled_data[str(next_id)] = new_request
                    next_id += 1
    
    # Write output file
    output_path = os.path.join('drums-with-llm-2', 'prompts', 'requests_unrolled.json')
    with open(output_path, 'w') as f:
        json.dump(unrolled_data, f, indent=4)
    
    print(f"Created {output_path} with {next_id} entries")

def update_unit_tests(unit_tests, inst_combo):
    """Update unit test arguments with instrument codes"""
    for test_type, test_list in unit_tests.items():
        if test_type in ["and", "or"]:
            for test in test_list:
                update_unit_tests(test, inst_combo)
        elif test_type == "unit_test_name":
            args = unit_tests.get("unit_test_args", [])
            for i, arg in enumerate(args):
                if isinstance(arg, str):
                    if arg == "@i0@" and inst_combo[0]:
                        args[i] = inst_combo[0]["code"]
                    elif arg in ["@i1@", "@ii@"] and inst_combo[1]:
                        args[i] = inst_combo[1]["code"]

if __name__ == "__main__":
    main()