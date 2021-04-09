#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tool to monitor job in hh.ru
(c) TI_Eugene, 2019-2021
"""
# 1. imports
# 1.1. std
import configparser
import datetime
import json
import os
# 1.2. 3rd
import sys

import addict
from flask import Flask, request, render_template, redirect, session, url_for
import requests
from urllib.parse import urljoin
# 1.3. local
from . import hh

# 3. consts
# flask
DEBUG = True
# local
CFG_FILE_NAME = "~/.hhmon.ini"
CFG_MAIN_SECT = "DEFAULT"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TPL_DIR = os.path.join(BASE_DIR, 'templates')
# hh.ru
BASE_URL = 'https://api.hh.ru'  # api.hh.ru hh.ru spb.hh.ru
RS_VACS = 'vacancies'
RS_VAC = 'vacancy'
AGENT = {'user-agent': 'wannajob/0.0.1 (wannajob@mail.ru)'}
default_filter = addict.Dict({
    'per_page': 20,
    'search_period': 3,
    'area': 2,
    'employment': None,
    'schedule': None,
    'specialization': None,
    # 'clusters': 'false',	# F default
    'no_magic': 'true',  # F default
    'enable_snippets': 'true',
})

# 4. vars
SECRET_KEY = 'you-will-never-guess'
VAR_DIR = BASE_DIR
VACS_DIR = ''
VACS_UPDATED = None     # last vacansies refreshed


# 5. utils
def eprint(s: str):
    print(s, file=sys.stdout)


def init_cfg():
    """
    Init app variables
    :return:
    """
    global VAR_DIR, VACS_DIR, SECRET_KEY
    cfg_real_path = os.path.expanduser(CFG_FILE_NAME)
    if not os.path.exists(cfg_real_path):
        return
    config = configparser.ConfigParser()
    # config.read(cfg_real_path)
    config.read_string("[{}]\n{}".format(CFG_MAIN_SECT, open(cfg_real_path, "rt").read()))
    config_default = config[CFG_MAIN_SECT]
    SECRET_KEY = config_default.get('secret', SECRET_KEY)
    VAR_DIR = config_default.get('vardir', VAR_DIR)
    VACS_DIR = os.path.join(VAR_DIR, '_saved')
    if not os.path.exists(VACS_DIR):  # FIXME: file
        os.mkdir(VACS_DIR)  # FIXME: chk ok


def load_filter(sess) -> addict.Dict:
    """
    Load current filter from session or defaults
    :param sess: flask session object
    :return: dict
    """
    session_filter = sess.get('filter', {})
    current_filter = addict.Dict({
        'per_page': session_filter.get('per_page', default_filter.per_page),
        'period': session_filter.get('search_period', default_filter.search_period),
        'area': session_filter.get('area', default_filter.area == 2),
        'employment': session_filter.get('employment', default_filter.employment),
        'schedule': session_filter.get('schedule', default_filter.schedule),
        'specialization': session_filter.get('specialization', default_filter.specialization),
    })
    return current_filter


def get_any(resource: str, any_id=None, payload=None):
    """
    Get data from hh.ru (vacancies, vacancy, employer
    :return: response
    On error: r.status_code, r.json()['description']
    TODO: filter/payload (dict)
    """
    url = urljoin(BASE_URL, resource if not any_id else resource + '/' + any_id)  # '/'.join((resource, id))
    rsp = requests.get(url, headers=AGENT, params=payload)
    # print(rsp.request.url)
    return rsp


def process_vacs(vacs: dict):
    """
    Process vacansies returned
    :param vacs: hh.ru response payload
    :return: None
    """
    with open(os.path.join(VACS_DIR, datetime.datetime.now().strftime('%y%m%d%H%M%S') + '.json'), "wt") as ofile:
        ofile.write(json.dumps(vacs, ensure_ascii=False, indent=1))


# 6. flask entry point
init_cfg()
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY


# 7. views
@app.route('/', methods=['GET'])
def index():
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
    current_filter = load_filter(session)
    current_filter.page = request.args.get('page', 0, type=int)
    vacs = get_any(RS_VACS, payload=current_filter)
    if vacs.status_code != requests.codes.ok:  # 200
        # TODO: flush err and ret to /
        eprint(f'Err: {vacs.status_code}')
        eprint(vacs.json()['description'])
        return redirect(url_for('index'))
    process_vacs(vacs.json())
    return render_template('list.html', title="Vacancies", data=vacs.json())


@app.route('/filter', methods=['GET', 'POST'])
def vac_filter():
    """
    Set list filter
    request.form: ImmutableMultiDict
    """
    if request.method == 'POST':
        session['filter'] = {
            'per_page': request.form.get('perpage'),
            'search_period': request.form.get('period'),
            'area': 2 if request.form.get('area') else None,
            'employment': request.form.getlist('empl'),
            'schedule': request.form.getlist('sched'),
            'specialization': request.form.getlist('spec'),
        }
        return redirect(url_for('index'))
    else:
        current_filter = load_filter(session)
        form = hh.FilterForm(
            perpage=current_filter.per_page,
            period=current_filter.search_period,
            area=current_filter.area,
            empl=current_filter.employment,
            sched=current_filter.schedule,
            spec=current_filter.specialization,
        )
        form.update_choices()
    return render_template('filter.html', title='Filter', form=form)


@app.route('/view/<int:vac_id>', methods=['GET'])
def vac_view(vac_id):
    return render_template('view.html', title='View')


# X. go
if __name__ == '__main__':
    app.run(debug=DEBUG)
