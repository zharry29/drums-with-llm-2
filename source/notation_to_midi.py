import pretty_midi

# Drum map: (name, midi_pitch)
drums = {
    'K',
    'S',
    'H',
    'T',
    'C',
    'R'
}

# The pattern lines; remove whitespace and '|' for easy indexing
pattern = {
    'K': "O--O|---o|O--O|----".replace('|', ''),
    'S': "----|S---|----|O---".replace('|', ''),
    'H': "-x--|-x--|----|x-xO".replace('|', ''),
    'T': "----|----|-OO-|----".replace('|', ''),
    'C': "----|----|----|---".replace('|', ''),
    'R': "--X-|--X-|----|---".replace('|', ''),
}

steps_per_bar = len(pattern['K'])  # 16 steps
bpm = 120
beats_per_bar = 4
steps_per_beat = steps_per_bar // beats_per_bar  # 4 steps per beat = 16th notes
seconds_per_beat = 60.0 / bpm
step_length = seconds_per_beat / steps_per_beat  # In seconds

def notation_to_midi(pattern, bpm=120):
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
                if drum_name == 'K':
                    midi_pitch = 36
                elif drum_name == 'S':
                    if char in ['S', 's']:
                        midi_pitch = 37
                    elif char in ['O', 'o']:
                        midi_pitch = 38
                elif drum_name == 'H':
                    if char in ['X', 'x']:
                        midi_pitch = 42
                    elif char in ['O', 'o']:
                        midi_pitch = 46
                elif drum_name == 'T':
                    midi_pitch = 45
                elif drum_name == 'C':
                    midi_pitch = 49
                elif drum_name == 'R':
                    midi_pitch = 51

                if char.isupper():
                    velocity = 100
                elif char.islower():
                    velocity = 50
                note = pretty_midi.Note(
                    velocity=velocity,  # reasonable default
                    pitch=midi_pitch,
                    start=start,
                    end=end,
                )
                drum.notes.append(note)

    # Add the drum instrument to the MIDI object
    midi.instruments.append(drum)

    # Write out the MIDI file
    midi.write('drum_pattern.mid')
    print("Saved as 'drum_pattern.mid'")

if __name__ == "__main__":
    notation_to_midi(pattern)