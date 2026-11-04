import json
import html
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent
SERVICES_FILE = ROOT / "services.json"
WORKS_FILE = ROOT / "works.json"
OUTPUT_DIR = ROOT / "public"

SITE_URL = "https://suzukichounan.github.io/auto-recommend-site-/"
SITE_NAME = "サブスク多すぎて選べないからアニメ特化で見る時用のメモ"
SITE_TAGLINE = "アニメ見放題サービスの料金・作品数・無料期間を事実データで比較します。"
GSV_META = "WrZyRp8m3nz5I-GorXWoi-pEZGwUzyVIQ-wghxEcWSU"
DATA_AS_OF = "2026年11月4日時点"  # services.json の調査日

# デザイン: E案「ライトポップ」（白基調＋コーラル×オレンジのグラデーション、
# 丸角カード、ピル型バッジ）。design-mockups/v2/design-e-light-pop.html が正。
CSS = """
:root {
    --bg: #fff9f4; --card: #ffffff; --ink: #2b2320; --sub: #756a63;
    --coral: #ff5a3c; --coral-dark: #d63d22; --orange: #ff9f1a;
    --teal: #0e9594; --purple: #7c5cd6; --line: #ffe1d3;
    --sans: "Hiragino Kaku Gothic ProN", "Hiragino Sans", "Yu Gothic UI", "Yu Gothic", sans-serif;
}
* { box-sizing: border-box; }
body {
    font-family: var(--sans);
    font-size: 15.5px;
    line-height: 1.85;
    margin: 0;
    background: var(--bg);
    color: var(--ink);
}
a { color: var(--coral-dark); }
.wrap { max-width: 920px; margin: 0 auto; padding: 0 20px; }

/* ---------- PRバー（全ページ冒頭） ---------- */
.pr-bar {
    background: var(--ink); color: #ffe9df; font-size: 12px;
    text-align: center; padding: 8px 16px; letter-spacing: .05em;
}

/* ---------- ヒーロー ---------- */
.hero {
    margin-top: 28px;
    background: linear-gradient(120deg, #ff5a3c, #ff8a3c);
    border-radius: 28px; padding: 36px 32px 32px; color: #fff;
    box-shadow: 0 12px 28px rgba(255,90,60,.28);
}
.hero-chip {
    display: inline-block; background: #fff; color: var(--coral-dark);
    font-size: 12px; font-weight: 800; padding: 4px 14px;
    border-radius: 999px; letter-spacing: .08em;
}
.hero h1 { font-size: 34px; font-weight: 900; letter-spacing: .06em; margin: 14px 0 0; line-height: 1.35; }
.hero p { margin: 10px 0 0; font-size: 15px; font-weight: 500; }
.hero-stats { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 20px; }
.hero-stats span {
    background: rgba(255,255,255,.22); border: 2px solid rgba(255,255,255,.55);
    padding: 5px 14px; border-radius: 999px; font-size: 13px; font-weight: 700;
}
.hero.compact { padding: 22px 26px; border-radius: 24px; }
.hero.compact h1 { font-size: 23px; margin: 0; }
.hero.compact h1 a { color: #fff; text-decoration: none; }
.hero.compact p { margin-top: 4px; font-size: 13.5px; }

/* ---------- セクション見出し ---------- */
section.sec { margin-top: 46px; }
.sec-head { display: flex; align-items: center; gap: 12px; margin-bottom: 18px; }
.sec-bar { width: 10px; height: 30px; border-radius: 6px; background: var(--coral); flex: none; }
.sec-bar.teal { background: var(--teal); }
.sec-bar.orange { background: var(--orange); }
.sec-bar.purple { background: var(--purple); }
.sec-title { font-size: 23px; font-weight: 900; letter-spacing: .03em; margin: 0; }
.sec-sub { color: var(--sub); font-size: 13px; margin-left: auto; }

/* ---------- カード ---------- */
.card {
    background: var(--card); border: 2px solid var(--line); border-radius: 20px;
    padding: 24px 28px; box-shadow: 0 6px 16px rgba(43,35,32,.05);
    margin-bottom: 18px;
}
.lead { margin-top: 26px; }
.lead p { margin: 0; }
.lead p + p { margin-top: 12px; }
.lead strong { color: var(--coral-dark); }
.lead strong.t { color: var(--teal); }
.card h2 { font-size: 24px; font-weight: 900; line-height: 1.5; margin: 8px 0 10px; }
.card h3 {
    font-size: 17px; font-weight: 900; margin-top: 26px;
    border-left: 6px solid var(--coral); border-radius: 3px; padding-left: 10px;
}
.card li { margin-bottom: 7px; }
.category {
    display: inline-block; background: var(--coral); color: #fff;
    font-size: 12px; font-weight: 800; padding: 3px 13px;
    border-radius: 999px; letter-spacing: .04em;
}
.note {
    background: #fff6ef; border: 1px solid var(--line);
    padding: 12px 14px; border-radius: 12px; font-size: 13px;
}
.table-note { margin-top: 12px; font-size: 12.5px; color: var(--sub); }

/* ---------- パンくず ---------- */
nav.breadcrumb { font-size: 13px; margin: 20px 0 12px; color: var(--sub); }
nav.breadcrumb a { color: var(--coral-dark); }

/* ---------- ボタン ---------- */
.button {
    display: block; text-align: center;
    background: linear-gradient(120deg, #ff5a3c, #ff8a3c);
    color: #fff; padding: 15px 12px; border-radius: 999px;
    text-decoration: none; font-weight: 900; letter-spacing: .03em;
    margin-top: 22px; box-shadow: 0 8px 20px rgba(255,90,60,.30);
}

/* ---------- テーブル ---------- */
.table-wrap {
    overflow-x: auto; -webkit-overflow-scrolling: touch;
    background: var(--card); border: 2px solid var(--line); border-radius: 20px;
    box-shadow: 0 6px 16px rgba(43,35,32,.05);
}
.card .table-wrap { box-shadow: none; }
table.compare, table.spec {
    border-collapse: collapse; width: 100%;
    font-size: 14px; line-height: 1.7;
}
table.compare { min-width: 760px; }
table.compare th, table.compare td,
table.spec th, table.spec td {
    padding: 12px 14px; text-align: left; vertical-align: top;
}
table.compare thead th {
    background: #fff1e8; color: var(--coral-dark); font-weight: 800;
    font-size: 13px; letter-spacing: .05em; white-space: nowrap;
    border-bottom: 2px solid var(--line);
}
table.compare tbody th, table.compare tbody td { border-bottom: 2px dotted #f3e2d8; }
table.compare tbody tr:last-child th, table.compare tbody tr:last-child td { border-bottom: none; }
table.compare tbody tr:hover { background: #fffaf6; }
table.compare tbody th { font-weight: 800; white-space: nowrap; }
table.compare tbody th a { color: var(--ink); text-decoration: none; }
table.compare tbody th a:hover { color: var(--coral-dark); }
table.compare td.price { font-weight: 900; font-size: 17px; color: var(--coral-dark); white-space: nowrap; }
.badge {
    display: inline-block; margin-left: 8px; padding: 2px 11px; border-radius: 999px;
    font-size: 11.5px; font-weight: 800; vertical-align: 2px; white-space: nowrap;
}
.badge-cheap { background: var(--coral); color: #fff; }
.badge-count { background: var(--teal); color: #fff; }
table.spec th {
    background: #fff1e8; color: var(--coral-dark);
    width: 34%; font-weight: 800; border-bottom: 2px dotted #f3e2d8;
}
table.spec td { border-bottom: 2px dotted #f3e2d8; }
table.spec tr:last-child th, table.spec tr:last-child td { border-bottom: none; }

/* ---------- グリッドカード（目的別／サービス一覧） ---------- */
.cards { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.cards .card { margin-bottom: 0; padding: 24px; }
.card-tag {
    display: inline-block; font-size: 12px; font-weight: 800; padding: 3px 13px;
    border-radius: 999px; color: #fff; letter-spacing: .04em;
}
.tag-coral { background: var(--coral); }
.tag-teal { background: var(--teal); }
.tag-purple { background: var(--purple); }
.tag-orange { background: var(--orange); color: #4a2c00; }
.purpose-card h3, .svc-card h3 {
    border: none; padding: 0; margin-top: 12px; font-size: 19px;
}
.purpose-card p { margin: 8px 0 0; font-size: 14px; }
.purpose-card .svc-links { font-size: 13.5px; color: var(--sub); }
.svc-card h3 { margin-top: 0; }
.svc-card h3 a { color: var(--ink); text-decoration: none; }
.svc-card h3 a:hover { color: var(--coral-dark); }
.card-price { margin-top: 2px; font-size: 14px; color: var(--sub); }
.card-price b { font-size: 21px; color: var(--coral-dark); }
.svc-card p { margin: 8px 0 0; font-size: 14px; }
.svc-card .meta { font-size: 13px; color: var(--sub); }
.work-list { margin: 0; padding-left: 20px; }
.work-list li { margin-bottom: 8px; }

/* ---------- フッター ---------- */
footer.site { margin-top: 56px; background: var(--ink); color: #e8ded9; }
.foot-inner { padding: 26px 0 40px; font-size: 12.5px; }
.foot-inner p { margin: 0; }
.foot-inner p + p { margin-top: 8px; }
.foot-inner a { color: #ffc4b2; }

@media (max-width: 640px) {
    body { font-size: 15px; }
    .hero { padding: 28px 22px; }
    .hero h1 { font-size: 27px; }
    .hero.compact { padding: 18px 20px; }
    .hero.compact h1 { font-size: 20px; }
    .cards { grid-template-columns: 1fr; }
    .sec-sub { display: none; }
    .card { padding: 20px; }
    .lead { padding: 20px; }
    .card h2 { font-size: 21px; }
}
"""


