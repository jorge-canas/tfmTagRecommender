#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.core.management import call_command
from django.core.management.base import BaseCommand
from StringIO import StringIO
import time
from django.db import connection
from pueblos.common.util.utilities import check_ok, create_dir


class Command(BaseCommand):
    help = 'Crea una prueba de test con los parámetros almacenados en la base de datos'

    def add_arguments(self, parser):
        parser.add_argument('n_news', nargs='?', type=int, default=1, help='Numero de noticias de entrenamiento')
        parser.add_argument('n_news_test', nargs='?', type=int, default=1, help='Numero de noticias de test')
        parser.add_argument('limit', type=int, nargs='?', default=5, help='limite de palabras por categoria')
        parser.add_argument('confidence', nargs='?', type=float, default=0.8,
                            help='Confianza para que se cumpla una regla, valor entre 0 y 1, indica el porcentaje')
        parser.add_argument('support', nargs='?', type=float, default=0.5,
                            help='Soporte para que se cumpla una regla, valor entre 0 y 1, indica el porcentaje')
        parser.add_argument('--use_syn_dict', action='store_true', dest='use_syn_dict', default=False,
                            help='Usar el diccionario sintactico para sustituir algunas palabras incorrectas')
        parser.add_argument('--path', dest='path', type=str, nargs='?', default='',
                            help='Ruta donde almacenar las pruebas')
        parser.add_argument('--output', dest='output', type=str, nargs='?', default='',
                            help='Directorio de salida')

    def handle(self, *args, **options):
        path_dir = 'test_cases/'
        if options['path']:
            path_dir = options['path']
            if not path_dir[-1:] == '/':
                path_dir += '/'

        output_dir = 'test' + str(time.strftime('%d%m%Y'))
        if options['output']:
            output_dir = options['output']
            if output_dir[-1:] == '/':
                output_dir = output_dir[:-1]
        dump = 'dumpdatabase'

        n_news = options['n_news']
        n_news_test = options['n_news_test']
        limit = options['limit']
        confidence = options['confidence']
        support = options['support']
        use_dict = options['use_syn_dict']

        start = time.time()
        create_dir(path_dir, output_dir)
        store_folder = path_dir + output_dir + '/'
        create_dir(store_folder, dump)
        dump_dir = store_folder + dump + '/'
        test_info = 'Test parameters: ' + str(n_news) + ' news training, ' + str(n_news_test) + \
                    ' news test, limit ' + str(limit) + ', confidence ' + str(confidence) + ', support ' +\
                    str(support) + ', store folder ' + store_folder + ' dump dir ' + dump_dir
        with open(store_folder + 'test info.txt', 'w') as f:
            f.write(test_info)
        self.stdout.write(test_info)
        self.run_test(n_news, n_news_test, limit, confidence, support, use_dict, store_folder, dump_dir)
        end = time.time()
        with open(store_folder + 'time.txt', 'w') as f:
            f.write(str(end - start) + ' seconds')
        return self.stdout.write('Finished')
        # return self.stdout.write('Finished')

    def run_test(self, n_news_training, n_news_test, limit, confidence, support, syn_dict, store_files, dump_dir):
        context_file = store_files + 'context'

        buf = StringIO()
        errbuf = StringIO()
        call_command('limpiar_bd', delete=True, number_of_news=n_news_training, stdout=buf, stderr=errbuf)
        if not check_ok('limpiar_bd', buf):
            return self.stderr.write('Problems with limpiar_bd command')

        buf = StringIO()
        errbuf = StringIO()
        call_command('procesar_lista_palabras', use_syn_dict=syn_dict, stdout=buf, stderr=errbuf)
        if not check_ok('procesar_lista_palabras', buf):
            return self.stderr.write('Problems with procesar_lista_palabras command')

        buf = StringIO()
        errbuf = StringIO()
        call_command('generate_context', limit=limit, output=context_file, stdout=buf, stderr=errbuf)
        if not check_ok('generate_context', buf):
            return self.stderr.write('Problems with generate_context command')

        buf = StringIO()
        errbuf = StringIO()
        context_file += '-' + str(n_news_training) + '-' + str(limit) + '.csv'
        rules_file = store_files + 'rules.txt'
        call_command('generate_store_rules', ctx=context_file, output=rules_file, stdout=buf, stderr=errbuf)
        if not check_ok('generate_store_rules', buf):
            return self.stderr.write('Problems with generate_store_rules command')

        connection.close()  # to avoid django.db.utils.OperationalError: (2006, 'MySQL server has gone away')

        buf = StringIO()
        errbuf = StringIO()
        call_command('get_random_news_with_categories_db', number_of_news=n_news_test,
                     stdout=buf, stderr=errbuf)
        if not check_ok('get_random_news_with_categories', buf):
            return self.stderr.write('Problems with get_random_news_with_categories command')

        buf = StringIO()
        errbuf = StringIO()
        matrix_file = store_files + 'matrix' + '-' + str(n_news_training) + '-' + str(limit) + '.csv'
        # filename = store_files + 'matrix_track.txt'
        call_command('context_set_matrix_tc', min_confidence=confidence, min_support=support,
                     use_syn_dict=syn_dict, output_file=matrix_file, stdout=buf,
                     stderr=errbuf)
        if not check_ok('context_set_matrix', buf):
            return self.stderr.write('Problems with context_set_matrix command')

        buf = StringIO()
        errbuf = StringIO()
        call_command('dump_test_pueblos_db', output_dir=dump_dir, stdout=buf, stderr=errbuf)
        if not check_ok('dump_test_pueblos', buf):
            return self.stderr.write('Problems with dump_test_pueblos command')
