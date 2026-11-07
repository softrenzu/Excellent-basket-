#!/usr/bin/env python3
"""GREEN SIDE: daily editorial post generator and static article publisher.

Creates one original evergreen fan-guide post each JST day (never invents
results, scores or news), renders HTML articles and refreshes sitemap.xml.
Runs from the repository root and needs only Python's standard library.
"""
from __future__ import annotations

import html
import json
import os
from datetime import date, datetime
from pathlib import Path
from urllib.parse import quote
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
POSTS = SITE / "data" / "posts.json"
MATCHES = SITE / "data" / "matches.json"
ARTICLES = SITE / "blog"
BASE_URL = "https://softrenzu.github.io/Excellent-basket-/"

# Original beginner-friendly ideas. They avoid unsupported factual reporting.
TIPS = [
    ("観戦ガイド", "試合前にチェックしておきたい３つのこと", "会場・開始時刻・チケットを確認するだけで、当日がぐっとスムーズになります。", "まずは公式日程で対戦カードと会場を見て、チケットの購入条件を確認しましょう。"),
    ("楽しみ方", "会場でしか味わえない音に耳を傾けて", "歓声、シューズの音、ブザー。ライブのバスケには画面とは違う魅力があります。", "最初は難しい戦術が分からなくても大丈夫。得点した瞬間の会場全体の空気を味わってみてください。"),
    ("観戦ガイド", "友だちをバスケ観戦に誘うなら", "初観戦の仲間と一緒なら、試合の前後の時間まで楽しみになります。", "予定を合わせるときは、土日か平日かだけでなく、開始時間と会場名まで共有しましょう。"),
    ("楽しみ方", "注目する選手を一人決めて観てみよう", "好きな選手を見つけると、パスやディフェンスも見どころに変わります。", "最初の数分だけでも、気になる選手の動きを追ってみましょう。ボールを持っていない時の動きにも発見があります。"),
    ("観戦ガイド", "チケット選びで迷ったときの考え方", "コートとの距離や見渡しやすさなど、観たいポイントによって席の魅力は変わります。", "価格・残席・見え方は試合ごとに違います。公式の座席表と販売ページを見て比較するのが安心です。"),
    ("楽しみ方", "応援の声を出さなくても楽しめる", "周囲の声援を聞くだけでも、アリーナの一体感は十分に伝わります。", "慣れないうちは拍手だけでも大丈夫。周囲の観客を参考にして、自分のペースで楽しみましょう。"),
    ("観戦ガイド", "ホームゲームとアウェーゲームの違い", "観戦先を選ぶときに知っておきたい、ホームとアウェーの基本。", "横浜で現地観戦したいなら、日程表のHOME表記をチェック。AWAYの会場は別の地域になる場合があります。"),
    ("楽しみ方", "試合前の時間もゲームデーの一部", "到着してすぐに席へ向かうだけではない、アリーナ観戦の楽しみ。", "時間に余裕を持って到着し、場内の雰囲気を感じてみましょう。入場開始時刻や実施イベントは公式案内が確実です。"),
    ("観戦ガイド", "子どもと一緒に観戦するための準備", "家族でのスポーツ観戦をより気軽にするための小さなチェックリスト。", "お子さまのチケット条件、ベビーカーや持ち込み品のルールなどは試合ごとの案内をチェックしましょう。"),
    ("楽しみ方", "最後の１分が面白い理由", "残り時間が少なくても目が離せないのがバスケットボール。", "得点差だけでなく、攻守の切り替えや時間の使い方を見てみると、終盤の見どころが広がります。"),
    ("観戦ガイド", "平日ナイトゲームという楽しみ方", "仕事や学校のあとの観戦も、いつもと違う時間の過ごし方になります。", "平日は開始時刻や帰りの交通手段を先に確認。余裕ある計画なら観戦に集中できます。"),
    ("楽しみ方", "ディフェンスを観ると面白さが増える", "得点以外の好プレーに注目すると、試合の見え方が変わります。", "相手のシュートを難しくする守備や、パスを止める瞬間にも注目してみましょう。"),
    ("観戦ガイド", "横浜武道館へ行く前の確認ポイント", "関内エリアのホームゲームを楽しむために。", "横浜武道館開催かどうかを必ず確認。建物名が似ている会場への行き間違いにも注意しましょう。"),
    ("観戦ガイド", "横浜BUNTAI観戦の日はここを確認", "ホームゲームの会場を間違えないための基本。", "横浜BUNTAI開催の試合もあります。チケットの会場名と、当日の入場案内を確認してください。"),
    ("楽しみ方", "パスがつながる瞬間に注目しよう", "得点までの連携が見えてくると、観戦がさらに面白くなります。", "ボールを受ける選手だけでなく、スペースへ走る味方の動きも追ってみましょう。"),
    ("観戦ガイド", "試合開始時刻と開場時刻は別", "当日の到着時間を決める前に知っておきたいこと。", "TIP OFFは試合開始時刻です。開場時刻や入場方法は別に案内される場合があるため、公式情報を確認しましょう。"),
    ("楽しみ方", "１試合の思い出を残すアイデア", "観戦の日を、また行きたくなる思い出に。", "会場で感じたことや気になったプレーを短くメモしてみるのもおすすめ。写真撮影の可否は会場ルールに従いましょう。"),
    ("観戦ガイド", "初観戦におすすめの持ち物", "忘れ物を減らして、試合に集中するための準備。", "チケットを表示できるスマートフォン、移動に必要なもの、羽織り物などをチェック。持ち込み制限も事前確認を。"),
    ("楽しみ方", "会場全体で生まれる一体感", "知らない人と同じプレーに反応する、その瞬間がスポーツ観戦の醍醐味。", "チームに詳しくなくても、周囲の熱気を感じながら拍手を送るだけで楽しめます。"),
    ("観戦ガイド", "観戦後に次の試合を探してみよう", "初めての１試合を、次の楽しみにつなげる方法。", "公式日程を確認すると次の対戦カードや別会場のゲームも見つかります。気になる日をカレンダーに入れてみましょう。"),
    ("楽しみ方", "選手交代に注目すると見えてくること", "一度の試合でも、さまざまな選手の役割が見えてきます。", "交代した選手の動きやチームのテンポの変化に注目すると、新しい見どころが生まれます。"),
    ("観戦ガイド", "２つの横浜会場を覚えよう", "横浜武道館と横浜BUNTAI。日によって異なるホームゲームの会場。", "どちらも横浜市中区の関内エリアですが、別の施設です。チケットに記載された会場名を確認しましょう。"),
    ("楽しみ方", "シュートが決まるまでの流れを見る", "ゴールの直前に起きている小さな連携にも注目。", "スクリーンやパス回しなど、得点に至るまでのチームプレーを見てみると興味が深まります。"),
    ("観戦ガイド", "チケット購入前に知っておきたいこと", "販売スケジュール、座席、入場条件の確認が大切です。", "公式チケットサイトの案内に従い、販売開始日時・座席種別・支払方法・会員登録の条件を確認しましょう。"),
]

