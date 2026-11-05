import json
import requests
from modules.load_config import dprint
from datetime import datetime, timedelta


# 查用户是否已经打卡
def check_sign(check_sign_token, sign_type):
    check_sign_url = "https://api.moguding.net:9000/attendence/clock/v2/listSynchro"
    search_start_time, search_end_time = get_current_day()
    data = {
        "startTime": search_start_time,
        "endTime": search_end_time,
    }
    headers = {"Authorization": f"{check_sign_token}"}
    response = requests.post(check_sign_url, json=data, headers=headers)
    response_data = response.json()
    print("[DEBUG] 打卡记录查询原始返回: %s" % json.dumps(response_data, ensure_ascii=False))

    if "data" not in response_data:
        print("[DEBUG] 打卡记录查询返回中没有 data 字段，token 可能无效或接口异常")
        return False
    for record in response_data["data"]:
        if record["type"] == sign_type:
            return True
    return False


# 获取当天起始时间
def get_current_day():
    now = datetime.now()
    start_of_day = datetime(now.year, now.month, now.day)
    end_of_day = start_of_day + timedelta(days=1, seconds=-1)
    day_start_time = start_of_day.strftime("%Y-%m-%d 00:00:00")
    day_end_time = end_of_day.strftime("%Y-%m-%d 23:59:59")
    return day_start_time, day_end_time
