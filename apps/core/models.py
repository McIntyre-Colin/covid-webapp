from random import choices
from django.db import models
from django.utils.timezone import now

from apps.accounts.models import User

CHARTS = [
    ('bar','Bar Chart'),
    ('pie', 'Pie Chart'),
]

MONTH = [
    ('01', 'January'), ('02', 'Feburary'), ('03', 'March'), ('04', 'April'),
    ('05', 'May'), ('06', 'June'), ('07',  'July'), ('08', 'August'), ('09', 'September'),
    ('10', 'October'), ('11', 'November'), ('12', 'December'),
]
YEAR = [
    ('2020', '2020'),
    ('2021', '2021')
]
DATA_FIELDS=[
    ('positive','Total Positive Cases to Date'),
    ('positiveIncrease', 'Daily Increase in Positive Cases'),
    ('hospitalizedCurrently', 'Currently Hospitalized'),
    ('onVentilatorCurrently', 'Currently On a Ventilator'),
    ('death', 'Deaths to Date'),
    ('deathIncrease', 'Daily Increase in Deaths'),
]

state_abbr_list=[
    'al', 'ak','az','ar','ca','co','ct','de','fl','ga','hi','id','il','in','ia',
    'ks','ky','la','me','md','ma','mi','mn','ms','mo','mt','ne','nv','nh','nj','nm','ny','nc',
    'nd','oh','ok','or','pa','ri','sc','sd','tn','tx','ut','vt','va','wa','wv','wi','wy',
]
class Chart(models.Model):
    creator_user= models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(auto_now_add=True) # Add current date
    last_modified = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=50, default='Title')
    plot_entry = models.TextField()
    votes = models.IntegerField(default=0)

    def increment_views(self):
        self.views += 1
        self.recalculate_popularity()
        self.save()

    #Algorithim to calculate 'hot' charts, need to implement
    def recalculate_popularity(self):
        # Calculate how old the post is in hours
        age = now() - self.created
        age_in_hours = age.total_seconds() / 60 / 60

        # Calculate the new score, which is 10% of view count, then subtracting
        # the age of the post in hours
        score = (self.views * 0.10) - age_in_hours

        # Round to the nearest whole value
        self.score = round(score)
    
class Voted(models.Model):
    chart = models.ManyToManyField(Chart)
    user = models.ManyToManyField(User)
    has_voted = models.BooleanField(default=False)
    vote = models.CharField(max_length = 4, blank=True)

class ChartProperties(models.Model):
    chart = models.ForeignKey(
        Chart,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=50, default='Title')
    chart_type = models.CharField(max_length=15, choices=CHARTS)
    day = models.CharField(max_length = 2, default='01')
    month = models.CharField(max_length = 15, choices= MONTH)
    year = models.CharField(max_length = 15, choices= YEAR)
    stateAbr = models.CharField(max_length=2)
    filter_field = models.CharField(max_length = 40,choices=DATA_FIELDS)

class StatesList(models.Model):
    chart = models.ForeignKey(
        Chart,
        on_delete=models.CASCADE,
    )
    state = models.CharField(max_length=2, default='',blank=True)
    


GENRES = [
    ('fiction', 'Adult Fiction'),
    ('nonfiction', 'Adult Non-Fiction'),
    ('children', "Children's Books"),
]

