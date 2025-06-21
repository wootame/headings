# Heading Fetcher

指定したウェブサイトの `<title>` および `<h1>`〜`<h6>` を抽出し、Markdown 形式で保存する Python スクリプトです。

## 🔧 前提

- Python 3.x インストール済み
- `pip` 使用可能

## 🐍 セットアップ

1. 仮想環境の作成
```bash
python -m venv venv
```

2. 仮想環境の有効化
windows: `venv\Scripts\activate`
Mac: `source venv/bin/activate`

3. 仮想環境の無効化
```bash
deactivate
```

3. 依存パッケージのインストール
```bash
pip install requests beautifulsoup4 lxml
```

## 🚀 使い方

1. sites.txt に、見出しリストを取得したい URL を記載します
  - URL ごとに改行してください

2. 以下で起動します

```bash
python main.py <保存先ディレクトリ名>
```

3. workspace/<保存先ディレクトリ名> の 下書き.md に結果が出力されています