from django.urls import path, include
from rest_framework import routers
from elekenGK.views import (TestView, AccessView, DiscordMessageView, CreateTempUserView, UpdateUserNameView)

#router = routers.DefaultRouter()
#router.register('test', TestView.as_view(), "test")

urlpatterns = [
    #path('', include(router.urls))
    path('', TestView.as_view()),
    path('touch', AccessView.as_view()),
    path('message', DiscordMessageView.as_view()),
    path('register_user', CreateTempUserView.as_view()),
    path('fetch_name', UpdateUserNameView.as_view()),
]
