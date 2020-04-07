# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 04:40:21 2020

@author: kulbushan
"""


# =============================================================================
# 
# Sensor
# 
# =============================================================================


import plotly.graph_objs, pandas as pd, altair as alt, numpy as np
from matplotlib import pyplot as plt, dates as mdates
import seaborn as sns
import matplotlib
matplotlib.style.use('ggplot')

class Sensor:
    
    def __init__(self, directory = ""):
        self.directory = pd.read_csv(directory)
        
    def event_accelerometer(self, dframe, jid, typ):
        
        colnames = ['timestamp','datetime','type','journeyID','x', 'y', 'z']
        event_data = dframe[colnames]
        df_event = event_data[(event_data['journeyID'] == jid) & (event_data['type']== typ)]
        plotly.offline.plot({"data": [plotly.graph_objs.Scatter(
                x=df_event.datetime,
                y=df_event['x'],
                name="X",
                line_color='deepskyblue',
                opacity=0.8),
        plotly.graph_objs.Scatter(
                x=df_event.datetime,
                y=df_event['y'],
                name="Y",
                line_color='lightcoral',
                opacity=0.8),
        plotly.graph_objs.Scatter(
                x=df_event.datetime,
                y=df_event['z'],
                name="Z",
                line_color='dimgray',
                opacity=0.8)
        ], "layout": plotly.graph_objs.Layout(
            title="Events registered during a single journey",
                  xaxis_title="Time stamp(H:M)",
                  yaxis_title="m/s**2",
                  autosize=False,
                  width=950,
                  height=600,
                  font=dict(
                  family="Arial",
                  size=18,
                  color="lightsalmon"),
                  margin=dict(
                      l=20,
                      r=20,
                      b=40,
                      t=50,
                      pad=5),)
                  })
                  
    
    def sensor_dist(self, dframe, jid, typ):
        
        colnames = ['timestamp','datetime','type','journeyID','x', 'y', 'z']
        event_data = dframe[colnames]
        df_event = event_data[(event_data['journeyID'] == jid) & (event_data['type']== typ)]
        
        density = dict(histtype='stepfilled', alpha=0.6, bins=5, edgecolor = 'black')

        plt.figure(figsize=[15,10])
        
        plt.hist(df_event['x'], label = 'X', **density)
        plt.hist(df_event['y'], label = 'Y', **density)
        plt.hist(df_event['z'], label = 'Z', **density)
        
        plt.grid(axis='y', alpha=0.75)
        plt.xlabel('Accelerometer measurements',fontsize=25)
        plt.ylabel('Frequency',fontsize=25)
        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)
        plt.ylabel('Frequency',fontsize=25)
        plt.title('Accelerometer Data Distribution',fontsize=30)
        plt.legend(bbox_to_anchor=(1.05, 0.8), loc=2, borderaxespad=0.2, prop={'size': 20})
        plt.show()
        
    
    def vel_speed(self, dframe, jid, typ):
        
        colnames = ['datetime','type','speed','journeyID']
        speed = dframe[colnames]
        vl_speed = speed[(speed['journeyID'] == jid) & (speed['type']== typ)]
        plotly.offline.plot({"data": 
            [
            plotly.graph_objs.Scatter(x=vl_speed['datetime'], 
                                      y=vl_speed['speed'], 
                                      name="speed",
                                      line_color='deepskyblue')],
            "layout": plotly.graph_objs.Layout(title="Events registered during a single journey",
                                              xaxis_title="Time stamp(H:M)",
                                              yaxis_title="speed (m/s)",
                                              autosize=False,
                                              width=950,
                                              height=600,
                                              font=dict(
                                              family="Arial",
                                              size=18,
                                              color="lightsalmon"),
                                              margin=dict(
                                                  l=20,
                                                  r=20,
                                                  b=40,
                                                  t=50,
                                                  pad=5),)
                  })
    
    def cor_speed_axes(self, dframe, jid):
        colnames = ['speed','x', 'y', 'z','journeyID']
        cor_data = dframe[colnames]
        cor_sp_ax = cor_data[(cor_data['journeyID'] == jid)] 
        
        cor_diag_na = cor_sp_ax.corr()
        cor_df_na = pd.DataFrame(cor_diag_na)

        cor_fil_na = cor_sp_ax.fillna(0)
        cor_diag = cor_fil_na.corr()
        cor_df = pd.DataFrame(cor_diag)
        
        corr_df = pd.concat([cor_df_na, cor_df], axis=1)
        
        # Create the default pairplot
        sns.pairplot(cor_diag, diag_kind="kde", 
                     plot_kws=dict(s=50, edgecolor="b", linewidth=1),
                     height=2.5)
        return corr_df
       
    def cor_speed_height(self, dframe, jid):
        colnames = ['speed','height', 'accuracy','journeyID', 'type']
        sub_data = dframe[colnames]
        sub_sp_ht = sub_data[(sub_data['journeyID'] == jid) & (sub_data['type'] == 'gps')] 
        cor_sh = sub_sp_ht[['speed','height', 'accuracy']]
        
        corr_df = cor_sh.corr()
       
        plt.figure(figsize=(13, 8), dpi=70)
        plt.scatter(sub_sp_ht['speed'], sub_sp_ht['height'])
        plt.xlabel('speed (meter per second)', fontsize=25)
        plt.ylabel('height (cm)', fontsize=25)
        plt.xticks(fontsize=25)
        plt.yticks(fontsize=25)
        plt.title('Correlation between Speed & Height', fontsize=25)
        plt.show()
        
        return corr_df
            
    def axes_measures(self, dframe):
        
# =============================================================================
#        upgrade Pandas through commnad prompt or spyder Console (below command)
#           
#        1. Check the version
#           pd.__version__ 
#       2. Upgrade Pandas to 0.25+
#          pip install --upgrade pandas
#       
#       3. restart the Kernal
# =============================================================================
        
        colnames = ['type','x', 'y', 'z','journeyID']
        subset = dframe[colnames]
        event_measure = subset[(subset['type']=='accelerometer')]
    
        dispersion_measure = event_measure.groupby('journeyID').agg(
                             std_x = pd.NamedAgg(column = 'x', aggfunc = np.std),
                             std_y = pd.NamedAgg(column = 'y', aggfunc = np.std),
                             std_z = pd.NamedAgg(column = 'y', aggfunc = np.std)
                             )
                            
        central_measure = event_measure.groupby('journeyID', as_index=True).agg(
                         # Get average of the x coordiante for each group
                         x_mean= pd.NamedAgg(column='x', aggfunc=np.mean),
                         # Get average of the y coordiante for each group
                         y_mean= pd.NamedAgg(column='y', aggfunc=np.mean),
                         # Get average of the z coordiante for each group
                         z_mean= pd.NamedAgg(column='z', aggfunc=np.mean),
                        
                         x_med= pd.NamedAgg(column='x', aggfunc=np.median),
                         # Get median of the y coordiante for each group
                         y_med= pd.NamedAgg(column='y', aggfunc=np.median),
                         # Get median of the z coordiante for each group
                        z_med= pd.NamedAgg(column='z', aggfunc=np.median))
        
        axes_measures = pd.concat([dispersion_measure, central_measure], axis=1)
          
        return axes_measures
     
    def gps_measures(self, dframe):
        
        colnames = ['type','speed', 'accuracy', 'height','journeyID']
        subset = dframe[colnames]
        event_measure = subset[(subset['type']=='gps')]
        
        
        
        dispersion_measure = event_measure.groupby('journeyID').agg(
                            std_speed = pd.NamedAgg(column = 'speed', aggfunc = np.std),
                            std_acc = pd.NamedAgg(column = 'accuracy', aggfunc = np.std),
                            std_height = pd.NamedAgg(column = 'height', aggfunc = np.std)
                            )
        
        central_measure = event_measure.groupby('journeyID', as_index=True).agg(
                        # Get average of the x coordiante for each group
                        speed_mean= pd.NamedAgg(column='speed', aggfunc=np.mean),
                        # Get average of the y coordiante for each group
                        acc_mean= pd.NamedAgg(column='accuracy', aggfunc=np.mean),
                        # Get average of the z coordiante for each group
                        height_mean= pd.NamedAgg(column='height', aggfunc=np.mean),
                        
                        speed_med= pd.NamedAgg(column='speed', aggfunc=np.median),
                        # Get median of the y coordiante for each group
                        acc_med= pd.NamedAgg(column='accuracy', aggfunc=np.median),
                        # Get median of the z coordiante for each group
                        height_med= pd.NamedAgg(column='height', aggfunc=np.median)
                        )
     
        gps_measures = pd.concat([dispersion_measure, central_measure], axis=1)
        
        return gps_measures
    
    def visual_accelerometer(self, dframe):
        
        colnames = ['type','x', 'y', 'z','journeyID']
        subset = dframe[colnames]
        event_measure = subset[(subset['type']=='accelerometer')]
        
        # Make the shaded area show the standard deviation
        fig1, ax1 = plt.subplots(figsize =(15, 10))
        sns.relplot(x='journeyID', y="x",
                    data=event_measure, kind="line", ci="sd", ax = ax1)
        
        fig2, ax2 = plt.subplots(figsize =(15, 10))
        sns.relplot(x='journeyID', y="y",
                  data=event_measure, kind="line", ci="sd", ax = ax2)
        
        
        fig3, ax3 = plt.subplots(figsize =(15, 10))
        sns.relplot(x='journeyID', y="z",
                    data=event_measure, kind="line", ci="sd", ax = ax3)
        plt.close(2)
        plt.close(4)
        plt.close(6)
        
    def visual_gps(self, dframe):
        
        colnames = ['type','speed', 'accuracy', 'height','journeyID']
        subset = dframe[colnames]
        event_measure = subset[(subset['type']=='gps')]
        
        # Make the shaded area show the standard deviation
        fig1, ax1 = plt.subplots(figsize =(15, 10))
        sns.relplot(x='journeyID', y="speed",
                    data=event_measure, kind="line", ci="sd", ax = ax1)
        
        fig2, ax2 = plt.subplots(figsize =(15, 10))
        sns.relplot(x='journeyID', y="accuracy",
                  data=event_measure, kind="line", ci="sd", ax = ax2)
        
        
        fig3, ax3 = plt.subplots(figsize =(15, 10))
        sns.relplot(x='journeyID', y="height",
                    data=event_measure, kind="line", ci="sd", ax = ax3)
        plt.close(2)
        plt.close(4)
        plt.close(6)

# =============================================================================
#   Validation using unit test cases
# =============================================================================
if __name__ == "__main__":
    sensor = Sensor('C:\\Users\\kulbh\\TheFloow\\data\\journeys.csv')
    
    sensor.event_accelerometer(sensor.directory, 'JID20', 'accelerometer')
    sensor.sensor_dist(sensor.directory, 'JID15', 'accelerometer')
    sensor.vel_speed(sensor.directory, 'JID15', 'gps')
    
    cor_spaxes = sensor.cor_speed_axes(sensor.directory, 'JID20')
    cor_spht = sensor.cor_speed_height(sensor.directory, 'JID6')
    
    meas_ax = sensor.axes_measures(sensor.directory)
    meas_gs = sensor.gps_measures(sensor.directory)
  
    sensor.visual_accelerometer(sensor.directory)
    sensor.visual_gps(sensor.directory)
    