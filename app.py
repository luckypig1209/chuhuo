#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import requests
import os, sys
import json
# import time
import yagmail
import subprocess

from flask import Response, Flask, jsonify, redirect, url_for, request, render_template, make_response

from concurrent.futures import ThreadPoolExecutor 
executor = ThreadPoolExecutor(1) 

app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False

# 本脚本 要求有如下信息
# 管理员的tenantSid，账户和密码
# 普通用户的 用户名  ，密码， 邮箱
# 普通用户的 用户名 的密码 ，可以用默认


# 获取url中 参数
# {
# "companyName": "二部自测7",
# "email": "zhangyug@digiwin.com",
# "name": "test7",
# "phone": "13801111111"
# }


# 测试
 

# tbbcn免费试用

#tenantSid = "192093419516480"
tenantId = "tbbtryout"
superuser = "tbbmail01" 
superpasswd = "tbbmail01"
superpasswd_ha = "9dOzS9wuImUtN5fmvfGeLw=="
ha_key = "RqxQmX4J89t/xMCiefzKKOmbIBit1htXIw+uUk2EJInnXfCIhC+EmH5PA17E4AeQLOGp31uLwyZjtEgQvjRKrDUbCyTeqZPRLJKVvETmkdbamVKHGv3eaFKXGmIKLijBx9djiR+yd67IUlrzDIiksFoQrZWcNyse3JuM++9TynQ2KDL27oH2sIkNG/EJapalz7D2wE/sNbLL3eGg/SWn+ZlK1Le6HDW7KHXP329bEjLxOazf4VZYQ1m2Yp3AQLXWqlHYedreZjf5iNymHY9Jx+i8C5hJP9qCHit3ceoO/6bobFRO89wNd+BqJ35PntqCFTpYbh7pzYoVpxLO/sUNVg=="

def send_iam_test():
        if request.method == 'POST':
            data = request.get_data()
            json_data = json.loads(data.decode("utf-8"))
            global name
            name = json_data.get("name")
            global companyName
            companyName = json_data.get("companyName")
            global user_email
            user_email = json_data.get("email")
            user_phone = json_data.get("phone")
            global register_name            
            register_name = str(name)
            register_companyName = str(companyName)
            global register_email
            register_email = str(user_email)
            register_phone = str(user_phone)


# 1邮箱帐号注册
# http://172.16.2.141:22694/html/web/controller/console/console.html

            #url1 = 'https://iam-test.digiwincloud.com.cn/api/iam/v2/user/register'
            url1 = 'https://iam-test.digiwincloud.com.cn/api/iam/v2/user/register/without/captcha'
            digi_app = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1MzczMjY2ODk0NjEsInNpZCI6NDA3MTI4ODI1NTM0NDY0MSwiaWQiOiJEaWdpd2luQ2xvdWQifQ.XGPl3brNeNTCivWN_bIYj8TfcxqlkQ0sFV2woPOr0TY'
            body1 = {"Id": register_email, "name": register_name, "telephone": register_phone, "cellphonePrefix": "mock", "email": register_email, "password": "czw123456"} 
            headers1 = {'Content-Type': 'application/json;charset=UTF-8', "digi-middleware-auth-app":digi_app}
            global req1
            req1 = requests.post(url=url1, headers=headers1, json=body1)
            # 'message': ' Id为已被注册  该邮箱账号已经注册 '
            # 判断 message里面是否有已经注册

 

 

def yaoqing():
##超管登录
            digi_app = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1MzczMjY2ODk0NjEsInNpZCI6NDA3MTI4ODI1NTM0NDY0MSwiaWQiOiJEaWdpd2luQ2xvdWQifQ.XGPl3brNeNTCivWN_bIYj8TfcxqlkQ0sFV2woPOr0TY'
            url51 = 'https://iam-test.digiwincloud.com.cn/api/iam/v2/identity/login'
            body51 = {"userId": superuser, "passwordHash": superpasswd_ha, "clientEncryptPublicKey": ha_key}
            headers51 = {'Content-Type': 'application/json;charset=UTF-8', "digi-middleware-auth-app":digi_app}
            req51 = requests.post(url=url51, headers=headers51, json=body51)

            token51 = req51.json()['token']

            global user_email

            url10 = 'https://iam-test.digiwincloud.com.cn/api/iam/v2/tenant/user/invite'

            body10 = {
    "user": user_email,
    "content": "竭誠邀請您加入使用鼎新雲平台,请登录https://market-test.digiwincloud.com.cn/ ，进入雲控制台，同意加入我们的企业。",
    "org": [

    ],
    "app": [
        {
            "id": "TipBiuBI",
            "sid": 0,
            "name": "敏捷BI-Tip Biu BI"
        }
    ],
    "role": [
        {
            "id": "superadmin",
            "sid": 174370702258752,
            "name": "超级管理員"
        }
    ]
}

            headers10 = {'Content-Type': 'application/json;charset=UTF-8', "digi-middleware-auth-app":digi_app, 'digi-middleware-auth-user': token51}
            req10 = requests.post(url=url10, headers=headers10, json=body10)


