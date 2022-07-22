from aip import AipSpeech
import requests
import json
import speech_recognition as sr
import win32com.client

# 1、人类说出问题，生成问题音频
speaker = win32com.client.Dispatch("SAPI.SpVoice")


def my_record(rate=16000):
    r = sr.Recognizer()
    with sr.Microphone(sample_rate=rate) as source:
        print("please say something")
        audio = r.listen(source)

    with open("voices.wav", "wb") as f:
        f.write(audio.get_wav_data())

# 2、问题音频文件转成问题文本
#    导入我们需要的模块，然后将音频文件发送出去，返回文本
#    百度语音识别API配置参数
APP_ID = '26753878'
API_KEY = 'mrTf1OIeCzAEcFGYiBpZyZIb'
SECRET_KEY = 'R6j78mANnhZFwvzcziqswu5ElpGmVDts'
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
path = "voices.wav"


# 将语音转文本STT
def listen():
    with open(path, 'rb') as fp:
        voices = fp.read()
    try:
        result = client.asr(voices, 'wav', 16000, {'dev_pid': 1537, }) # 'dev_pid'参数1537是识别普通话，也可以设置成其他语言，详情见百度AI开放平台
        result_text = result["result"][0]
        print("you said: " + result_text)
        return result_text
    except KeyError:
        print("KeyError")
        speaker.Speak("我没有听清楚，请再说一遍...")


# 3、与机器人对话：调用的是图灵机器人
#    图灵机器人的API_KEY、API_URL配置
turing_api_key = "266e2f13a14a4bd3a1318b97710ed2ca"
api_url = "http://openapi.tuling123.com/openapi/api/v2"  # 图灵机器人api网址
headers = {'Content-Type': 'application/json;charset=UTF-8'}


# 图灵机器人回复
def Turing(text_words=""):
    req = {
        "reqType": 0,
        "perception": {
            "inputText": {
                "text": text_words
            },

            "selfInfo": {
                "location": {
                    "city": "扬州",  # 必须有的参数
                    "province": "可有可无的参数",
                    "street": "可有可无的参数"
                }
            }
        },
        "userInfo": {
            "apiKey": turing_api_key,  # 你的图灵机器人apiKey
            "userId": "Stephanie"  # 用户唯一标识（随便填，非密钥）
        }
    }

    req["perception"]["inputText"]["text"] = text_words
    response2 = requests.request("post", api_url, json=req, headers=headers)
    response_dict = json.loads(response2.text)

    result = response_dict["results"][0]["values"]["text"]
    print("AI Robot said:" + result)
    return result


while True:
    my_record()
    request1 = listen()
    response = Turing(request1)
# 4、回复文本转成回复音频输出，回复问题
    speaker.Speak(response)
