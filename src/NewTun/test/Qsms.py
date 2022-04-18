from qcloudsms_py import SmsSingleSender
from qcloudsms_py.httpclient import HTTPError
import ssl

# 短信应用SDK AppID
appid = 1400218666  # SDK AppID是1400开头
# 短信应用SDK AppKey
appkey = "414c40f8dcd85a9806db3be68ecde570"
# 需要发送短信的手机号码
phone_numbers = ["15652466911"]

# 短信模板ID，需要在短信应用中申请
template_id = 1285045
# template_id = 351072

# 签名
sms_sign = "程序科学"
ssl._create_default_https_context = ssl._create_unverified_context
ssender = SmsSingleSender(appid, appkey)
params = ["000009.sz","15.56-买入"]  # 当模板没有参数时，`params = []`
try:
    result = ssender.send_with_param(86, phone_numbers[0],template_id, params, sign=sms_sign, extend="", ext="")  # 签名参数不允许为空串
    print("-------------------发送成功--------------------")
except HTTPError as e:
    print(e)
except Exception as e:
    print(e)