def add_iam():
            global register_email
            global register_name
            global name
            global companyName
            global user_email
            
###用户加入企业            
            global req1
            token = req1.json()['token']
            digi_app = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1MzczMjY2ODk0NjEsInNpZCI6NDA3MTI4ODI1NTM0NDY0MSwiaWQiOiJEaWdpd2luQ2xvdWQifQ.XGPl3brNeNTCivWN_bIYj8TfcxqlkQ0sFV2woPOr0TY'
            url6 = 'https://iam-test.digiwincloud.com.cn/api/iam/v2/user/tenant/apply'
            body6 = {"tenantId": tenantId, "content": ""}
            headers6 = {'Content-Type': 'application/json;charset=UTF-8', "digi-middleware-auth-app":digi_app, 'digi-middleware-auth-user': token}
            req6 = requests.post(url=url6, headers=headers6, json=body6)
            print("第一步")
            # 3企業管理员 登录-得-token---注意是企業管理员的token
            # 注意token 会过期，需要登录一下，取得新token
            # digi-middleware-auth-app 是固定的
            #digi_app = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1MzczMjY2ODk0NjEsInNpZCI6NDA3MTI4ODI1NTM0NDY0MSwiaWQiOiJEaWdpd2luQ2xvdWQifQ.XGPl3brNeNTCivWN_bIYj8TfcxqlkQ0sFV2woPOr0TY'
            url5 = 'https://iam-test.digiwincloud.com.cn/api/iam/v2/identity/login'
            body5 = {"userId": superuser, "passwordHash": superpasswd_ha, "clientEncryptPublicKey": ha_key}
            headers5 = {'Content-Type': 'application/json;charset=UTF-8', 'digi-middleware-auth-app':digi_app}
            req5 = requests.post(url=url5, headers=headers5, json=body5)
            print("第二步")
            token5 = req5.json()['token']
            # print (req5.json())
            # 4  查询所有未审批的申請用戶清單   ----取得邀请记录中的用户 --对应的sid  -下面流程要用
            #
            url11 = 'https://iam-test.digiwincloud.com.cn/api/iam/v2/tenant/user/apply/query'
            headers11 = {'Content-Type': 'application/json;charset=UTF-8', "digi-middleware-auth-app":digi_app,  'digi-middleware-auth-user': token5}
            req11 = requests.post(url=url11, headers=headers11)
            print("第三步")
            lt = eval(req11.text)
            print(lt)
            for i in lt:
                  for key in i:
                        if i[key] == register_name and key == 'userName':
                              yaoqing_sid = i['sid']
                              # print(yaoqing_sid)

            # 5企業同意用戶申請
            url7 = 'https://iam-test.digiwincloud.com.cn/api/iam/v2/tenant/agree/apply'
            body7 = {"sid": yaoqing_sid}
            headers7 = {'Content-Type': 'application/json;charset=UTF-8', "digi-middleware-auth-app":digi_app, 'digi-middleware-auth-user': token5}
            req7 = requests.post(url=url7, headers=headers7, json=body7)
            print("第四步")

# 更新角色

            url8 = 'https://iam-test.digiwincloud.com.cn/api/iam/v2/user/update/allinfo'

            body8 = {
    "user": {
        "id": register_email,
        "name": register_name
    },
    "metadata": [],
    "role": [
        {
            "catalogId": "administrators",
            "id": "superadmin"
        }
    ],
    "userInOrg": [

    ],
    "defaultOrg": [

    ],
    "userInTag": [

    ]
}

            headers8 = {'Content-Type': 'application/json;charset=UTF-8', "digi-middleware-auth-app":digi_app, 'digi-middleware-auth-user': token5}
            req8 = requests.post(url=url8, headers=headers8, json=body8)
            print("第五步")
