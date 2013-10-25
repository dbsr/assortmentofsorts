# -*- coding: utf-8 -*-
# dydrmntion@gmail.com ~ 2013

import commands
from datetime import datetime
import re


def expac():
    cmd = 'expac "%n||%E||%G||%N||%d||%l||%m||%u||%w" -Q'
    parse_lambdas = {
        'modify': {
            'install_date': lambda k, v: (
                'age',
                '{} days'.format((datetime.now() - datetime.strptime(v, '%a %b %d %H:%M:%S %Y')).days)
            ),
            'install_size': lambda k, v: (k, "{} KB".format(int(float(int(v)) / 1024))),
            'project_url': lambda k, v: ('url', v)
        },
        'add': {
            'required_by': lambda k, v: ('req_by_num', len(v)),
            'depends_on': lambda k, v: ('dep_on_num', len(v))
        }
    }

    packages = []
    for p in [pkg.split('||') for pkg in commands.getoutput(cmd).split('\n')]:

        pdict = {}

        for i, k in enumerate(['name', 'depends_on', 'groups', 'required_by', 'description',
                               'install_date', 'install_size', 'project_url', 'install_reason' ]):

            v = p[i].split() if k in ['required_by', 'depends_on'] else p[i]

            if k in parse_lambdas['modify']:

                k, v = parse_lambdas['modify'][k](k, v)

            elif k in parse_lambdas['add']:

                k_, v_ = parse_lambdas['add'][k](k, v)

                pdict[k_] = v_

            pdict[k] = v

        packages.append(pdict)

    return packages


def load_packages():
    global packages
    packages = expac()


def get(kwargs):

    lambda_kwargs = {
        'sort': {
            'on': 'name',
            'reverse': False,
            'lambda': lambda packages, sort_idx, cast=str: sorted(packages, key=lambda k: cast(k[sort_idx][1].split()[0]), reverse=lambda_kwargs['sort']['reverse'])
        },
        'filters': {
            'active': [],
            'skip_base': lambda package: re.search(r'base|devel', package.get('groups')),
            'dependency': lambda package: package.get('install_reason') == 'dependency',
            'explicit': lambda package: package.get('install_reason') == 'explicit',
            'has_dependencies': lambda package: package.get('req_by_num') > 0,
            'lambda': lambda package: len(
                [f for f in lambda_kwargs['filters']['active'] if
                lambda_kwargs['filters'][f](package)]
              ) > 0
        }
    }
    fields = ['name', 'url', 'age', 'install_size', 'install_reason', 'req_by_num', 'dep_on_num']
    sort_on = kwargs.get('sort', lambda_kwargs['sort']['on'])
    cast = int if sort_on in ['age', 'install_size', 'req_by_num', 'dep_on_num'] else str
    reverse = bool(int(kwargs.get('reverse', lambda_kwargs['sort']['reverse'])))
    filters = []
    for f in lambda_kwargs['filters'].keys():
       if kwargs.get(f):
            filters.append(f)

    print filters
    lambda_kwargs['filters']['active'] = filters
    cur_packages = [[(k, package[k]) for k in fields] for package in packages
                    if not lambda_kwargs['filters']['lambda'](package)]

    if cur_packages:
      sort_idx = [k for k, v in cur_packages[0]].index(sort_on)
    data = {
        'packages': sorted(cur_packages, key=lambda k: cast(str(k[sort_idx][1]).split()[0]), reverse=reverse),
        'thead': [('checkbox', '')] + [(x, x.replace('_', ' ')) for x in fields],
        'sub_data': dict((p.get('name'), p.get('description')) for p in packages),
        'block': ['depends_on', 'required_by'],
        'filters': [
          {
            'filter': 'skip_base',
            'name': 'base / devel groups',
            'state': 'active' if 'skip_base' in lambda_kwargs['filters']['active'] else 'inactive'
          },
          {
            'filter': 'dependency',
            'name': 'installed as dependency',
            'state': 'active' if 'dependency' in lambda_kwargs['filters']['active'] else 'inactive'
          },
          {
            'filter': 'explicit',
            'name': 'installed explicitly',
            'state': 'active' if 'explicit' in lambda_kwargs['filters']['active'] else 'inactive'
          },
          {
            'filter': 'has_dependencies',
            'name': 'has dependencies',
            'state': 'active' if 'has_dependencies' in lambda_kwargs['filters']['active'] else 'inactive'
          }

       ],
        'sort': {
            'on': sort_on,
            'reverse': int(reverse)
        }
    }

    return data

packages = None

load_packages()
