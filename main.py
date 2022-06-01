from functions import save_song_data, join_audio, save_chord_data, change_volume
save_chord_data("a:2-c+F:2-", "chords.wav")
save_song_data("blank-a:1-g:1-F:1", "melody.wav")
join_audio(["chords.wav", "melody.wav"], "song.wav")
change_volume("song.wav", "louder.wav", 20)