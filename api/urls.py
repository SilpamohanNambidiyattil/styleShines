from django.urls import path

from api import views

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register('jewellery',views.JewelleryView,basename="jewellery")
router.register('carts',views.CartsView,basename="carts")
router.register('orders',views.OrdersView,basename="orders")
router.register('review',views.ReviewView,basename="review")


urlpatterns=[
    path("register/",views.UserCreationView.as_view()),
    path('token/',ObtainAuthToken.as_view()),

]+ router.urls