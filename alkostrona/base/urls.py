from django.urls import path
from .views import MainMenu, AlcoholDetail, AlcoholAdd, AlcoholChange, AlcoholRemove, activate, password_change,\
    custom_login, register, ProfileView, ProfileUpdate, AlcoholTypeChosen, like_alcohol, LikedAlcohols, review_alcohol,\
    forgot_password, forgotPasswordConfirm, UnverifiedAlcohols, verify_alcohol, delete_review
from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('login/', custom_login, name='login'),
    path('logout/', LogoutView.as_view(next_page='main_menu'), name='logout'),
    path('like/', like_alcohol, name='like-alcohol'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='user_profile'),
    path('profile/<int:pk>/liked', LikedAlcohols.as_view(), name='liked_alcohols'),
    path('edit-profile/<int:pk>/', ProfileUpdate.as_view(), name='profile_change'),
    path('alcohol-type/<str:type>/', AlcoholTypeChosen.as_view(), name='alcohol_type'),
    path('activate/<uidb64>/<token>', activate, name='activate'),
    path('register/', register, name='register'),
    path('password_change/', password_change, name="password_change"),
    path('forgot_password/', forgot_password, name="forgot_password"),
    path('reset/<uidb64>/<token>', forgotPasswordConfirm, name='forgot_password_confirm'),
    path('', MainMenu.as_view(), name='main_menu'),
    path('alcohol/<int:pk>/', AlcoholDetail.as_view(), name='alco_det'),
    path('alcohol_unverified/', UnverifiedAlcohols.as_view(), name='unverified'),
    path('verify/', verify_alcohol, name='verify'),
    path('alcohol/<int:pk>/review', review_alcohol, name='alcohol_review'),
    path('delete_review/', delete_review, name='delete_review'),
    path('alcohol-add', AlcoholAdd.as_view(), name='alcohol-add'),
    path('alcohol-update/<int:pk>/', AlcoholChange.as_view(), name='alcohol-change'),
    path('alcohol-remove/<int:pk>/', AlcoholRemove.as_view(), name='alcohol-remove'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

