# -*- coding: utf-8 -*-
"""
@date: 2020/4/30 2:49 下午
@desc：
    获取HTTP签名和发送HTTP请求Demo
    content-type: application/json
    python版本 > 3.0
 
"""
import uuid
import base64
import hmac
import time
import requests
import json
 
from hashlib import sha1
from urllib.parse import quote
from requests.exceptions import RequestException
import lpAccount # 存密钥的文件
 
 
class ApplicationJsonRequest(object):
    def __init__(self, url, url_params, body_params, access_key_id, access_key_secret):
 
        # 设置请求头content-type
        self.headers = {'content-type': "application/json"}
 
        # 请求URL，请替换自己的真实地址
        self.url = url
 
        # 填写自己AK
        # 获取AK教程：https://openai.100tal.com/documents/article/page?fromWhichSys=admin&id=27
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret
 
        # 根据接口要求，填写真实Body参数。key1、key2仅做举例
        self.body_params = body_params
 
        # 根据接口要求，填写真实URL参数。key1、key2仅做举例
        self.url_params = url_params
 
    @property
    def timestamp(self):
        # 获取当前时间（东8区）
        return time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())
 
    @staticmethod
    def url_format(params):
        """
        # 对params进行format
        # 对 params key 进行从小到大排序
        :param params: dict()
        :return:
        a=b&c=d
        """
 
        sorted_parameters = sorted(params.items(), key=lambda d: d[0], reverse=False)
 
        param_list = ["{}={}".format(key, value) for key, value in sorted_parameters]
 
        string_to_sign = '&'.join(param_list)
        return string_to_sign
 
    def _generate_signature(self, parameters, access_key_secret):
 
        # 计算证书签名
        string_to_sign = self.url_format(parameters)
 
        #  进行base64 encode
        secret = access_key_secret + "&"
        h = hmac.new(secret.encode('utf-8'), string_to_sign.encode('utf-8'), sha1)
        signature = base64.b64encode(h.digest()).strip()
        signature = str(signature, encoding="utf8")
        return signature
 
    def get_signature(self):
 
        self.url_params['access_key_id'] = self.access_key_id
        self.url_params['timestamp'] = self.timestamp
 
        # 组合URL和Body参数，并计算签名
        self.url_params['signature_nonce'] = str(uuid.uuid1())
 
        sign_param = {
            "request_body": json.dumps(self.body_params)
        }
        sign_param.update(self.url_params)
 
        signature = self._generate_signature(sign_param, self.access_key_secret)
 
        self.url_params['signature'] = quote(signature, 'utf-8')
 
 
    def run(self):
        # 生成签名
        self.get_signature()
 
        # 生成URL
        url = self.url + '?' + self.url_format(self.url_params)
        # 响应结果httpResponse
        try:
            response = requests.post(url, json=self.body_params, headers=self.headers)
            result = response.text
        except RequestException as e:
            result = str(e)
        print(result)
        return result
 
 
def main():
    url = "http://openai.100tal.com/aiimage/common-formula-reg"
    
    f = open('1.png', 'rb')
    base64_data = base64.b64encode(f.read())	# base64编码
    f.close()
    base64_data = base64_data.decode()

    url_params = dict()
    # 根据接口要求，填写真实URL参数。key1、key2仅做举例
    body_params = {
        # "image_url": ["http://xxxxxxx.com/xxx.jpg"],

        "image_base64": [base64_data],

        # "image_stroke": [[], {}],

        "reg_flag": 0,

        "type": 1
    }
 
    access_key_id = lpAccount.hwlPlt["access_key_id"]
    access_key_secret = lpAccount.hwlPlt["access_key_secret"]
 
    ApplicationJsonRequest(url=url, access_key_id=access_key_id, access_key_secret=access_key_secret,
                           body_params=body_params, url_params=url_params).run()
 
 
if __name__ == '__main__':
    main()