from pydub import AudioSegment, effects
from pydub.silence import detect_nonsilent

#adjust target amplitude
def match_target_amplitude(sound, target_dBFS):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)

species = { 8:"Asian Koel"}
xcid = "594949"
filename = "XC594949 - Asian Koel - Eudynamys scolopaceus.mp3"

#Convert wav to audio_segment
#audio_segment = AudioSegment.from_wav(filename)
birdsound = AudioSegment.from_mp3(filename)

#normalize audio_segment to -20dBFS
normalized_sound = match_target_amplitude(birdsound, -20.0)
print("length of audio_segment={} seconds".format(len(normalized_sound)/1000))

#Print detected non-silent chunks, which in our case would be spoken words.
nonsilent_data = detect_nonsilent(normalized_sound, min_silence_len=400, silence_thresh=-30, seek_step=1)

print(nonsilent_data)
#print(nonsilent_data[0][0])
#print(nonsilent_data[0][1])
#exit(0)

#convert ms to seconds
print("start,Stop")
f = open("muraitempdata.csv", "w")
f.write("slice-file-name,xcid,start,dur,salience,speciesid,english\n")
seq = 1

for chunks in nonsilent_data:
#    print( [chunk/1000 for chunk in chunks])

    start = chunks[0]-100
    end = chunks[1]+100
#    print("clip={0}-{1}".format(start,end))

    outputfilename = "xc" + xcid + "-" + str(start) + "-" + str(end-start) + ".wav"
    print(outputfilename)
    clip = normalized_sound[start:end]
    clip.export(outputfilename, format="wav")
    s = "00"+ str(seq)
    num = s[:3]

    string = xcid +"-8-" + num + ",594949," + str(start/1000) \
            + "," + str((end-start)/1000) + ",1,8,"\
            + species[8] + "\n"
    f.write(string)
    seq += 1

f.close()
exit(0)
normalized_sound.export("./output.wav", format="wav")

#rawsound = AudioSegment.from_file("./input.m4a", "m4a")
#normalizedsound = effects.normalize(audio_segment)
#normalized_sound = match_target_amplitude(birdsound, -20.0)


