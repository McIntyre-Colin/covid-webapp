from django.urls import path

from apps.core import views

urlpatterns = [
    # CRUD views for ReadingLists
    path('', views.reading_list_home, name="home"),
    path('nationwide/', views.state_data),
    path('charts/<username>/', views.user_page, name='userPage'),
    path('charts/<username>/create/',views.create_chart, name='createChart'),
    path('charts/<username>/<chart_id>/', views.edit_chart, name='editChart'),
    path('charts/<chart_id>/<id>/delete/', views.delete_state, name='deleteState'),
    path('charts/<username>/<chart_id>/delete/', views.delete_chart, name='deleteChart'),
    path('list/<int:list_id>/', views.reading_list_details),
    path('list/create/', views.reading_list_create),
    path('list/delete/<int:list_id>/', views.reading_list_delete),

    # CRUD views for editing Books within ReadingLists
    path('book-create/<int:list_id>/', views.reading_list_create_book),
    path('book-delete/<int:book_id>/', views.reading_list_delete_book),
]
