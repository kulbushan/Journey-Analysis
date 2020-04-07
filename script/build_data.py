# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 16:06:10 2020

@author: kulbushan
"""

import os, pandas as pd, numpy as np, plotly.graph_objs
from datetime import datetime, timedelta
from matplotlib import pyplot as plt, dates as mdates
from math import sin, cos, sqrt, atan2, radians
import seaborn as sns
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# =============================================================================
# 
#   Class to read csv file and perform data analysis
#
# =============================================================================

class BuiltData:
    
    def __init__(self, directory = ""):
        self.directory = directory
        
    def filebrowser(self):
# =============================================================================
#         Retrieves csv file from directory specified
# =============================================================================
        items = os.listdir(self.directory)
        files = []
        for f in items:
              if f.endswith(".csv"):
                   files.append(f)
        return files
        
    def read_telematic(self, filespath = ''):
# =============================================================================
#          Reads all files information and 
#          returns journeys data
# =============================================================================
        
         getpath = os.getcwd()
         dates = []
         eventfiles = filespath
         os.chdir(self.directory)
        
         df=pd.DataFrame()   
         line_count = 0
         for file in eventfiles:
             line_count += 1
             newdf = pd.read_csv(file, encoding = 'utf-8', 
                               # NA and Missing Data Handling                
                               na_values=None,
                               keep_default_na=True)
             newdf['sessionID'] = os.path.splitext(file)[0]
             newdf['journeyID'] = 'JID'+ str(line_count) 
             df=df.append(newdf,ignore_index=True, sort=False)  
            
         os.chdir(getpath)
         
         for time in df['timestamp']:
             # Assuming that this timestamp is in milliseconds:
             dts =  datetime.utcfromtimestamp(time/1000).strftime("%d-%m-%Y %H:%M:%S")
             dates.append(dts)
         df['datetime'] = pd.to_datetime(dates)
         
         
         #df_new = df.rename({"speed": "speed(mi/m)"}, axis='columns')
         # Assuming speed is in meter per second, converting to miles per minute
         # Divide the speed value by 26.822 for approximate result
         #df_new['speed(mi/m)']  = (df_new['speed(mi/m)']/26.822)
 
         df = df.fillna(0)
         
         # use index = false to ignore the index column to appear in csv
         df.to_csv('C:\\Users\\kulbh\\TheFloow\\data\\journeys.csv', index=False, sep=',', header='true')
         
         return df

    def cal_dist_dur(self, dframe, sourcetype = '', jid = ''):
# =============================================================================
#         Calculates distance and duration and 
#         returns single journey data based on GPS and Journey ID
# =============================================================================
        
        colnames = ['timestamp','type','lat','lon','height','accuracy',
                    'speed','bearing','sessionID','journeyID','datetime']
        totdist_df = dframe[colnames]
        dist_dur_df = totdist_df[(totdist_df['type'] == sourcetype) & 
                                (totdist_df['journeyID'] == jid)]
        
        # approximate radius of earth in km
        R = 6371.0
        
        lat1 = lon1 = lat2 = lon2 = 0
        dist_dur_df['distance(miles)'] = 0.0
        dist_dur_df['duration(min)'] =  0
              
        for i in range(0, len(dist_dur_df)):
            if i != len(dist_dur_df)-1:
                lat1 = radians(dist_dur_df['lat'].iloc[0])
                lon1 = radians(dist_dur_df['lon'].iloc[0]) 
                i += 1
            else:
                pass
            for j in range(i, i+1):
                lat2 = radians(dist_dur_df['lat'].iloc[j])
                lon2 = radians(dist_dur_df['lon'].iloc[j])
                ctm = dist_dur_df['datetime'].iloc[j]
            dlon = lon2 - lon1
            dlat = lat2 - lat1
        
            a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            dist_dur_df['distance(miles)'].iloc[i] = ((R * c)/1.609)
            
            starttime = dist_dur_df['datetime'].iloc[0]
            currenttime = ctm
            
            # Total duration of a journey in minutes
            date_time_difference = round((pd.to_datetime(currenttime) - pd.to_datetime(starttime)).total_seconds()/60)
            dist_dur_df['duration(min)'].iloc[i] = date_time_difference
   
        dist_dur_df.to_csv('C:\\Users\\kulbh\\TheFloow\\data\\singlejourney.csv', index=False, sep=',', header='true')
        return dist_dur_df
    
        
        

# =============================================================================
#   Validation using unit test cases
# =============================================================================
if __name__ == "__main__":
    builtdata = BuiltData('C:\\Users\\kulbh\\TheFloow\\data\\all_journeys')
    
    filespath = builtdata.filebrowser()
    
    dframe = builtdata.read_telematic(filespath)
    
    cal_dd_df = builtdata.cal_dist_dur(dframe, 'gps', 'JID3')
   
    
    
    
    
    
    
    
    