def esc(value):
    return html.escape(str(value), quote=True)


def yen(value):
    return f"{value:,}円"


def json_ld(data):
    payload = json.dumps(data, ensure_ascii=False)
    return f'<script type="application/ld+json">{payload}</script>'


def render_page(title, description, path, body, structured=None, is_top=False):
    """共通レイアウトで1ページ分のHTMLを返す。path はサイトルート相対（末尾スラッシュ）。"""
    url = SITE_URL + path
    gsv = f'\n<meta name="google-site-verification" content="{GSV_META}" />' if is_top else ""
    ld = f"\n{json_ld(structured)}" if structured else ""
    if is_top:
        hero = f"""
  <header class="hero">
    <span class="hero-chip">アニメ見放題くらべ</span>
    <h1>{SITE_NAME}</h1>
    <p>{SITE_TAGLINE}</p>
    <div class="hero-stats">
      <span>最安は月額550円</span>
      <span>作品数 最大7,400作品以上</span>
      <span>無料期間 最大31日間</span>
    </div>
  </header>"""
    else:
        hero = f"""
  <header class="hero compact">
    <h1><a href="{SITE_URL}">{SITE_NAME}</a></h1>
    <p>{SITE_TAGLINE}</p>
  </header>"""
    return f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">{gsv}
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{esc(url)}">
<meta property="og:site_name" content="{esc(SITE_NAME)}">
<link rel="canonical" href="{esc(url)}">{ld}
<style>{CSS}</style>
</head>
<body>
<div class="pr-bar"><strong>PR：</strong>当サイトはアフィリエイト広告を利用しています。</div>
<main class="wrap">{hero}
{body}
</main>
<footer class="site">
  <div class="wrap foot-inner">
    <p>※当サイトはアフィリエイト広告を利用しています。</p>
    <p>料金・作品数などの情報は{DATA_AS_OF}の各社公式発表に基づきます。最新情報は各サービスの公式サイトでご確認ください。</p>
    <p><a href="{SITE_URL}">トップ</a> ／ <a href="{SITE_URL}privacy/">プライバシーポリシー・広告について</a></p>
  </div>
