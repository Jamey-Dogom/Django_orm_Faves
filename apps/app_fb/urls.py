from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^create_user$', views.create_user),
    url(r'^login', views.login),
    url(r'^logout$', views.logout),
    url(r'^books$', views.success),
    url(r'add_book', views.add_book),
    url(r'fave/(?P<book_id>\d+)$', views.fave_book),
    url(r'books/(?P<book_id>\d+)$', views.edit),
    url(r'books/logout$', views.logout),    
    url(r'delete/(?P<book_id>\d+)$', views.delete),
    url(r'update/(?P<book_id>\d+)$', views.update),    
]