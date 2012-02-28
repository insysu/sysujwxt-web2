#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import pycurl
import re
import StringIO

login_url = 'http://uems.sysu.edu.cn/jwxt/j_unieap_security_check.do'
def login(username, passward):
    print username, passward
    ch = pycurl.Curl()
    ch.setopt(pycurl.URL, login_url)
    ch.setopt(pycurl.POST, True)
    data = urllib.urlencode({'j_username': username, 'j_password': passward})
    ch.setopt(pycurl.POSTFIELDS, data)
    ch.setopt(pycurl.HEADER, True)
    ret = StringIO.StringIO()
    ch.setopt(pycurl.WRITEFUNCTION, ret.write)

    ch.perform()
    ret_code = ch.getinfo(pycurl.HTTP_CODE)
    ch.close()
    if ret_code == 200:
        return 
    else:
        ret_header = ret.getvalue() 
        #print ret_header
        cookies = re.findall(r'^Set-Cookie: (.*);', ret_header, re.MULTILINE)
        cookie = cookies[0][11:]
        return cookie


# get score
score_url = 'http://uems.sysu.edu.cn/jwxt/xscjcxAction/xscjcxAction.action?method=getKccjList'
def get_score(sno, year, term, cookie):
    print sno, year, term, cookie
    srt = '{body:{dataStores:{kccjStore:{rowSet:{"primary":[],"filter":[],"delete":[]},name:"kccjStore",pageNumber:1,pageSize:100,rowSetName:"pojo_com.neusoft.education.sysu.xscj.xscjcx.model.KccjModel"}},parameters:{"kccjStore-params": [{"name": "Filter_t.pylbm_0.1950409999148804", "type": "String", "value": "\'01\'", "condition": " = ", "property": "t.pylbm"}, {"name": "Filter_t.xn_0.3563793106347481", "type": "String", "value": "\''+year+'\'", "condition": " = ", "property": "t.xn"}, {"name": "Filter_t.xq_0.7983325881237213", "type": "String", "value": "\''+term+'\'", "condition": " = ", "property": "t.xq"}, {"name": "xh", "type": "String", "value": "\''+sno+'\'", "condition": " = ", "property": "t.xh"}], "args": ["student"]}}}';

    ch = pycurl.Curl()
    ch.setopt(pycurl.URL, score_url)
    ch.setopt(pycurl.POST, True)
    ch.setopt(pycurl.POSTFIELDS, srt)
    ret = StringIO.StringIO()
    ch.setopt(pycurl.WRITEFUNCTION, ret.write)
    ch.setopt(pycurl.HTTPHEADER, ['Content-Type: multipart/form-data', 'render: unieap'])
    ch.setopt(pycurl.COOKIE, "JSESSIONID="+cookie)

    ch.perform()
    ret_code = ch.getinfo(pycurl.HTTP_CODE)
    ret_body = ret.getvalue() 
    ch.close()
    return ret_body

course_schedule_url = 'http://uems.sysu.edu.cn/jwxt/sysu/xk/xskbcx/xskbcx.jsp'
def get_course_schedule(year, term, cookie):
    print year, term, cookie
    ch = pycurl.Curl()
    ch.setopt(pycurl.URL, course_schedule_url+'?'+urllib.urlencode({'xnd':year, 'xq':term}))
    ret = StringIO.StringIO()
    ch.setopt(pycurl.WRITEFUNCTION, ret.write)
    ch.setopt(pycurl.COOKIE, "JSESSIONID="+cookie)

    ch.perform()
    ret_code = ch.getinfo(pycurl.HTTP_CODE)
    ret_body = ret.getvalue() 
    ch.close()

    # add course time to schedule table
    pat = r'^var jcshowdata.*$'
    sub = """var jcshowdata=["","第一节<br>08:00-08:45","第二节<br>08:55-09:40","第三节<br>09:50-10:35","第四节<br>10:45-11:30","第五节<br>11:40-12:25","第六节<br>12:35-13:20","第七节<br>13:30-14:15","第八节<br>14:25-15:10","第九节<br>15:20-16:05","第十节<br>16:15-17:00","第十一节<br>17:10-17:55","第十二节<br>18:05-18:50","第十三节<br>19:00-19:45","第十四节<br>19:55-20:40","第十五节<br>20:50-21:35"];\r"""
    html = re.sub(pat, sub, ret_body, flags=re.M)
    return html

