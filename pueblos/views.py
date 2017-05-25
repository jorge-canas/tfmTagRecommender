#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import time
from StringIO import StringIO

from django.core.management import call_command
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import ContextOptionsForm, ContextOptionsForm1, ContextOptionsForm2, ContextOptionsForm3, \
    ContextOptionsForm4, GetTagForNewsText
from .models import PueblosNoticias, PueblosNoticias200, PueblosNoticiasPalabras, PueblosPalabrasEliminar, \
    PueblosNoticiaCategorizada, PueblosCategoriasSemandal, PueblosDiccionarioSintactico, PueblosTestCase


class IndexView(generic.ListView):
    template_name = 'pueblos/index.html'
    # context_object_name = 'last_news_list'

    def get_queryset(self):
        return
        # Return the last five published news.
        # return PueblosNoticias.objects.order_by('fecha_ins')[:5]
        # return PueblosNoticias200.objects.all()[:5]


class DetailView(generic.DetailView):
    model = PueblosNoticias
    template_name = 'pueblos/detail.html'


class News200ListView(generic.ListView):
    template_name = 'pueblos/news200List.html'
    context_object_name = 'lista_noticias_200'

    def get_queryset(self):
        return PueblosNoticias200.objects.all()


def noticia200(request, noticia_200_id):
    noticia = get_object_or_404(PueblosNoticias200, pk=noticia_200_id)
    try:
        lista_palabras = PueblosNoticiasPalabras.objects.filter(noticia_200=noticia.id)
        categorias = noticia.get_categorias_string()
    except PueblosNoticiasPalabras.DoesNotExist:
        raise Http404("No hay palabras para esta noticia.")
    return render(request, 'pueblos/noticia200.html', {'noticia': noticia,
    'lista_palabras': lista_palabras, 'categorias': categorias})


def delete_words(request, noticia_200_id):
    # news = get_object_or_404(PueblosNoticias200, pk=noticia_200_id)
    words = request.POST.getlist('words[]')
    filename = './pueblos/docs/lista_palabras_eliminar.txt'
    with open(filename, 'a') as writer:
        for word in words:
            if 'delete' in request.POST:
                PueblosNoticiasPalabras.objects.filter(palabra=word).delete()
                # Almacenar la palabra en la base de datos de palabras a ignorar y al fichero de carga
                p = PueblosPalabrasEliminar.objects.filter(palabra=word)
                if not p.exists():
                    delete_word = PueblosPalabrasEliminar(palabra=word)
                    delete_word.save()
                    word = word.encode('utf-8')
                    writer.write(word + '\n')
            else:
                PueblosNoticiasPalabras.objects.get(noticia_200=noticia_200_id, palabra=word).delete()
    # return HttpResponseRedirect(reverse('pueblos:listaNoticias200'))
    return redirect('pueblos:noticia200', noticia_200_id=noticia_200_id)


def show_news_categories(request, noticia_id):
    news = PueblosNoticiaCategorizada.objects.filter(noticia=noticia_id)
    if len(news) == 0:
        return render(request, 'pueblos/showNewsCategories.html', {'news': None})
    suggested_categories = {}
    this_news = None
    categories = None
    if len(news) > 0:
        this_news = get_object_or_404(PueblosNoticias, pk=noticia_id)
        categories = this_news.get_categorias_string()
        for n in news:
            cat_id = n.categorias_sugeridas_id
            if cat_id:
                cat = PueblosCategoriasSemandal.objects.get(pk=cat_id)
                suggested_categories[cat.dscategoria] = {'status': n.comprobado, 'category_id': cat_id}
    # print suggested_categories
    return render(request, 'pueblos/showNewsCategories.html', {'news': this_news, 'categories': categories,
                                                               'suggested_categories': suggested_categories})


def save_category(request):
    message = 'Hubo un problema con la petición'
    stat = 'error'
    if request.method == 'POST':
        news_id = request.POST.get('news_id', None)
        category_id = request.POST.get('category_id', None)
        option = request.POST.get('option', None)
        news = PueblosNoticiaCategorizada.objects.filter(noticia=news_id, categorias_sugeridas=category_id)
        if len(news) == 0:
            message = 'El id de la noticia o categoría no es correcto'
        else:
            news = news[0]
            if option == 'add' or option == 'remove':
                if option == 'add':
                    news.comprobado = 1
                elif option == 'remove':
                    news.comprobado = 2
                news.save()
                message = 'Opción guardada con éxito'
                stat = 'ok'
            else:
                message = 'La opción no se reconoce'
    data = {'stat': stat, 'message': message}
    return HttpResponse(json.dumps(data), content_type="application/json")

"""
Show list of news with suggested categories
"""


