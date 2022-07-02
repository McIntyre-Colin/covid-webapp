from multiprocessing import context
from django.forms import ValidationError
import requests
import pygal
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.core.exceptions import SuspiciousOperation

from apps.accounts.models import User
from apps.core.models import Book, ReadingList, Chart, StatesList
from apps.core.forms import AddBookForm, AddReadingListForm, AddChartForm, EditChartForm, AddStateForm


# Start of my changes
def state_data(request):
    # Tabular data relating to covid cases by state
    # Returns most current information (in this case 2021 data) for covid data. 
    # Will probably make it so any date can be input in the near future
    response = requests.get('https://api.covidtracking.com/v1/states/current.json')
    state_data = response.json()

   
    context = {
        'state_data': state_data,
    }
    return render(request, 'pages/nationwide-data.html', context)



# Seperate function for handling editing charts
def chart_function(chart):
    print('Using Editing Function')

    states_for_chart = StatesList.objects.filter(chart_id=chart.id)
    for state in states_for_chart:
        print(' Getting data frrrom chart',state.chart_id)
        print('The state is: ', state.state)
    state_dict = {}
    if chart.chart_type == 'bar':
        plot = pygal.Bar()
    else:
        plot = pygal.Pie()

    for state in states_for_chart:
        print('------------------')
        #ensuring valid url
        print('url', 'https://api.covidtracking.com/v1/states/'+ state.state.lower() +'/'+ chart.year + chart.month + str(chart.day) +'.json')
        print('------------------')
        response = requests.get('https://api.covidtracking.com/v1/states/'+ state.state.lower() +'/'+ chart.year + chart.month + str(chart.day) +'.json')
        state_data = response.json()
        state_dict[state_data['state']] = state_data[chart.filter_field]
        print(state_dict)
    
    sorted_state_keys = sorted(state_dict, key=state_dict.get, reverse=True)
    print(sorted_state_keys)

    for k in sorted_state_keys:
        v =state_dict[k]
        value = int(v)
        label = str(k)
        plot.add(label, value)
    plots_svg = plot.render(is_unicode=True)
    chart.plot_entry = plots_svg
    chart.save()
    return chart
         

def user_page(request, username):

    user = User.objects.get(username=username)
    
# Checkign to see if the user has created any charts
# If not they are redirected to the create chart page
# If they do have at least one chart they will stay on their page and their charts will be displayed
# Maybe going to have the svg be saved in the model instead of being regenerated upon refresh
   #Checks how many charts the user has plotted
    if  len(Chart.objects.filter(creator_user_id = user.id)) != 0:
        charts = Chart.objects.filter(creator_user_id = user.id)
        print( len(Chart.objects.filter(creator_user_id = user.id)))
        
    else:
        return redirect('/charts/' + username +'/create/')
    
   
   
#Maybe move  this to the create page   
    rendered_charts = []
    ids = []
    for chart in charts:
        rendered_charts.append({
            'plot':chart.plot_entry,
            'chart_id': chart.id
        })
        print('group of ids: ',ids)
    chart = Chart.objects.filter(creator_user_id = user.id).values('plot_entry')
    
    print('the rendered chart is: ', rendered_charts)
    print('------------------------')
    print('------------------------')
    context = {
            
            'rendered_charts': rendered_charts,
    }
    return render(request, 'pages/user_charts.html', context)

@login_required
def create_chart(request, username):
    
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request
        form = AddChartForm(request.POST)
        if form.is_valid():
            # If we had omitted commit=False, then the user would not have been
            # properly set-up
            new_chart = form.save(commit=False)
            new_chart.creator_user = request.user
            print('---------------')
            print('The creator user: ', new_chart.creator_user)
            print('---------------')
            new_chart.save()
            # Creating the linked entry in the statesList table
            stateList = StatesList.objects.create(chart = new_chart, state = new_chart.stateAbr)

            chart = Chart.objects.get(id = new_chart.id)
            plots_svg = chart_function(chart)
            return redirect('/charts/'+username+'/')
    else:
        # if a GET  we'll create a blank form
        form = AddChartForm()
    context = {
        'form': form,
        'form_title': 'New Chart',
    }
    return render(request, 'pages/form_page.html', context)


