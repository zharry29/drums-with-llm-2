# universal checks
def correct_insts(drum_dict):
    """Check if the drum_dict contains all the required instruments."""
    required_insts = ['K', 'S', 'H', 'T', 'C', 'R']
    for inst in required_insts:
        if inst not in drum_dict:
            return False
    return True

def correct_articulations(drum_dict):
    """Check if the drum_dict contains all the required articulations."""
    permitted_articulations = {
        'K': ['O', 'o', '-'],
        'S': ['O', 'o', 'X', 'x', '-'],
        'H': ['O', 'o', 'X', 'x', '-'],
        'T': ['O', 'o', '-'],
        'C': ['O', 'o', '-'],
        'R': ['O', 'o', 'X', 'x', '-']
    }
    for inst in drum_dict:
        beats = drum_dict[inst]
        # Flatten the list of lists
        notes = [note for beat in beats for note in beat]
        for note in notes:
            if note not in permitted_articulations.get(inst, []):
                return False
    return True

def correct_durations(drum_dict):
    """Check if there are exactly 4 beats, and each beat contains exactly 4 notes."""
    for inst in drum_dict:
        beats = drum_dict[inst]
        if len(beats) != 4:
            return False
        for beat in beats:
            if len(beat) != 4:
                return False
    return True

def universal_checks(drum_dict):
    """Run all the universal checks on the drum_dict."""
    if not correct_insts(drum_dict):
        return False
    if not correct_articulations(drum_dict):
        return False
    if not correct_durations(drum_dict):
        return False
    return True

def have_inst(drum_dict, inst):
    beats = drum_dict.get(inst, [])
    # Flatten the list of lists
    notes = [note for beat in beats for note in beat]
    # If all notes are '-', return False
    if notes and all(note == '-' for note in notes):
        return False
    return True

def no_inst(drum_dict, inst):
    beats = drum_dict.get(inst, [])
    # Flatten the list of lists
    notes = [note for beat in beats for note in beat]
    # If all notes are '-', return False
    if notes and not all(note == '-' for note in notes):
        return False
    return True

def have_articulation(drum_dict, inst, articulation):
    beats = drum_dict.get(inst, [])
    # Flatten the list of lists
    notes = [note for beat in beats for note in beat]
    if articulation not in notes:
        return False
    return True

def no_articulation(drum_dict, inst, articulation):
    beats = drum_dict.get(inst, [])
    # Flatten the list of lists
    notes = [note for beat in beats for note in beat]
    if articulation in notes:
        return False
    return True

def have_inst_on_note(drum_dict, inst, pos):
    beats = drum_dict.get(inst, [])
    # Flatten the list of lists
    notes = [note for beat in beats for note in beat]
    # If the note at the position is not '-', return True
    if notes[pos] != '-':
        return True
    return False

def have_inst_on_beat(drum_dict, inst, pos):
    beats = drum_dict.get(inst, [])
    for note in beats[pos]:
        if note == '-':
            return False
    return True

def no_inst_on_beat(drum_dict, inst, pos):
    beats = drum_dict.get(inst, [])
    for note in beats[pos]:
        if note != '-':
            return False
    return True

def no_inst_on_note(drum_dict, inst, pos):
    beats = drum_dict.get(inst, [])
    # Flatten the list of lists
    notes = [note for beat in beats for note in beat]
    # If the note at the position is '-', return True
    if notes[pos] != '-':
        return False
    return True

def have_articulation_on_note(drum_dict, inst, articulation, pos):
    beats = drum_dict.get(inst, [])
    # Flatten the list of lists
    notes = [note for beat in beats for note in beat]
    # If the note at the position is the articulation, return True
    if notes[pos] == articulation:
        return True
    return False

def no_articulation_on_note(drum_dict, inst, articulation, pos):
    beats = drum_dict.get(inst, [])
    # Flatten the list of lists
    notes = [note for beat in beats for note in beat]
    # If the note at the position is not the articulation, return True
    if notes[pos] != articulation:
        return True
    return False

def num_notes_more_than(drum_dict, threshold):
    total_count = 0 
    for inst, beats in drum_dict.items():
        # Flatten the list of lists
        notes = [note for beat in beats for note in beat]
        total_count += len([note for note in notes if note != '-'])
    if total_count > threshold:
        return True
    return False

def num_notes_less_than(drum_dict, threshold):
    total_count = 0 
    for inst, beats in drum_dict.items():
        # Flatten the list of lists
        notes = [note for beat in beats for note in beat]
        total_count += len([note for note in notes if note != '-'])
    if total_count < threshold:
        return True
    return False

def num_notes_inst_more_than(drum_dict, inst, threshold):
    beats = drum_dict.get(inst, [])
    # Flatten the list of lists
    notes = [note for beat in beats for note in beat]
    return len([note for note in notes if note != '-']) > threshold

def num_notes_inst_less_than(drum_dict, inst, threshold):
    beats = drum_dict.get(inst, [])
    # Flatten the list of lists
    notes = [note for beat in beats for note in beat]
    return len([note for note in notes if note != '-']) < threshold

def num_same_beats_inst_more_than(drum_dict, inst, threshold):
    beats = drum_dict.get(inst, [])
    return max(beats.count(beat) for beat in beats) > threshold

def num_same_beats_inst_less_than(drum_dict, inst, threshold):
    beats = drum_dict.get(inst, [])
    return max(beats.count(beat) for beat in beats) < threshold