from django.conf.urls import url
from routing import views

urlpatterns = [
    url(r'^home/', views.home, name='map'),
    url(r'^result/', views.result, name='result')
]
