from django.urls import path
from . import views

urlpatterns = [
    path('novo/', views.cadastrar_cliente, name='cadastrar_cliente'),
]