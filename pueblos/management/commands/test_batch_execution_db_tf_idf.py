#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from django.core.management import call_command
from django.core.management.base import BaseCommand
from StringIO import StringIO
import time


class Command(BaseCommand):
    help = 'Prueba la matriz de confusion'

    def handle(self, *args, **options):
        filesdir = 'files_batch/'
        dump = 'dumpdatabase'

        # -------------------------  50 noticias  - limite 5  ---------------------------------
        """
        start = time.time()
        dirname = 'test50-5'
        self.create_dir(filesdir, dirname)
        store_folder = filesdir + dirname + '/'
        self.create_dir(store_folder, dump)
        dump_dir = store_folder + dump + '/'
        # self.run_test(n_news_training, n_news_test, percentage, limit, store_folder, dump_folder)
        self.stdout.write('Test parameters 50 news training, 200 news test, 30%, limit 5, store folder ' +
                          store_folder + ' dump dir ' + dump_dir)
        self.run_test(50, 200, 30, 5, store_folder, dump_dir)
        end = time.time()
        with open(store_folder + 'time.txt', 'w') as f:
            f.write(str(end - start) + ' seconds')

        # -------------------------  50 noticias  - limite 10  ---------------------------------
        start = time.time()
        dirname = 'test50-10'
        self.create_dir(filesdir, dirname)
        store_folder = filesdir + dirname + '/'
        self.create_dir(store_folder, dump)
        dump_dir = store_folder + dump + '/'

        self.stdout.write('Test parameters 50 news training, 200 news test, 30%, limit 10, store folder ' +
                          store_folder + ' dump dir ' + dump_dir)
        self.run_test(50, 200, 30, 10, store_folder, dump_dir)
        end = time.time()
        with open(store_folder + 'time.txt', 'w') as f:
            f.write(str(end - start) + ' seconds')
        # -------------------------  50 noticias  - limite 20  ---------------------------------
        start = time.time()
        dirname = 'test50-20'
        self.create_dir(filesdir, dirname)
        store_folder = filesdir + dirname + '/'
        self.create_dir(store_folder, dump)
        dump_dir = store_folder + dump + '/'

        self.stdout.write('Test parameters 50 news training, 200 news test, 30%, limit 20, store folder ' +
                          store_folder + ' dump dir ' + dump_dir)
        self.run_test(50, 200, 30, 20, store_folder, dump_dir)
        end = time.time()
        with open(store_folder + 'time.txt', 'w') as f:
            f.write(str(end - start) + ' seconds')
        """
        """
        # -------------------------  200 noticias  - limite 5  ---------------------------------
        start = time.time()
        dirname = 'test200-5'
        self.create_dir(filesdir, dirname)
        store_folder = filesdir + dirname + '/'
        self.create_dir(store_folder, dump)
        dump_dir = store_folder + dump + '/'

        self.stdout.write('Test parameters 200 news training, 200 news test, 30%, limit 5, store folder ' +
                          store_folder + ' dump dir ' + dump_dir)
        self.run_test(200, 200, 30, 5, store_folder, dump_dir)
        end = time.time()
        with open(store_folder + 'time.txt', 'w') as f:
            f.write(str(end - start) + ' seconds')
        """
        """
        # -------------------------   noticias 200 - limite 10  ---------------------------------
        start = time.time()
        dirname = 'test200-10'
        self.create_dir(filesdir, dirname)
        store_folder = filesdir + dirname + '/'
        self.create_dir(store_folder, dump)
        dump_dir = store_folder + dump + '/'

        self.stdout.write('Test parameters 200 news training, 200 news test, 30%, limit 10, store folder ' +
                          store_folder + ' dump dir ' + dump_dir)
        self.run_test(200, 200, 30, 10, store_folder, dump_dir)
        end = time.time()
        with open(store_folder + 'time.txt', 'w') as f:
            f.write(str(end - start) + ' seconds')

        """"""
        # -------------------------  200 noticias  - limite 20  ---------------------------------
        start = time.time()
        dirname = 'test200-20'
        self.create_dir(filesdir, dirname)
        store_folder = filesdir + dirname + '/'
        self.create_dir(store_folder, dump)
        dump_dir = store_folder + dump + '/'

        self.stdout.write('Test parameters 200 news training, 200 news test, 30%, limit 20, store folder ' +
                          store_folder + ' dump dir ' + dump_dir)
        self.run_test(200, 200, 30, 20, store_folder, dump_dir)
        end = time.time()
        with open(store_folder + 'time.txt', 'w') as f:
            f.write(str(end - start) + ' seconds')
        """"""
        # -------------------------   noticias 400 - limite 5  ---------------------------------
        start = time.time()
        dirname = 'test400-5'
        self.create_dir(filesdir, dirname)
        store_folder = filesdir + dirname + '/'
        self.create_dir(store_folder, dump)
        dump_dir = store_folder + dump + '/'

        self.stdout.write('Test parameters 400 news training, 200 news test, 30%, limit 5, store folder ' +
                          store_folder + ' dump dir ' + dump_dir)
        self.run_test(400, 200, 30, 5, store_folder, dump_dir)
        end = time.time()
        with open(store_folder + 'time.txt', 'w') as f:
            f.write(str(end - start) + ' seconds')
        """
        # -------------------------   noticias 400 - limite 10  ---------------------------------
        start = time.time()
        dirname = 'test400-10'
        self.create_dir(filesdir, dirname)
        store_folder = filesdir + dirname + '/'
        self.create_dir(store_folder, dump)
        dump_dir = store_folder + dump + '/'

        self.stdout.write('Test parameters 400 news training, 200 news test, 30%, limit 10, store folder ' +
                          store_folder + ' dump dir ' + dump_dir)
        self.run_test(400, 200, 30, 10, store_folder, dump_dir)
        end = time.time()
        with open(store_folder + 'time.txt', 'w') as f:
            f.write(str(end - start) + ' seconds')
        """
        # -------------------------   noticias 400 - limite 20  ---------------------------------
        start = time.time()
        dirname = 'test400-20'
        self.create_dir(filesdir, dirname)
        store_folder = filesdir + dirname + '/'
        self.create_dir(store_folder, dump)
        dump_dir = store_folder + dump + '/'

        self.stdout.write('Test parameters 400 news training, 200 news test, 30%, limit 20, store folder ' +
                          store_folder + ' dump dir ' + dump_dir)
        self.run_test(400, 200, 30, 20, store_folder, dump_dir)
        end = time.time()
        with open(store_folder + 'time.txt', 'w') as f:
            f.write(str(end - start) + ' seconds')
        """"""
        # -------------------------   noticias 1000 - limite 5  ---------------------------------
        start = time.time()
        dirname = 'test1000-5'
        self.create_dir(filesdir, dirname)
        store_folder = filesdir + dirname + '/'
        self.create_dir(store_folder, dump)
        dump_dir = store_folder + dump + '/'

        self.stdout.write('Test parameters 1000 news training, 200 news test, 30%, limit 5, store folder ' +
                          store_folder + ' dump dir ' + dump_dir)
        self.run_test(1000, 200, 30, 5, store_folder, dump_dir)
        end = time.time()
        with open(store_folder + 'time.txt', 'w') as f:
            f.write(str(end - start) + ' seconds')

        # -------------------------   noticias 1000 - limite 10  ---------------------------------
        start = time.time()
        dirname = 'test1000-10'
        self.create_dir(filesdir, dirname)
        store_folder = filesdir + dirname + '/'
        self.create_dir(store_folder, dump)
        dump_dir = store_folder + dump + '/'

        self.stdout.write('Test parameters 1000 news training, 200 news test, 30%, limit 10, store folder ' +
                          store_folder + ' dump dir ' + dump_dir)
        self.run_test(1000, 200, 30, 10, store_folder, dump_dir)
        end = time.time()
        with open(store_folder + 'time.txt', 'w') as f:
            f.write(str(end - start) + ' seconds')

        # -------------------------   noticias 3000 - limite 10  ---------------------------------
        start = time.time()
        dirname = 'test3000-10'
        self.create_dir(filesdir, dirname)
        store_folder = filesdir + dirname + '/'
        self.create_dir(store_folder, dump)
        dump_dir = store_folder + dump + '/'

        self.stdout.write('Test parameters 3000 news training, 200 news test, 30%, limit 10, store folder ' +
                          store_folder + ' dump dir ' + dump_dir)
        self.run_test(3000, 200, 30, 10, store_folder, dump_dir)
        end = time.time()
        with open(store_folder + 'time.txt', 'w') as f:
            f.write(str(end - start) + ' seconds')
        # ---------------------------------------------------------------
        """
        return self.stdout.write('Finished')

    @staticmethod
    def check_ok(command_name, buf):
        buf.seek(0)
        print command_name + ' returned value ' + buf.read()
        buf.seek(0)
        message = buf.read()
        return 'Finished' in message

    @staticmethod
    def create_dir(filesdir, dirname):
        new_dir = filesdir + dirname
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)

    def run_test(self, n_news_training, n_news_test, percentage, limit, store_files, dump_dir):
        if not store_files[-1:] == '/':
            store_files += '/'
        if not dump_dir[-1:] == '/':
            dump_dir += '/'
        """
        buf = StringIO()
        errbuf = StringIO()
        call_command('limpiar_bd', delete=True, number_of_news=n_news_training, stdout=buf, stderr=errbuf)
        if not self.check_ok('limpiar_bd', buf):
            return self.stderr.write('Problems with limpiar_bd command')
        """
        buf = StringIO()
        errbuf = StringIO()
        call_command('procesar_lista_palabras', stdout=buf, stderr=errbuf)
        if not self.check_ok('procesar_lista_palabras', buf):
            return self.stderr.write('Problems with procesar_lista_palabras command')

        buf = StringIO()
        errbuf = StringIO()
        context_file = store_files + 'context'
        call_command('generate_context_tf_idf', percentage=percentage, limit=limit, output=context_file, stdout=buf,
                     stderr=errbuf)
        if not self.check_ok('generate_context', buf):
            return self.stderr.write('Problems with generate_context command')

        buf = StringIO()
        errbuf = StringIO()
        context_file += '-' + str(n_news_training) + '-' + str(limit) + '.csv'
        rules_file = store_files + 'rules.txt'
        call_command('generate_store_rules', ctx=context_file, output=rules_file, stdout=buf, stderr=errbuf)
        if not self.check_ok('generate_store_rules', buf):
            return self.stderr.write('Problems with generate_store_rules command')
        """
        buf = StringIO()
        errbuf = StringIO()
        call_command('get_random_news_with_categories_db', number_of_news=n_news_test,
                     stdout=buf, stderr=errbuf)
        if not self.check_ok('get_random_news_with_categories', buf):
            return self.stderr.write('Problems with get_random_news_with_categories command')
        """
        buf = StringIO()
        errbuf = StringIO()
        matrix_file = store_files + 'matrix' + '-' + str(n_news_training) + '-' + str(limit) + '.csv'
        # filename = store_files + 'matrix_track.txt'
        call_command('context_set_matrix_db_set', output_file=matrix_file, stdout=buf,
                     stderr=errbuf)
        if not self.check_ok('context_set_matrix', buf):
            return self.stderr.write('Problems with context_set_matrix command')

        buf = StringIO()
        errbuf = StringIO()
        news_file = store_files + 'news_test' + '-' + str(n_news_training) + '-' + str(limit) + '.txt'
        call_command('get_random_test_news', output_file=news_file, number_of_news=10, stdout=buf,
                     stderr=errbuf)
        if not self.check_ok('get_random_test_news', buf):
            return self.stderr.write('Problems with get_random_test_news command')

        buf = StringIO()
        errbuf = StringIO()
        call_command('dump_test_pueblos_db', output_dir=dump_dir, stdout=buf, stderr=errbuf)
        if not self.check_ok('dump_test_pueblos', buf):
            return self.stderr.write('Problems with dump_test_pueblos command')
