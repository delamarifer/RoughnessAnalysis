from analysis_functions import ProcessTrials
import csv
import ast
import json
import pandas as pd
from plotly.offline import init_notebook_mode, iplot
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import plotly.offline as py
from analysis_functions import ProcessTrials


new_subjects = [
   'A1LDHBBBCJ7T0V:3OWEPKL08AKLINPHHFX49XURR4SN7E'
    ]

filename = "trial_data.csv"
trials = ProcessTrials(filename, new_subjects)


speed_dictionaries = {-2: "Short vs Long", -1: "Short vs Medium | Medium vs Long", 0: "Short vs Short | Medium vs Medium | Long vs Long", 1: "Medium vs Short | Long vs Short", 2: "Long vs Short"}


df_trials = trials.get_responses("real_trials")
# plotly figure
df = df_trials

fig=go.Figure()
for t in df['delta_vspeed'].unique():
    dfp = df[df['delta_vspeed']==t]
    fig.add_traces(go.Scatter(x=dfp['delta_aspeed'], y = dfp['mean_rt'], name=str(t) + ":  " + speed_dictionaries[t],
            error_y=dict(
            type='data', # value of error bar given in data coordinates
            array=dfp['std'],
            visible=True)
    ))

fig.update_layout(
    legend=dict(
    yanchor="top",
    y=1,
    xanchor="left",
    x=0.01
    ),
    template='ggplot2',
    legend_title=r'$ \text{Visual Distance } \Delta \text{ (Left - Right)}$',
    xaxis_title=r'$ \text{Auditory Roughness } \Delta \text{ (Left - Right)}$',
    yaxis_title=dict( text=r'$ \text{Proportion Left judged rougher}$', ),
    font=dict(
        family='Rockwell',
        size=15,
    ),
    width=1000,
    height=1000,
    xaxis = dict(
    tickmode = 'array',
    tickvals = [-2 , -1, 0, 1, 2],
    tickfont=dict(family='Rockwell', size=14)
    ),
    yaxis = dict(
    tickfont=dict(family='Rockwell', size=14)
    )
)
fig.update_yaxes(
    range=[0,1],  # sets the range of xaxis
    constrain="domain",  # meanwhile compresses the xaxis by decreasing its "domain"
)
fig.update_xaxes(
    range=[-2,2],  # sets the range of xaxis
    constrain="domain",  # meanwhile compresses the xaxis by decreasing its "domain"
)
# fig.update_traces(mode='lines')
fig.show()