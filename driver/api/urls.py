from django.urls import path
from .views import DeleteDriverByIdAPIView

urlpatterns = [
    path('driver/delete/<int:id>/', DeleteDriverByIdAPIView.as_view(), name='driver-delete-id'),
]