#   给用戶授权

            url9 = 'https://cac-test.digiwincloud.com.cn/api/cac/v4/counting/user/add'

            body9 = {"countingId": "TipBiuBI", "tenantId":tenantId, "userId": user_email}

            headers9 = {'Content-Type': 'application/json;charset=UTF-8', "digi-middleware-auth-app":digi_app}
            req9 = requests.post(url=url9, headers=headers9, json=body9)
            print("第六步")
# 发邮件--
def mail():
            global companyName
            global user_email    
            yag = yagmail.SMTP(user="tipbiubi@digiwin.com", password="bItIpbI2020888", host='dwm6.digiwin.com')

            # 邮箱正文
            html = """
<table>
	<tbody>
		<tr>
			<td>
				<img class="mail-Mbanner image_zoomin" src="https://escloud.digiwincloud.com/static/zh-CN/file/header.jpg" style="height:40px;border:none;" title="" alt="" width="900" height="45" align="" /> 
			</td>
		</tr>
		<tr>
			<td>
				<span style="font-family:微软雅黑;font-size:16px;">【Tip&nbsp;Biu&nbsp;BI<span class="tlid-translation translation">免费试用通知</span>】</span> 
			</td>
		</tr>
		<tr>
			<td>
				<p class="MsoNormal" style="text-align:left;">
					<span style="font-family:微软雅黑;font-size:12.0000pt;">%s</span><span style="font-family:微软雅黑;font-size:12.0000pt;">&nbsp;<span>企<span class="tlid-translation translation">业</span>您好</span>:</span><span style="font-family:微软雅黑;font-size:12.0000pt;"></span> 
				</p>
				<p class="MsoNormal" style="text-align:left;">
					<span style="font-family:微软雅黑;font-size:12.0000pt;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span><span class="tlid-translation translation">感谢您对鼎捷产品的支持与爱护.</span></span></span><span style="font-family:微软雅黑;font-size:12.0000pt;"></span> 
				</p>
				<p class="MsoNormal" style="text-align:left;">
					<span style="font-family:微软雅黑;font-size:12.0000pt;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span><span class="tlid-translation translation">您申请的Tip Biu BI网址为</span></span>：<a href="https://bi-demo-cn.apps.digiwincloud.com.cn/index.html#/account/login" target="_blank">https://bi-demo-cn.apps.digiwincloud.com.cn/index.html#/account/login</a></span><span style="font-family:微软雅黑;font-size:12.0000pt;"></span> 
				</p>
				<p class="MsoNormal" style="text-indent:24.0000pt;text-align:left;">
					<span style="font-family:微软雅黑;font-size:12.0000pt;"><span><span class="tlid-translation translation">登入的帐号是：%s 密码是</span></span></span><span style="font-family:微软雅黑;font-size:12.0000pt;"><span>：</span>czw123456</span><span style="font-family:微软雅黑;font-size:12.0000pt;"></span><span style="font-family:微软雅黑;font-size:12.0000pt;"><br />
</span> 
				</p>
				<p class="MsoNormal" style="text-indent:24.0000pt;text-align:left;">
					<span style="font-family:微软雅黑;font-size:12.0000pt;">账号和密码即日生效，有效期限为30天。</span>
				</p>
				<p class="MsoNormal" style="text-indent:24.0000pt;text-align:left;">
					<span style="font-family:微软雅黑;font-size:12.0000pt;"><br />
</span> 
				</p>
				<p class="MsoNormal" style="text-indent:24.0000pt;text-align:left;">
					<span style="font-family:微软雅黑;font-size:12.0000pt;"><span><span class="tlid-translation translation">参考视频:<a href="https://escloud.digiwincloud.com/static/zh-CN/video/5_9.mp4" target="_blank">上传Excel报表到TBB</a><br />
</span></span></span>
				</p>
				<p class="MsoNormal" style="text-indent:24.0000pt;text-align:left;">
					<span style="font-family:微软雅黑;font-size:12.0000pt;"><span><span class="tlid-translation translation">请用chrome浏览器打开上述网址链接。<br />
</span></span></span>
				</p>
				<p class="MsoNormal" style="text-indent:24.0000pt;text-align:left;">
					<span style="font-family:微软雅黑;font-size:12.0000pt;"><span><span class="tlid-translation translation"><br />
</span></span></span> 
				</p>
				<p>
					<br />
				</p>
			</td>
		</tr>
		<tr>
			<td>
				<span style="font-family:微软雅黑;font-size:16px;">&nbsp; &nbsp;<span class="tlid-translation translation">顺祝商祺</span></span> 
			</td>
		</tr>
		<tr>
			<td>
				<span style="font-family:微软雅黑;font-size:16px;">&nbsp; &nbsp;<span class="tlid-translation translation">鼎捷云团队敬上</span></span> 
			</td>
		</tr>
		<tr>
			<td>
				<div>
				</div>
<br />
			</td>
		</tr>
		<tr>
			<td>
				<span style="font-family:微软雅黑;font-size:16px;"><a href="https://market.digiwincloud.com.cn/email-consultation">&nbsp; &nbsp;※ <span class="tlid-translation translation">此信件为系统发出信件，请勿直接回覆。若您有相关问题请至网站「咨询回馈」提出，谢谢！</span></a></span> 
			</td>
		</tr>
		<tr>
			<td>
				<span style="font-family:微软雅黑;font-size:16px;">&nbsp;&nbsp; 鼎捷云市场：<a href="">https://market.digiwincloud.com.cn/</a></span> 
			</td>
		</tr>
		<tr>
			<td>
				<span style="font-family:微软雅黑;font-size:16px;">&nbsp; &nbsp;鼎捷软件股份有限公司|上海市静安区江场路1377弄1号楼</span> 
			</td>
		</tr>
		<tr>
			<td>
				&nbsp;&nbsp;&nbsp; <img src="https://dmc.digiwincloud.com.cn/api/dmc/v1/buckets/digiwincloud/shareFiles/files/7c24a441-8caf-4a7b-972a-92b3b7f92929/toAnyOne" alt="" title="" width="900" height="35" align="" /><br />
			</td>
		</tr>
	</tbody>
</table>
""" % (companyName, user_email)

            ##
            to1 = user_email
            # 林秀蓉
            to6 = 'keran@digiwin.com'
            to7 = 'xili@digiwin.com'
            to10 = 'huangad@digiwin.com'
            to11 = 'zhoudao@digiwin.com'
            to12 = 'wangkang0305@digiwin.com' 
            to13 = 'zhuhr@digiwin.com'         
            subject = '* 鼎捷_Tip Biu BI免费试用通知'
            contents=[html]
            # 发送邮件
            yag.send(to=[to13], subject=subject, contents=contents, newline_to_break=False)
            yag.close()
            print ('邮件发送成功') 
