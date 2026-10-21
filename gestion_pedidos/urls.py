from django.urls import path
from . import views

urlpatterns = [
    path('', views.catalogo_productos, name='catalogo_productos'),
    path('pedido/nuevo/', views.crear_pedido, name='crear_pedido'),
    path('dashboard/', views.dashboard, name='dashboard'),
]