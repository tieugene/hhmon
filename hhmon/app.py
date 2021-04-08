#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tool to monitor job in hh.ru
(c) TI_Eugene, 2019-2021

Dups:
https://spb.hh.ru/vacancy/34597232
https://spb.hh.ru/vacancy/34461767
"""
# 1. imports
# 1.1. std
import os
# 1.2. 3rd
import addict
from flask import Flask, request, render_template, redirect, url_for
import requests
from urllib.parse import urljoin
# 1.3. local
from . import hh


# 3. consts
DEBUG = True
BASE_URL = 'https://api.hh.ru'  # api.hh.ru hh.ru spb.hh.ru
RS_VACS = 'vacancies'
RS_VAC = 'vacancy'
AGENT = {'user-agent': 'wannajob/0.0.1 (wannajob@mail.ru)'}

# 4. vars
query_filter = addict.Dict({    # TODO: store in coockie
    'per_page': 20,         # 20 default; 100 max; ? items_on_page ?
    'search_period': 1,     # days B4; 30 max
    'area': 2,
    'employment': None,
    'schedule': None,
    'specialization': None,
    # 'clusters': 'false',	# F default
    'no_magic': 'true',     # F default
    'enable_snippets': 'true',
})
settings = addict.Dict({
    'per_page': 20,
    'search_period': 3,
    'area': 2,
    'employment': None,
    'schedule': None,
    'specialization': None,
    'no_magic': 'true',     # F default
    'enable_snippets': 'true',
})

# 5. flask entry point
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder=os.path.join(BASE_DIR, 'templates'))
app.config['SECRET_KEY'] = 'you-will-never-guess'


# 6. utils
def get_any(resource, any_id=None, payload=None):
    """
    Get data from hh.ru
    @return
    On error: r.status_code, r.json()['description']
    TODO: filter/payload (dict)
    """
    url = urljoin(BASE_URL, resource if not any_id else resource + '/' + any_id)  # '/'.join((resource, id))
    rsp = requests.get(url, headers=AGENT, params=payload)
    print(rsp.request.url)
    return rsp


# 7. views
@app.route('/', methods=['GET'])
def index():
    print(query_filter.per_page)
    return render_template('index.html')


@app.route('/list', methods=['GET'])
def vac_list():
    """
    Args:
    args:ImmutableMultiDict (!)
    Vacancy list
    Returns last month only
    Filters - by request params
    TODO: set params if exists only (or key=None)
    TODO: multiple key values (key=[v1, v2])
    TODO: catch Etag
    """
    payload = dict()
    payload['per_page'] = 5
    payload['page'] = request.args.get('page', 0, type=int)
    # fill_dict(payload, 'page')
    # print('Args:', request.args)
    settings.page = request.args.get('page', 0, type=int)
    vacs = get_any(RS_VACS, payload=settings)  # payload/filter
    if vacs.status_code != requests.codes.ok:  # 200
        # TODO: flush
        print('Err:', vacs.status_code)
        print(vacs.json()['description'])
    return render_template('list.html', title="Vacancies", data=vacs.json())


@app.route('/filter', methods=['GET', 'POST'])
def vac_filter():
    """
    Set list filter
    request.form: ImmutableMultiDict
    """
    if request.method == 'POST':
        settings.per_page = request.form.get('perpage')
        settings.search_period = request.form.get('period')
        settings.area = 2 if request.form.get('area') else None
        settings.employment = request.form.getlist('empl')
        settings.schedule = request.form.getlist('sched')
        settings.specialization = request.form.getlist('spec')
        return redirect(url_for('index'))
    else:
        form = hh.FilterForm(
            perpage=settings.per_page,
            period=settings.search_period,
            area=settings.area == 2,
            empl=settings.employment,
            sched=settings.schedule,
            spec=settings.specialization,
        )
        form.update_choices()
    return render_template('filter.html', title='Filter', form=form)


@app.route('/view/<int:vac_id>', methods=['GET'])
def vac_view(vac_id):
    return render_template('view.html', title='View')


# X. go
if __name__ == '__main__':
    app.run(debug=DEBUG)
