def have_inst(drum_dict, inst):
    measures = drum_dict.get(inst, [])
    # Flatten the list of lists
    notes = [note for measure in measures for note in measure]
    # If all notes are '-', return False
    if notes and all(note == '-' for note in notes):
        return False
    return True

def no_inst(drum_dict, inst):
    measures = drum_dict.get(inst, [])
    # Flatten the list of lists
    notes = [note for measure in measures for note in measure]
    # If all notes are '-', return False
    if notes and not all(note == '-' for note in notes):
        return False
    return True

def have_articulation(drum_dict, inst, articulation):
    measures = drum_dict.get(inst, [])
    # Flatten the list of lists
    notes = [note for measure in measures for note in measure]
    if articulation not in notes:
        return False
    return True

def no_articulation(drum_dict, inst, articulation):
    measures = drum_dict.get(inst, [])
    # Flatten the list of lists
    notes = [note for measure in measures for note in measure]
    if articulation in notes:
        return False
    return True

def have_inst_on_note(drum_dict, inst, pos):
    measures = drum_dict.get(inst, [])
    # Flatten the list of lists
    notes = [note for measure in measures for note in measure]
    # If the note at the position is not '-', return True
    if notes[pos] != '-':
        return True
    return False

def no_inst_on_note(drum_dict, inst, pos):
    measures = drum_dict.get(inst, [])
    # Flatten the list of lists
    notes = [note for measure in measures for note in measure]
    # If the note at the position is '-', return True
    if notes[pos] != '-':
        return False
    return True

def have_articulation_on_note(drum_dict, inst, articulation, pos):
    measures = drum_dict.get(inst, [])
    # Flatten the list of lists
    notes = [note for measure in measures for note in measure]
    # If the note at the position is the articulation, return True
    if notes[pos] == articulation:
        return True
    return False

def no_articulation_on_note(drum_dict, inst, articulation, pos):
    measures = drum_dict.get(inst, [])
    # Flatten the list of lists
    notes = [note for measure in measures for note in measure]
    # If the note at the position is not the articulation, return True
    if notes[pos] != articulation:
        return True
    return False

def num_notes_more_than(drum_dict, threshold):
    total_count = 0 
    for inst, measures in drum_dict.items():
        # Flatten the list of lists
        notes = [note for measure in measures for note in measure]
        total_count += len([note for note in notes if note != '-'])
    if total_count > threshold:
        return True
    return False

def num_notes_less_than(drum_dict, threshold):
    total_count = 0 
    for inst, measures in drum_dict.items():
        # Flatten the list of lists
        notes = [note for measure in measures for note in measure]
        total_count += len([note for note in notes if note != '-'])
    if total_count < threshold:
        return True
    return False