from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.validators import MaxValueValidator, MinValueValidator

from .models import CustomUser, Komentarz, Profile


class BootstrapAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label="Nazwa użytkownika",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Nazwa użytkownika"}),
    )
    password = forms.CharField(
        label="Hasło",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Hasło"}),
    )


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "E-mail"}),
    )
    username = forms.CharField(
        label="Nazwa użytkownika",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Nazwa użytkownika"}),
    )
    password1 = forms.CharField(
        label="Hasło",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Hasło"}),
    )
    password2 = forms.CharField(
        label="Powtórz hasło",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Powtórz hasło"}),
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("email", "username")


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("avatar", "bio")
        labels = {"avatar": "Awatar", "bio": "O mnie"}
        widgets = {
            "bio": forms.Textarea(
                attrs={"class": "form-control", "rows": 4, "placeholder": "Krótki opis profilu..."}
            ),
        }


class OcenaForm(forms.Form):
    wartosc = forms.IntegerField(
        label="Ocena",
        min_value=1,
        max_value=10,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        widget=forms.NumberInput(attrs={"class": "form-control", "min": 1, "max": 10}),
    )


class KomentarzForm(forms.ModelForm):
    class Meta:
        model = Komentarz
        fields = ("tresc",)
        labels = {"tresc": "Komentarz"}
        widgets = {
            "tresc": forms.Textarea(
                attrs={"class": "form-control", "rows": 3, "placeholder": "Napisz komentarz..."}
            ),
        }

    def clean_tresc(self):
        tresc = (self.cleaned_data.get("tresc") or "").strip()
        if not tresc:
            raise forms.ValidationError("Komentarz nie może być pusty.")
        return tresc


class SearchForm(forms.Form):
    q = forms.CharField(
        label="Szukaj",
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Szukaj po tytule lub gatunku..."}
        ),
    )
