import requests
import time
import random

# 闯关通过接口
URL_GAME_OVER = "https://cat-match.easygame2021.com/sheep/v1/game/game_over?rank_score={}&rank_state={}&rank_time={}&rank_role=1&skin={}"
# 话题挑战结束接口
URL_TOPIC_OVER = "https://cat-match.easygame2021.com/sheep/v1/game/topic_game_over?rank_score={}&rank_state={}&rank_time={}&rank_role=1&skin={}"

REQ_HEADER = {
    "Host": "cat-match.easygame2021.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI MiniGame WindowsWechat",
    "t": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTQ0NDM1MjgsIm5iZiI6MTY2MzM0MTMyOCwiaWF0IjoxNjYzMzM5NTI4LCJqdGkiOiJDTTpjYXRfbWF0Y2g6bHQxMjM0NTYiLCJvcGVuX2lkIjoiIiwidWlkIjo2Mjk1MDIyMCwiZGVidWciOiIiLCJsYW5nIjoiIn0.0ARK6n9W-J6bUjcEH2r6VXu0OhAuOZX-MZ_UgpyjI24",
    "Referer": "https://servicewechat.com/wx141bfb9b73c970a9/17/page-frame.html",
    "Accept-Encoding": "gzip,compress,br,deflate"
}

def parse_req(url):
    resp_game = requests.get(url, timeout=25, verify=True, headers=REQ_HEADER).json()
    print(resp_game)
    if resp_game["err_code"] == 0:
        print("==== pass stage successfully! ====")
    else:
        print("==== request failed! ====")

if __name__ == '__main__':
    count = 0
    while count < 500:
        url_game_over = URL_GAME_OVER.format(1, 1, 20 * 60, 1)
        url_topic_over = URL_TOPIC_OVER.format(1, 1, 20 * 60, 1)
        parse_req(url_game_over)
        time.sleep(random.randint(10, 25))
        parse_req(url_topic_over)
        time.sleep(random.randint(15, 60))
        count = count + 1
