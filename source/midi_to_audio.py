import pretty_midi
import librosa
import numpy as np
import soundfile as sf

SAMPLE_MAP = {
    36: "../samples/kick_hard.wav",  # Kick
    37: "../samples/snare_sidestick_hard.wav",  # Snare sidestick
    38: "../samples/snare_open_hard.wav",  # Snare open
    42: "../samples/hihat_closed_hard.wav",  # Closed Hi-hat
    46: "../samples/hihat_open_hard.wav",  # Closed Hi-hat
    45: "../samples/tom_hard.wav",  # Low Tom
    49: "../samples/crash_hard.wav",  # Crash Cymbal 1
    51: "../samples/ride_hard.wav",  # Ride Cymbal 1
}

# Load your MIDI
midi = pretty_midi.PrettyMIDI('drum_pattern.mid')
sample_rate = 44100
audio_length = int((midi.get_end_time() + 1) * sample_rate)
audio_out = np.zeros(audio_length)

for note in midi.instruments[0].notes:
    # Get your sample file based on note.pitch
    sample_path = SAMPLE_MAP[note.pitch]
    y, sr = librosa.load(sample_path, sr=sample_rate)
    
    # Compute where to put this sample in the output buffer
    start = int(note.start * sample_rate)
    end = start + len(y)
    if end > len(audio_out):
        y = y[:len(audio_out)-start]  # Prevent overflow
        end = len(audio_out)
    audio_out[start:end] += y  # Add (mix) the sample

# Normalize to avoid clipping
audio_out /= np.max(np.abs(audio_out))

# Save audio
sf.write('output.wav', audio_out, sample_rate)
print("Saved to output.wav!")