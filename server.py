#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import with_statement
from functools import wraps
from contextlib import closing
from flask import Flask, request, g, redirect, url_for, abort, \
        render_template, flash, make_response
import re

import fakesysujwxt as sysujwxt

# basic config
SITENAME = 'SYSU JWXT'
DEBUG = True
SECRET_KEY = 'development key'
SESSION_TIMEOUT = 60*30

# create application
app = Flask(__name__)
app.config.from_object(__name__)

# -----------------
# useful functions
# -----------------
def logged_in():
    """Check whether a user is logged in"""
    return request.cookies.get('JSESSIONID') and request.cookies.get('sno')

def requires_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not logged_in():
            flash(u'矮油，登录后再看吧.', 'error')
            return redirect(url_for('sign_in', next=request.path))
        return f(*args, **kwargs)
    return decorated_function

def requires_api_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not logged_in():
            return 'expired'
        return f(*args, **kwargs)
    return decorated_function

@app.before_request
def detect_user_agent():
    user_agent = request.headers['User-Agent']

    g.is_handheld_device = False
    g.is_ie = False
    if re.search('iPod|iPhone|Android|Opera Mini|BlackBerry|webOS|UCWEB|Blazer|PSP|IEMobile', user_agent):
        g.is_handheld_device = True
    if re.search('MSIE', user_agent):
        g.is_ie = True

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# ------
# Pages
# ------
@app.route('/')
def index():
    if not logged_in():
        return sign_in()

    name, school, major, sno = [request.cookies[x] for x in ['name', 'school', 'major', 'sno']]
    return render_template('dashboard.html', name=name, school=school,
                           major=major, sno=sno)

@app.route('/score')
@requires_login
def score():
    name, sno = [request.cookies[x] for x in ['name', 'sno']]
    return render_template('score.html', name=name, sno=sno)

@app.route('/timetable')
@requires_login
def timetable():
    name, sno = [request.cookies[x] for x in ['name', 'sno']]
    return render_template('timetable.html', name=name, sno=sno)

@app.route('/course')
@requires_login
def course():
    name, sno = [request.cookies[x] for x in ['name', 'sno']]
    return render_template('course.html', name=name, sno=sno)


@app.route('/sign_in', methods=['POST', 'GET'])
def sign_in():
    if logged_in():
        return redirect(url_for('index'))

    if request.method == 'GET':
        return render_template('sign_in.html')

    # POST
    username, password = [request.form[x] for x in ['username', 'password']]

    #login in with sysujwxt module here
    success, result = sysujwxt.login(username, password)

    if success:
        flash(u'登录成功', 'success')

        info_success, info_result = sysujwxt.get_info(result)
        if info_success:
            info = re.match(r'.+"xm":"(?P<name>.+?)".+"xymc":"(?P<school>.+?)".+"zyfxmc":"(?P<major>.+?)"',
                            info_result)
            name, school, major = info.groups()
            # set cookie here
            next_url = request.args.get('next', '/')
            response = make_response(redirect(next_url))
            response.set_cookie('sno', username, SESSION_TIMEOUT)
            response.set_cookie('name', name, SESSION_TIMEOUT)
            response.set_cookie('school', school, SESSION_TIMEOUT)
            response.set_cookie('major', major, SESSION_TIMEOUT)
            response.set_cookie('JSESSIONID', result, SESSION_TIMEOUT)
            return response
        elif info_result == 'timeout' or info_result == 'expired':
            flash(u'= =哦希特, 貌似学校的系统挂了，换个时间再来试试吧', 'info')
            return render_template('sign_in.html', username=username)
    elif result == 'timeout':
        flash(u'= =哦希特, 貌似学校的系统挂了，换个时间再来试试吧', 'info')
        return render_template('sign_in.html', username=username)
    elif result == 'errorpass':
        flash(u'密码错误', 'error')
        return render_template('sign_in.html', username=username)

@app.route('/sign_out')
def sign_out():
    flash(u'登出成功', 'success')
    response = make_response(redirect(url_for('sign_in')))
    response.set_cookie('sno', '', expires=-1)
    response.set_cookie('JSESSIONID', '', expires=-1)
    return response

# -----
# APIs
# -----
@app.route('/api/timetable')
@requires_api_login
def get_timetable():
    cookie = request.cookies.get('JSESSIONID')
    sno = request.cookies.get('sno')
    year, term = [request.args[x] for x in ['year', 'term']]
    _, result = sysujwxt.get_timetable(cookie.encode('ascii'),
                                       year.encode('ascii'),
                                       term.encode('ascii'))
    return result

