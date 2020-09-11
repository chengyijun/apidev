from django.urls import path, re_path

from api import views

app_name = 'api'
urlpatterns = [
    # 版本检查 需要如此格式的规则
    re_path(r'^(?P<version>.*?)/test/$', views.TestView.as_view(), name='test'),

    path('roles/', views.RolesView.as_view(), name='roles'),
    path('userinfos/', views.UserInfosView.as_view(), name='userinfos'),
    path('test/', views.TestView.as_view(), name='test'),
    # path('test/<int:token>/', views.TestView.as_view(), name='test'),
    # re_path(r'^test/(?P<token>\d+)/$', views.TestView.as_view(), name='test'),
    # path('login/', views.LoginView.as_view(), name='login'),
    # path('code/', views.CodeView.as_view(), name='code'),
    # path('tempauth/', views.TempAuthView.as_view(), name='tempauth'),

    # APIView
    # path('articles/', views.ArticleView.as_view(), name='articles'),
    # re_path(r'article/(?P<id>\d+)/$', views.ArticleDetailView.as_view(), name='article-detail'),
    # 等价于上面的写法 建议使用上面一种 便于理解
    # path('article/<id>/', views.ArticleDetailView.as_view(), name='article-detail'),
]
