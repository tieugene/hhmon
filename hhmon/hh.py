# -*- coding: utf-8 -*-
"""
Spec:
- if all - main only
"""

import json
import os.path

from flask_wtf import FlaskForm
from wtforms import BooleanField, SelectField, SelectMultipleField
from wtforms.widgets.core import html_params

# from hh_data import list_empl, list_sched

list_perpage = ((20, 20), (50, 50), (100, 100))
list_period = ((1, 1), (3, 3), (7, 7), (30, 30))
list_empl = None
list_sched = None
list_spec = None
DATA_DIR = 'json'


def _load_jsons():
    global list_empl, list_sched, list_spec
    if (not list_empl) or (not list_empl):
        print("Loading dicts...")
        json_data = json.load(open(os.path.join(DATA_DIR, 'dictionaries.json')))
        list_empl = list(map(lambda x: (x['id'], x['name']), json_data['employment']))
        list_sched = list(map(lambda x: (x['id'], x['name']), json_data['schedule']))
    if not list_spec:
        print("Loading specs...")
        json_data = json.load(open(os.path.join(DATA_DIR, 'specializations.json')))
        list_spec = list()
        for i in json_data:
            list_spec.append((i['id'], i['name']))
            list_spec.extend(list(map(lambda j: (j['id'], j['name']), i['specializations'])))


def _multi_checkbox(field, ul_class: str = '', **kwargs):
    kwargs.setdefault('type', 'checkbox')
    field_id = kwargs.pop('id', field.id)
    html = [u'<ul %s>' % html_params(id=field_id, class_=ul_class)]
    for value, label, checked in field.iter_choices():
        choice_id = u'%s-%s' % (field_id, value)
        options = dict(kwargs, name=field.name, value=value, id=choice_id)
        if checked:
            options['checked'] = 'checked'
        html.append(u'<li><input %s/> ' % html_params(**options))
        html.append(u'<label for="%s">%s</label></li>' % (choice_id, label))  # was field_id
    html.append(u'</ul>')
    return u''.join(html)


def _nested_checkbox(field, ul_class: str = '', **kwargs):
    prev = True  # 1st level
    empty = True
    kwargs.setdefault('type', 'checkbox')
    field_id = kwargs.pop('id', field.id)
    html = [u'\n<ul %s>' % html_params(id=field_id, class_=ul_class)]
    parent = None
    for value, label, checked in field.iter_choices():
        empty = False
        top = ('.' not in value)
        if top and (not prev):
            html.append(u'</ul> </details> </li>')
        choice_id = u'%s-%s' % (field_id, value)
        options = dict(kwargs, name=field.name, value=value, id=choice_id)
        if checked:
            options['checked'] = 'checked'
        if top:
            parent = choice_id
            html.append(u'\n<li> <details> <summary> <input %s/> ' % html_params(**options))
            html.append(u'<label for="%s">%s</label> </summary> <ul name="%s">' % (choice_id, label, choice_id))
        else:
            options['parent'] = parent
            html.append(u'\n\t<li> <input %s/> ' % html_params(**options))
            html.append(u'<label for="%s">%s</label> </li>' % (choice_id, label))
        prev = top
    if not empty:
        html.append(u'\n</ul> </details> </li>')
    html.append(u'\n</ul>')
    return u''.join(html)


class FilterForm(FlaskForm):
    """docstring for FilterForm"""
    like = BooleanField("Like a virgin: ")
    hide = BooleanField("Hide excluded vacs: ")
    sortby = SelectField("Sort by: ", choices=((1, 'так'), (2, 'сяк')))
    perpage = SelectField("Строк: ", choices=list_perpage, coerce=int)
    period = SelectField("Дней", choices=list_period, coerce=int)
    area = BooleanField("СПб: ")
    empl = SelectMultipleField("Занятость: ", widget=_multi_checkbox,
                               render_kw={'class': 'myclass', 'ul_class': 'ulclass'})
    sched = SelectMultipleField("График: ", widget=_multi_checkbox, render_kw={'ul_class': 'ulclass'})
    spec = SelectMultipleField("Специализация: ", widget=_nested_checkbox, render_kw={
        'ul_class': 'ulclass'})  # 2-level checkbox list; inputInstance.indeterminate = true;

    # widget = widgets.TableWidget()

    def update_choices(self):
        _load_jsons()
        self.empl.choices = list_empl
        self.sched.choices = list_sched
        self.spec.choices = list_spec
    # pprint(list_spec)
