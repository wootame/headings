import sys
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def fetch_headings_in_order(url: str) -> list[tuple[int, str]]:
    """
    ページ内の h1〜h6 を順番通りに抽出して、
    (見出しレベル, テキスト) のリストで返す
    """
    try:
        # 一度だけリクエストを送る
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to fetch {url}: {e}")
        return []

    # レスポンスをパース
    soup = BeautifulSoup(resp.content, "lxml")

    # h1〜h6 のタグ名リスト
    tags = ['h1','h2','h3','h4','h5','h6']

    headings = []
    for tag in soup.find_all(tags):
        level = int(tag.name[1])  # 'h2' -> 2
        text = tag.get_text(strip=True)
        if text:
            headings.append((level, text))
    return headings

def save_headings_markdown(url: str, headings: list[tuple[int, str]]) -> None:
    out_dir = "sites"
    os.makedirs(out_dir, exist_ok=True)

    domain = urlparse(url).netloc.replace(":", "_") or "output"
    filepath = os.path.join(out_dir, f"{domain}.md")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# Headings from: {url}\n\n")
        for level, text in headings:
            indent = "  " * (level - 1)
            f.write(f"{indent}- H{level}: {text}\n")

    print(f"[INFO] Markdown出力ファイル: {filepath}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("使い方: python headings.py <URL>")
        sys.exit(1)

    url = sys.argv[1]
    print(f"\n=== Headings from: {url} ===")

    headings = fetch_headings_in_order(url)
    for level, text in headings:
        indent = "  " * (level - 1)
        print(f"{indent}- H{level}: {text}")

    save_headings_markdown(url, headings)
