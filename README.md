# desktopPdfMerger: PDF結合アプリ (Desktop)
- 単一ファイルで動作するシンプルなデスクトップGUIアプリ
- 依存: pypdf, FreeSimpleGUI

## 使い方:
1) 必要なパッケージをインストール
   pip install pypdf FreeSimpleGUI

2) このファイルを保存 (例: pdf_merger.py) して実行
   python pdf_merger.py

3) ファイルを追加して順序を整え、[結合] を押して保存先を指定

### パッケージ化 (Windows/Mac/Linux):
  pip install pyinstaller
  pyinstaller --onefile --windowed pdf_merger.py


# webPdfMerger: PDF結合アプリ (Web App)
- desktopPdfMergerのWebアプリバージョン
- フレームワーク：streamlit
