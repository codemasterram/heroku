from todos import views, views_api
from django.conf.urls import url


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create$', views.create, name='create'),
    url(r'^savepost$', views.save, name='save'),
    url(r'^about$', views.about, name='about'),
    url(r'^edit/todos/(\d+)$', views.edit, name='edit'),
    url(r'^remove/todos/(\d+)$', views.remove, name='remove'),
    url(r'^api/remove/(\d+)$', views_api.remove, name='api_remove_todo'),

    # url(r'^api/todos/(\d+)$', views_api.update, name='api_update_todo'),
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^signup$', views.signup, name='signup'),
    url(r'^signupdetails$', views.signupdetails, name='signupdetails'),
    url(r'^submission$', views.submission, name='submission'),
    url(r'^hastagg/(\d+)$', views.hastagg, name='hastagg'),
    # api url to work with api for other applicaions
     url(r'^api/todos$', views.TodoListView.as_view(), name='api_todo_list'),
     url(r'^api/todos/(?P<pk>[0-9]+)$', views.TodoItemView.as_view(), name='api_todo_item')
]
