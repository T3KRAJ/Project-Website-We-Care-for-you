from django.urls import path
from Confession.views import (
    ConfessionPostList, 
    confessionpost_detail,
    CreateConfessionPost,
    CPUpdateView,
    CPDeleteView,
    like_confessionpost,
)

app_name = 'confession' 

urlpatterns = [
    path('confessions/', ConfessionPostList.as_view(), name='posts'),
    path('confession/<slug:slug>/', confessionpost_detail, name='post-detail'),
    path('confessionpost/create/', CreateConfessionPost.as_view(), name='create-post'),
    path('confessionpost/<slug>/update/', CPUpdateView.as_view(), name='post-update'),
    path('confessionpost/<slug>/delete/', CPDeleteView.as_view(), name='post-delete'),
    path('confessionpost/like/', like_confessionpost, name='like-post'),

]