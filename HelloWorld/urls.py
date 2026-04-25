from django.urls import path
from . import views
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', cache_page(300)(views.PostList.as_view()), name='home'),
]