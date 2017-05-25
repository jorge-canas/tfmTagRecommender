#!/usr/bin/python
# -*- coding: utf-8 -*-
from django import forms
from django.core.validators import MinLengthValidator

value_error1000 = 'El valor tiene que estar entre 1 y 1000'
value_error40 = 'El valor tiene que estar entre 1 y 40'
value_error100 = 'El valor tiene que estar entre 1 y 100'
required = 'Este campo es requerido'

default_errors100 = {
        'required': required,
        'invalid': value_error100
    }
default_errors1000 = {
    'required': required,
    'invalid': value_error1000
}

default_errors40 = {
    'required': required,
    'invalid': value_error40
}


class ContextOptionsForm1(forms.Form):
    delete = forms.BooleanField(required=False, label='Eliminar noticias')
    numberOfNews = forms.IntegerField(required=False, min_value=1, max_value=1000, error_messages=default_errors1000,
                                      label='Nº de Noticias (Máx. 1000) - Se ejecuta si se eliminan las noticias')


class ContextOptionsForm2(forms.Form):
    use_syn_dict = forms.BooleanField(required=False, label='¿Usar diccionario sintáctico?')


class ContextOptionsForm3(forms.Form):
    """
    percentage = forms.IntegerField(required=True, min_value=1, max_value=100, error_messages=default_errors100,
                                    label='Porcentaje de palabras por categoría')
    """
    limit = forms.IntegerField(required=True, min_value=1, max_value=1000, error_messages=default_errors1000,
                               label='Límite de palabras por categoría')


class ContextOptionsForm4(forms.Form):
    testNews = forms.IntegerField(required=True, min_value=1, max_value=1000, error_messages=default_errors1000,
                                  label='Número de noticias de test - Máx. 1000')


class ContextOptionsForm(forms.Form):
    n_news = forms.IntegerField(required=False, min_value=1, max_value=1000, error_messages=default_errors1000,
                                label='Número de noticias de entrenamiento (Max 1000)')
    n_news_test = forms.IntegerField(required=True, min_value=1, max_value=1000, error_messages=default_errors1000,
                                     label='Numero de noticias de test (Max 1000)')
    limit = forms.IntegerField(required=True, min_value=1, max_value=40, error_messages=default_errors100,
                               label='Limite de palabras por categoria (Max 40)')
    confidence = forms.IntegerField(required=True, min_value=1, max_value=100, error_messages=default_errors100,
                                    label='Porcentaje de confianza que tiene que cumplir la regla')
    support = forms.IntegerField(required=True, min_value=1, max_value=100, error_messages=default_errors100,
                                 label='Porcentaje noticias que tiene que cumplir la regla (soporte)')
    use_syn_dict = forms.BooleanField(required=False, label='Usar diccionario sintáctico')


class GetTagForNewsText(forms.Form):
    news_body = forms.CharField(required=True, error_messages={'required': 'Por favor inserte algún texto'},
                                validators=[MinLengthValidator(50, 'El texto debe tener al menos 50 caracteres')],
                                label='Texto de la noticia', widget=forms.Textarea(attrs={'class': 'col-xs-9'}))