</footer>
</body>
</html>
"""


def breadcrumb(items):
    """items: [(label, url or None), ...]"""
    parts = []
    for label, url in items:
        if url:
            parts.append(f'<a href="{esc(url)}">{esc(label)}</a>')
        else:
            parts.append(esc(label))
    joined = " ＞ ".join(parts)
    return f'<nav class="breadcrumb">{joined}</nav>'


def affiliate_button(service):
    """affiliate_url がある場合だけ申込ボタンを出す。"""
    url = str(service.get("affiliate_url", "")).strip()
    if not url.startswith("https://"):
        return ""
    return (
        f'<a class="button" href="{esc(url)}" '
        f'rel="nofollow sponsored noopener" target="_blank">'
        f'{esc(service["name"])}の公式サイトを見る →</a>'
    )


def sec_head(title, bar_class="", sub=""):
    sub_html = f'<div class="sec-sub">{esc(sub)}</div>' if sub else ""
    return (
        f'<div class="sec-head"><div class="sec-bar {bar_class}"></div>'
        f'<h2 class="sec-title">{esc(title)}</h2>{sub_html}</div>'
    )


# 目的別のおすすめ（事実ベースの編集セクション）
PURPOSES = [
    {
        "tag": "アニメだけを安く",
        "tag_class": "tag-coral",
        "title": "アニメだけをとにかく安く見たい",
        "text": "月額が最安なのはDMM TVの550円（Web登録）。アニメ専門で作品数を求めるなら、7,400作品以上のdアニメストア（660円）が候補になります。",
        "slugs": ["dmm-tv", "d-anime-store"],
    },
    {
        "tag": "まとめて見たい",
        "tag_class": "tag-purple",
        "title": "アニメ以外もまとめて見たい",
        "text": "見放題作品数で選ぶならU-NEXT（44万本以上）。買い物などの特典も含めて考えたい場合は、プライム特典込みのAmazonプライム（月額600円）があります。",
        "slugs": ["u-next", "amazon-prime-video"],
    },
    {
        "tag": "無料で試す",
        "tag_class": "tag-teal",
        "title": "まず無料で試したい",
        "text": "無料期間が長いのはU-NEXTとdアニメストアの31日間、Amazonプライムの30日間。Netflix、Hulu、Disney+には現在無料トライアルがありません。",
        "slugs": ["u-next", "d-anime-store", "amazon-prime-video"],
    },
    {
        "tag": "家族で使う",
        "tag_class": "tag-orange",
        "title": "家族と分け合って同時視聴したい",
        "text": "同時視聴台数はU-NEXTとHuluが最大4台、Disney+はプレミアムプランで4台、Netflixはプレミアムで4台です。同一作品の同時視聴には制限があるサービスもあります。",
        "slugs": ["u-next", "hulu", "disney-plus"],
    },
]

# 比較表のサービス名に付けるバッジ（slug -> (文言, クラス)）
TABLE_BADGES = {
    "dmm-tv": ("最安", "badge-cheap"),
    "d-anime-store": ("作品数が多い", "badge-count"),
}


def build_top(services, works, by_slug):
    rows = []
    for s in services:
        badge = ""
        if s["slug"] in TABLE_BADGES:
            label, cls = TABLE_BADGES[s["slug"]]
            badge = f'<span class="badge {cls}">{label}</span>'
        rows.append(
            "<tr>"
            f'<th><a href="{SITE_URL}service/{s["slug"]}/">{esc(s["name"])}</a>{badge}</th>'
            f'<td class="price">{esc(s["price_monthly"])}</td>'
            f"<td>{esc(s['free_trial'])}</td>"
            f"<td>{esc(s['anime_count'])}</td>"
            f"<td>{esc(s['simultaneous'])}</td>"
            f"<td>{esc(s['download'])}</td>"
            "</tr>"
        )
    table = (
        '<div class="table-wrap"><table class="compare">'
        "<thead><tr><th>サービス</th><th>月額料金（税込）</th><th>無料期間</th>"
        "<th>アニメ作品数</th><th>同時視聴</th><th>ダウンロード</th></tr></thead>"
        f"<tbody>{''.join(rows)}</tbody></table></div>"
    )

    purpose_cards = []
    for p in PURPOSES:
        links = "、".join(
            f'<a href="{SITE_URL}service/{slug}/">{esc(by_slug[slug]["name"])}</a>'
            for slug in p["slugs"]
            if slug in by_slug
        )
        purpose_cards.append(
            '<article class="card purpose-card">'
            f'<span class="card-tag {p["tag_class"]}">{esc(p["tag"])}</span>'
            f"<h3>{esc(p['title'])}</h3>"
            f"<p>{esc(p['text'])}</p>"
            f'<p class="svc-links">該当サービス：{links}</p>'
            "</article>"
        )

    cards = []
    for s in services:
        cards.append(
            '<article class="card svc-card">'
            f'<h3><a href="{SITE_URL}service/{s["slug"]}/">{esc(s["name"])}</a></h3>'
            f'<p class="card-price">月額 <b>{esc(s["price_monthly"])}</b> ／ 無料期間 {esc(s["free_trial"])}</p>'
            f"<p>{esc(s['summary'])}</p>"
            f'<p class="meta">アニメ作品数：{esc(s["anime_count"])}</p>'
            "</article>"
        )

    works_section = ""
    if works:
        items = "".join(
            f'<li><a href="{SITE_URL}work/{w["slug"]}/">{esc(w["title"])}はどこで見れる？</a></li>'
            for w in works
        )
        works_section = f"""
  <section class="sec">
    {sec_head("作品から探す", "purple")}
    <div class="card">
      <ul class="work-list">{items}</ul>
    </div>
  </section>"""

    body = f"""
  <div class="card lead">
    <p>アニメだけを安く見たいなら、月額<strong>550円</strong>のDMM TVか、作品数<strong>7,400作品以上</strong>のdアニメストア（<strong>660円</strong>）が軸になります。映画やドラマもまとめて見たいなら、見放題<strong class="t">440,000本以上</strong>のU-NEXT（<strong>2,189円</strong>）が候補です。</p>
    <p>このページでは主要8サービスを、料金・無料期間・作品数といった同じ条件で並べました。数字はすべて各社の公式発表にもとづきます（{DATA_AS_OF}）。</p>
  </div>
  <section class="sec">
    {sec_head("アニメ見放題サービス 比較表", "", "料金は税込")}
    {table}
    <p class="table-note">料金は税込。月額料金は登録方法（Web／アプリ）で異なる場合があります。作品数が「非公表」のサービスは、公式に本数を発表していません。</p>
  </section>
  <section class="sec">
    {sec_head("目的別のおすすめ", "teal", "迷ったらここから")}
    <div class="cards">{''.join(purpose_cards)}</div>
  </section>
  <section class="sec">
    {sec_head("サービス一覧", "orange", "各サービスの詳細ページへ")}
    <div class="cards">{''.join(cards)}</div>
  </section>{works_section}
