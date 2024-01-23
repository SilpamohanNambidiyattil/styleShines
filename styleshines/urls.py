from django.urls import path
from styleshines.views import SignUpView,SignInView,IndexView,\
CategoryAddView,remove_categories,\
JewelleryCreateView,JewelleryListView,JewelleryUpdateView,remove_jewellery,JewelleryDetailView,\
JewelleryVarientsAddView,JewelleryVarientUpdateView,remove_jewellery_varient,\
OfferAddView,remove_offers

urlpatterns=[
    path('register/',SignUpView.as_view(),name='signup'),
    path('',SignInView.as_view(),name='signin'),
    path('categories/add',CategoryAddView.as_view(),name='cat-add'),
    path('categories/<int:pk>/remove',remove_categories,name='cat-remove'),
    path('jewellery/add',JewelleryCreateView.as_view(),name='jewellery-add'),
    path('jewellery/all',JewelleryListView.as_view(),name='jewellery-list'),
    path('jewellery/<int:pk>/change',JewelleryUpdateView.as_view(),name='jewellery-change'),
    path('jewellery/<int:pk>/remove',remove_jewellery,name='jewellery-remove'),
    path('jewellery/<int:pk>/varients/add',JewelleryVarientsAddView.as_view(),name='jewellery-varients-add'),
    path('jewellery/<int:pk>',JewelleryDetailView.as_view(),name='jewellery-detail'),
    path('varients/<int:pk>/change',JewelleryVarientUpdateView.as_view(),name='jewellery-varient-change'),
    path('varient/<int:pk>/remove',remove_jewellery_varient,name='jewellery-varient-remove'),
    path('jewelleryvarient/<int:pk>/offers/add',OfferAddView.as_view(),name='offers-add'),
    path('offers/<int:pk>/remove',remove_offers,name='offer-remove'),

    path('index/',IndexView.as_view(),name='index')


]