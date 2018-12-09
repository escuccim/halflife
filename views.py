# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse

def blood_level(dose, halflife, start_level=0):
    # starting level = 0
    level_0 = start_level
    # level after first dose = dose
    level = dose + start_level

    # hf in days
    hf_days = halflife / 24

    # start at day 0
    day = 0
    levels = [level_0]

    keep_looping = True
    stop_loop = False

    # loop through days
    while keep_looping:
        if stop_loop == True:
            keep_looping = False

        # how much will the levels decrease today
        day_decrease = (level / 2) / hf_days

        # subtract the decrease
        level -= day_decrease

        # add the daily dose
        level += dose

        # check difference between current level and previous
        diff = abs(level - levels[-1])

        # if the difference is less than 1% of the previous level we will say we've reached steady state
        if diff < (levels[-1] * .001):
            stop_loop = True

        levels.append(level)

        # increase the day
        day += 1

        level_0 = level

    return list(range(day)), levels, (day - 1)

# Create your views here.
def Index(request):
    return render(request, 'halflife/index.html', {})

def Calculate(request):
    daily_dose = request.POST.get("daily_dose", 10)
    halflife = request.POST.get("half_life", 12)
    start_level = request.POST.get("start_level", 0)

    days, levels, ssd = blood_level(float(daily_dose), float(halflife), float(start_level))

    steady_level = round(levels[-1], 1)

    return JsonResponse({'days': days, 'levels': levels, 'steady_state': ssd, 'final_level': steady_level}, safe=False)
