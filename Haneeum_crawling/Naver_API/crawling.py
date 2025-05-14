import os
import requests
import json

from dotenv import load_dotenv

load_dotenv()

# 네이버 API 인증 정보
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

# 검색할 키워드
query = '한동훈'
display_count = 10  # 원하는 수
url = f"https://openapi.naver.com/v1/search/news.json?query={query}&display={display_count}&sort=date"

# 요청 헤더 설정
headers = {
    'X-Naver-Client-Id': CLIENT_ID,
    'X-Naver-Client-Secret': CLIENT_SECRET
}

# 요청 보내기
response = requests.get(url, headers=headers)

# 결과 출력
if response.status_code == 200:
    items = response.json()['items']
    for idx, item in enumerate(items, 1):
        print(f"[{idx}] {item['title']} ({item['link']})")
else:
    print(f"Error Erruption: {response.status_code}")
    