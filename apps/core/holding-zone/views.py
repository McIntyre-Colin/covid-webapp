import requests
import pygal
from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    # This is the view function for the landing page
    return render(request, 'index.html')


def state_data(request):
    # Tabular data relating to covid cases by state
    # Returns most current information (in this case 2021 data) for covid data. 
    # Will probably make it so any date can be input in the near future
    response = requests.get('https://api.covidtracking.com/v1/states/current.json')
    state_data = response.json()

   
    context = {
        'state_data': state_data,
    }
    return render(request, 'state-data.html', context)


#List of state abbreviations initialized outside the function so it stays current during the session
states = []
sorted_state_dict = {}
state_dict = {}
#function which handles the graphing of state specific data
def graphing_state_values(states):
    chart = pygal.Bar()

    for state in states:
        response = requests.get('https://api.covidtracking.com/v1/states/'+ state +'/20200501.json')     
        state_data = response.json()
        state_dict[str(state_data['state'])] = state_data['positive']
    sorted_state_keys = sorted(state_dict, key=state_dict.get, reverse=True)
    #checking if sort worked
    print(sorted_state_keys)
    print(state_dict)

    #Graphing the sorted list
    for k in sorted_state_keys:
        v =state_dict[k]
        print(k)
        print(state_dict)
        value = int(v)
        label = str(k)
        chart.add(label, value)

    chart_svg = chart.render()
    return chart_svg




def comparison(request):
    #Setting a default data type and value
    stateAbr = ""
    #Getting a list of state abbreviations to compare against what the user enters
    #will maybe allow for users to enter full state names eventually
    response = requests.get('https://worldpopulationreview.com/static/states/abbr-list.json')
    state_abr = response.json()
    

    print(state_abr)
    #Allowing for /comparison/ to be run without a search term
    if 'searchterm' in request.GET.keys():
        stateAbr = request.GET['searchterm'].lower()
    
    if stateAbr not in states and stateAbr != "" and stateAbr.upper() in state_abr:
        states.append(stateAbr)
    # Graphing highest covid cases by state
        chart_svg = graphing_state_values(states)

    else:
        chart_svg = graphing_state_values(states)
    context = {
            'states': states,
            'rendered_chart': chart_svg.decode(),
            }
    return render(request, 'comparison-state.html', context)