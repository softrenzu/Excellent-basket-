# GREEN SIDE

横浜エクセレンスの観戦者を増やすための独立ファンメディアです。  
スマホ対応の観戦ガイド、ホームゲーム日程、チケットリンク、毎日更新の観戦ブログを提供します。

- リポジトリ: https://github.com/softrenzu/Excellent-basket-
- 公開予定URL: https://softrenzu.github.io/Excellent-basket-/
- 公式クラブサイト: https://yokohama-ex.jp/
- 公式チケット: https://ticket.bleague.jp/
- デザインの参考: 所有リポジトリ `softrenzu/goodspace-main` の `preview/デザインプレビュー.html`。ソースは独立して新規制作し、元リポジトリは変更していません。

## GitHub Pages公開（初回のみ）

2026年11月7日時点でこのリポジトリは **private** であり、Pagesは未有効化です。
GitHub Actionsの「Configure Pages」が `Get Pages site failed: Not Found` で失敗するのはこのためです。

1. リポジトリの [Settings > Pages](https://github.com/softrenzu/Excellent-basket-/settings/pages) を開く
2. GitHub Freeの場合、先に [Settings > General](https://github.com/softrenzu/Excellent-basket-/settings) の「Danger Zone > Change repository visibility」から **Public** に変更（Pages公開用のソースのみ含まれており、秘密情報は置いていません）。GitHub ProなどprivateのPages公開に対応する契約ならPrivateのままでも可
3. 「Build and deployment > Source」を **GitHub Actions** にする
4. [Actions > Publish GREEN SIDE and daily blog](https://github.com/softrenzu/Excellent-basket-/actions/workflows/publish.yml) で **Run workflow** を一度実行
5. Actionsの `Deploy to GitHub Pages` が成功したことを確認し、公開URLを開く

以後、mainブランチ更新時および毎日10:00（JST）前後に自動生成とデプロイを試みます。GitHubのスケジュール起動は遅延することがあります。

## ファイル構成

- `site/index.html`: トップページ
- `site/styles.css`: レスポンシブデザイン
- `site/app.js`: 日程、ブログ、検索フィルター、記事表示
- `site/data/matches.json`: 手作業で確認したホームゲーム日程
- `site/data/posts.json`: 全ブログ記事の本文・メタデータ
- `site/blog/`: SEOを考慮した公開記事HTML（GitHub Actionsで自動生成）
- `site/sitemap.xml`: 検索エンジン向けサイトマップ
- `scripts/daily_blog.py`: 自動執筆とHTML生成
- `.github/workflows/publish.yml`: 毎日更新・公開ワークフロー

## 更新運用

**毎朝10:00 JST** にGitHub Actionsが `scripts/daily_blog.py` を実行します。日本時間で当日の記事がなければオリジナルの観戦ガイドを1件追加し、記事ページとサイトマップを更新します。同日に手動で記事を作った場合は重複投稿しません。

当日記事はあくまで初心者向け観戦コラムです。実際の試合結果、観客動員、最新の出来事は自動で捏造・推測しません。時事的な試合レポートや選手インタビューは人間が公式発表を確認して執筆してください。自動記事はあらかじめ用意したテーマを循環するため、継続的に新しいテーマを追加し、品質レビューしてください。

**手動の記事を掲載する方法**: `site/data/posts.json` の `posts` に以下の形式の要素を追加し、mainへコミット。Actionsが静的記事ページを生成します。既存の `id` は変更しないでください。

```json
{
  "id": "2026-11-09-unique-title",
  "date": "2026-11-09",
  "category": "観戦ガイド",
  "visual": "EX",
  "title": "記事タイトル",
  "summary": "概要",
  "body": ["第1段落", "第2段落", "第3段落"]
}
```

**試合日程**: `site/data/matches.json` を [公式日程](https://yokohama-ex.jp/schedule/calendar/) と照合して更新してください。古い試合はトップ画面で自動的に非表示になり、将来の登録試合がない場合は公式日程への案内に切り替わります。チケットの購入先はB.LEAGUE公式チケットサイトです。販売中・空席ありとは表示しません。

## 観戦者増加のための導線

**検索 → 観戦ブログ → ホームゲーム一覧 → チケット購入** の動線を想定しています。

- 初観戦向けの質問と回答を固定コンテンツ化
- タイトル・メタディスクリプション・OGP・記事別静的URL・サイトマップ対応
- B.LEAGUE公式チケットへのCTAを複数配置
- ブログから公式日程へのリンクを設置
- 試合情報は各月の公式発表をもとに手動更新

最初に計測すべき指標は「記事への流入数」「日程セクション閲覧」「公式チケットクリック数」「実際の購入・来場数（クラブと連携した場合）」です。現時点で解析タグやコンバージョン計測用IDは設定していません。必要ならGA4の測定IDと公式チケット側の成果照合方法を設定してください。

## 免責・権利

GREEN SIDEは横浜エクセレンスおよびB.LEAGUEの公式サイトではない、独立したファンメディアです。公式写真・ロゴ・記事本文は転載していません。写真を追加する場合は掲載許諾を確認してください。
