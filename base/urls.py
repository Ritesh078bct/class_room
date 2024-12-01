from django.urls import path
from . import views



urlpatterns = [
    path('sign-up/',views.registerUser, name='sign-up'),

    path('',views.index, name='index') ,
    path('create-room/', views.createRoom, name='create-room'),
    path('delete-room/<int:room_id>/',views.deleteRoom,name='delete-room'),
    path('update-room/<int:room_id>/',views.updateRoom, name='update-room'),
    path('room/<int:room_id>',views.room,name="room"),
    path('delete-message/<int:message_id>/',views.deleteMessage,name='delete-message'),

    path('profile/<int:user_id>',views.userProfile,name='profile'),
    path('update-profile/',views.updateProfile,name='update-profile'),

    path('search/', views.search_feature, name='search'),

]
