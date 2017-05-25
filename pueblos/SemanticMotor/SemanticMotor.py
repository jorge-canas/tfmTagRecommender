#!/usr/bin/python
# -*- coding: utf-8 -*-

from pueblos.models import PueblosRule, PueblosConclusion, PueblosPremise


class Rule(object):
    """Rule structure to use in the Semantic Motor"""
    support = 0
    confidence = 0.0

    def __init__(self, support=0, confidence=0, premise=[], conclusion=[]):
        self.support = support
        self.confidence = confidence
        self.premise = premise
        self.conclusion = conclusion

    def __unicode__(self):
        premise = ''
        conclusion = ''
        for p in self.premise:
            premise += p + ','
        for c in self.conclusion:
            conclusion += c + ','
        text = '< ' + str(self.support) + ' > ' + premise[:-1] + ' -- ' + '{0:.2f}'.format(self.confidence * 100.0) + \
               '% --> ' + conclusion[:-1]
        return text

    def __str__(self):
        return unicode(self).encode('utf-8')

    def str_csv(self):
        premise = ''
        conclusion = ''
        for p in self.premise:
            premise = premise + p + ','
        for c in self.conclusion:
            conclusion = conclusion + c + ','
        text = str(self.support) + ';' + premise[:-1] + ';' + '{0:.2f}'.format(self.confidence) + '%;' + conclusion[:-1]
        return text

    def get_support(self):
        return self.support

    def get_confidence(self):
        return self.confidence

    def get_premise(self):
        return self.premise

    def get_conclusion(self):
        return self.conclusion


class CategoryResult(object):
    category = ''
    rule = Rule()

    def __init__(self, category, rule):
        self.category = category
        self.rule = rule

    def __unicode__(self):
        text = 'Category ' + self.category + ' Rule ' + self.rule.__unicode__()
        return text

    def __str__(self):
        return unicode(self).encode('utf-8')


class SemanticMotor(object):
    """Semantic motor which contains the rules and the logic of the category suggestion"""

    def __unicode__(self):
        output = ''
        for rule in self.rules:
            output += rule.__unicode__() + '\n'
        return output

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __init__(self):
        self.rules = []
        rules = PueblosRule.objects.all()
        for rule in rules:
            premise = []
            conclusion = []
            p_premises = PueblosPremise.objects.filter(r_id=rule.r_id)
            for p_premise in p_premises:
                premise.append(p_premise.p_word)
            p_conclusions = PueblosConclusion.objects.filter(r_id=rule.r_id)
            for p_conclusion in p_conclusions:
                conclusion.append(p_conclusion.c_word)
            r = Rule(rule.support, rule.confidence, premise, conclusion)
            self.rules.append(r)
        # Sorting rules by confidence, descending order
        self.rules.sort(key=lambda x: x.get_confidence(), reverse=True)

        """
        for rule in self.rules[:100]:
            print rule
            for premise in rule.premise:
                print premise
            for conclusion in rule.conclusion:
                print conclusion
        """

    def get_rules(self):
        return self.rules

    @staticmethod
    def satisfy_motor_rule(attributes, rule):
        conclusion = []
        premise = rule.get_premise()
        for s in rule.get_conclusion():  # Set the conclusion words which may be in the attributes
            if 'ETIQUETA_' not in s:
                conclusion.append(s)
        """
        if set(premise) <= set(attributes):
            print "Premise " + str(premise) + " Atributes " + str(attributes)

        if set(conclusion) <= set(attributes):
            print "Conclusion " + str(conclusion) + " Atributes " + str(attributes)
        """
        return set(premise) <= set(attributes) and set(conclusion) <= set(attributes)

    def save_semantic_motor(self, filename):
        with open(filename, 'w') as f:
            output = self.__unicode__()
            f.write(output.encode('utf-8'))
            return 'Saved'

    def get_conclusion_names(self, facts):
        result = []
        for rule in self.rules:
            if self.satisfy_motor_rule(facts, rule):
                for word in rule.get_conclusion():
                    if 'ETIQUETA_' in word:
                        result.append(CategoryResult(word, rule))

        return result

    @staticmethod
    def check_correct(stored_categories, suggested_categories):
        return set(stored_categories) <= set(suggested_categories)
