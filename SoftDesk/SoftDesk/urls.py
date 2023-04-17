"""SoftDesk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_nested import routers

from issuetracking.views import ProjectViewset,\
    ContributorViewset,\
    IssueViewset,\
    CommentViewset
from authentication.views import CreateUserAPIView

router = routers.SimpleRouter()
router.register(r'projects', ProjectViewset, basename='project')

projects_router = routers.NestedSimpleRouter(router, r'projects', lookup='project')
projects_router.register(r'users', ContributorViewset, basename='project-contributors')
projects_router.register(r'issues', IssueViewset, basename='project-issues')

issue_router = routers.NestedSimpleRouter(projects_router, r'issues', lookup='issue')
issue_router.register(r'comment', CommentViewset, basename='issue-comments')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('rest_framework.urls')),
    path('signup/', CreateUserAPIView.as_view(), name='create_user'),

    path('', include(router.urls)),
    path('', include(projects_router.urls)),
    path('', include(issue_router.urls)),

    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
