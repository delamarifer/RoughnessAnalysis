"""
Class to generate stimuli for the roughness experiment
2022-11-01

TODO
"""

import os
import json
import subprocess
from collections import Counter
import random
import pandas as pd
import numpy as np 

# CONTROL_PATH = '/Users/mdelatorre/Desktop/psiturk-roughness/templates/output/'
CONTROL_PATH = './output/'
view_dict = {0:'forward', 1:'backward'}



angles = ['flat', '15','25','35']
angle_type = angles[0]
class RoughnessExpStimuliGen(object):
    def __init__(self):
        """
        This function is used to initialize the class
        """
        self.data = []

        l_dir = os.listdir('output')
        self.list_dir = [f.lower() for f in l_dir if f.endswith('.mp4')]   # Convert to lower case

        self.speed_dict = {"low":1, "medium":2, "high":3}
        self.vis_speed_dict = {"short":1, "medium":2, "long":3}
        self.sound_speed = {"low":'0.02', "medium":'0.1',"high":'0.5'}

        self.movie_speed = ["short", "medium", "long"]
        self.sound_label = ["low", "medium", "high"]

        self.mat = ['1','3','5']
       

    def add_control_trials(self):
        """
        This function is used to add the control trials
        """
        data = []
        count = 0 
        audiofile = 'sounds/control_sounds/trimmed3.m4a'
        rand_vids = random.sample(range(1,16), 15)
        rand_vids2 = random.sample(range(1,16), 15)
        rand_view = np.random.randint(2, size=15)
        rand_view2 = np.random.randint(2, size=15)
        print(rand_view)
        
        for m in self.movie_speed:
            print(m)
            for m2 in self.movie_speed:
                print(m2)
                rand_vid = rand_vids[count]
                print(rand_view[count])
                # rand_viewf = view_dict[rand_view[count]]
                rand_viewf = view_dict[0]
                inputvid = m + '_' + angle_type + '_' + rand_viewf + '_' + str(rand_vid).zfill(3) + '.mp4'
                outputname = CONTROL_PATH + 'control_trials/left_visual_' + m + '_' + angle_type + '_' + rand_viewf + '_' + str(rand_vid).zfill(3) + '_music.mp4'
                
                cmd = 'ffmpeg -i movies/' + inputvid + ' -i ' + audiofile + ' -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 ' + outputname
                subprocess.call(cmd, shell=True)                                     # "Muxing Done
                print('Muxing Done')

                rand_vid2 = rand_vids2[count]
                # rand_view2f = view_dict[rand_view2[count]]
                rand_view2f = view_dict[0]
                inputvid = m2 + '_' + angle_type + '_' + rand_view2f + '_' + str(rand_vid2).zfill(3) + '.mp4'
                outputname2 = CONTROL_PATH + 'control_trials/right_visual_' + m2 + '_' + angle_type + '_' + rand_view2f + '_' + str(rand_vid2).zfill(3) + '_music.mp4'

                cmd = 'ffmpeg -i movies/' + inputvid + ' -i ' + audiofile + ' -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 ' + outputname2
                subprocess.call(cmd, shell=True)                                     # "Muxing Done
                print('Muxing Done')


                stim_dict = {} 
                stim_dict['stimulus'] = ['output/' + outputname]
                stim_dict['stim_mat'] = 'NA'
                stim_dict['stim_room'] = rand_vid



                stim_dict['stimulus2'] = ['output/' + outputname2]
                stim_dict['stim2_mat'] = 'NA'
                stim_dict['stim2_room'] = rand_vid2

                stim_dict["delta_vspeed"] = self.vis_speed_dict[m] - self.vis_speed_dict[m2]
                stim_dict["delta_aspeed"] = 10000
                data.append(stim_dict)
                count += 1
                if count >= 14:
                    count = 0
        return pd.DataFrame.from_dict(data)

    def generate_data(self,data):
        """
        This function is used to balance the data by sampling k elements from each group
        """
        stimuli_count = 0 
        sub_from = 15
        for r in range(6):
            random_rooms = []
            for i in range(11):
                random_rooms += random.sample(range(1,16), 15)

            random_materials = []
            for i in range(54):
                random_materials += random.sample([1,3,5], 3)
            for m in self.movie_speed: # left
                for i, audio in enumerate(self.sound_label):  # left
                    for m2 in self.movie_speed: # right
                        for audio2 in self.sound_label: # right
                            stim_dict = {} 
                            # rand_viewf = view_dict[np.random.randint(2)]
                            rand_viewf = view_dict[0]
                            stim1 = "left_" + rand_viewf + "_vis_" + m + "_audio_" + audio + "_mat_" + str(random_materials[stimuli_count]) + "_" + str(random_rooms[stimuli_count])
                            stimuli_count += 1
                            stim_dict['stimulus'] = ['output/' + stim1]
                            stim_dict['stim_mat'] = random_materials[stimuli_count]
                            stim_dict['stim_room'] = random_materials[stimuli_count]


                            # rand_viewf2 = view_dict[np.random.randint(2)]
                            rand_viewf2 = view_dict[0]
                            stim2 = "right_" + rand_viewf2 + "_vis_" + m2 + "_audio_" + audio2 + "_mat_" + str(random_materials[sub_from-stimuli_count]) + "_" +  str(random_rooms[sub_from-stimuli_count])
                            stim_dict['stimulus2'] = ['output/' + stim2]
                            stim_dict['stim2_mat'] = random_materials[sub_from-stimuli_count]
                            stim_dict['stim2_room'] = random_rooms[sub_from-stimuli_count]

                            stim_dict["delta_vspeed"] = self.vis_speed_dict[m] - self.vis_speed_dict[m2]
                            stim_dict["delta_aspeed"] = self.speed_dict[audio] - self.speed_dict[audio2]
                            # print(stimuli_count)
                            stimuli_count += 1
                            if stimuli_count == 162:
                                stimuli_count = 0
                            

                            data.append(stim_dict)
            df = pd.DataFrame.from_dict(data)
        # print(df)
        balanced = df.groupby(['delta_aspeed','delta_vspeed']).apply(self.sampling_k_elements).reset_index(drop=True)
        return balanced

    def sampling_k_elements(self, group, k=5):
        """
        This function is used to sample k elements from each group
        """
        if len(group) < k:
            
            return group
        print("__",len(group.sample(k, replace=False) ))
        return group.sample(k, replace=False) 


    def write_json(self, balanced):
        """
        This function is used to write the json file
        """
        out = balanced.to_json(orient='records')
        with open(CONTROL_PATH + '/trial_vars.json', 'w') as f:
            f.write(out)

    def make_trial_videos(self):
        """
        This function is used to make the trial videos
        """
        count = 0
        for row in self.df.iterrows():
            count += 1
            print(count)
            stim1_name = row[1].stimulus[0]
            print(stim1_name.split('_'))
            rand_viewf = stim1_name.split('_')[1]
            m = stim1_name.split('_')[3]  
            audio_label = stim1_name.split('_')[5]
            filemat1 = stim1_name.split('_')[7]
            rand_vid = stim1_name.split('_')[-1]
            # filemat1 = stim1_name.split('_')[7]
            audio = self.sound_speed[audio_label]
            matfolder = 'Metal_' + filemat1 + '/'
            audiofile = 'roughness_' + audio + '.wav'
            inputvid = m + '_' + angle_type + '_' + rand_viewf + '_' + str(rand_vid).zfill(3) + '.mp4'
            outputname =  stim1_name + '.mp4'
            cmd = 'ffmpeg -i movies/' + inputvid + ' -i sounds/scraping_sounds/' + matfolder + audiofile + ' -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 ' + outputname
            subprocess.call(cmd, shell=True)                                     # "Muxing Done
            print('Muxing Done')


            stim1_name = row[1].stimulus2[0]
            print(stim1_name.split('_'))
            rand_viewf = stim1_name.split('_')[1]
            m = stim1_name.split('_')[3]  
            audio_label = stim1_name.split('_')[5]
            filemat1 = stim1_name.split('_')[7]
            rand_vid = stim1_name.split('_')[-1]
            # filemat1 = stim1_name.split('_')[7]
            audio = self.sound_speed[audio_label]
            matfolder = 'Metal_' + filemat1 + '/'
            audiofile = 'roughness_' + audio + '.wav'
            inputvid = m + '_' + angle_type + '_' + rand_viewf + '_' + str(rand_vid).zfill(3) + '.mp4'
            outputname = stim1_name + '.mp4'
            cmd = 'ffmpeg -i movies/' + inputvid + ' -i sounds/scraping_sounds/' + matfolder + audiofile + ' -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 ' + outputname
            subprocess.call(cmd, shell=True)                                     # "Muxing Done
            print('Muxing Done')

        

    def generate_stim(self):
        """
        This function is used to generate the stimuli
        """
        self.df = self.generate_data(self.data)
        self.df = self.df.groupby(['delta_vspeed','delta_aspeed']).sample(frac=0.4, random_state=2).reset_index(drop=True)
        self.make_trial_videos()
        self.df = pd.concat([self.df, self.add_control_trials()])
        # self.df = self.df.sample(frac=1).reset_index(drop=True)
        # self.df = self.df,
        print(self.df.groupby(['delta_vspeed', 'delta_aspeed'])['stimulus'].count())
            # print(g.count())
        
        print(len(self.df.stimulus.explode().unique()))
        



        
        self.write_json(self.df)


if __name__ == '__main__':
    stim_obj = RoughnessExpStimuliGen()
    stim_obj.generate_stim()