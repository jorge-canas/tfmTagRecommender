#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from . import views

app_name = 'pueblos'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<noticia_200_id>[0-9]+)/noticia200/$', views.noticia200, name='noticia200'),
    url(r'^(?P<noticia_200_id>[0-9]+)/deleteWords/$', views.delete_words, name='delete_words'),
    url(r'^news200List/$', views.News200ListView.as_view(), name='news200List'),
    url(r'^listCategorizedNews/$', views.list_categorized_news, name='list_categorized_news'),
    url(r'^(?P<noticia_id>[0-9]+)/showNewsCategories/$', views.show_news_categories,
        name='show_news_categories'),
    url(r'^saveCategory/$', views.save_category, name='save_category'),
    url(r'^newsContext/$', views.news_context_view, name='news_context'),
    url(r'^newsContextStep/$', TemplateView.as_view(template_name="pueblos/newsContextStep.html"),
        name='news_context_step'),
    # url(r'^setContextOptionsRun/$', views.set_context_options_run, name='set_context_options_run'),
    # url(r'^processWord/setIndividualContext/$', views.context_options_process, name='context_options_process'),
    url(r'(?P<option>[a-zA-Z]+)/setIndividualContext/$', views.context_options_router, name='context_options_router'),
    url(r'(?P<page>[0-9]+)/syntacticDictionary/(?P<filter>\w+)$', views.syntactic_dictionary,
        name='syntactic_dictionary'),
    url(r'^searchWord/$', views.search_word, name="search_word"),
    url(r'^saveWord/$', views.save_word, name="save_word"),
    url(r'^newsSuggestTags/$', views.news_suggest_tags, name='news_suggest_tags'),
    url(r'^(?P<test_case_id>[0-9]+)/checkStatus/$', views.check_status, name='check_status'),
    url(r'^singularize/$', views.singularize, name='singularize'),
    # url(r'^test_task/$', views.test_task_view, name='test_task'),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
