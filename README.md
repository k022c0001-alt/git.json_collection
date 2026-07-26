# git.json_collection
"""
src/
├── components/          # 画面の見た目（UIパーツ）を分ける場所
│   ├── MapView.jsx          # 地図を表示する部品
│   ├── RankingList.jsx      # 23位までのランキングを表示する部品
│   ├── FilterButtons.jsx    # 「治安」「保育」などのボタン群
│   └── SafetyPanel.jsx      # ★治安ボタンを押した時に出る詳細パネル（別ファイル！）
│
├── utils/               # 計算やロジック（処理）を分ける場所
│   ├── scoreCalculator.js   # 足し算スコアを計算するロジック（別ファイル！）
│   └── safetyAnalyzer.js    # ★治安データの解析・評価ロジック（別ファイル！）
│
├── data/
│   └── snapshot.json        # データ本体
│
└── App.jsx              # 全体を組み上げる「司令塔」（コードは数十行で済む）
"""