def edit_chart(request, username, chart_id):
    print('EDITING CHART VIEW')
    #Getting chart that the user selected
    chart = Chart.objects.get(id = chart_id)
    #Get the stateslist instance linked to the chart id so the user can enter data
   
    url = '/charts/'+str(username)+'/'+str(chart_id)+'/'
    print('------------------------')
    print('The url is :', url)
    print('the chart is: ', chart.id)

    print('------------------------')

    if request.method == 'POST':
        # Create a form instance for the non-state fields
        #  and populate it with data from the request
        formChart = EditChartForm(request.POST, instance=chart)

        #Create form instance for adding state to plot
        formStateList = AddStateForm(request.POST)
        if formStateList.is_valid():
            #Updates values in the stateList database
            new_state = formStateList.save(commit=False)
            #Check if already in chart
            existing_states = StatesList.objects.filter(chart_id = chart.id)

            for existing_state in existing_states:
                print(existing_state.state.lower())
                if existing_state.state.lower() != new_state.state.lower():
                    new_state.chart = chart
                    new_state.save()
                #Delete New Entry as to not have duplicates  
                else:
                    new_state.delete()
            

        if formChart.is_valid():
            chart = formChart.save(commit=False)
            chart.save()
            return redirect(url)
        

    else:
        # A GET, create a pre-filled form with the instance.
        formChart = EditChartForm(instance=chart)
        formStateList = AddStateForm()

    plots_svg = chart_function(chart)
    qs = StatesList.objects.filter(chart_id = chart.id).values('id', 'state', 'chart_id')
    print(qs)
    states=[]
    for entry in qs:
        states.append({
            'id': entry['id'],
            'state': entry['state'],
            'chart': entry['chart_id'],
        })

    context = {
        'formChart' : formChart,
        'formState' : formStateList,
        'rendered_chart': chart.plot_entry,
        'states': states,

    }

    return render(request, 'pages/edit_chart.html', context)

def delete_state(request, chart_id, id):
    print('---------------')
    print('deleting state with id', id)
    state = StatesList.objects.filter(chart_id = chart_id)
    state = state.get(id = id)
    state.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def delete_chart(request, username, chart_id):
    print('-----------')
    print('Deleting chart with ID: ', chart_id)
    print('-----------')
    chart = Chart.objects.get(id = chart_id)
    chart.delete()
    # Prevent users who are not the owner user from deleting this
    if chart.creator_user_id != request.user.id:
       raise SuspiciousOperation('Attempted to delete wrong list')

    return redirect('/charts/'+username+'/')
# Existing content/functionality to be removed/phased out
def reading_list_home(request):
    # R in CRUD --- READ ReadingLists from database
    plots_svg = []
    charts = Chart.objects.all()
   
    for chart in charts:
        plot_svg = chart.plot_entry
        plots_svg.append(plot_svg)
        
    
    #.select_related('creator_user')

    # Let's sort by their "score"
    #reading_lists = reading_lists.order_by('-score')

    # And "paginate" the results (split them into pages)
    # https://docs.djangoproject.com/en/3.0/topics/pagination/
    page_number = request.GET.get('page', 1)
    paginator = Paginator(charts, 4)
    results_page = paginator.page(page_number)

    context = {
        'results_page': results_page,
        'rendered_chart' : plots_svg,
    }
    return render(request, 'pages/home.html', context)

def reading_list_details(request, list_id):
    # R in CRUD --- READ a single ReadingList & its books from database
    reading_list_requested = ReadingList.objects.get(id=list_id)

    # Count views of pages for determining what's popular
    reading_list_requested.increment_views()

    books = Book.objects.filter(reading_list=reading_list_requested)
    context = {
        'reading_list': reading_list_requested,
        'all_books': books,
    }
    return render(request, 'pages/details.html', context)

@login_required
def reading_list_create(request):
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request
        form = AddReadingListForm(request.POST)
        if form.is_valid():
            # If we had omitted commit=False, then the user would not have been
            # properly set-up
            new_reading_list = form.save(commit=False)
            new_reading_list.creator_user = request.user
            new_reading_list.save()
            return redirect(new_reading_list.get_absolute_url())
    else:
        # if a GET  we'll create a blank form
        form = AddReadingListForm()
    context = {
        'form': form,
        'form_title': 'New book list',
    }
    return render(request, 'pages/form_page.html', context)


@login_required
def reading_list_delete(request, list_id):
    # D in CRUD --- DELETE reading list from database
    readinglist = ReadingList.objects.get(id=list_id)

    # Prevent users who are not the owner user from deleting this
    #if readinglist.creator_user != request.user:
    #    raise SuspiciousOperation('Attempted to delete wrong list')

    readinglist.delete()
    return redirect('/')