@app.route('/api/score')
@requires_api_login
def get_score():
    sno = request.cookies.get('sno')
    cookie = request.cookies.get('JSESSIONID')
    year = request.args.get('year', '')
    term = request.args.get('term', '')
    _, result = sysujwxt.get_score(cookie.encode('ascii'),
                                   sno.encode('ascii'),
                                   year.encode('ascii'),
                                   term.encode('ascii'))
    return result

@app.route('/api/available_courses')
@requires_api_login
def get_selected_course():
    sno = request.cookies.get('sno')
    cookie = request.cookies.get('JSESSIONID')
    year, term , course_type, campus = [request.args[x] for x in ['year', 'term', 'course_type', 'campus']]
    _, result = sysujwxt.get_available_courses(cookie.encode('ascii'),
                                               year.encode('ascii'),
                                               term.encode('ascii'),
                                               course_type.encode('ascii'),
                                               campus.encode('ascii'))
    return result

@app.route('/api/add_course')
@requires_api_login
def add_course():
    sno = request.cookies.get('sno')
    cookie = request.cookies.get('JSESSIONID')
    id, year, term = [request.args[x] for x in ['id', 'year', 'term']]
    _, result = sysujwxt.add_course(cookie.encode('ascii'),
                                    id.encode('ascii'),
                                    year.encode('ascii'),
                                    term.encode('ascii'))
    return result

@app.route('/api/course_result')
@requires_api_login
def get_course_result():
    sno = request.cookies.get('sno')
    cookie = request.cookies.get('JSESSIONID')
    year, term = [request.args[x] for x in ['year', 'term']]
    _, result = sysujwxt.get_course_result(cookie.encode('ascii'),
                                     year.encode('ascii'),
                                     term.encode('ascii'))
    return result

@app.route('/course_result_by_type')
@requires_api_login
def get_course_result_by_type():
    sno = request.cookies.get('sno')
    cookie = request.cookies.get('JSESSIONID')
    year, term, course_type = [request.args[x] for x in ['year', 'term', 'course_type']]
    _, result = sysujwxt.get_course_result_by_type(cookie.encode('ascii'),
                                                   year.encode('ascii'),
                                                   term.encode('ascii'),
                                                   course_type.encode('ascii'))
    return result

@app.route('/api/remove_course')
@requires_api_login
def remove_course():
    sno = request.cookies.get('sno')
    cookie = request.cookies.get('JSESSIONID')
    id  = request.args.get('id')
    _, result = sysujwxt.remove_course(cookie.encode('ascii'), id.encode('ascii'))
    return result

@app.route('/api/info')
@requires_api_login
def get_info():
    sno = request.cookies.get('sno')
    cookie = request.cookies.get('JSESSIONID')
    _, result = sysujwxt.get_info(cookie.encode('ascii'))
    return result

@app.route('/api/tno')
@requires_api_login
def get_tno():
    sno = request.cookies.get('sno')
    cookie = request.cookies.get('JSESSIONID')
    _, result = sysujwxt.get_tno(cookie.encode('ascii'))
    return result

@app.route('/api/required_credit')
@requires_api_login
def get_required_credit():
    sno = request.cookies.get('sno')
    cookie = request.cookies.get('JSESSIONID')
    grade, tno = [request.args[x] for x in ['grade', 'tno']]
    _, result = sysujwxt.get_required_credit(cookie.encode('ascii'),
                                       grade.encode('ascii'),
                                       tno.encode('ascii'))
    return result

@app.route('/api/earned_credit')
@requires_api_login
def get_earned_credit():
    sno = request.cookies.get('sno')
    cookie = request.cookies.get('JSESSIONID')
    year = request.args.get('year', '')
    term = request.args.get('term', '')
    _, result = sysujwxt.get_earned_credit(cookie.encode('ascii'),
                                           sno.encode('ascii'),
                                           year.encode('ascii'),
                                           term.encode('ascii'))
    return result

@app.route('/api/gpa')
@requires_api_login
def get_gpa():
    sno = request.cookies.get('sno')
    cookie = request.cookies.get('JSESSIONID')
    year = request.args.get('year', '')
    term = request.args.get('term', '')
    _, result = sysujwxt.get_gpa(cookie.encode('ascii'),
                                 sno.encode('ascii'),
                                 year.encode('ascii'),
                                 term.encode('ascii'))
    return result

@app.route('/api/tips')
def tips():
    return redirect(url_for('static', filename='tips.json'))

if __name__ == '__main__':
    app.run(host='0.0.0.0')