"""

    structured = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "アニメ見放題サービス比較一覧",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "name": s["name"],
                "url": f"{SITE_URL}service/{s['slug']}/",
            }
            for i, s in enumerate(services)
        ],
    }
    return render_page(
        f"{SITE_NAME}｜アニメ見放題サービスの料金・作品数を比較",
        "DMM TV、dアニメストア、U-NEXTなど主要8つのアニメ見放題サービスを、月額料金・無料期間・アニメ作品数・同時視聴台数で比較。事実データのみで選べます。",
        "",
        body,
        structured=structured,
        is_top=True,
    )


def build_service_page(s, services):
    plans_rows = "".join(
        f"<tr><th>{esc(p['name'])}</th><td>月額{esc(yen(p['price']))}（税込）</td></tr>"
        for p in s.get("plans", [])
    )
    spec_rows = (
        f"<tr><th>月額料金</th><td>{esc(s['price_monthly'])}</td></tr>"
        f"<tr><th>無料期間</th><td>{esc(s['free_trial'])}</td></tr>"
        f"<tr><th>アニメ作品数</th><td>{esc(s['anime_count'])}</td></tr>"
        f"<tr><th>総作品数（見放題など）</th><td>{esc(s['total_count'])}</td></tr>"
        f"<tr><th>同時視聴</th><td>{esc(s['simultaneous'])}</td></tr>"
        f"<tr><th>ダウンロード視聴</th><td>{esc(s['download'])}</td></tr>"
    )
    strengths = "".join(f"<li>{esc(x)}</li>" for x in s.get("strengths", []))
    cautions = "".join(f"<li>{esc(x)}</li>" for x in s.get("cautions", []))

    others = [o for o in services if o["slug"] != s["slug"]]
    others_links = "、".join(
        f'<a href="{SITE_URL}service/{o["slug"]}/">{esc(o["name"])}</a>'
        for o in others
    )

    body = f"""
  {breadcrumb([("トップ", SITE_URL), (s['name'], None)])}
  <article class="card">
    <p class="category">サービス個別ページ</p>
    <h2>{esc(s['name'])}</h2>
    <p>{esc(s['summary'])}</p>
    <h3>基本情報</h3>
    <div class="table-wrap"><table class="spec"><tbody>{spec_rows}</tbody></table></div>
    <h3>料金プラン</h3>
    <div class="table-wrap"><table class="spec"><tbody>{plans_rows}</tbody></table></div>
    <p class="note">{esc(s['price_notes'])}</p>
    <h3>強み</h3>
    <ul>{strengths}</ul>
    <h3>注意点</h3>
    <ul>{cautions}</ul>
    {affiliate_button(s)}
  </article>
  <section class="card">
    <h2>ほかのサービスと比較する</h2>
    <p>{others_links}</p>
    <p><a href="{SITE_URL}">トップの比較表に戻る</a></p>
  </section>
