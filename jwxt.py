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

class_url = 'http://uems.sysu.edu.cn/jwxt/sysu/xk/xskbcx/xskbcx.jsp'
def get_class(year, term, cookie):
    print year, term, cookie
    ch = pycurl.Curl()
    ch.setopt(pycurl.URL, class_url+'?'+urllib.urlencode({'xnd':year, 'xq':term}))
    ret = StringIO.StringIO()
    ch.setopt(pycurl.WRITEFUNCTION, ret.write)
    ch.setopt(pycurl.COOKIE, "JSESSIONID="+cookie)

    ch.perform()
    ret_code = ch.getinfo(pycurl.HTTP_CODE)
    ret_body = ret.getvalue() 
    ch.close()
    return ret_body


if __name__ == '__main__':
    c = login('0938ooxx', 'password')
    print get_score('0938ooxx', '2011-2012', '1', c)
    print get_class('2010-2011', 1, c)
