from django.urls import path

from apps.core import views

# In this example, we've separated out the views.py into a new file
urlpatterns = [
    path('', views.index),
    path('state-data', views.state_data),
    path('comparison/', views.comparison)
]

# Boilerplate to include static files
from django.conf import settings
from django.conf.urls.static import static
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

