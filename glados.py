import requests,json,os
# -------------------------------------------------------------------------------------------
# github workflows
# -------------------------------------------------------------------------------------------
if __name__ == '__main__':
# pushplus秘钥 申请地址 http://www.pushplus.plus
    sckey = os.environ.get("PUSHPLUS_TOKEN", "")
# 推送内容
    sendContent = ''
# glados账号cookie 直接使用数组 如果使用环境变量需要字符串分割一下
    cookies = os.environ.get("GLADOS_COOKIE", []).split("&")
    if cookies[0] == "":
        print('未获取到COOKIE变量') 
        cookies = []
        exit(0)
    url= "https://glados.rocks/api/user/checkin"
    url2= "https://glados.rocks/api/user/status"
    referer = 'https://glados.rocks/console/checkin'
    origin = "https://glados.rocks"
    useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
    payload={
        'token': 'glados.one'
    }
    for cookie in cookies:
        try:
            checkin = requests.post(url,headers={'cookie': cookie ,'referer': referer,'origin':origin,'user-agent':useragent,'content-type':'application/json;charset=UTF-8'},data=json.dumps(payload))
            state =  requests.get(url2,headers={'cookie': cookie ,'referer': referer,'origin':origin,'user-agent':useragent})
        #--------------------------------------------------------------------------------------------------------#  
            # 检查API响应中是否包含必要的数据
            response_data = state.json()
            if 'data' not in response_data or 'leftDays' not in response_data['data'] or 'email' not in response_data['data']:
                print('API响应数据不完整，跳过此账号')
                continue
                
            time = response_data['data']['leftDays']
            # 确保time不为None且可以转换为字符串
            if time is None:
                print('leftDays数据为空，跳过此账号')
                continue
            time = str(time).split('.')[0]
            email = response_data['data']['email']
            if 'message' in checkin.text:
                mess = checkin.json()['message']
                print(email+'----结果--'+mess+'----剩余('+time+')天')  # 日志输出
                sendContent += email+'----'+mess+'----剩余('+time+')天\n'
            else:
                requests.get('http://www.pushplus.plus/send?token=' + sckey + '&content='+email+'cookie已失效')
                print('cookie已失效')  # 日志输出
        except:
            print(email+'----签到失败')  # 日志输出
     #--------------------------------------------------------------------------------------------------------#   
    if sckey != "":
         requests.get('http://www.pushplus.plus/send?token=' + sckey + '&title='+email+'签到成功'+'&content='+sendContent)

