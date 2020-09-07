from django.shortcuts import render
from .models import Shot
import pandas as pd
from ncaa_basketball.utils import draw_court,get_image,get_pie_chart,get_bar_plot,get_pct
import matplotlib.pyplot as plt
from matplotlib.offsetbox import  OffsetImage
import urllib.request
import seaborn as sns
from matplotlib import cm
from matplotlib import rcParams
import numpy as np
# Create your views here.
def shot_chart_view(request):
    graph = None
    error_message = None
    df = None 
    name = None
    fg_pct = None
    pct_3 = None
    pct_2 = None
    round_str = None
    paint_pct = None
    mid_pct = None
    corner3_pct = None
    opponent = ""
    try:
        df = pd.DataFrame(Shot.objects.all().values())
        if request.method == 'POST':
            name = request.POST.get('player')
            playoff_round = request.POST.get('round')
            
            if playoff_round == 'all':
                round_str = "PLAYOFF STATS"
                df['name'] = df['name'].str.lower()
                player_shots = df.loc[df['name'] == name]
            elif playoff_round == 'first':
                round_str = "FIRST ROUND"
                df['name'] = df['name'].str.lower()
                player_shots = df.loc[(df['name'] == name) & ((df['opponent'] == 'IND') | (df['opponent'] == 'SAS'))]
                opponent = " vs. " + player_shots.iloc[0]['opponent']
            elif playoff_round == 'second':
                round_str = 'SECOND ROUND'
                df['name'] = df['name'].str.lower()
                player_shots = df.loc[(df['name'] == name) & ((df['opponent'] == 'TOR') | (df['opponent'] == 'NOP'))]
                opponent = " vs. " + player_shots.iloc[0]['opponent']
            elif playoff_round == 'conference finals':
                round_str = 'CONFERENCE FINALS'
                df['name'] = df['name'].str.lower()
                player_shots = df.loc[(df['name'] == name) & ((df['opponent'] == 'BOS') | (df['opponent'] == 'HOU'))]
                opponent = " vs. " + player_shots.iloc[0]['opponent']
            else:
                round_str = 'NBA FINALS'
                df['name'] = df['name'].str.lower()
                player_shots = df.loc[(df['name'] == name) & ((df['opponent'] == 'CLE') | (df['opponent'] == 'GSW'))]
                opponent = " vs. " + player_shots.iloc[0]['opponent']

            plt.switch_backend('Agg')
            made = player_shots.loc[player_shots['made'] == 1]
            missed = player_shots.loc[player_shots['made'] == 0]

            threes = player_shots.loc[player_shots['shot_type'] == '3PT Field Goal']
            made_threes = threes.loc[threes['made'] ==  1]

            twos = player_shots.loc[player_shots['shot_type'] == '2PT Field Goal']
            made_twos = twos.loc[twos['made'] == 1]

            paint = player_shots.loc[(player_shots['shot_zone']== 'Restricted Area') | (player_shots['shot_zone'] == 'In The Paint (Non-RA)')]
            made_paint = paint.loc[paint['made'] == 1]

            midrange = player_shots.loc[player_shots['shot_zone'] == 'Mid-Range']
            made_midrange = midrange.loc[midrange['made'] == 1]

            corner3 = player_shots.loc[(player_shots['shot_zone']== 'Left Corner 3') | (player_shots['shot_zone'] == 'Right Corner 3')]
            made_corner = corner3.loc[corner3['made']==1]


            fig, ax = plt.subplots()
            fig.set_size_inches(7.5, 6.5)
            ax.scatter(missed['loc_x'], missed['loc_y'],c = 'red', label='Missed')
            ax.scatter(made['loc_x'], made['loc_y'],c = 'green', label='Made',alpha=0.5)
            draw_court(outer_lines=True)
            plt.xlim(300,-300)
            plt.ylim(-100,500)
            plt.axis('off')

            
            ax.legend()
            graph = get_image() 
            name = name.upper()
            
            fg_pct = int(made.size)/(int(made.size)+int(missed.size))*100
            pct_2 = (int(made_twos.size) / int(twos.size))*100
            pct_3 = (int(made_threes.size) / int(threes.size))*100
            paint_pct = (int(made_paint.size)/int(paint.size))*100
            mid_pct = (int(made_midrange.size)/int(midrange.size))*100
            corner3_pct = (int(made_corner.size)/int(corner3.size))*100

    except Exception as error: 
        print(error)
        error_message = 'No records in the database'

    context = {
        'graph':graph, 
        'name':name,
        'fg_pct':fg_pct,
        'pct_2':pct_2,
        'pct_3':pct_3,
        'mid_pct': mid_pct,
        'corner3_pct':corner3_pct,
        'paint_pct':paint_pct,
        'round_str':round_str,
        'opponent':opponent,
        'error_message': error_message
    }
    return render(request,'nba/shots_charts.html',context)


