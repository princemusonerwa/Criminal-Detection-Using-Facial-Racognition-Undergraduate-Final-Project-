from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import MyAuthenticationForm

urlpatterns = [
    path('user/create', views.register, name="register"),
    path('user/<int:id>/edit', views.updateUser, name='edit_user'),
    path('user/<int:id>/delete', views.deleteUser, name='delete_user'),
    path('user', views.allUsers, name="users"),
    path('profile', views.profile, name="profile"),
    path('signin', views.signIn, name="signin"),
    path('logout', views.signOut, name="logout"),
    path('pass-reset', auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"), name="password_reset"),
    path('pass-reset/done', auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_done.html"), name="password_reset_done"),
    path('pass-reset-confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    path('pass-reset-complete', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
    path('export-user-csv', views.exportUserListCsv, name='export_user_csv'),
    path('export-user-excel', views.exportUserListExcel, name='export_user_excel'),
    path('export-user-pdf', views.exportUserListPdf, name='export_user_pdf'),
]