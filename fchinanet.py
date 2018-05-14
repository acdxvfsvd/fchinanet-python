import urllib2, base64, hashlib, time, json, re, struct

ua = "Mozilla/5.0 (iPhone 84; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.0 MQQBrowser/7.8.0 Mobile/14G60 Safari/8536.25 MttCustomUA/2 QBWebViewType/1 WKType/1"

# input username and password here
username = ""
password = ""
BigTime = 0
auth_header = base64.b64encode('%s:%s' % (username, password))

# get version
url = "http://pre.f-young.cn/js/conf.js"
request = urllib2.Request(url, headers = {"User-Agent" : ua})
response = urllib2.urlopen(request)
text = response.read()
version = re.search('LoochaCollege-[0-9].[0-9].[0-9]-[0-9].+\.apk', text).group()
version = "Android_college_" + re.search('[0-9].[0-9].[0-9]', version).group()
print "[+] Version: %s" % version

# get uid
url = "https://cps.loocha.cn:9607/anony/login?1=" + version
request = urllib2.Request(url, headers = {"User-Agent" : ua, "Authorization": "Basic %s" % auth_header})
response = urllib2.urlopen(request)
text = response.read()
encoded_uid = struct.unpack('<I', text[3:7])[0]
a = encoded_uid >> 24 & 0x7f
b = (encoded_uid & 0x00FF0000) >> 16 & 0x7f
c = (encoded_uid & 0x0000FF00) >> 8 & 0x7f
d = encoded_uid & 0x7f
uid = a * (1 << 21) + b * (1 << 14) + c * (1 << 7) + d
print "[+] Uid: %d" % uid

did = 0
account = username

# get passwd
model = "default"
ts = str(int(time.time() * 1000)) 
if (BigTime):
    ts = "2525780731349"

params = "server_did=%d&time=%s&type=1" % (did, ts)
sign = hashlib.md5("mobile=%s&model=%s&%s" % (account, model, params)).hexdigest().upper()
url = "https://wifi.loocha.cn/%d/wifi/telecom/pwd?1=%s&mm=%s&%s&sign=%s" % (uid, version, model, params, sign)
request = urllib2.Request(url, headers = {"User-Agent" : ua, "Authorization": "Basic %s" % auth_header})
response = urllib2.urlopen(request)
text = response.read()
res_json = json.loads(text)

wifi_passwd = res_json['telecomWifiRes']['password']
print "[+] Wifi passwd: %s" % wifi_passwd

# get ip
class NoRedirection(urllib2.HTTPErrorProcessor):
    def http_response(self, request, response):
        return response
    https_response = http_response

opener = urllib2.build_opener(NoRedirection)
url = "http://test.f-young.cn"
request = urllib2.Request(url, headers = {"User-Agent" : ua, "Authorization": "Basic %s" % auth_header})
response = opener.open(request)
text = response.headers['Location']
ips = re.findall(r'\d+\.\d+\.\d+\.\d+', text)
wanip = ips[1]
brasip = ips[2]

print "[+] Wan IP: %s" % wanip
print "[+] Bras IP: %s" % brasip

# get qrcode 
url = "https://wifi.loocha.cn/%d/wifi/qrcode?1=%s&brasip=%s&ulanip=%s&wlanip=%s&mm=default" % (uid, version, brasip, wanip, wanip)
request = urllib2.Request(url, headers = {"User-Agent" : ua, "Authorization": "Basic %s" % auth_header})
response = urllib2.urlopen(request)
text = response.read()
qrcode = re.search('HIWF://[a-z0-9]{32}', text).group()
print "[+] QR Code: %s" % qrcode

# login
ts = str(int(time.time() * 1000)) 
if (BigTime):
    ts = "2525780731349"
params = "server_did=%d&time=%s&type=1" % (did, ts)
sign = hashlib.md5(("mobile=%s&model=%s&" % (account, model)) + params).hexdigest().upper()
url = ("https://wifi.loocha.cn/%d/wifi/telecom/auto/login?" % uid) + ("1=%s&qrcode=%s&code=%s&mm=%s&%s&sign=%s" % (version, qrcode, wifi_passwd, model, params, sign))
request = urllib2.Request(url, "1=%s&qrcode=%s&code=%s&mm=%s&%s&sign=%s" % (version, qrcode, wifi_passwd, model, params, sign), headers = {"User-Agent" : ua, "Authorization": "Basic %s" % auth_header})
response = urllib2.urlopen(request)
text = response.read()
print text
