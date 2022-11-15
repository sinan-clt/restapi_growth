from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('register', views.Register.as_view()),
    path('login', views.UserLogin.as_view()),
    
    path('addEbook', views.addEbook.as_view()),
    path('getAllEbooks', views.getAllEbooks.as_view()),
    path('editEbook/<int:id>', views.editEbook.as_view()),
    path('deleteEbook/<int:id>', views.deleteEbook.as_view()),

]