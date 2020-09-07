from django.shortcuts import render
from .models import Team
import pandas as pd
import seaborn as sns
from .utils import get_image,get_correlation_plot
import matplotlib.pyplot as plt

# Create your views here.
def winning_correlation_view(request):
    graph = None
    error_message = None
    df = None
    corr = None
    try:
        df = pd.DataFrame(Team.objects.all().values())
        if request.method == 'POST':
            chart_title = request.POST.get('title')
            print(chart_title)
            if chart_title == "offensive efficiency vs. winning %":
                graph, corr= get_correlation_plot(chart_title,
                                            x='offensive_efficiency',
                                            y='win_pct',
                                            data=df,
                                            x_label='Offensive Efficiency Rating \n (Points Scored per 100 Possessions)',
                                            y_label='Winning %')
            
            elif chart_title == "defensive efficiency vs. winning %":
                graph, corr = get_correlation_plot(chart_title,
                                            x='defensive_efficiency',
                                            y='win_pct',
                                            data=df,
                                            x_label='Defensive Efficiency Rating \n (Points Allowed per 100 Possessions)',
                                            y_label='Winning %')
            else:
                error_message = 'Please select a chart to continue'
    except:
        error_message = 'No records in the database'
    
    context = {
        'graph': graph,
        'corr':corr,
        'error_message': error_message
    }

    return render(request,'ncaa_basketball/correlations.html', context)


