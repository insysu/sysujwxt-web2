#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import with_statement
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, abort, \
        render_template, flash, make_response
import jwxt
import re

# configuration
SITENAME = 'SYSU JWXT'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'admin'

# create application
app = Flask(__name__)
app.config.from_object(__name__)

# check whether a user is  logged in
def logged_in():
    return request.cookies.get('JSESSIONID') and request.cookies.get('sno')

@app.route('/')
def index():
    # check whether logged in
    if not logged_in():
        return redirect(url_for('sign_in'))

    # logged in
    return render_template('index.html', sno = request.cookies.get('sno'))

@app.route('/sign_in', methods=['POST', 'GET'])
def sign_in():
    if logged_in():
        return redirect(url_for('index'))

    if request.method == 'GET':
        return render_template('sign_in.html')

    # POST
    username, password = [request.form[x] for x in ['username', 'password']]

    #login in with jwxt module here
    ret = jwxt.login(username, password)

    if ret:
        # if succeed
        flash(u'登录成功')
        print username, "successfully logged in"

        # set cookie here
        response = make_response(redirect(url_for('index')))
        response.set_cookie('sno', username, 15*60)
        response.set_cookie('JSESSIONID', ret, 15*60)
        return response
    else:
        flash(u'密码错误')
        print username, "wrong password"
        return render_template('sign_in.html', username=username)

@app.route('/sign_out')
def sign_out():
    flash(u'登出成功')
    response = make_response(redirect(url_for('sign_in')))
    response.set_cookie('sno', '', -3600)
    response.set_cookie('JSESSIONID', '', -3600)
    return response

@app.route('/score')
def get_score():
    sno = request.cookies.get('sno') 
    cookie = request.cookies.get('JSESSIONID')
    year, term = [request.args[x] for x in ['year', 'term']]
    print 'Query score with sno: ', sno
    ret = jwxt.get_score(sno.encode('ascii'),
            year.encode('ascii'),
            term.encode('ascii'),
            cookie.encode('ascii'))
    return ret

@app.route('/selecting_course')
def get_selecting_course():
    sno = request.cookies.get('sno') 
    cookie = request.cookies.get('JSESSIONID')
    year, term , course_type= [request.args[x] for x in ['year', 'term', 'course_type']]
    print 'Query seleting course with sno:', sno
    ret = jwxt.get_selecting_course(year.encode('ascii'),
            term.encode('ascii'),
            course_type.encode('ascii'),
            cookie.encode('ascii'))
    return ret

@app.route('/selected_course')
def get_selected_course():
    sno = request.cookies.get('sno') 
    cookie = request.cookies.get('JSESSIONID')
    year, term , course_type= [request.args[x] for x in ['year', 'term', 'course_type']]
    print 'Query seleted course with sno: ', sno
    ret = jwxt.get_selected_course(year.encode('ascii'),
            term.encode('ascii'),
            course_type.encode('ascii'),
            cookie.encode('ascii'))
    return ret

@app.route('/course_result')
def get_course_result():
    sno = request.cookies.get('sno') 
    cookie = request.cookies.get('JSESSIONID')
    year, term = [request.args[x] for x in ['year', 'term']]
    print 'Query course result with sno:', sno
    ret = jwxt.get_course_result(year.encode('ascii'),
            term.encode('ascii'),
            cookie.encode('ascii'))
    return ret

@app.route('/remove_course')
def remove_course():
    sno = request.cookies.get('sno') 
    cookie = request.cookies.get('JSESSIONID')
    id  = request.args.get('id')
    print sno, 'is removing course result with id:', id
    ret = jwxt.remove_course(id.encode('ascii'), cookie.encode('ascii'))
    return ret

@app.route('/info')
def get_info():
    sno = request.cookies.get('sno') 
    cookie = request.cookies.get('JSESSIONID')
    print 'Get info with sno:', sno
    ret = jwxt.get_info(cookie.encode('ascii'))
    return ret

@app.route('/overall_credit')
def get_overall_credit():
    sno = request.cookies.get('sno') 
    cookie = request.cookies.get('JSESSIONID')
    grade, tno = [request.args[x] for x in ['grade', 'tno']]
    print 'Query overall credit with sno:', sno
    ret = jwxt.get_overall_credit(grade.encode('ascii'),
            tno.encode('ascii'),
            cookie.encode('ascii'))
    return ret

@app.route('/obtained_credit')
def get_obtained_credit():
    sno = request.cookies.get('sno') 
    cookie = request.cookies.get('JSESSIONID')
    print 'Query obtained credit with sno:', sno
    ret = jwxt.get_obtained_credit(sno.encode('ascii'),
            cookie.encode('ascii'))
    return ret

@app.route('/gpa')
def get_gpa():
    sno = request.cookies.get('sno') 
    cookie = request.cookies.get('JSESSIONID')
    print 'Query gpa with sno:', sno
    ret = jwxt.get_gpa(sno.encode('ascii'),
            cookie.encode('ascii'))
    return ret

@app.route('/course_schedule', methods=['POST', 'GET'])
def get_course_schedule():
    cookie = request.cookies.get('JSESSIONID')
    year, term = [request.form[x] for x in ['class-year', 'class-term']]
    sno = request.cookies.get('sno') 
    print 'Query course schedule with sno:', sno
    ret = jwxt.get_course_schedule(year.encode('ascii'),
            term.encode('ascii'),
            cookie.encode('ascii'))
    return ret

if __name__ == '__main__':
    app.run(host='0.0.0.0')
