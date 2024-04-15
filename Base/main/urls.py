from django.urls import path
from . import views
from . import Dump


urlpatterns = [
    path('', views.index, name='home'),
    path('copy', views.copy, name='copy'),
    path('requests', views.requests, name='requests'),
    path('tables', views.tables, name='tables'),
    path('add_object', views.add_object, name='add_object'),
    path('edit/<int:id>/', views.edit, name='edit'),
    path('directory', views.directory, name='directory'),
    path('directory1', views.directory1, name='directory1'),
    path('directory2', views.directory2, name='directory2'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('search', views.search, name='search'),
    path("tmplt/", views.tmplt),
    path("create/", views.create),
    path("print_users/", views.print_users),
    path("dump", Dump.dump_base, name='dump'),
    path("load", Dump.load_base, name='load'),

]
