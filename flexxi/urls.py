from django.urls import path
from flexxi import views

app_name = 'flexxi'

urlpatterns = [
    path('', views.index, name='home'),
    path('signup/', views.signup, name='signup'),
    path('user_login/',views.user_login,name='user_login'),
    path('blog/', views.blog, name='blog'),
    path('enquiries/', views.enquiries, name='enquiries'),
    path('computer/', views.computer, name='computer'),
    path('tag/<slug:tag_slug>/', views.blog, name='blog_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.detail, name='detail'),
]