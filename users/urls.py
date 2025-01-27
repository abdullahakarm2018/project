from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from users import views
urlpatterns = [
    path('registerapi/',views.register_api ,name='registerapi'),
    
]
urlpatterns = format_suffix_patterns(urlpatterns)
