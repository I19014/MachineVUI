import simpleaudio as sa

filename = 'TestSounds/test.wav'
wave_object = sa.WaveObject.from_wave_file(filename)
play_obj = wave_object.play()
play_obj.wait_done() 
