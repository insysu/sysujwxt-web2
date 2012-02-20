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
    print type(ret_code)
    if ret_code == 200:
        print 'asdds'
        return 
    else:
        ret_header = ret.getvalue() 
        #print ret_header
        #print type(ret_header)
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
    return ret_body

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
    print ret_body
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
    print ret_body
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
    print ret_body
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
    print ret_body
    return ret_body

if __name__ == '__main__':
    c = login('09388448', '8453100')
    print get_score('09388448', '2011-2012', '1', c)
