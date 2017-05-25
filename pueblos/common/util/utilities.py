#!/usr/bin/python
# -*- coding: utf-8 -*-
from distance import levenshtein
import re
import os
from django.db import connection


def clean_text(x):
    x = x.strip()
    # palabras con tamanio menor o igual a 3 no suelen representar buenas etiquetas
    if len(x) <= 3 or len(x) >= 30:  # Para evitar palabras que son url a ficheros
        return True
    """
    if x[0].isupper() and not x[1].isupper():
        return True
    """
    return False


def get_news_without_category(any_category=False):
    with connection.cursor() as cursor:
        if any_category:
            query = """
                        SELECT DISTINCT nc.noticia_id
                        FROM pueblos_nc nc
                        LEFT JOIN pueblos_noticia_categorizada noticia_cat
                            ON nc.noticia_id = noticia_cat.noticia_id
                        WHERE noticia_cat.noticia_id IS NULL
                        ORDER BY RAND()
                        LIMIT 1
                        """
        else:
            query = """
                SELECT DISTINCT nc.noticia_id
                FROM pueblos_nc nc
                LEFT JOIN pueblos_noticia_categorizada noticia_cat
                    ON nc.noticia_id = noticia_cat.noticia_id
                WHERE noticia_cat.noticia_id IS NULL AND nc.categoria_id = 53
                ORDER BY RAND()
                LIMIT 1
                """

        cursor.execute(query)
        row = cursor.fetchone()
        return row[0]


def check_ok(command_name, buf):
    buf.seek(0)
    print command_name + ' returned value ' + buf.read()
    buf.seek(0)
    message = buf.read()
    return 'Finished' in message


def create_dir(filesdir, dirname):
    new_dir = filesdir + dirname
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)


def get_list_words(text):
    words = re.sub(ur'[^a-zA-ZÁÉÍÓÚÜáéíóúüñÑ]', ' ', text)
    words = clean_accents(words)
    words = re.sub(ur'[ ]+', ' ', words)
    words = words.lower()
    words = words.split(' ')
    words[:] = [x.strip() for x in words if not clean_text(x)]
    words.sort()
    return words


def save_file(filename, mode, output):
    with open(filename, mode) as f:
        f.write(output.encode('utf-8'))


def esta(word, dictionary):
    for key, palabra in dictionary.items():
        # si la distancia de la palabra con respecto a las almacenadas es > 3 no se guarda
        # if the distance between the word and the stored ones is bigger than 3 the word is not saved
        if levenshtein(word, palabra) <= 3:
            # print word + ' repetida ' + palabra
            return True
    return False


def clean_accents(word):
    word = re.sub(ur'[áàäâ]', 'a', word)
    word = re.sub(ur'[ÁÀÄÂ]', 'A', word)

    word = re.sub(ur'[éèëê]', 'e', word)
    word = re.sub(ur'[ÉÈËÊ]', 'E', word)

    word = re.sub(ur'[íìïî]', 'i', word)
    word = re.sub(ur'[ÍÌÏÎ]', 'I', word)

    word = re.sub(ur'[óòöô]', 'o', word)
    word = re.sub(ur'[ÓÒÖÔ]', 'O', word)

    word = re.sub(ur'[úùüû]', 'u', word)
    word = re.sub(ur'[ÚÙÜÛ]', 'U', word)

    return word
