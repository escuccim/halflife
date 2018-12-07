# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse

def blood_level(dose, halflife, start_level=0, days=200):
    # starting level = 0
    level_0 = start_level
    # level after first dose = dose
    level = dose + start_level

    # hf in days
    hf_days = halflife / 24

    # start at day 0
    day = 0
    levels = [level_0]
    steady_state_days = 0

    # loop through days
    while day < days:
        # how much will the levels decrease today
        day_decrease = (level / 2) / hf_days

        # subtract the decrease
        level -= day_decrease

        # add the daily dose
        level += dose

        levels.append(level)

        # increase the day
        day += 1

        level_0 = level

    # figure out the time to steady state
    prev_level = -10
    for i, current_level in enumerate(levels):
        print("Day:",i, "Diff:", current_level - prev_level)
        if (current_level - prev_level) < 0.1:
            steady_state_days = i
            break

        prev_level = current_level

    return list(range(days+1)), levels, steady_state_days

# Create your views here.
def Index(request):
    return render(request, 'halflife/index.html', {})

def Calculate(request):
    daily_dose = request.POST.get("daily_dose", 10)
    halflife = request.POST.get("half_life", 12)
    start_level = request.POST.get("start_level", 0)
    days = request.POST.get("days", 200)

    days, levels, ssd = blood_level(float(daily_dose), float(halflife), float(start_level), int(days))

    return JsonResponse({'days': days, 'levels': levels, 'steady_state': ssd}, safe=False)
