import pretty_midi

example_notation = {
    "K: O--O|---o|O--O|----",
    "S: ----|S---|----|O---",
    "H: -x--|-x--|----|x-xO",
    "T: ----|----|-OO-|----",
    "C: ----|----|----|---",
    "R: --X-|--X-|----|---",
}

def notation_to_midi(notation, out_fname, bpm=120, fname="temp"):
    # Drum map: (name, midi_pitch)
    drums = {
        'K',
        'S',
        'H',
        'T',
        'C',
        'R'
    }
    
    def parse_pattern(notation):
        pattern = {}
        for line in notation.split('\n'):
            if ':' in line:
                key = line.split(': ')[0]
                value = line.split(': ')[1].strip().replace('|', '')
                pattern[key] = value
        return pattern

    pattern = parse_pattern(notation)

    steps_per_bar = len(pattern['K'])  # 16 steps
    bpm = 120
    beats_per_bar = 4
    steps_per_beat = steps_per_bar // beats_per_bar  # 4 steps per beat = 16th notes
    seconds_per_beat = 60.0 / bpm
    step_length = seconds_per_beat / steps_per_beat  # In seconds
    
    # Create a PrettyMIDI object
    midi = pretty_midi.PrettyMIDI(initial_tempo=bpm)

    # Add one Drum instrument on channel 9 (10 in 1-based)
    drum = pretty_midi.Instrument(program=0, is_drum=True)

    # Parse and add notes
    for drum_name in drums:
        steps = pattern[drum_name]
        for i, char in enumerate(steps):
            #if char.upper() in ['O', 'X']:
            if char != '-':
                start = i * step_length
                end = start + step_length * 0.8  # short duration for drums
                midi_pitch = 0
                if drum_name == 'K':
                    if char == 'O':
                        midi_pitch = 36
                    elif char == 'o':
                        midi_pitch = 16
                elif drum_name == 'S':
                    if char == 'X':
                        midi_pitch = 37
                    elif char == 'x':
                        midi_pitch = 17
                    elif char == 'O':
                        midi_pitch = 38
                    elif char == 'o':
                        midi_pitch = 18
                elif drum_name == 'H':
                    if char == 'X':
                        midi_pitch = 42
                    elif char == 'x':
                        midi_pitch = 22
                    elif char == 'O':
                        midi_pitch = 46
                    elif char == 'o':
                        midi_pitch = 26
                elif drum_name == 'T':
                    if char == 'O':
                        midi_pitch = 45
                    elif char == 'o':
                        midi_pitch = 25
                elif drum_name == 'C':
                    if char == 'O':
                        midi_pitch = 49
                    elif char == 'o':
                        midi_pitch = 29
                elif drum_name == 'R':
                    if char == 'X':
                        midi_pitch = 51
                    elif char == 'x':
                        midi_pitch = 31
                    if char == 'O':
                        midi_pitch = 53
                    elif char == 'o':
                        midi_pitch = 33
                else:
                    midi_pitch = 0
                try:
                    note = pretty_midi.Note(
                        velocity=100,  # velocity does not matter
                        pitch=midi_pitch,
                        start=start,
                        end=end,
                    )
                except UnboundLocalError:
                    print(f"UnboundLocalError: {char} not found in drum map.")
                    return
                drum.notes.append(note)

    # Add the drum instrument to the MIDI object
    midi.instruments.append(drum)

    # Write out the MIDI file
    midi.write(out_fname)
    #print(f"Saved as '{out_fname}'")

if __name__ == "__main__":
    notation_to_midi(example_notation)