def shot_graphs_view(request):
    name = None
    graph = None
    graph2 = None
    graph3 = None
    pie = None
    pie2 = None
    pie3 = None
    error_message = None
    df = None 
    pct1 = None
    pct2 = None
    pct3 = None
    shot1 = None
    shot2 = None
    shot3 = None
    try:
        df = pd.DataFrame(Shot.objects.all().values())
        if request.method == 'POST':
            print(request.POST)
            name = request.POST.get('player')

            if name == '':
                error_message = "Please select a player"

            else:
                event = request.POST.get('event')

                df['name'] = df['name'].str.lower()
                df = df.loc[df['name'] == name]
            
                
                made = df.loc[(df['made']==1) & (df['action_type'].isin(df['action_type'].value_counts().index))]
                made = made['action_type'].value_counts().to_frame('counts')

                attempts = df['action_type'].value_counts().to_frame('counts')
                
                merge = pd.merge(attempts, made, left_index=True, right_index=True)
          
                largest = merge.nlargest(5, 'counts_x')
                largest['pct'] = largest['counts_y']/largest['counts_x']*100
                

                shot_types = list(largest.index)
                percents = list(largest['pct'])

                pct1 = percents[0]
                shot1 = shot_types[0]

                pct2 = percents[1]
                shot2 = shot_types[1]

                pct3 = percents[2]
                shot3 = shot_types[2]



                plt.switch_backend('Agg')
                fig, ax = plt.subplots()
                fig.set_size_inches(11.50, 4)
                rcParams.update({'figure.autolayout': True})
                
                N=5
                ind = np.arange(N) 
                width = 0.25 

                ax.bar(ind,largest['counts_x'],width=0.25)
                # made = df.loc[(df['made']==1) & (df['action_type'].isin(df['action_type'].value_counts()[:5].index))]
                ax.bar(ind+width,largest['counts_y'], color='#2ca02c',width=0.25)
                plt.xticks(ind + width / 2, largest.index)
                ax.legend(labels=['Attempted','Made'])
                for i, v in enumerate(largest['counts_y']):
                    plt.text(i+0.2,v-6, str(v), color='white',weight="bold")

                for i, v in enumerate(largest['counts_x']):
                    plt.text(i-0.06,v-6, str(v), color='white',weight="bold")
                max_value = df['action_type'].value_counts()[0]
                plt.ylim(0,max_value+20)
                graph = get_image()
                plt.close()
                               

    except Exception as error: 
        print(error)
        error_message = 'No records in the database'
    
    context = {
        'name': name,
        'graph':graph,
        'graph2':graph2,
        'graph3':graph3,
        'pie':pie,
        'pie2':pie2,
        'pie3':pie3,
        'pct1':pct1,
        'shot1':shot1,
        'pct2':pct2,
        'shot2':shot2,
        'pct3':pct3,
        'shot3':shot3,
        'error_message': error_message
    }
  
    return render(request,'nba/shot_graphs.html',context)