def list_categorized_news(request):
    news = PueblosNoticiaCategorizada.objects.all().values_list('noticia', flat=True).distinct()
    news_list = []
    for n in news:
        this_news = PueblosNoticias.objects.filter(pk=n).get()
        if this_news:
            news_list.append(this_news)
    if news_list:
        return render(request, 'pueblos/listCategorizedNews.html', {'news': news_list})
    return render(request, 'pueblos/listCategorizedNews.html', {'news': None})


# ---------------------------- Context ----------------------------#

"""
class NewsContextView(TemplateView):
    template_name = 'pueblos/newsContextOptions.html'
    form_class = ContextOptionsForm

    def dispatch(self, request, *args, **kwargs):
        return super(NewsContextView, self).dispatch(request, *args, **kwargs)
"""


def check_status(request, test_case_id):
    try:
        test_case = PueblosTestCase.objects.get(pk=test_case_id)
        state = test_case.state
    except PueblosTestCase.DoesNotExist:
        state = None
    return render(request, 'pueblos/checkStatus.html', {'state': state})


def news_suggest_tags(request):
    form = GetTagForNewsText()
    suggested_tags = None
    if request.method == 'POST':
        form = GetTagForNewsText(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
            suggested_tags = recommend_tags(request, clean_data['news_body'])
            print 'suggested_tags ' + suggested_tags
    return render(request, 'pueblos/newsSuggestTags.html', {'form': form, 'suggested_tags': suggested_tags})


def recommend_tags(request, news_body, use_syn_dict=False):
    print 'recommend_tags, use dict ' + str(use_syn_dict)
    errbuf = StringIO()
    suggested_categories = StringIO()
    call_command('recommend_tags', news_body=news_body, use_syn_dict=use_syn_dict, stdout=suggested_categories,
                 stderr=errbuf)
    tags = suggested_categories.getvalue()
    if len(tags) <= 2:
        tags = 'No se encuentra una categoría adecuada'
    return tags


def news_context_view(request):
    data = {}
    if request.method == 'POST':
        form = ContextOptionsForm(request.POST)
        if form.is_valid():
            time.sleep(10)
            # request.session['cleaned_data'] = form.cleaned_data
            clean = form.cleaned_data
            data['stat'] = 'ok'
            confidence = clean['confidence'] / 100.0
            support = clean['support'] / 100.0
            if clean['limit'] > 40:
                limit = 40
            else:
                limit = clean['limit']
            test_case = PueblosTestCase(n_news=clean['n_news'], n_news_test=clean['n_news_test'], limit=limit,
                                        use_syn_dict=clean['use_syn_dict'], confidence=confidence, support=support)
            test_case.save()
            messages = ['Datos recogidos en el servidor',
                        'Numero de noticias de entrenamiento: ' + str(clean['n_news']),
                        'Número de Noticias de test: ' + str(clean['n_news_test']),
                        'Límite de palabras por categoría: ' + str(limit),
                        'Confianza ' + str(clean['confidence']), 'Soporte ' + str(clean['support']),
                        'Usar diccionario sintáctico: ' + str(clean['use_syn_dict'])]
            data['message'] = messages
            data['test_link'] = '/' + str(test_case.id) + '/checkStatus'
            return HttpResponse(json.dumps(data), content_type="application/json")
        # return set_context_options_run(request)
        else:
            data['stat'] = 'error'
            return render(request, 'pueblos/newsContextOptions.html', {'form': form})
    else:
        form = ContextOptionsForm()
        return render(request, 'pueblos/newsContextOptions.html', {'form': form})


"""
def set_context_options_run(request):
    cleaned_data = request.session.get('cleaned_data')
    if cleaned_data:
        if cleaned_data['numberOfNews'] is None:
            cleaned_data['numberOfNews'] = 10
        return render(request, 'pueblos/setContextOptionsAndRun.html', {'cleaned_data': cleaned_data})
    else:
        return redirect('pueblos:news_context')
"""


def context_options_router(request, option):
    print 'context_options_router option ' + option
    form = None
    action_url = 'pueblos/' + option + '/setIndividualContext/'
    if option == 'cleanDB':
        if request.method == 'POST':
            form = ContextOptionsForm1(request.POST)
            if form.is_valid():
                clean_data = form.cleaned_data
                return clean_db(request, clean_data['delete'], clean_data['numberOfNews'])
        else:
            form = ContextOptionsForm1()

    elif option == 'processWord':
        form = ContextOptionsForm2()
        if request.method == 'POST':
            form = ContextOptionsForm2(request.POST)
            if form.is_valid():
                clean_data = form.cleaned_data
                return process_word_list(request, clean_data['use_syn_dict'])
    elif option == 'generateContext':
        form = ContextOptionsForm3()
        if request.method == 'POST':
            form = ContextOptionsForm3(request.POST)
            if form.is_valid():
                clean_data = form.cleaned_data
                # return generate_context(request, clean_data['percentage'], clean_data['limit'])
                return generate_context(request, clean_data['limit'])
    elif option == 'getRandomNews':
        form = ContextOptionsForm4()
        if request.method == 'POST':
            form = ContextOptionsForm4(request.POST)
            if form.is_valid():
                clean_data = form.cleaned_data
                return get_random_news(request, clean_data['testNews'])
    if form:
        errors = form.errors
        print form.errors
    return render(request, 'pueblos/setIndividualContext.html', {'form': form, 'action_url': action_url})


def context_options_process(request):
    # print 'context_options_process'
    action_url = 'pueblos/processWord/setIndividualContext/'
    if request.is_ajax():
        return process_word_list(request)
    return render(request, 'pueblos/setIndividualContext.html', {'action_url': action_url})

"""
Diccionary
"""


def syntactic_dictionary(request, page='1', filter='empty'):
    MAX_ITEMS_FOR_PAGE = 50
    saved = False
    if filter == 'plural':
        dictionary_list = PueblosDiccionarioSintactico.objects.filter(word__endswith='s').order_by('word')
    else:
        dictionary_list = PueblosDiccionarioSintactico.objects.all().order_by('word')
    paginator = Paginator(dictionary_list, MAX_ITEMS_FOR_PAGE)  # Show 50 words per page
    # page = request.GET.get('page')
    if request.method == 'POST':
        """
            Delete this words
        """
        del_words = request.POST.getlist('del_words[]')
        filename = './pueblos/docs/lista_palabras_eliminar.txt'
        with open(filename, 'a') as writer:
            for word in del_words:
                word = word.lower().strip()
                PueblosNoticiasPalabras.objects.filter(palabra=word).delete()  # delete this word from the database
                PueblosDiccionarioSintactico.objects.filter(word=word).delete()
                p = PueblosPalabrasEliminar.objects.filter(palabra=word)
                if not p.exists():
                    delete_word = PueblosPalabrasEliminar(palabra=word)
                    delete_word.save()
                    word = word.encode('utf-8')
                    writer.write(word + '\n')
        """
            Set word to be replaced
        """
        try:
            words = paginator.page(page)
        except PageNotAnInteger:
            words = paginator.page(1)
        except EmptyPage:
            words = paginator.page(paginator.num_pages)
        for word in words:
            if request.POST.get(word.word, False):
                this_word = word.word.lower().strip()
                del_words = PueblosDiccionarioSintactico.objects.filter(word=this_word)
                for d_word in del_words:
                    this_word = request.POST[word.word].lower().strip()
                    d_word.replace_word = this_word
                    d_word.save()
                    saved = True
    if filter == 'plural':
        dictionary_list = PueblosDiccionarioSintactico.objects.filter(word__endswith='s').order_by('word')
    else:
        dictionary_list = PueblosDiccionarioSintactico.objects.all().order_by('word')
    paginator = Paginator(dictionary_list, MAX_ITEMS_FOR_PAGE)  # Show 50 words per page
    try:
        words = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        words = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        words = paginator.page(paginator.num_pages)
    return render(request, 'pueblos/syntacticDictionary.html', {'words': words, 'saved': saved, 'filter': filter})


def search_word(request):
    if request.method == 'POST':
        if request.POST.get('search_word', False):
            word = request.POST.get("search_word").lower().strip()
            try:
                dict_entry = PueblosDiccionarioSintactico.objects.get(word__exact=word)
                word_found = {'word': dict_entry.word, 'replace_word': dict_entry.replace_word}
                return HttpResponse(json.dumps({'stat': 'ok', 'word_found': word_found}),
                                    content_type="application/json")
            except PueblosDiccionarioSintactico.DoesNotExist:
                return HttpResponse(
                    json.dumps({'stat': 'error', 'message': word + ' no se encuentra en el diccionario'}),
                    content_type="application/json")
        # return set_context_options_run(request)
    return HttpResponse(json.dumps({'stat': 'error', 'message': 'La petición no es correcta o existe algún fallo'}),
                        content_type="application/json")


def save_word(request):
    if request.method == 'POST':
        if request.POST.get("word", False):
            word = request.POST.get("word")
            del_words = request.POST.get('delete_word')
            if del_words == 'true':
                filename = './pueblos/docs/lista_palabras_eliminar.txt'
                with open(filename, 'a') as writer:
                    PueblosNoticiasPalabras.objects.filter(palabra=word).delete()
                    PueblosDiccionarioSintactico.objects.filter(word=word).delete()
                    p = PueblosPalabrasEliminar.objects.filter(palabra=word)
                    if not p.exists():
                        delete_word = PueblosPalabrasEliminar(palabra=word)
                        delete_word.save()
                        word = word.encode('utf-8')
                        writer.write(word + '\n')
                        return HttpResponse(json.dumps({'stat': 'ok', 'message': 'Palabra eliminada'}),
                                            content_type="application/json")
                    else:
                        return HttpResponse(json.dumps({'stat': 'ok', 'message': 'Palabra ya eliminada'}),
                                            content_type="application/json")

            elif request.POST.get('replace_word', False):
                replace_word = request.POST.get("replace_word")
                if len(replace_word) >= 3:
                    dict_entry = PueblosDiccionarioSintactico.objects.get(word__iexact=word)
                    if dict_entry:
                        dict_entry.replace_word = replace_word
                        dict_entry.save()
                        return HttpResponse(json.dumps({'stat': 'ok', 'message': 'Datos guardados'}),
                                            content_type="application/json")
                else:
                    return HttpResponse(
                        json.dumps({'stat': 'error', 'message': 'La palabra tiene que ser mayor o igual a 3 caracteres'}
                                   ), content_type="application/json")
    return HttpResponse(json.dumps({'stat': 'error', 'message': 'La petición no es correcta o existe algún fallo'}),
                        content_type="application/json")

"""
End dictionary
"""


def singularize(request):
    words = PueblosDiccionarioSintactico.objects.all()
    for word in words:
        if word.replace_word == '':
            if word.word[-3:] == 'ces':
                word.replace_word = word.word[:-3] + 'z'
            # if word.word[-2:] == 'es':
            #    word.replace_word = word.word[:-2]
            if word.word[-1:] == 's':
                word.replace_word = word.word[:-1]
            word.save()
    return render(request, 'pueblos/singularize.html')


def process_word_list(request, use_syn_dict):
    print '--------------------process_word_list-----------------------'
    print use_syn_dict
    buf = StringIO()
    errbuf = StringIO()

    call_command('procesar_lista_palabras', use_syn_dict=use_syn_dict, stdout=buf, stderr=errbuf)
    return construct_response('processWord', buf, errbuf)


def clean_db(request, delete, number_of_news):
    print str(delete) + ' ' + str(number_of_news)
    buf = StringIO()
    errbuf = StringIO()
    if delete:
        if number_of_news is not None and number_of_news > 0 <= 1000:
            call_command('limpiar_bd', delete=delete, number_of_news=number_of_news, stdout=buf, stderr=errbuf)
            return construct_response('limpiar_bd', buf, errbuf)
        else:
            message = 'El número de noticias tiene que estar entre 1 y 1000'
            stat = 'error'
    else:
        call_command('limpiar_bd', stdout=buf, stderr=errbuf)
        return construct_response('limpiar_bd', buf, errbuf)
    data = {'cleanDB': 'cleanDB', 'stat': stat, 'message': message}
    return HttpResponse(json.dumps(data), content_type="application/json")


# def generate_context(request, percentage, limit):
def generate_context(request, limit):
    if limit > 0 <= 1000:  # if percentage > 0 <= 100 and limit > 0 <= 1000:
        buf = StringIO()
        errbuf = StringIO()
        # call_command('generate_context', percentage=percentage, limit=limit, stdout=buf, stderr=errbuf)
        call_command('generate_context', limit=limit, stdout=buf, stderr=errbuf)
        return construct_response('generate_context', buf, errbuf)
        # data = {'percentage': percentage, 'limit': limit, 'stat': stat, 'message': message}
    else:
        data = {'message': 'El porcentaje tiene que estar entre 1 y 100 y el límite entre 1 y 1000',
                'stat': 'error'}
    return HttpResponse(json.dumps(data), content_type="application/json")


def get_random_news(request, number_of_news):
    if number_of_news > 0 <= 1000:
        buf = StringIO()
        errbuf = StringIO()

        call_command('get_random_news_with_categories_db', number_of_news=number_of_news, stdout=buf, stderr=errbuf)
        return construct_response('get_random_news_with_categories_db', buf, errbuf)
    else:
        data = {'message': 'El número de noticias tiene que estar entre 1 y 1000', 'stat': 'error'}
        return HttpResponse(json.dumps(data), content_type="application/json")


def construct_response(command, buf, errbuf):
    if errbuf.len > 0:
        errbuf.seek(0)
        print errbuf.read()
        errbuf.seek(0)
        message = errbuf.read()
        stat = 'error'
    else:
        buf.seek(0)
        print 'Valor devuelto ' + buf.read()
        buf.seek(0)
        message = buf.read()
        stat = 'ok'
    data = {command: command, 'stat': stat, 'message': message}
    return HttpResponse(json.dumps(data), content_type="application/json")
