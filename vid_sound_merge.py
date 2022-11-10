from curses.ascii import STX
from logging.config import valid_ident
import subprocess
import os
from tokenize import maybe
import random

from random import randrange
# cmd = 'ffmpeg -i videotest.mp4 -i audiotest.wav -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 output.mp4'
# subprocess.call(cmd, shell=True)                                     # "Muxing Done
# print('Muxing Done')

movie_speed = ["short", "medium", "long"]
sound_label = ["low", "medium", "high"]
sound_speed = ['0.02', '0.1','0.5']
mat = ['1','3','5']
outof = random.sample(range(1,16), 15)



outofthree = random.sample(range(3), 3)

# left and right - (3 x 3 x 3 x 3)
count = 0
# vid_count = 0



for side in ["left", "right"]:
    for m in movie_speed: 
        for i, audio in enumerate(sound_speed): 
            # for m2 in movie_speed:
            #     for audio2 in sound_speed: 
                    for vid_count in range(1,16):
                        for material in range(3):
                    
                            print(vid_count)
                            # print('vid_', m, '_sound_',s,'_mat_', mat[i])
                            filemat1 = mat[material]
                            matfolder = 'Metal_' + filemat1 + '/'
                            audiofile = 'roughness_' + audio + '.wav'

                            outputname = 'output2/' + side + "_vis_" +  m   + '_audio_' + sound_label[i] + '_mat_' + filemat1 + '_' + str(vid_count) + '_.mp4'
                            inputvid = m + '_' + str(vid_count).zfill(3) + '.mp4'
                            cmd = 'ffmpeg -i movies/' + inputvid + ' -i sounds/scraping_sounds/' + matfolder + audiofile + ' -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 ' + outputname
                            subprocess.call(cmd, shell=True)                                     # "Muxing Done
                            print('Muxing Done')
                            # print('vid_', m, '_sound_',audio,'_mat_', mat[i])
                            
                            count += 1
                            print(outputname)
                        


print(count)