selecting_course_url = 'http://uems.sysu.edu.cn/jwxt/xsxk/xsxk.action?method=getJxbxxFunc'
def get_selecting_course(year, term, course_type, cookie):
    print year, term, course_type, cookie
    srt = '{header:{"code": -100, "message": {"title": "", "detail": ""}},body:{dataStores:{table1kxkcStore:{rowSet:{"primary":[],"filter":[],"delete":[]},name:"table1kxkcStore",pageNumber:1,pageSize:280,recordCount:9,rowSetName:"pojo_com.neusoft.education.sysu.xk.zxxkgg.model.KkblbModel"}},parameters:{"table1kxkcStore-params": [], "args": ["'+year+'", "'+str(term)+'", "'+course_type+'"]}}}';
    ch = pycurl.Curl()
    ch.setopt(pycurl.URL, selecting_course_url)
    ch.setopt(pycurl.POST, True)
    ch.setopt(pycurl.POSTFIELDS, srt)
    ret = StringIO.StringIO()
    ch.setopt(pycurl.WRITEFUNCTION, ret.write)
    ch.setopt(pycurl.HTTPHEADER, ['Content-Type: multipart/form-data', 'render: unieap'])
    ch.setopt(pycurl.COOKIE, "JSESSIONID="+cookie)

    ch.perform()
    ret_code = ch.getinfo(pycurl.HTTP_CODE)
    ret_body = ret.getvalue() 
    ch.close()
    return ret_body

selected_course_url = 'http://uems.sysu.edu.cn/jwxt/xsxk/xsxk.action?method=getTab1YxkcByxndxqkclbmpylbmxh'
def get_selected_course(year, term, course_type, cookie):
    srt = '{header:{"code": -100, "message": {"title": "", "detail": ""}},body:{dataStores:{table1yxkcStore:{rowSet:{"primary":[],"filter":[],"delete":[]},name:"table1yxkcStore",pageNumber:1,pageSize:10,recordCount:0,rowSetName:"pojo_com.neusoft.education.sysu.xk.drxsxkjg.entity.XkjgAndSsjhModel"}},parameters:{"args": ["01", "'+course_type+'", "'+year+'", "'+term+'"]}}}'
    ch = pycurl.Curl()
    ch.setopt(pycurl.URL, selected_course_url)
    ch.setopt(pycurl.POST, True)
    ch.setopt(pycurl.POSTFIELDS, srt)
    ret = StringIO.StringIO()
    ch.setopt(pycurl.WRITEFUNCTION, ret.write)
    ch.setopt(pycurl.HTTPHEADER, ['Content-Type: multipart/form-data', 'render: unieap'])
    ch.setopt(pycurl.COOKIE, "JSESSIONID="+cookie)
    ch.perform()
    ret_code = ch.getinfo(pycurl.HTTP_CODE)
    ret_body = ret.getvalue() 
    ch.close()
    return ret_body

remove_course_url = 'http://uems.sysu.edu.cn/jwxt/xsxk/xsxk.action?method=delXsxkjgFuncChanged'
def remove_course(id, cookie):
    srt = '{header:{"code": -100, "message": {"title": "", "detail": ""}},body:{dataStores:{},parameters:{"args": ["'+id+'"], "responseParam": "dataSave"}}}'
    ch = pycurl.Curl()
    ch.setopt(pycurl.URL, remove_course_url)
    ch.setopt(pycurl.POST, True)
    ch.setopt(pycurl.POSTFIELDS, srt)
    ret = StringIO.StringIO()
    ch.setopt(pycurl.WRITEFUNCTION, ret.write)
    ch.setopt(pycurl.HTTPHEADER, ['Content-Type: multipart/form-data', 'render: unieap'])
    ch.setopt(pycurl.COOKIE, "JSESSIONID="+cookie)
    ch.perform()
    ret_code = ch.getinfo(pycurl.HTTP_CODE)
    ret_body = ret.getvalue() 
    ch.close()
    return ret_body


