from pydub import AudioSegment
from scipy.io.wavfile import write
import numpy as np

chordsscale = {"C": "CEG", "D": "DfA", "E": "EgB", "F": "FAC", "G": "GBD", "A": "AcE", "B": "Bdf", "Cm": "CdG", "Dm": "DFA", "Em": "EGB", "Fm": "FgC", "Gm": "GaD", "Am": "ACE", "Bm": "BDf"}
allkeys = "A-a-B-C-c-D-d-E-F-f-G-g"
keyswithkeys = {"A": "A", "W": "a", "S": "B", "D": "C", "R": "c", "F": "D", "T": "d", "G": "E", "H": "F", "U": "f", "J": "G", "I": "g", "K": "A"}
samplerate = 44100

def get_piano_notes():
    octave = ['C', 'c', 'D', 'd', 'E', 'F', 'f', 'G', 'g', 'A', 'a', 'B']
    base_freqs = {"0": 16.35, "1": 32.70, "2": 65.41, "3": 130.81, "4": 261.63, "5": 523.25, "6": 1046.50, "7": 2093.00, "8": 4186.01}
    base_freq = 261.63 #Frequency of Note C4
    note_freqs = {}
    for i in range(len(octave)):
      note_freqs[octave[i]] = base_freq * pow(2,(i/12))
    for freq in base_freqs.keys():
      for i in range(len(octave)):
        note_freqs[octave[i] + freq] = base_freqs[freq] * pow(2,(i/12))
    note_freqs[''] = 0.0
    note_freqs['blank'] = 0.0
    return note_freqs
    
def get_wave(freq, duration=0.5):
    amplitude = 4096
    t = np.linspace(0, duration, int(samplerate * duration))
    wave = amplitude * np.sin(2 * np.pi * freq * t)
    
    return wave
    
def get_song_data(music_notes):
    note_freqs = get_piano_notes()
    song = []
    for note in music_notes.split("-"):
      if ":" in note:
        notesplit = note.split(":")
        note = notesplit[0]
        duration = float(notesplit[1])
      else:
        duration = 0.5
      song.append(get_wave(note_freqs[note], duration=duration))
    song = np.concatenate(song)
    return song.astype(np.int16)
    
def get_chord_data(chords):
    chords = chords.split('-')
    note_freqs = get_piano_notes()
    chord_data = []
    for chord in chords:
        if ":" in chord:
          chordsplit = chord.split(":")
          chord = chordsplit[0]
          duration = float(chordsplit[1])
        else:
          duration = 0.5
        data = sum([get_wave(note_freqs[note], duration=duration) for note in chord.split("+")])
        chord_data.append(data)
    chord_data = np.concatenate(chord_data, axis=0)    
    return chord_data.astype(np.int16)

def save_song_data(music_notes, filename):
  data = get_song_data(music_notes)
  data = data * (16300/np.max(data))
  write(filename, samplerate, data.astype(np.int16))

def save_chord_data(chords, filename):
  # data = np.resize(data, (len(data)*5,))
  data = get_chord_data(chords)
  data = data * (16300/np.max(data))
  write(filename, samplerate, data.astype(np.int16))

def get_chord(scale, octave="", duration=0.5):
  chords = chordsscale[scale]
  newchords = ""
  new = False
  for letter in list(chords):
    if new == False:
      newchords = newchords + letter + octave
      new = True
    else:
      newchords = newchords + "+" + letter + octave
  newchords = newchords + ":" + str(duration)
  return newchords

def join_audio(sounds, output_path):
    sound1 = sounds[0]
    sound1 = AudioSegment.from_wav(sound1)
    sound2 = sounds[1]
    sound2 = AudioSegment.from_wav(sound2)
    combined = sound1.overlay(sound2)
    for i in range(2):
      del sounds[0]
    for sound in sounds:
      sound = AudioSegment.from_wav(sound)
      combined = combined.overlay(sound)
    combined.export(output_path, format='wav')

def change_volume(inputfile, outputfile, amount):
    song = AudioSegment.from_mp3(inputfile)
    louder_song = song + float(amount)
    louder_song.export(outputfile, format='wav')