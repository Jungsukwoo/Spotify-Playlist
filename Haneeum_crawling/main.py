import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.crawler.naver_api import run_crawler

if __name__ == "__main__":
    run_crawler()