course_result_url = 'http://uems.sysu.edu.cn/jwxt/xstk/xstk.action?method=getXkxkjglistByxh'
def get_course_result(year, term, cookie):
    print year, term, cookie
    srt = '{header:{"code": -100, "message": {"title": "", "detail": ""}},body:{dataStores:{xsxkjgStore:{rowSet:{"primary":[],"filter":[],"delete":[]},name:"xsxkjgStore",pageNumber:1,pageSize:10,recordCount:0,rowSetName:"pojo_com.neusoft.education.sysu.xk.drxsxkjg.entity.XkjgEntity",order:"xnd desc,xq desc"}},parameters:{"xsxkjgStore-params": [{"name": "xnd", "type": "String", "value": "\''+year+'\'", "condition": " = ", "property": "xnd"}, {"name": "xq", "type": "String", "value": "\''+term+'\'", "condition": " = ", "property": "xq"}], "args": []}}}';
    ch = pycurl.Curl()
    ch.setopt(pycurl.URL, course_result_url)
    ch.setopt(pycurl.POST, True)
    ch.setopt(pycurl.POSTFIELDS, srt)
    ret = StringIO.StringIO()
    ch.setopt(pycurl.WRITEFUNCTION, ret.write)
    ch.setopt(pycurl.HTTPHEADER, ['Content-Type: multipart/form-data', 'render: unieap'])
    ch.setopt(pycurl.COOKIE, "JSESSIONID="+cookie)
    ch.perform()
    ret_code = ch.getinfo(pycurl.HTTP_CODE)
    ret_body = ret.getvalue() 
    ch.close()
    return ret_body

info_url = 'http://uems.sysu.edu.cn/jwxt/xscjcxAction/xscjcxAction.action?method=judgeStu'
def get_info(cookie):
    """
    获取[学号], [年级], [教学号]
    """
    srt = """{header:{
    "code": -100, 
    "message": {"title": "", "detail": ""}},
    body:{
        dataStores:{
            tempStore:{
                rowSet:{
                    "primary":[],
                    "filter":[],
                    "delete":[]},
                name:"tempStore",
                pageNumber:1,
                pageSize:2147483647,
                recordCount:0,
                rowSetName:"pojo_com.neusoft.education.sysu.xy.xyjy.model.OnecolumModel"}},
        parameters:{
            "args": [], 
            "responseParam": 
            "result"}}}"""
    ch = pycurl.Curl()
    ch.setopt(pycurl.URL, info_url)
    ch.setopt(pycurl.POST, True)
    ch.setopt(pycurl.POSTFIELDS, srt)
    ret = StringIO.StringIO()
    ch.setopt(pycurl.WRITEFUNCTION, ret.write)
    ch.setopt(pycurl.HTTPHEADER, ['Content-Type: multipart/form-data', 'render: unieap'])
    ch.setopt(pycurl.COOKIE, "JSESSIONID="+cookie)

    ch.perform()
    ret_code = ch.getinfo(pycurl.HTTP_CODE)
    ret_body = ret.getvalue() 
    ch.close()
    return ret_body

