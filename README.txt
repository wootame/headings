python3, pip がインストール済み前提

py venv 立ち上げ
`source venv/bin/activate`

py venv 終了
`deactivate`

依存関係インストール
`pip install requests beautifulsoup4`

main.py 実行
`python main.py {アクセス先URL}`
→ ./sites/ {配下にプロトコルを削除したアクセス先URL}.md の形式で、見出し一覧が出力されます

今後のタスク
- リスト形式でURLを受け取り、一気に出力できるようにしたいです。