"""

    structured = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": s["name"],
        "description": s["summary"],
        "url": f"{SITE_URL}service/{s['slug']}/",
        "offers": {
            "@type": "Offer",
            "priceCurrency": "JPY",
            "price": s["price_from"],
        },
    }
    return render_page(
        f"{s['name']}の料金・作品数・無料期間｜{SITE_NAME}",
        f"{s['name']}の月額料金（{s['price_monthly']}）、無料期間（{s['free_trial']}）、アニメ作品数（{s['anime_count']}）を公式発表ベースでまとめました。強みと注意点も確認できます。",
        f"service/{s['slug']}/",
        body,
        structured=structured,
    )


def build_privacy_page():
    body = f"""
  {breadcrumb([("トップ", SITE_URL), ("プライバシーポリシー・広告について", None)])}
  <article class="card">
    <h2>プライバシーポリシー・広告について</h2>
    <h3>アフィリエイト広告について</h3>
    <p>当サイト「{SITE_NAME}」は、アフィリエイトプログラムを利用した広告を掲載しています。当サイト内のリンクを経由してサービスへの申込や商品の購入が行われた場合、当サイト運営者に報酬が支払われることがあります。</p>
    <p>当サイトでは、料金・作品数などの事実データに基づいて情報を掲載しており、報酬の有無によって比較内容や掲載順を変更することはありません。</p>
    <h3>掲載情報について</h3>
    <p>当サイトの料金・作品数などの情報は、{DATA_AS_OF}に各サービスの公式サイト・公式発表で確認したものです。料金改定等により実際と異なる場合があります。申込の際は、必ず各サービスの公式サイトで最新情報をご確認ください。</p>
    <h3>アクセス解析について</h3>
    <p>当サイトでは、サイトの利用状況を把握するためにアクセス解析ツールを使用する場合があります。これらのツールはCookieを使用してデータを収集しますが、個人を特定する情報は含まれません。ブラウザの設定によりCookieを無効にすることも可能です。</p>
    <h3>個人情報の取り扱い</h3>
    <p>当サイトでは、氏名・住所・メールアドレスなどの個人情報を収集する機能は設けていません。各サービスへの申込時に提供する個人情報の取り扱いについては、申込先の各事業者のプライバシーポリシーをご確認ください。</p>
    <h3>免責事項</h3>
    <p>当サイトの情報の正確性については万全を期していますが、その内容を保証するものではありません。当サイトの利用により生じた損害について、運営者は一切の責任を負いかねます。</p>
  </article>
