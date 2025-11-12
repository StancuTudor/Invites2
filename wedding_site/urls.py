from django.urls import path, include

urlpatterns = [
    path('api/invites/', include('invites.urls')),
]