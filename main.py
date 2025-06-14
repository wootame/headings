import os
import sys
import requests
from bs4 import BeautifulSoup

URL_LIST_FILE = "sites.txt"
WORKSPACE_DIR = "workspace"

# ファイルからURLリストを読み込む
def read_urls_from_file(path: str) -> list[str]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[ERROR] URLリストファイルが見つかりません: {path}")
        sys.exit(1)

# ページ内の h1〜h6 を順番通りに抽出して、(見出しレベル, テキスト) のリストで返す
# また、<title> タグの内容をタイトルとして返す（なければ空文字列）
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

    # タイトル取得（なければ空文字）
    title_tag = soup.title
    title = title_tag.string.strip() if title_tag and title_tag.string else ""

    # h1〜h6 のタグ名リスト
    tags = ['h1','h2','h3','h4','h5','h6']
    headings = []
    for tag in soup.find_all(tags):
        level = int(tag.name[1])  # 'h2' -> 2
        text = tag.get_text(strip=True)
        if text:
            headings.append((level, text))
    return title, headings

def save_all_headings_markdown(
    results: list[tuple[str, str, list[tuple[int, str]]]],
    subdir: str
) -> None:
    """
    複数サイトの見出し情報を 1 つの Markdown ファイルにまとめて保存する。
    出力先は `root/workspace/<subdir>/下書き.md`。
    清書用の空ファイル `清書.md` も同ディレクトリに作成する。
    """
    base_dir = os.path.join(WORKSPACE_DIR, subdir)
    os.makedirs(base_dir, exist_ok=True)

    draft_path = os.path.join(base_dir, "下書き.md")
    final_path = os.path.join(base_dir, "清書.md")

    with open(draft_path, "w", encoding="utf-8") as f:
        # 上部リンク一覧
        for url, title, _ in results:
            f.write(f"## Headings from: [{title}]({url})\n")
        f.write("\n---\n\n")

        # 下部に各ページの見出し一覧
        for _, _, headings in results:
            for level, text in headings:
                indent = "  " * (level - 1)
                f.write(f"{indent}- H{level}: {text}\n")
            f.write("\n---\n\n")

    # 空の清書ファイルを作成（上書きOK）
    with open(final_path, "w", encoding="utf-8") as f:
        pass

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("使い方: python main.py <保存先ディレクトリ名>")
        sys.exit(1)

    # URL リスト取得
    urls = read_urls_from_file(URL_LIST_FILE)

    if not urls:
        print("[ERROR] URLリストファイルが空です")
        sys.exit(1)
    
    results = []
    
    for url in urls:
        print(f"\n=== Headings from: {url} ===")
        
        try:
            print(f"Fetching headings from: {url}")
            title, headings = fetch_headings_in_order(url)
            results.append((url, title, headings))
        except Exception as e:
            print(f"[ERROR] エラーが発生しました: {e}")
            continue

    if results:
        save_all_headings_markdown(results, sys.argv[1])
    else:
        print("[ERROR] 見出し情報が取得できませんでした")
            