"""
    return render_page(
        f"プライバシーポリシー・広告について｜{SITE_NAME}",
        "当サイトのアフィリエイト広告の利用、掲載情報の出典、個人情報の取り扱いについて説明します。",
        "privacy/",
        body,
    )


def build_work_page(w, by_slug):
    """works.json の1作品分のページ。w: slug, title, services(配信中slug配列), note"""
    rows = []
    buttons = []
    for slug in w.get("services", []):
        s = by_slug.get(slug)
        if not s:
            continue
        rows.append(
            "<tr>"
            f'<th><a href="{SITE_URL}service/{slug}/">{esc(s["name"])}</a></th>'
            f'<td class="price">{esc(s["price_monthly"])}</td>'
            f"<td>{esc(s['free_trial'])}</td>"
            "</tr>"
        )
        btn = affiliate_button(s)
        if btn:
            buttons.append(btn)
    note = w.get("note", "")
    note_html = f'<p class="note">{esc(note)}</p>' if note else ""
    body = f"""
  {breadcrumb([("トップ", SITE_URL), (f"「{w['title']}」はどこで見れる？", None)])}
  <article class="card">
    <p class="category">作品の配信情報</p>
    <h2>「{esc(w['title'])}」はどこで見れる？</h2>
    <p>「{esc(w['title'])}」を見放題で配信しているサービスは以下のとおりです（{DATA_AS_OF}）。</p>
    <div class="table-wrap"><table class="compare">
      <thead><tr><th>サービス</th><th>月額料金（税込）</th><th>無料期間</th></tr></thead>
      <tbody>{''.join(rows)}</tbody>
    </table></div>
    {note_html}
    {''.join(buttons)}
  </article>
