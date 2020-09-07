from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .forms import CsvForm
from .models import Csv
import csv
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from ncaa_basketball.models import Team
from nba.models import Shot
# Create your views here.


def upload_file_view(request):
    error_message = None
    success_message = None
    form = CsvForm(request.POST or None, request.FILES or None)
    
    if form.is_valid():
        form.save()
        form = CsvForm()
        try:
            obj = Csv.objects.get(activated=False)
            with open(obj.file_name.path, 'r') as f:
                reader = csv.reader(f)
                header = next(reader)
                for row in reader:
                    name = row[0]
                    conference = row[1]
                    total_games = row[2]
                    games_won = row[3]
                    games_lost = int(total_games) - int(games_won)
                    win_pct = (int(games_won) / int(total_games)) * 100
                    offensive_efficiency = row[4]
                    defensive_efficiency = row[5]
                    Team.objects.create(
                        name=name,
                        conference = conference,
                        total_games = int(total_games),
                        games_won = int(games_won),
                        games_lost = int(games_lost),
                        win_pct = float(win_pct),
                        offensive_efficiency = float(offensive_efficiency),
                        defensive_efficiency = float(defensive_efficiency)
                    )
            obj.activated=True
            obj.save()
            success_message= "Uploaded sucessfully"
        except:
            error_message = "Something went wrong...."
    
    context = {
        'form': form,
        'success_message': success_message,
        'error_message': error_message,
    }
    return render(request,'csvs/upload.html',context)


def upload_nba_file_view(request):
    error_message = None
    success_message = None
    form = CsvForm(request.POST or None, request.FILES or None)
    
    if form.is_valid():
        form.save()
        form = CsvForm()
        try:
            obj = Csv.objects.get(activated=False)
            with open(obj.file_name.path, 'r') as f:
                reader = csv.reader(f)
                header = next(reader)
                cle = 'Cleveland Cavaliers'
                gsw = 'Golden State Warriors'
                for row in reader:
                    print(row)
                    name = row[5]
                    x_loc = row[18]
                    y_loc = row[19]
                    made = row[21]
                    shot_type = row[13]
                    shot_zone = row[14]
                    action_type = row[12]
                    if (row[7] == cle and row[-1] == 'CLE') or (row[7] == gsw and row[-1] == 'GSW'):
                        opponent = row[-2]
                    else:
                        opponent = row[-1]
                    

                    Shot.objects.create(
                        name=name,
                        loc_x=x_loc,
                        loc_y=y_loc,
                        opponent=opponent,
                        made=made,
                        shot_type=shot_type,
                        shot_zone=shot_zone,
                        action_type=action_type
                    )
            obj.activated=True
            obj.save()
            success_message= "Uploaded sucessfully"
        except:
            error_message = "Something went wrong...."
    
    context = {
        'form': form,
        'success_message': success_message,
        'error_message': error_message,
    }
    return render(request,'csvs/upload_nba.html',context)

