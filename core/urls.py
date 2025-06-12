from django.urls import path
from .views import (
    AboutUsView,ContactUsView
)

urlpatterns = [
    path('about/',AboutUsView.as_view(),name='about_us'),
    path('contact/',ContactUsView.as_view(),name='contact_us')
]