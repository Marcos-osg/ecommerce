from django.urls import path
from store import views


urlpatterns = [
    path('', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    
    path('update_item/', views.updateItem, name='update-item'),
    path('process_order/', views.processOrder, name='process-order'),
    path('status_order/', views.status_order, name='order-status'),
    #path('att_order/?P<id>[0-9]+', views.atualiza, name='order-atualiza'),
]