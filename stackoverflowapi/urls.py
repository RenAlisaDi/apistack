from django.contrib import admin
from django.db import router
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from main.views import *

router = DefaultRouter()
router.register('problems', ProblemViewSet)
router.register('replies', ReplyViewSet)
router.register('comments', CommentViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v2/', include(router.urls)),
    path('api/v2/', include('account.urls')),
]
