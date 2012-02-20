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

intranet_domain = 'http://jwxt2.lovemaple.info'

def is_from_intranet(ip):
    intranet_ip_patten = r"""(^10\.)|
(^172\.1[6-9]\.)|(^172\.2[0-9]\.)|(^172\.3[0-1]\.)|
(^192\.168\.)"""
    return re.match(intranet_ip_patten, ip)

@app.route('/')
def index():
    # check intranet ip
    remote_ip = request.remote_addr
    if is_from_intranet(remote_ip):
        print 'Got intranet ip: ', remote_ip
        return redirect(intranet_domain)

    # check whether logged in
    if not request.cookies.get('JSESSIONID') or not request.cookies.get('sno'):
        return redirect(url_for('sign_in'))

    # logged in
    return render_template('index.html', sno = request.cookies.get('sno'))

@app.route('/sign_in', methods=['POST', 'GET'])
def sign_in():

    if request.method == 'GET':
        return render_template('sign_in.html')

    # POST
    username, password = [request.form[x] for x in ['username', 'password']]

    #login in with jwxt module here
    ret = jwxt.login(username, password)

    if ret:
        # if succeed
        flash(u'登录成功')
        #print "successfully logged in"
        # set cookie here
        response = make_response(redirect(url_for('index')))
        response.set_cookie('sno', username, 60*30)
        response.set_cookie('JSESSIONID', ret, 60*30)
        return response
    else:
        flash(u'密码错误')
        #print "wrong password"
        return render_template('sign_in.html', username=username)

@app.route('/sign_out')
def sign_out():
    flash(u'登出成功')
    response = make_response(redirect(url_for('sign_in')))
    response.set_cookie('sno', '', -3600)
    response.set_cookie('JSESSIONID', '', -3600)
    return response

@app.route('/score')
def score():
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
def selecting_course():
    sno = request.cookies.get('sno') 
    cookie = request.cookies.get('JSESSIONID')
    year, term , course_type= [request.args[x] for x in ['year', 'term', 'course_type']]
    print year, term, course_type
    ret = jwxt.get_selecting_course(year.encode('ascii'),
            term.encode('ascii'),
            course_type.encode('ascii'),
            cookie.encode('ascii'))
    return ret

@app.route('/selected_course')
def selected_course():
    sno = request.cookies.get('sno') 
    cookie = request.cookies.get('JSESSIONID')
    year, term , course_type= [request.args[x] for x in ['year', 'term', 'course_type']]
    print year, term, course_type
    ret = jwxt.get_selected_course(year.encode('ascii'),
            term.encode('ascii'),
            course_type.encode('ascii'),
            cookie.encode('ascii'))
    return ret

@app.route('/course_result')
def course_result():
    sno = request.cookies.get('sno') 
    cookie = request.cookies.get('JSESSIONID')
    year, term = [request.args[x] for x in ['year', 'term']]
    print year, term
    ret = jwxt.get_course_result(year.encode('ascii'),
            term.encode('ascii'),
            cookie.encode('ascii'))
    return ret

@app.route('/remove_course')
def remove_course():
    sno = request.cookies.get('sno') 
    cookie = request.cookies.get('JSESSIONID')
    id  = request.args.get('id')
    print id
    ret = jwxt.remove_course(id.encode('ascii'), cookie.encode('ascii'))
    return ret

@app.route('/course_schedule', methods=['POST', 'GET'])
def course_schedule():
    cookie = request.cookies.get('JSESSIONID')
    year, term = [request.form[x] for x in ['class-year', 'class-term']]
    ret = jwxt.get_course_schedule(year.encode('ascii'),
            term.encode('ascii'),
            cookie.encode('ascii'))
    return ret

if __name__ == '__main__':
    app.run(host='0.0.0.0')
