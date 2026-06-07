from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import (
    AppLoginView,
    AppLogoutView,
    FavoritesView,
    FilmDetailView,
    HistoryView,
    HomeView,
    ProfileEditView,
    RegisterView,
    SearchView,
    add_comment,
    delete_comment,
    submit_rating,
    toggle_favorite,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("szukaj/", SearchView.as_view(), name="search"),
    path("film/<int:pk>/", FilmDetailView.as_view(), name="film_detail"),
    path("film/<int:pk>/ulubione/", toggle_favorite, name="toggle_favorite"),
    path("film/<int:pk>/ocena/", submit_rating, name="submit_rating"),
    path("film/<int:pk>/komentarz/", add_comment, name="add_comment"),
    path("komentarz/<int:pk>/usun/", delete_comment, name="delete_comment"),
    path("ulubione/", FavoritesView.as_view(), name="favorites"),
    path("historia/", HistoryView.as_view(), name="history"),
    path("login/", AppLoginView.as_view(), name="login"),
    path("logout/", AppLogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("profil/", ProfileEditView.as_view(), name="profile_edit"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
