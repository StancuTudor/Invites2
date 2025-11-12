from django.urls import path
from .views import InviteDetailView, InviteAccessUpdateView, ResponseCreateView, MenuTypeListView

urlpatterns = [
    path('invite-detail/code=<str:code>/', InviteDetailView.as_view(), name='invite-detail'),
    path("update-date-last-access/code=<str:code>/", InviteAccessUpdateView.as_view(), name="update-date-last-access"),
    path("responses/", ResponseCreateView.as_view(), name="response-create"),
    path("menu-types/", MenuTypeListView.as_view(), name="menu-types-list"),
]