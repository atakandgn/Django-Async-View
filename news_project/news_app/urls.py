from django.urls import path
from .views import async_news, sync_news, homepage, async_file_upload_view

urlpatterns = [
   path('', homepage, name='homepage'),
   path('async_news/', async_news, name='async_news'),
   path('sync_news/', sync_news, name='sync_news'),
   path('async_file_upload/', async_file_upload_view, name='async_file_upload'),
]


