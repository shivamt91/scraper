from django.urls import path
from . views import CrawlView
from . views import StatusView
from . views import HomePageView
from . views import RequiredData
from rest_framework import routers
from flip import views
from django.conf.urls import include


router = routers.DefaultRouter()
router.register('data', views.DataViewSet)

urlpatterns = [
    path('', HomePageView.as_view()),
    path('crawl', CrawlView.as_view()),
    path('status', StatusView.as_view()),
    path('closest_price', RequiredData.as_view()),
    path('', include(router.urls)),
]
