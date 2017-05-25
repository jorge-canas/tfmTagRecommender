#!/usr/bin/python
# -*- coding: utf-8 -*-
from collections import defaultdict, OrderedDict

import numpy
from pandas import *

STORED_CATEGORY_MATRIX_LABEL = 'zz_missing_stored_category'
SUGGESTED_CATEGORY_MATRIX_LABEL = 'zz_missing_suggested_category'


class ConfusionMatrix(object):
    """Class to hold the confusion matrix and get results"""
    matrix = defaultdict(dict)

    def __init__(self, labels):
        for stored_category in labels:
            for suggested_category in labels:
                self.matrix[stored_category][suggested_category] = 0
            self.matrix[stored_category][STORED_CATEGORY_MATRIX_LABEL] = 0
            self.matrix[SUGGESTED_CATEGORY_MATRIX_LABEL][stored_category] = 0

    def __unicode__(self):
        df = DataFrame(self.matrix).T.fillna(0)
        return df.__str__()

    def __str__(self):
        return unicode(self).encode('utf-8')

    def save_confusion_matrix(self, filename):
        df = DataFrame(self.matrix).T.fillna(0)
        try:
            with open(filename, 'w') as f:
                df.to_csv(f, sep=';', encoding='utf-8')
                return 'Saved'
        except IOError:
            return 'Error'

    def set_values(self, previous_categories, suggested_categories):
        # print 'Previous ' + str(previous_categories)
        # print 'Suggested ' + str(suggested_categories)
        common = []
        for pc in previous_categories:
            if pc in suggested_categories:
                """If there is a common value, it's removed from both lists"""
                index_prev = previous_categories.index(pc)
                common.append(previous_categories.pop(index_prev))
                suggested_categories.remove(pc)
        for cat in common:
            self.set_value(cat, cat)
        # Case 1 suggested empty, previous > 0
        if not suggested_categories:
            # print 'Missing stored category'
            for pc in previous_categories:
                # print pc
                self.set_value(pc, STORED_CATEGORY_MATRIX_LABEL)
        # Case 2 suggested > 0, previous empty
        elif not previous_categories:
            # print 'Missing previous category'
            for sc in suggested_categories:
                # print sc
                self.set_value(SUGGESTED_CATEGORY_MATRIX_LABEL, sc)
        else:
            for pc in previous_categories:
                for sc in suggested_categories:
                    self.set_value(pc, sc)

    def set_value(self, previous_category, suggested_category):
        """Set the value to the correct match in the confusion matrix. Probably it will need some dictionary checks"""
        # print 'Set value ' + previous_category + ' ' + suggested_category
        # print '----------------------------'
        self.matrix[previous_category][suggested_category] += 1

    def get_recall(self):
        """Calculates the true positive rate/recall/hit rate - Calcula la traza"""
        recall = 0.0
        for label in self.matrix[SUGGESTED_CATEGORY_MATRIX_LABEL].keys():
            recall += self.matrix[label][label]
        return recall

    def get_errors(self):
        """Calculates the errors - Calcula los errores"""
        return self.get_total() - self.get_recall()

    def get_total(self):
        """Calculates the sumatory of all matrix - Calcula la sumatoria de la matriz"""
        total = 0.0
        for stored, suggested in self.matrix.items():
            for suggest, value in suggested.items():
                total += value
        return total

    def get_results(self):
        """Generates a string with the Confusion Matrix results"""
        output = 'Results\n'
        output += 'total ' + str(self.get_total()) + '\n'
        output += 'Recall ' + str(self.get_recall()) + ' - ' + str(self.get_recall() / self.get_total() * 100.0) + '%\n'
        output += 'Errors ' + str(self.get_errors()) + ' - ' + str(self.get_errors() / self.get_total() * 100.0) + '%\n'
        return output
