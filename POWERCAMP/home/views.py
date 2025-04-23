from typing import Final

from django.core.validators import EmailValidator, RegexValidator
from django.forms import CharField, EmailField, Form
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render


CONTACT: Final[str] = (
    'Olá, sou {name}, celular {cel}, RG {rg} e email {email}, '
    'quero realizar minha inscrição no PowerCamp 2025'
)


class EventForm(Form):
    name: CharField = CharField(
        label='NOME COMPLETO:',
        min_length=5,
        max_length=256,
        strip=True,
        required=True,
    )
    cel: CharField = CharField(
        label='CELULAR:',
        min_length=11,
        max_length=15,
        strip=True,
        required=True,
        validators=[
            RegexValidator(
                r'^\(\d{2}\) 9\d{4}-\d{4}$',
                'Seu número de celular deve conter apenas números',
            )
        ],
    )
    rg: CharField = CharField(
        label='RG:',
        min_length=9,
        max_length=12,
        strip=True,
        required=True,
        validators=[
            RegexValidator(
                r'^\d{2}\.\d{3}\.\d{3}-\d{1}$',
                'Seu RG deve conter apenas números',
            )
        ],
    )
    email: EmailField = EmailField(
        label='EMAIL:',
        min_length=11,
        max_length=64,
        required=True,
        validators=[EmailValidator],
    )


def landpage(r: HttpRequest) -> HttpResponse:
    return render(r, 'home/landpage.html')


def event_form(r: HttpRequest) -> HttpResponse:
    if r.method != 'POST':
        return render(r, 'home/register.html', {'form': EventForm()})

    form: EventForm = EventForm(r.POST)

    if not form.is_valid():
        return render(r, 'home/register.html', {'form': form})

    name: str = form.cleaned_data['name']
    cel: str = form.cleaned_data['cel']
    rg: str = form.cleaned_data['rg']
    email: str = form.cleaned_data['email']

    return redirect(
        'https://wa.me/+5511985774716?text='
        + CONTACT.format(name=name.title(), cel=cel, rg=rg, email=email)
    )
