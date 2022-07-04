from django.urls import path

from apps.core import views

urlpatterns = [
    # CRUD views for ReadingLists
    path('', views.chart_home, name="home"),
    path('nationwide/', views.state_data),
    path('charts/<username>/', views.user_page, name='userPage'),
    path('charts/<username>/create/',views.create_chart, name='createChart'),
    path('charts/<username>/<int:chart_id>/', views.edit_chart, name='editChart'),
    path('charts/<int:chart_id>/delete/<int:id>/', views.delete_state, name='deleteState'),
    path('charts/<username>/delete/<chart_id>/', views.delete_chart, name='deleteChart'),
    path('charts/<user_id>/<chart_id>/vote/up/', views.chart_vote_up, name='voteUp'),
    path('charts/<user_id>/<chart_id>/vote/down/', views.chart_vote_down, name='voteDown'),


]
