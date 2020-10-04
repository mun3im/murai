#!/usr/bin/env python

#import librosa
#y, sr = librosa.load('your_file.mp3')
from pydub import AudioSegment
import csv
import os.path
import time
from urllib import request, error


start_time = time.time()
metadatafn = './murai-metadata.csv'
if os.path.isfile(metadatafn):
    print(f'{metadatafn} found')
else:
    print(f'{metadatafn} not found')   
    quit()
with open(metadatafn) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    audio_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
        else:
            outfn = row[0]
            xcid = row[1]
            t1 = row[2]
            t2 = row[3]
            dirname = row[5] # speciesID
            audiosource = xcid+".mp3"
            if not os.path.isfile(audiosource):
                try:
                    url = 'http://www.xeno-canto.org/' + xcid + '/download'
                    request.urlretrieve(url, audiosource)
                    print(f'\nDownloaded: {audiosource}')
                    # r = request.urlopen(url)
                except error.HTTPError as e:
                    print('An error has occurred: ' + str(e))
                    exit()
#            print(f'Processing file {audiosource}')
            start = int(1000*float(t1))
            end = start + int(1000*float(t2))
#            print(f'{outfn} : \t{t1} + {t2}')
            print('.',end='')
            newAudio = AudioSegment.from_mp3(audiosource)
            newAudio = newAudio[start:end]
            if not os.path.isdir(dirname):
                try:
                    os.mkdir(dirname)
                except OSError:
                    print(f'failed to make directory {dirname}')
                    exit()
            outfn = dirname + '/' + outfn + '.mp3'
            newAudio.export(outfn, format="mp3", codec="mp3")
            audio_count += 1
        line_count += 1
print(f'\nProcessed {audio_count} / {line_count} lines.')
print('--- %s seconds ---' % (time.time() - start_time))