@login_required
def reading_list_create_book(request, list_id):
    # C in CRUD --- CREATE books in database
    reading_list_requested = ReadingList.objects.get(id=list_id)

    # TODO: BONUS CHALLENGE - Uncomment this to fix the security defect
    #if reading_list_requested.creator_user != request.user:
    #    raise SuspiciousOperation('Attempted to add book to wrong list')

    if request.method == 'POST':
        # Create a form instance and populate it with data from the request
        form = AddBookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.reading_list = reading_list_requested
            book.save()

            # Redirect back to the reading list we were at
            return redirect(reading_list_requested.get_absolute_url())
    else:
        # if a GET  we'll create a blank form
        form = AddBookForm()
    context = {
        'form': form,
        'form_title': 'Add book',
    }
    return render(request, 'pages/form_page.html', context)


@login_required
def reading_list_delete_book(request, book_id):
    # D in CRUD, delete book
    book = Book.objects.get(id=book_id)

    # Ensure that the creator of the reading list of the book is indeed the
    # person requesting that the book be deleted
    # TODO: Challenge 4 Uncomment this to fix the security defect
    #if book.reading_list.creator_user != request.user:
    #    raise SuspiciousOperation('Attempted to delete book to wrong list')

    book.delete()

    return redirect(book.reading_list.get_absolute_url())






    #Legay code for requesting data

    #function which handles the graphing of state specific data
# def graphing_state_values(charts):
#     state_dict = {}

#     for chart in charts:
#         if chart.chart_type == 'bar':
#             plot = pygal.Bar()
#         else:
#             plot = pygal.Pie()

#         print('------------------')
#         print('state', chart.stateAbr.lower())
#         print(chart.year + chart.month + str(chart.day))
#         #ensuring valid url
#         print('url', 'https://api.covidtracking.com/v1/states/'+ chart.stateAbr.lower() +'/'+ chart.year + chart.month + str(chart.day) +'.json')
#         print('------------------')

#         response = requests.get('https://api.covidtracking.com/v1/states/'+ chart.stateAbr.lower() +'/'+ chart.year + chart.month + str(chart.day) +'.json')
#         state_data = response.json()
#         state_dict[state_data['state']] = state_data[chart.filter_field]
#         print(state_dict)
#         sorted_state_keys = sorted(state_dict, key=state_dict.get, reverse=True)
#         print(sorted_state_keys)

#         for k in sorted_state_keys:
#             v =state_dict[k]
#             print(v)
#             print(k)
#             print(state_dict)
#             value = int(v)
#             label = str(k)
#             plot.add(label, value)
#         plots_svg = plot.render(is_unicode=True)
#         print('------------')
#         print(' they type is: ', type(plots_svg))
#         print('-------------')
#         chart.plot_entry = plots_svg
#         chart.save()
#         print(chart.plot_entry)
#         print('-------------')
#     return plots_svg



    # #Setting a default data type and value
    # stateAbr = ""
    # #Getting a list of state abbreviations to compare against what the user enters
    # #will maybe allow for users to enter full state names eventually
    # response = requests.get('https://worldpopulationreview.com/static/states/abbr-list.json')
    # state_abr = response.json()
    

    # print(state_abr)
    # #Allowing for /comparison/ to be run without a search term
    # if 'searchterm' in request.GET.keys():
    #     stateAbr = request.GET['searchterm'].lower()
    
    # if stateAbr not in states and stateAbr != "" and stateAbr.upper() in state_abr:
    #     states.append(stateAbr)
    # # Graphing highest covid cases by state
    #     chart_svg = graphing_state_values(states)

    # else:
    #     chart_svg = graphing_state_values(states)
    # context = {
    #         'states': states,
    #         'rendered_chart': chart_svg.decode(),
    #         }
    # return render(request, 'pages/chart-visualization.html', context)

    #Legacy for plotting
             
    # chart = pygal.Bar()

    # for state in states:
    #     response = requests.get('https://api.covidtracking.com/v1/states/'+ state +'/20200501.json')     
    #     state_data = response.json()
    #     state_dict[str(state_data['state'])] = state_data['positive']
    # sorted_state_keys = sorted(state_dict, key=state_dict.get, reverse=True)
    # #checking if sort worked
    # print(sorted_state_keys)
    # print(state_dict)

    # #Graphing the sorted list
    # for k in sorted_state_keys:
    #     v =state_dict[k]
    #     print(k)
    #     print(state_dict)
    #     value = int(v)
    #     label = str(k)
    #     chart.add(label, value)

    # chart_svg = chart.render()
    # return chart_svg
