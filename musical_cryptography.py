import mido
from mido import Message, MidiFile, MidiTrack

# Define a mapping from letters to MIDI note numbers
note_mapping = {char: 60 + i for i, char in enumerate('ABCDEFGHIJKLMNOPQRSTUVWXYZ ')}

def text_to_notes(text):
    return [note_mapping[char] for char in text.upper() if char in note_mapping]

def create_midi(notes, filename):
    mid = MidiFile()
    
    # Melody track
    track_melody = MidiTrack()
    mid.tracks.append(track_melody)
    
    # Chords track
    track_chords = MidiTrack()
    mid.tracks.append(track_chords)

    # Major scale pattern
    major_scale = [0, 2, 4, 5, 7, 9, 11, 12]
    
    # Previous note used for chord generation
    prev_note = 60

    for note in notes:
        # Melody
        track_melody.append(Message('note_on', note=note, velocity=64, time=32))
        track_melody.append(Message('note_off', note=note, velocity=64, time=64))
        
        # Chords (triads based on major scale)
        chord_root = note - (note - prev_note) % 12
        chord_notes = [chord_root, chord_root + major_scale[2], chord_root + major_scale[4]]
        
        for chord_note in chord_notes:
            track_chords.append(Message('note_on', note=chord_note, velocity=50, time=0))
        
        for chord_note in chord_notes:
            track_chords.append(Message('note_off', note=chord_note, velocity=50, time=64))
        
        prev_note = note

    mid.save(filename)

message = "Hallå FRA."
notes = text_to_notes(message)
create_midi(notes, 'output.mid')