########
@app.route('/topbicn/api/email', methods=['POST'])
def sendmail():
        send_iam_test()
        global req1
        alljson = req1.json()
        print(alljson)
        if ('message' in alljson):
            message2 = req1.json()['message']
           # if ('被注册' in message2):
           #       return '此用户名已被注册,请更换用户名'
            if ('该邮箱账号已经注册' in message2):
                  yaoqing()
                  return '此邮箱之前已被注册过了,已经发您邮件了，邀请您加入使用鼎新云平台,请登录https://market-test.digiwincloud.com.cn，进入云控制台，同意加入我们的企业 。或者更换邮箱，重新注册。'
            if ('该手机号已经注册' in message2):
                  yaoqing()
                  return '此手机号之前已被注册过了,已经发您邮件了，邀请您加入使用鼎新云平台,请登录https://market-test.digiwincloud.com.cn，进入云控制台，同意加入我们的企业 。或者更换邮箱，重新注册。'
            if ('公司内部账号' in message2):
                  return '公司内部邮箱,禁止使用,请更换邮箱'                  
        else:
            executor.submit(addid_email)
            print("进入到else")
        #response = make_response(jsonify({'注册': '成功'}))
        #return response, 200
        return "ok", 200

def addid_email():
        add_iam()
        mail()
        print ("部署完成")
if __name__ == '__main__':
#      app.run(port=7000, debug=True)
      sendmail()

