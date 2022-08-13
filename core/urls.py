from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_auth.views import LoginView, LogoutView,PasswordResetView, PasswordResetConfirmView, PasswordChangeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('rest-auth/Login/', LoginView.as_view(), name='login_view'),
    path('rest-auth/Logout/', LogoutView.as_view(), name='logout_view'),
    path('rest-auth/password/reset/',PasswordResetView.as_view(), name='password_reset' ),
    path('rest-auth/password/reset-confirm/<uidb64>/<token>',PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('userapp/', include('userapp.api.urls'))
 ]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