def today_jst() -> date:
    override = os.environ.get("BLOG_DATE")
    return date.fromisoformat(override) if override else datetime.now(ZoneInfo("Asia/Tokyo")).date()

def safe(value: object) -> str:
    return html.escape(str(value), quote=True)

def render_page(post: dict) -> str:
    title = safe(post["title"])
    desc = safe(post["summary"])
    paragraphs = "\n".join(f"<p>{safe(text)}</p>" for text in post.get("body", []))
    canonical = BASE_URL + quote("blog/" + post["id"] + ".html")
    return f'''<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#082c23"><meta name="description" content="{desc}">
<meta property="og:type" content="article"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">
<link rel="canonical" href="{canonical}"><link rel="icon" href="../favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="../styles.css">
<title>{title}｜GREEN SIDE</title>
<style>
.article-page{{background:#f5f6ef;min-height:100vh}}.article-page-header{{background:#082c23;color:#d8f34f;padding:23px 0}}
.article-page-header a{{font:900 28px "Barlow Condensed",sans-serif;letter-spacing:-.02em}}
.article-page-main{{max-width:850px;margin:0 auto;padding:60px 24px 100px}}
.article-page-meta{{color:#37724c;font-weight:900;font-size:12px}}.article-page-main h1{{font-size:clamp(26px,4.5vw,48px);line-height:1.5;letter-spacing:-.07em;margin:20px 0}}
.article-page-lead{{font-size:18px;font-weight:700;line-height:1.9;border-bottom:2px solid #d1ded2;padding-bottom:30px}}
.article-page-body p{{font-size:15px;line-height:2.35;margin:27px 0;color:#30493e}}
.article-page-cta{{background:#0c372b;color:#fff;padding:27px;margin-top:60px}}
.article-page-cta a{{color:#d8f34f;font-weight:900}}.article-page-footer{{font-size:11px;color:#718578;margin-top:44px}}
</style></head><body class="article-page"><header class="article-page-header"><div class="wrap"><a href="../">GREEN SIDE.</a></div></header>
<main class="article-page-main"><p><a href="../#blog">← ブログ一覧に戻る</a></p><p class="article-page-meta">{safe(post["date"])} / {safe(post["category"])}</p>
<h1>{title}</h1><p class="article-page-lead">{desc}</p><div class="article-page-body">{paragraphs}</div>
<div class="article-page-cta"><p>次のホームゲームを探してみませんか？</p><a href="https://yokohama-ex.jp/schedule/calendar/" target="_blank" rel="noopener noreferrer">横浜エクセレンス公式試合日程を見る ↗</a></div>
<p class="article-page-footer">GREEN SIDE は非公式観戦メディアです。試合日程・会場・販売情報の最新内容は公式サイトをご確認ください。</p></main></body></html>'''

