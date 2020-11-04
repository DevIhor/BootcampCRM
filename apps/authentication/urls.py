from django.urls import path

from apps.authentication.views import ObtainJSONWebToken, RefreshJSONWebToken, VerifyJSONWebToken, SignUpView, \
    ActivateUserView

urlpatterns = [
    path('', ObtainJSONWebToken.as_view(), name='auth'),
    path('refresh/', RefreshJSONWebToken.as_view(), name='auth-refresh'),
    path('verify/', VerifyJSONWebToken.as_view(), name='auth-verify'),
    path('signup/', SignUpView.as_view(), name='auth-signup'),
    path('activate/', ActivateUserView.as_view(), name='auth-activate'),
]
