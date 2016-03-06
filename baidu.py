# -*- coding: utf8 -*-

import os 
import urllib2
import urllib
import cookielib
import re
import json
import time
from ctypes import *
import ssl
import socket

socket.setdefaulttimeout(10.0)

ssl._create_default_https_context = ssl._create_unverified_context



YDMApi = windll.LoadLibrary('yundamaAPI')
#第三方打码函数
def dama(codetype):
	appId = 1981
	appKey = 'a4f912fb73c263d8c50479b6546b3b15'
	username = {{yours}}
	password = {{yours}}
	codetype = codetype
	result = c_char_p("                              ")
	timeout = 60
	filename = '1.jpg'
	captchaId = YDMApi.YDM_EasyDecodeByPath(username, password, appId, appKey, filename, codetype, timeout, result)
	return captchaId,result.value

#把数字转换成九宫格坐标
def NumToLoc(nums):
	NumToLoc_table = {'1':'00000000','2':'00010000','3':'00020000','4':'00000001','5':'00010001','6':'00020001','7':'00000002','8':'00010002','9':'00020002'}
	vcode = ''
	for num in nums:
		vcode += NumToLoc_table[num]
	return vcode


try:
	os.remove('posted.txt')
except:
	print 'no posted file'

f = open('posted.txt','a')
f.close()




URL_BAIDU_INDEX = u'http://www.baidu.com/';
#https://passport.baidu.com/v2/api/?getapi&class=login&tpl=mn&tangram=true 也可以用这个
URL_BAIDU_TOKEN = 'https://passport.baidu.com/v2/api/?getapi&tpl=pp&apiver=v3&class=login';
URL_BAIDU_LOGIN = 'https://passport.baidu.com/v2/api/?login';
URL_BAIDU_SIGN = 'http://tieba.baidu.com/sign/add'
   
#设置用户名、密码
username = raw_input('user: ');
password = raw_input('password: ');
   
#设置cookie，这里cookiejar可自动管理，无需手动指定
cj = cookielib.CookieJar();
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj));
urllib2.install_opener(opener);
reqReturn = urllib2.urlopen(URL_BAIDU_INDEX);
   
#获取token,
tokenReturn = urllib2.urlopen(URL_BAIDU_TOKEN);
token_html = tokenReturn.read()
matchVal = re.search(u'"token" : "(?P<tokenVal>.*?)"',token_html);
tokenVal = matchVal.group('tokenVal');

#print tokenVal

#构造登录请求参数，该请求数据是通过抓包获得，对应https://passport.baidu.com/v2/api/?login请求
postData = {
    'username' : username,
    'password' : password,
    'u' : 'https://passport.baidu.com/',
    'tpl' : 'pp',
    'token' : tokenVal,
    'staticpage' : 'https://passport.baidu.com/static/passpc-account/html/v3Jump.html',
    'isPhone' : 'false',
    'charset' : 'UTF-8',
    'callback' : 'parent.bd__pcbs__ra48vi'
    };
postData = urllib.urlencode(postData);
   
#发送登录请求
loginRequest = urllib2.Request(URL_BAIDU_LOGIN,postData);
loginRequest.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8');
loginRequest.add_header('Accept-Encoding','gzip,deflate,sdch');
loginRequest.add_header('Accept-Language','zh-CN,zh;q=0.8');
loginRequest.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36');
loginRequest.add_header('Content-Type','application/x-www-form-urlencoded');
sendPost = urllib2.urlopen(loginRequest);


#print urllib2.urlopen('https://passport.baidu.com/center?_t=1449154972#3,0').read().decode('utf-8').encode('GBK')

#获取关注的贴吧名字,贴吧主页返回的页面信息就有
tieba_home = urllib2.urlopen('http://tieba.baidu.com/index.html#').read()
re_tieba_info = re.compile(r'"forum_id":(.+?),"forum_name":"(.+?)"')
'''
fw = open('tieba_test.txt','w')
fw.write(tieba_home)
fw.close()
'''
tieba_infos_raw = re.findall(re_tieba_info,tieba_home)
n = len(tieba_infos_raw)
i = 0
BaseTiebaUrl = 'http://tieba.baidu.com/f?kw='
TiebaInfos = []
while i < n/2:
	TiebaInfo = {}
	TiebaInfo['fid'] = tieba_infos_raw[i][0].decode('GBK').encode('utf-8')
	TiebaInfo['name'] = tieba_infos_raw[i][1].decode('GBK').encode('utf-8')
	TiebaInfo['url'] = BaseTiebaUrl + tieba_infos_raw[i][1].decode('GBK').encode('utf-8')
	TiebaInfos.append(TiebaInfo)
	i += 1
