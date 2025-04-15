def have_inst(drum_dict, insts):
    for inst in insts:
        measures = drum_dict.get(inst, [])
        # Flatten the list of lists
        notes = [note for measure in measures for note in measure]
        # If all notes are '-', return False
        if notes and all(note == '-' for note in notes):
            return False
    return True