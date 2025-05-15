from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests
import json
import os

# config 경로 기준으로 로드
CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config", "all_domains.json")

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = json.load(f)

DOMAIN_SELECTORS = config.get("domain_selectors", {})

def extract_article_body(url: str) -> str:
    domain = urlparse(url).netloc

    if domain != "n.news.naver.com":
        return "❌ 지원하지 않는 도메인입니다"

    try:
        res = requests.get(url, timeout=5, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(res.text, "html.parser")

        selector = DOMAIN_SELECTORS.get(domain, "#dic_area")
        tag = soup.select_one(selector)

        if tag:
            return tag.get_text("\n", strip=True)
        else:
            return "본문 크롤링 실패 (선택자 일치 없음)"

    except Exception as e:
        return f"❌ 크롤링 오류: {str(e)}"