"""
    return render_page(
        f"「{w['title']}」はどこで見れる？配信サービスまとめ｜{SITE_NAME}",
        f"アニメ「{w['title']}」を見放題で配信しているサービスをまとめました。各サービスの月額料金と無料期間もあわせて確認できます。",
        f"work/{w['slug']}/",
        body,
    )


def main():
    with SERVICES_FILE.open("r", encoding="utf-8") as f:
        services = json.load(f)
    works = []
    if WORKS_FILE.exists():
        with WORKS_FILE.open("r", encoding="utf-8") as f:
            works = json.load(f)
    by_slug = {s["slug"]: s for s in services}

    pages = []  # (相対パス, HTML) 相対パスは "" がトップ

    pages.append(("", build_top(services, works, by_slug)))
    for s in services:
        pages.append((f"service/{s['slug']}/", build_service_page(s, services)))
    pages.append(("privacy/", build_privacy_page()))
    for w in works:
        pages.append((f"work/{w['slug']}/", build_work_page(w, by_slug)))

    for path, page_html in pages:
        if path == "":
            out = OUTPUT_DIR / "index.html"
        else:
            out = OUTPUT_DIR / path / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page_html, encoding="utf-8")
        print(f"生成しました: {out}")

    robots = OUTPUT_DIR / "robots.txt"
    robots.write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}sitemap.xml\n",
        encoding="utf-8",
    )
    print(f"生成しました: {robots}")

    today = date.today().isoformat()
    urls = "\n".join(
        f"  <url>\n    <loc>{SITE_URL}{path}</loc>\n    <lastmod>{today}</lastmod>\n  </url>"
        for path, _ in pages
    )
    sitemap = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{urls}\n</urlset>\n"
    )
    sitemap_file = OUTPUT_DIR / "sitemap.xml"
    sitemap_file.write_text(sitemap, encoding="utf-8")
    print(f"生成しました: {sitemap_file}（URL数: {len(pages)}）")


if __name__ == "__main__":
    main()
