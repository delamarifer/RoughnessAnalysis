import csv
import json
import pandas as pd
import numpy as np


class ProcessTrials:
    """
    This function is used to get the response for each subject for each trial type
    """
    def __init__(self, filename, subjectList,all_subjects=True) -> None:
        self.filename = filename
        self.subject_list = subjectList
        self.filter_trials = []
        self.control_trials = []
        self.real_trials = []
        self.all_subjects = all_subjects
        
    def openfile(self):
        with open(self.filename,newline='') as f:
            spamreader = csv.reader(f, delimiter=',')
            for row in spamreader:
                res = json.loads(row[-1]) # get trial data
                res.update({"subjectID":row[0]}) # add subjectID to each trial input 

                


                # get trials where the stimulus were control
                if "stimulus2" in res.keys():
                        words = res["stimulus2"][0].split('_')
                        # print(words)
                        if "right_answer" in res.keys(): # get filter trials
                            self.filter_trials.append(res)
                        elif "output/control" in words:
                            self.control_trials.append(res)
                        else:
                            self.real_trials.append(res)


        


    def df_control(self):
        # transform to dataframe
        df_control = pd.DataFrame(self.control_trials)
        # print(df_contrxsol)
        # get trials for subjects in list 
        # df_control.delta_aspeed = [item[0] for item in df_control.delta_aspeed]
        # df_control.delta_vspeed = [item[0] for item in df_control.delta_vspeed]

        if not self.all_subjects:
             df_real = df_real.loc[df_real['subjectID'].isin(self.subject_list)]
        # filter out by accuracy on attention trials
        df = self.filter_attention_accuracy(df_control)
        
        # set the right response values
        mymap = {0:1, 1:0}
        df.response = [mymap[item] for item in df.response]
        # replace none with 0 for responses
        mymap2 = {10000:0}
        df.delta_aspeed = [mymap2[item] for item in df.delta_aspeed]
        return df 

    def df_realtrials(self):
        # transform to dataframe
        df_real = pd.DataFrame(self.real_trials)
      

        # df_real.delta_aspeed = [item[0] for item in df_real.delta_aspeed]
        # df_real.delta_vspeed = [item[0] for item in df_real.delta_vspeed]
        # df.[print(item[0]) for item in df.delta_aspeed]
        # 
        # print(df_real)
        # get trials for subjects in list 
        if not self.all_subjects:
            df_real = df_real.loc[df_real['subjectID'].isin(self.subject_list)]
        # filter out by accuracy on attention trials
        df = self.filter_attention_accuracy(df_real)
        
        # set the right response values
        mymap = {0:1, 1:0}
        df.response = [mymap[item] for item in df.response]
        # replace none with 0 for responses

        
        return df 

    def filter_attention_accuracy(self,df):
        df_real = pd.DataFrame(self.real_trials)
        counts = df_real['subjectID'].value_counts()

        df = df[~df['subjectID'].isin(counts[counts < 50].index)]
        # get right answer out of list 
        df_trials = pd.DataFrame(self.filter_trials)
        df_trials.right_answer = [item[0] for item in df_trials.right_answer]
        # check which ones are correct
        df_trials['Diff'] = np.where( df_trials['response'] == df_trials['right_answer'] , 1, 0)
        # calculate accuracy per subject and remove those below 80% accuracy
        df_trials = pd.DataFrame({"accuracy": df_trials.groupby("subjectID")["Diff"].sum()}).reset_index()
        df_failed = df_trials.where(df_trials['accuracy'] < 4).dropna()
        ind_drop = df[df['subjectID'].apply(lambda x: x in list(df_failed["subjectID"]))].index
        df = df.drop(ind_drop)
        
        return df


    def get_responses(self,trial_type):
        self.openfile()
        # print(self.df_realtrials())
        if trial_type == "control":
            df = self.df_control()
        else:
            df = self.df_realtrials()

        print(df.delta_aspeed)
    
        print(len(df["subjectID"].unique()))
        

        # print(df.groupby(['delta_vspeed','delta_aspeed']).head())
        # get mean response
        df2 = pd.DataFrame({"mean_rt": df.groupby(['delta_vspeed','delta_aspeed'])['response'].mean()}).reset_index()
        # get error
        dferr = pd.DataFrame({"err": df.groupby(['delta_vspeed','delta_aspeed'])['response'].sem()}).reset_index()

        df2["std"] = dferr["err"]

        
        
        
        return df2



