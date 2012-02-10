# -*- coding: utf-8 -*-
from __future__ import with_statement
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, abort, \
        render_template, flash, make_response
import jwxt

# configuration
SITENAME = 'SYSU JWXT'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'admin'

# create application
app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def index():
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
    print 'begin'
    ret = jwxt.login(username, password)
    print 'end'
    print ret

    if ret:
        # if succeed
        flash('Login Successfully')
        print "successfully logged in"
        # set cookie here
        response = make_response(redirect(url_for('index')))
        response.set_cookie('sno', username, 60*15)
        response.set_cookie('JSESSIONID', ret, 60*15)
        return response
    else:
        flash('Error password')
        print "wrong password"
        return render_template('sign_in.html', username=username)

@app.route('/sign_out')
def sign_out():
    flash('Logout Successfully')
    response = make_response(redirect(url_for('sign_in')))
    response.set_cookie('sno', '', -3600)
    response.set_cookie('JSESSIONID', '', -3600)
    return response

@app.route('/get_score')
def get_score():
    sno = request.cookies.get('sno') 
    cookie = request.cookies.get('JSESSIONID')
    year, term = [request.args[x] for x in ['year', 'term']]
    print sno, year, term, cookie
    print type(cookie)
    ret = jwxt.get_score(sno.encode('ascii'),
            year.encode('ascii'),
            term.encode('ascii'),
            cookie.encode('ascii'))
    print ret
    return ret

@app.route('/get_class', methods=['POST', 'GET'])
def get_class():
    print 'asads'
    cookie = request.cookies.get('JSESSIONID')
    year, term = [request.form[x] for x in ['class-year', 'class-term']]
    print year, term, cookie
    print type(cookie)
    ret = jwxt.get_class(year.encode('ascii'),
            term.encode('ascii'),
            cookie.encode('ascii'))
    print ret
    return ret


if __name__ == '__main__':
    app.run(host='0.0.0.0')
