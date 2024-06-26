from django.urls import path

from . import views

urlpatterns = [
    path("", views.profiles, name="profiles"),
    path("profile/<str:id>", views.profile, name="profile"),
    path("login", views.login_user, name="login"),
    path("logout", views.logout_user, name="logout"),
    path("register", views.register_user, name="register"),
    path("account", views.user_account, name="account"),
    path("edit", views.edit_account, name="edit-account"),
    path("create-skill", views.create_skill, name="create-skill"),
    path("update-skill/<uuid:id>", views.update_skill, name="update-skill"),
    path("delete-skill/<uuid:id>", views.delete_skill, name="delete-skill"),
    path("inbox/", views.inbox, name="inbox"),
    path("message/<uuid:id>", views.view_message, name="message"),
    path("create-message/<uuid:recipient_id>", views.create_message, name="create-message"),
]