def main() -> None:
    data = json.loads(POSTS.read_text(encoding="utf-8"))
    posts = data.get("posts", [])
    current = today_jst()
    date_string = current.isoformat()
    if not any(post.get("date") == date_string for post in posts):
        category, title, summary, tip = TIPS[current.toordinal() % len(TIPS)]
        readable = f"{current.month}月{current.day}日"
        matches = json.loads(MATCHES.read_text(encoding="utf-8")).get("matches", [])
        next_games = sorted((m for m in matches if m["date"] >= date_string), key=lambda m: m["date"])
        extra = ("次に予定されている掲載ホームゲームは、" + next_games[0]["date"].replace("-", "年", 1).replace("-", "月", 1) + "日、"
                 + next_games[0]["opponent"] + "戦（" + next_games[0]["venue"] + "）です。"
                 if next_games else "今後のホームゲームは、横浜エクセレンス公式の試合日程でご確認ください。")
        post = {"id": date_string + "-daily", "date": date_string, "category": category, "visual": "DAILY",
                "title": readable + "の観戦ノート｜" + title, "summary": summary,
                "body": [summary, tip, extra, "チケット・試合日時・会場・入場ルールは変更の可能性があります。出発前にクラブ公式サイトの最新情報をご確認ください。"],
                "autoGenerated": True}
        posts.append(post)
        print("Created:", post["title"])
    else:
        print("A post already exists for", date_string)

    ARTICLES.mkdir(parents=True, exist_ok=True)
    posts.sort(key=lambda p: (p["date"], p["id"]), reverse=True)
    for post in posts:
        post["url"] = "blog/" + post["id"] + ".html"
        (ARTICLES / (post["id"] + ".html")).write_text(render_page(post), encoding="utf-8")
    data["posts"] = posts
    data["updatedAt"] = date_string
    POSTS.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    urls = [BASE_URL] + [BASE_URL + quote(post["url"]) for post in posts]
    body = "\n".join("  <url><loc>" + safe(url) + "</loc></url>" for url in urls)
    (SITE / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + body + '\n</urlset>\n', encoding="utf-8")
    print(f"Rendered {len(posts)} article pages")

if __name__ == "__main__":
    main()
