from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Avg, Count, Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import FormView, ListView, TemplateView, UpdateView

from django.conf import settings

from .forms import (
    BootstrapAuthenticationForm,
    KomentarzForm,
    OcenaForm,
    ProfileForm,
    RegisterForm,
    SearchForm,
)
from .models import Film, HistoriaOgladania, Kategoria, Komentarz, Ocena, Profile, Ulubiony


def _films_queryset():
    return Film.objects.annotate(
        avg_ocena=Avg("oceny__wartosc"),
        liczba_ocen=Count("oceny"),
    )


def _record_watch_history(user, film):
    if user.is_authenticated:
        HistoriaOgladania.objects.update_or_create(
            uzytkownik=user,
            film=film,
            defaults={},
        )


class HomeView(ListView):
    model = Film
    template_name = "films/home.html"
    context_object_name = "filmy"
    paginate_by = None

    def get_queryset(self):
        qs = _films_queryset()
        kategoria_id = self.request.GET.get("kategoria")
        if kategoria_id:
            qs = qs.filter(kategorie__id=kategoria_id).distinct()
        return qs

    def get_paginate_by(self, queryset):
        return settings.FILMS_PER_PAGE

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["najnowsze"] = _films_queryset()[:6]
        ctx["najwyzej_oceniane"] = (
            _films_queryset()
            .filter(liczba_ocen__gte=1)
            .order_by("-avg_ocena", "-liczba_ocen")[:6]
        )
        ctx["kategorie"] = Kategoria.objects.all()
        ctx["aktywna_kategoria"] = self.request.GET.get("kategoria", "")
        ctx["search_form"] = SearchForm()
        return ctx


class SearchView(ListView):
    model = Film
    template_name = "films/search.html"
    context_object_name = "filmy"
    paginate_by = None

    def get_queryset(self):
        query = (self.request.GET.get("q") or "").strip()
        qs = _films_queryset()
        if query:
            qs = qs.filter(Q(tytul__icontains=query) | Q(gatunek__icontains=query))
        return qs

    def get_paginate_by(self, queryset):
        return settings.FILMS_PER_PAGE

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["query"] = (self.request.GET.get("q") or "").strip()
        ctx["search_form"] = SearchForm(initial={"q": ctx["query"]})
        return ctx


class FilmDetailView(TemplateView):
    template_name = "films/detail.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        film = get_object_or_404(_films_queryset(), pk=kwargs["pk"])
        _record_watch_history(self.request.user, film)

        user_ocena = None
        is_favorite = False
        if self.request.user.is_authenticated:
            user_ocena = Ocena.objects.filter(uzytkownik=self.request.user, film=film).first()
            is_favorite = Ulubiony.objects.filter(uzytkownik=self.request.user, film=film).exists()

        ctx["film"] = film
        ctx["komentarze"] = film.komentarze.select_related("uzytkownik").all()
        ctx["ocena_form"] = OcenaForm(initial={"wartosc": user_ocena.wartosc if user_ocena else 5})
        ctx["komentarz_form"] = KomentarzForm()
        ctx["user_ocena"] = user_ocena
        ctx["is_favorite"] = is_favorite
        return ctx


class FavoritesView(LoginRequiredMixin, ListView):
    model = Film
    template_name = "films/favorites.html"
    context_object_name = "filmy"

    def get_queryset(self):
        return _films_queryset().filter(
            ulubione_wpisy__uzytkownik=self.request.user
        ).order_by("-ulubione_wpisy__dodano")


class HistoryView(LoginRequiredMixin, ListView):
    model = Film
    template_name = "films/history.html"
    context_object_name = "filmy"

    def get_queryset(self):
        return _films_queryset().filter(
            historia_wpisy__uzytkownik=self.request.user
        ).order_by("-historia_wpisy__obejrzano")


class AppLoginView(LoginView):
    template_name = "auth/login.html"
    authentication_form = BootstrapAuthenticationForm


class AppLogoutView(LogoutView):
    pass


class RegisterView(FormView):
    template_name = "auth/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "Konto zostało utworzone. Witaj!")
        return super().form_valid(form)


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = "films/profile_edit.html"
    success_url = reverse_lazy("profile_edit")

    def get_object(self, queryset=None):
        return self.request.user.profile

    def form_valid(self, form):
        messages.success(self.request, "Profil został zaktualizowany.")
        return super().form_valid(form)


@login_required
@require_POST
def toggle_favorite(request, pk):
    film = get_object_or_404(Film, pk=pk)
    ulubiony, created = Ulubiony.objects.get_or_create(uzytkownik=request.user, film=film)
    if not created:
        ulubiony.delete()
        messages.info(request, f"Usunięto „{film.tytul}” z ulubionych.")
    else:
        messages.success(request, f"Dodano „{film.tytul}” do ulubionych.")
    return redirect("film_detail", pk=film.pk)


@login_required
@require_POST
def submit_rating(request, pk):
    film = get_object_or_404(Film, pk=pk)
    form = OcenaForm(request.POST)
    if form.is_valid():
        Ocena.objects.update_or_create(
            uzytkownik=request.user,
            film=film,
            defaults={"wartosc": form.cleaned_data["wartosc"]},
        )
        messages.success(request, "Ocena została zapisana.")
    else:
        messages.error(request, "Podaj ocenę od 1 do 10.")
    return redirect("film_detail", pk=film.pk)


@login_required
@require_POST
def add_comment(request, pk):
    film = get_object_or_404(Film, pk=pk)
    form = KomentarzForm(request.POST)
    if form.is_valid():
        komentarz = form.save(commit=False)
        komentarz.uzytkownik = request.user
        komentarz.film = film
        komentarz.save()
        messages.success(request, "Komentarz został dodany.")
    else:
        messages.error(request, "Nie udało się dodać komentarza.")
    return redirect("film_detail", pk=film.pk)


@login_required
@require_POST
def delete_comment(request, pk):
    komentarz = get_object_or_404(Komentarz, pk=pk, uzytkownik=request.user)
    film_pk = komentarz.film_id
    komentarz.delete()
    messages.info(request, "Komentarz został usunięty.")
    return redirect("film_detail", pk=film_pk)