overall_credit_url = 'http://uems.sysu.edu.cn/jwxt/xscjcxAction/xscjcxAction.action?method=getZyxf'
def get_overall_credit(grade, tno, cookie):
    """
    获取总学分
    """
    srt = '{header:{"code": -100, "message": {"title": "", "detail": ""}},body:{dataStores:{zxzyxfStore:{rowSet:{"primary":[],"filter":[],"delete":[]},name:"zxzyxfStore",pageNumber:1,pageSize:2147483647,recordCount:0,rowSetName:"pojo_com.neusoft.education.sysu.djks.ksgl.model.TwoColumnModel"}},parameters:{"zxzyxfStore-params": [{"name": "pylbm", "type": "String", "value": "\'01\'", "condition": " = ", "property": "x.pylbm"}, {"name": "nj", "type": "String", "value": "\''+grade+'\'", "condition": " = ", "property": "x.nj"}, {"name": "zyh", "type": "String", "value": "\''+tno+'\'", "condition": " = ", "property": "x.zyh"}], "args": []}}}'
    ch = pycurl.Curl()
    ch.setopt(pycurl.URL, overall_credit_url)
    ch.setopt(pycurl.POST, True)
    ch.setopt(pycurl.POSTFIELDS, srt)
    ret = StringIO.StringIO()
    ch.setopt(pycurl.WRITEFUNCTION, ret.write)
    ch.setopt(pycurl.HTTPHEADER, ['Content-Type: multipart/form-data', 'render: unieap'])
    ch.setopt(pycurl.COOKIE, "JSESSIONID="+cookie)

    ch.perform()
    ret_code = ch.getinfo(pycurl.HTTP_CODE)
    ret_body = ret.getvalue() 
    ch.close()
    return ret_body

obtained_credit_url = 'http://uems.sysu.edu.cn//jwxt/xscjcxAction/xscjcxAction.action?method=getAllXf'
def get_obtained_credit(sno, cookie):
    """
    获取已取得的学分
    """
    srt = '{header:{"code": -100, "message": {"title": "", "detail": ""}},body:{dataStores:{allJdStore:{rowSet:{"primary":[],"filter":[],"delete":[]},name:"allJdStore",pageNumber:1,pageSize:2147483647,recordCount:0,rowSetName:"pojo_com.neusoft.education.sysu.djks.ksgl.model.TwoColumnModel"}},parameters:{"args": ["'+sno+'", "", "", ""]}}}'
    ch = pycurl.Curl()
    ch.setopt(pycurl.URL, obtained_credit_url)
    ch.setopt(pycurl.POST, True)
    ch.setopt(pycurl.POSTFIELDS, srt)
    ret = StringIO.StringIO()
    ch.setopt(pycurl.WRITEFUNCTION, ret.write)
    ch.setopt(pycurl.HTTPHEADER, ['Content-Type: multipart/form-data', 'render: unieap'])
    ch.setopt(pycurl.COOKIE, "JSESSIONID="+cookie)

    ch.perform()
    ret_code = ch.getinfo(pycurl.HTTP_CODE)
    ret_body = ret.getvalue() 
    ch.close()
    return ret_body

gpa_url = 'http://uems.sysu.edu.cn/jwxt/xscjcxAction/xscjcxAction.action?method=getAllJd'
def get_gpa(sno, cookie):
    """
    获取已取得的总基点: 专必 公必 公选 专选
    """
    srt = '{header:{"code": -100, "message": {"title": "", "detail": ""}},body:{dataStores:{allJdStore:{rowSet:{"primary":[],"filter":[],"delete":[]},name:"allJdStore",pageNumber:1,pageSize:2147483647,recordCount:0,rowSetName:"pojo_com.neusoft.education.sysu.djks.ksgl.model.TwoColumnModel"}},parameters:{"args": ["'+sno+'", "", "", ""]}}}'
    ch = pycurl.Curl()
    ch.setopt(pycurl.URL, gpa_url)
    ch.setopt(pycurl.POST, True)
    ch.setopt(pycurl.POSTFIELDS, srt)
    ret = StringIO.StringIO()
    ch.setopt(pycurl.WRITEFUNCTION, ret.write)
    ch.setopt(pycurl.HTTPHEADER, ['Content-Type: multipart/form-data', 'render: unieap'])
    ch.setopt(pycurl.COOKIE, "JSESSIONID="+cookie)

    ch.perform()
    ret_code = ch.getinfo(pycurl.HTTP_CODE)
    ret_body = ret.getvalue() 
    ch.close()
    return ret_body

if __name__ == '__main__':
    c = login('093800xx', '00xx00xx')
    print get_score('0938ooxx', '2011-2012', '1', c)
    print get_course_schedule('2011-2012', '2', c)
