def have_inst_on_note(drum_dict, insts_pos):
    for inst, pos in insts_pos:
        measures = drum_dict.get(inst, [])
        # Flatten the list of lists
        notes = [note for measure in measures for note in measure]
        # If all notes are '-', return False
        if notes[pos] == inst:
            return False
    return True