#for TiebaUrl in TiebaUrls:
#	print TiebaUrl
#print urllib2.urlopen(TiebaUrls[3]).read()
#print TiebaInfos

#记录成功发帖贴吧数
count = 0 
print len(TiebaInfos)

for TiebaInfo in TiebaInfos:
	#检测今天该吧是否已经发过帖子了
	print '############################'
	print u'正在',TiebaInfo['name'].decode('utf-8').encode('GBK'),u'发帖'
	fr = open('posted.txt','r')
	posted_list = fr.read().split('\n')
	fr.close()
	if TiebaInfo['name'].decode('utf-8').encode('GBK') in posted_list:
		continue
	
	#page = urllib2.urlopen('http://tieba.baidu.com/f?ie=utf-8&kw=eighteen_stars')
	try:
		page = urllib2.urlopen(TiebaInfo['url'])
	except:
		continue
	page = page.read()
	
	#检测该贴吧第一页是否已经有了我的宣传帖子，如果有了进入下一个贴吧
	#ReMyTie = ur'秀色驿站'
	#ReMyTieComp = re.compile(ReMyTie)
	#if re.search(ReMyTieComp,page.decode('utf-8','ignore')):
		#print u'该贴吧首页已经有我们的帖子，去下一个贴吧发帖'
		#continue
	
	#获取所在贴吧tbs
	
	re1 = r'\'tbs\': \"(.+?)\"'
	re1_comp = re.compile(re1)
	re1_result = re.search(re1_comp,page)
	if re1_result:
		tbs = re1_result.group(1)
	else:
		re2 = r'\'tbs\':\'(.+?)\''
		re2_comp = re.compile(re2)
		re2_result = re.search(re2_comp,page)
		if re2_result:
			tbs = re2_result.group(1)
		else:
			re3 = r'tbs = "(.+?)"'
			re3_comp = re.compile(re3)
			re3_result = re.search(re3_comp,page)
			if re3_result:
				tbs = re3_result.group(1)
			else:
				print u'该贴吧找不到tbs,去下一个贴吧发帖'
				continue
	#print tbs
	
		
	#贴吧签到
	PostData = {
		'ie' : 'utf-8',
		'kw' : TiebaInfo['name'],
		'tbs' : tbs	
		}
	PostData = urllib.urlencode(PostData)
	SignRequest = urllib2.Request(URL_BAIDU_SIGN,PostData)
	#我请求头什么都不加看可以不可以
	SignPost = urllib2.urlopen(SignRequest)
	#print u'签到结果：',SignPost.read()
	
	#print page.read()
	
	title = '这腿在吧里算什么水平？'
	content = '一楼看不到哦~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[br][br]  图 视 频 丰 富 [br]百度【xiuseyizhan】[br] '
	#两次发帖，第一次如果需要验证码，就进入验证码逻辑
	form_data = {'ie':'utf-8','kw':TiebaInfo['name'],'fid':TiebaInfo['fid'],'tid':0,'vcode_md5':'','floor_num':0,'rich_text':1,'tbs':tbs,'content':content,'title':title,'prefix':'','files':'[]','mouse_pwd':'6,4,30,7,10,10,11,59,3,30,2,30,3,30,2,30,3,30,2,30,3,30,2,30,3,30,2,59,11,2,11,7,3,59,3,1,4,4,30,5,4,10,14491439810500','mouse_pwd_t':'1449143981050','mouse_pwd_isclick':0,'__type__':'thread'}
	req = urllib2.Request('http://tieba.baidu.com/f/commit/thread/add',urllib.urlencode(form_data))
	req.add_header('Accept','*/*')
	req.add_header('Accept-Encoding','deflate')
	req.add_header('Accept-Language','zh-CN,zh;q=0.8')
	req.add_header('Connection','keep-alive')
	#req.add_header('Content-Length','79')
	req.add_header('Content-Type','application/x-www-form-urlencoded; charset=UTF-8')
	#req.add_header('Cookie','noticeLoginFlag=1; pgv_pvi=1648069632; noticeLoginFlag=1')
	req.add_header('Host','tieba.baidu.com')
	req.add_header('Origin','http://tieba.baidu.com')
	req.add_header('Referer',TiebaInfo['url'])
	req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36')
	req.add_header('X-Requested-With','XMLHttpRequest')
	try:
		ret = urllib2.urlopen(req)
	except:
		print u'打开网页失败，去下一个贴吧'
		continue
	retread = ret.read()
	matchno = re.search(u'"no":(?P<no>.*?),',retread)
	PostResultOne = matchno.group('no')
	
	if PostResultOne == '40':
		while True:
			#retcontent = json.loads(retread)
			matchv = re.search(u'"captcha_vcode_str":"(?P<vcode_md5>.*?)"',retread)
			vcode_md5 = matchv.group('vcode_md5')
			#print vcode_md5

			#构造验证码地址
			url_v = 'http://tieba.baidu.com/cgi-bin/genimg?' + vcode_md5 + '&tag=pc'
			response = urllib2.urlopen(url_v)
			data = response.read()
			f = open('1.jpg','wb')
			f.write(data)
			f.close()
			#验证码有两类要分情况，判断文件大小的方法，以2000为界，小于是汉字码，大于是九宫格
			ImageSize = os.path.getsize('1.jpg')
			if ImageSize < 2000:
				captchaId,damaResult = dama(2004)
				print u'打码结果:',damaResult
				if damaResult == u'看不清'.encode('GBK'):
					continue
				vcode = damaResult.decode('GBK').encode('utf-8')
			else:		
				#计算识别验证码后的vcode
				captchaId,damaResult = dama(6200)
				print u'打码结果:',damaResult
				if damaResult == u'看不清'.encode('GBK'):
					continue
				try:
					vcode = NumToLoc(damaResult)
				except:
					break
			#测试输出
			print vcode

			#得到vcode最后的发帖
			form_data = {'ie':'utf-8','kw':TiebaInfo['name'],'fid':TiebaInfo['fid'],'tid':0,'vcode_md5':vcode_md5,'floor_num':0,'rich_text':1,'tbs':tbs,'content':content,'title':title,'prefix':'','files':'[]','mouse_pwd':'6,4,30,7,10,10,11,59,3,30,2,30,3,30,2,30,3,30,2,30,3,30,2,30,3,30,2,59,11,2,11,7,3,59,3,1,4,4,30,5,4,10,14491439810500','mouse_pwd_t':'1449143981050','mouse_pwd_isclick':0,'__type__':'thread','vcode':vcode}
			req = urllib2.Request('http://tieba.baidu.com/f/commit/thread/add',urllib.urlencode(form_data))
			req.add_header('Accept','*/*')
			req.add_header('Accept-Encoding','deflate')
			req.add_header('Accept-Language','zh-CN,zh;q=0.8')
			req.add_header('Connection','keep-alive')
			#req.add_header('Content-Length','79')
			req.add_header('Content-Type','application/x-www-form-urlencoded; charset=UTF-8')
			#req.add_header('Cookie','noticeLoginFlag=1; pgv_pvi=1648069632; noticeLoginFlag=1')
			req.add_header('Host','tieba.baidu.com')
			req.add_header('Origin','http://tieba.baidu.com')
			req.add_header('Referer',TiebaInfo['url'])
			req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36')
			req.add_header('X-Requested-With','XMLHttpRequest')
			try:
				ret = urllib2.urlopen(req)
			except:
				print u'打开网页失败，去下一个贴吧'
				continue
			retread = ret.read()
			matchno = re.search(u'"no":(?P<no>.*?),',retread)
			ResultNo = matchno.group('no')
			print 'Result: %s' % ResultNo
			if ResultNo == '0':
				print u'发帖成功'
				count += 1
				#写入posted.txt
				f = open('posted.txt','a')
				f.write(TiebaInfo['name'].decode('utf-8').encode('GBK'))
				f.write('\n')
				f.close()
				break
			#打码出错
			elif ResultNo == '40':
				print u'打码出错'
				#调用接口上报
				ReportCode = YDMApi.YDM_EasyReport('testdemo_str','48667063',1981,'a4f912fb73c263d8c50479b6546b3b15',captchaId,False)
				print u'上报错码：',ReportCode
			else:
				print u'发帖失败，未知错误'
				break

	if PostResultOne == '12' or PostResultOne == '308':
		print u'被封禁或权限不够'
		f = open('posted.txt','a')
		f.write(TiebaInfo['name'].decode('utf-8').encode('GBK'))
		f.write('\n')
		f.close()
		continue
	if PostResultOne not in ('12','40','308'):
		print u'发帖成功'
		count += 1
	time.sleep(180)
print u'发帖完毕，成功发帖贴吧数%d' % count;