# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 09:03:31 2020

@author: kulbushan
"""

import pandas as pd,  plotly
class EventTrigger:
    
    def __init__(self, directory):
        self.directory = directory
        pass
    
    def event_teasing(self, dframe):
                      
        readdf = pd.read_csv(dframe)
        colnames = ['datetime', 'journeyID', 'speed', 'x', 'y', 'z']
        eventdata = readdf[colnames]
        eventdata = eventdata.fillna(0)
        eventdata['confidence'] = eventdata['severityIndex'] = ''
        
        for i in range(0, len(eventdata)):
            if eventdata['speed'].iloc[i] > 0 and eventdata['speed'].iloc[i] <= 30/2.237:
                eventdata['severityIndex'].iloc[i] = '1'
                eventdata['confidence'].iloc[i] = 'Low'
    
            elif eventdata['speed'].iloc[i] > 30/2.237 and eventdata['speed'].iloc[i] <= 60/2.237:
                eventdata['severityIndex'].iloc[i] = '2'
                eventdata['confidence'].iloc[i] = 'Medium'
    
            elif eventdata['speed'].iloc[i] > 60/2.237:
                eventdata['severityIndex'].iloc[i] = '3'
                eventdata['confidence'].iloc[i] = 'High'
    
            else:
                eventdata['severityIndex'].iloc[i] = '0'
                eventdata['confidence'].iloc[i] = 'Neutral'
        eventdata.to_csv('C:\\Users\\kulbh\\TheFloow\\data\\event_teasing.csv', index=False, sep=',', header='true')
        return eventdata
    
    def visual_event(self, sevent, jid):
        
        tracedf = sevent[(sevent['journeyID']== jid) & (sevent['confidence']!='Neutral')]
        plotly.offline.plot({"data": [plotly.graph_objs.Scatter(x=tracedf.datetime,
                y=tracedf['speed'],
                name='Speed',
                line = dict(
                    color = 'dimgray'
                )),
        plotly.graph_objs.Scatter(x=tracedf.datetime,
                y=tracedf['confidence'],
                name='Notional Confidence',
                yaxis='y2',
                mode='markers',
                marker=dict(
                        color='LightSkyBlue',
                        size=5,
                        opacity=0.5,
                        line=dict(
                            color='MediumPurple',
                            width=0.5)
                ))], 
                "layout": plotly.graph_objs.Layout(
                title= "Event registered with notional confidence", 
                yaxis=dict(title='Speed', titlefont=dict(color='dimgray'), tickfont=dict(color='dimgray')),
                yaxis2=dict(title='Notional Confidence', overlaying='y',side='right', titlefont=dict(color='dimgray'),
                            tickfont=dict(color='dimgray')),
                legend=dict(x=0, y=1, traceorder="normal", font=dict(family="sans-serif", size=12, color="black"),
                            bgcolor= "LightSteelBlue", borderwidth=0.2), width=950, height=500, font=dict(family='Arial', size=20))
     })
     
    
# =============================================================================
#   Validation using unit test cases
# =============================================================================
if __name__ == "__main__":
    event = EventTrigger('C:\\Users\\kulbh\\TheFloow\\data\\journeys.csv')
    event_registred = event.event_teasing(event.directory)
    event.visual_event(event_registred, 'JID9')
    