import mido
from mido import Message, MidiFile, MidiTrack
from random import choice

# Define a mapping from letters to MIDI note numbers
note_mapping = {char: 60 + i for i, char in enumerate('ABCDEFGHIJKLMNOPQRSTUVWXYZ ')}

def text_to_notes(text):
    return [note_mapping[char] for char in text.upper() if char in note_mapping]

def create_midi(notes, filename):
    mid = MidiFile()
    
    # Melody track (Flute)
    track_melody = MidiTrack()
    track_melody.append(Message('program_change', program=73))  # Flute
    mid.tracks.append(track_melody)
    
    # Chords track (String Ensemble)
    track_chords = MidiTrack()
    track_chords.append(Message('program_change', program=48))  # String Ensemble 1
    mid.tracks.append(track_chords)
    
    # Major scale pattern
    major_scale = [0, 2, 4, 5, 7, 9, 11, 12]
    
    # Chord progressions reminiscent of classical pieces
    chord_progressions = [
        [0, 4, 5, 3],  # I V IV ii
        [0, 5, 3, 4]   # I IV ii V
    ]

    # Choose a random progression
    progression = choice(chord_progressions)
    
    for idx, note in enumerate(notes):
        # Melody with simple rhythm variations
        rhythm = choice([32, 48, 64])
        track_melody.append(Message('note_on', note=note, velocity=64, time=rhythm))
        track_melody.append(Message('note_off', note=note, velocity=64, time=rhythm))
        
        # Chords based on the chosen progression
        chord_root = 60 + major_scale[progression[idx % len(progression)]]
        chord_notes = [chord_root, chord_root + major_scale[2], chord_root + major_scale[4]]
        
        for chord_note in chord_notes:
            track_chords.append(Message('note_on', note=chord_note, velocity=50, time=0))
        
        for chord_note in chord_notes:
            track_chords.append(Message('note_off', note=chord_note, velocity=50, time=rhythm))

    # Replicate ABA form by copying initial segments
    A_section = notes[:len(notes)//2]
    for note in A_section:
        track_melody.append(Message('note_on', note=note, velocity=64, time=32))
        track_melody.append(Message('note_off', note=note, velocity=64, time=32))
        
    mid.save(filename)

message = "Sarhang Said. Music in style."
notes = text_to_notes(message)
create_midi(notes, 'output.mid')
