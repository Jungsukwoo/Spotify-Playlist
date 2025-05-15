import os
import requests
import json
from dotenv import load_dotenv
from time import sleep
from core.crawler.article_extractor import extract_article_body

def run_crawler():
    load_dotenv()

    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")

    query = "트럼프"
    display_count = 10
    url = f"https://openapi.naver.com/v1/search/news.json?query={query}&display={display_count}&sort=date"

    headers = {
        "X-Naver-Client-Id": CLIENT_ID,
        "X-Naver-Client-Secret": CLIENT_SECRET
    }

    response = requests.get(url, headers=headers)
    news_data = []

    if response.status_code == 200:
        items = response.json()["items"]

        for idx, item in enumerate(items, 1):
            title = item["title"]
            link = item["link"]

            if "n.news.naver.com" not in link:
                continue

            print(f"\n[{idx}] {title}\n🔗 {link}")

            content = extract_article_body(link)
            print(f"📄 본문 요약: {content[:100]}...")

            news_data.append({
                "title": title,
                "url": link,
                "content": content
            })

            sleep(1.0)

        # ✅ 항상 최상위 Haneeum_crawling/data 에 저장
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        output_dir = os.path.join(BASE_DIR, "data")
        os.makedirs(output_dir, exist_ok=True)

        output_path = os.path.join(output_dir, "news_data.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(news_data, f, ensure_ascii=False, indent=2)

        print(f"\n✅ 저장 완료: {output_path}")
    else:
        print(f"❌ API 요청 실패: {response.status_code}")
        