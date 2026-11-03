import json
import html
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent
SERVICES_FILE = ROOT / "services.json"
WORKS_FILE = ROOT / "works.json"
OUTPUT_DIR = ROOT / "public"

SITE_URL = "https://suzukichounan.github.io/auto-recommend-site-/"
SITE_NAME = "アニメ配信くらべ帖"
SITE_TAGLINE = "アニメ見放題サービスの料金・作品数・無料期間を事実データで比較します。"
GSV_META = "WrZyRp8m3nz5I-GorXWoi-pEZGwUzyVIQ-wghxEcWSU"
DATA_AS_OF = "2026年11月4日時点"  # services.json の調査日

CSS = """
* { box-sizing: border-box; }
body {
    font-family: sans-serif;
    line-height: 1.9;
    margin: 0;
    background: #f6f7f9;
    color: #292929;
}
main {
    max-width: 760px;
    margin: 0 auto;
    padding: 18px 14px 32px;
}
.pr-notice {
    background: #fff3cd;
    border: 1px solid #ead28a;
    border-radius: 8px;
    padding: 9px 12px;
    font-size: 13px;
    margin-bottom: 16px;
}
header, .card {
    background: #fff;
    padding: 22px;
    border-radius: 14px;
    margin-bottom: 18px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
header h1 { font-size: 26px; margin: 0; }
header h1 a { color: #292929; text-decoration: none; }
header p { margin-bottom: 0; color: #555; }
nav.breadcrumb { font-size: 13px; margin-bottom: 12px; color: #555; }
nav.breadcrumb a { color: #1769aa; }
.category { color: #1769aa; font-size: 13px; font-weight: bold; }
.card h2 { font-size: 22px; line-height: 1.5; margin-top: 0; }
.card h3 {
    font-size: 17px;
    margin-top: 26px;
    border-left: 4px solid #1769aa;
    padding-left: 10px;
}
.card li { margin-bottom: 7px; }
.note {
    background: #f3f5f7;
    padding: 12px;
    border-radius: 8px;
    font-size: 13px;
}
.button {
    display: block;
    text-align: center;
    background: #1769aa;
    color: white;
    padding: 15px 12px;
    border-radius: 9px;
    text-decoration: none;
    font-weight: bold;
    margin-top: 22px;
}
.table-wrap { overflow-x: auto; -webkit-overflow-scrolling: touch; }
table.compare, table.spec {
    border-collapse: collapse;
    width: 100%;
    font-size: 14px;
    line-height: 1.6;
}
table.compare th, table.compare td,
table.spec th, table.spec td {
    border: 1px solid #dde3ea;
    padding: 8px 10px;
    text-align: left;
    vertical-align: top;
}
table.compare thead th {
    background: #1769aa;
    color: #fff;
    white-space: nowrap;
}
table.compare tbody th { background: #eef3f8; white-space: nowrap; }
table.compare tbody th a { color: #1769aa; }
table.spec th { background: #eef3f8; width: 34%; }
.grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.svc-card {
    background: #fff;
    border: 1px solid #e3e8ee;
    border-radius: 12px;
    padding: 16px;
}
.svc-card h3 { margin: 0 0 6px; font-size: 17px; border: none; padding: 0; }
.svc-card h3 a { color: #1769aa; text-decoration: none; }
.svc-card p { margin: 4px 0; font-size: 14px; }
.svc-card .price { font-size: 18px; font-weight: bold; color: #1769aa; }
footer { color: #666; font-size: 12px; padding: 8px; }
footer a { color: #1769aa; }
@media (max-width: 480px) {
    header, .card { padding: 18px; }
    header h1 { font-size: 23px; }
    .card h2 { font-size: 20px; }
    .grid { grid-template-columns: 1fr; }
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
<main>
  <div class="pr-notice">
    <strong>PR：</strong>当サイトはアフィリエイト広告を利用しています。
  </div>
  <header>
    <h1><a href="{SITE_URL}">{SITE_NAME}</a></h1>
    <p>{SITE_TAGLINE}</p>
  </header>
{body}
  <footer>
    <p>※当サイトはアフィリエイト広告を利用しています。</p>
    <p>料金・作品数などの情報は{DATA_AS_OF}の各社公式発表に基づきます。最新情報は各サービスの公式サイトでご確認ください。</p>
    <p><a href="{SITE_URL}">トップ</a> ／ <a href="{SITE_URL}privacy/">プライバシーポリシー・広告について</a></p>
  </footer>
</main>
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


# 目的別のおすすめ（事実ベースの編集セクション）
PURPOSES = [
    {
        "title": "アニメだけをとにかく安く見たい",
        "text": "月額が最安なのはDMM TVの550円（Web登録）。アニメ専門で作品数を求めるなら、7,400作品以上のdアニメストア（660円）が候補になります。",
        "slugs": ["dmm-tv", "d-anime-store"],
    },
    {
        "title": "アニメ以外もまとめて見たい",
        "text": "見放題作品数で選ぶならU-NEXT（44万本以上）。買い物などの特典も含めて考えたい場合は、プライム特典込みのAmazonプライム（月額600円）があります。",
        "slugs": ["u-next", "amazon-prime-video"],
    },
    {
        "title": "まず無料で試したい",
        "text": "無料期間が長いのはU-NEXTとdアニメストアの31日間、Amazonプライムの30日間。Netflix、Hulu、Disney+には現在無料トライアルがありません。",
        "slugs": ["u-next", "d-anime-store", "amazon-prime-video"],
    },
    {
        "title": "家族と分け合って同時視聴したい",
        "text": "同時視聴台数はU-NEXTとHuluが最大4台、Disney+はプレミアムプランで4台、Netflixはプレミアムで4台です。同一作品の同時視聴には制限があるサービスもあります。",
        "slugs": ["u-next", "hulu", "disney-plus"],
    },
]


def build_top(services, works, by_slug):
    rows = []
    for s in services:
        rows.append(
            "<tr>"
            f'<th><a href="{SITE_URL}service/{s["slug"]}/">{esc(s["name"])}</a></th>'
            f"<td>{esc(s['price_monthly'])}</td>"
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

    purpose_html = []
    for p in PURPOSES:
        links = "、".join(
            f'<a href="{SITE_URL}service/{slug}/">{esc(by_slug[slug]["name"])}</a>'
            for slug in p["slugs"]
            if slug in by_slug
        )
        purpose_html.append(
            f"<h3>{esc(p['title'])}</h3><p>{esc(p['text'])}</p><p>該当サービス：{links}</p>"
        )

    cards = []
    for s in services:
        cards.append(
            '<div class="svc-card">'
            f'<h3><a href="{SITE_URL}service/{s["slug"]}/">{esc(s["name"])}</a></h3>'
            f'<p class="price">月額{esc(s["price_monthly"])}</p>'
            f"<p>{esc(s['summary'])}</p>"
            f"<p>無料期間：{esc(s['free_trial'])} ／ アニメ作品数：{esc(s['anime_count'])}</p>"
            "</div>"
        )

    works_section = ""
    if works:
        items = "".join(
            f'<li><a href="{SITE_URL}work/{w["slug"]}/">{esc(w["title"])}はどこで見れる？</a></li>'
            for w in works
        )
        works_section = f"""
  <section class="card">
    <h2>作品から探す</h2>
    <ul>{items}</ul>
  </section>"""

    body = f"""
  <section class="card">
    <h2>アニメ見放題サービス 比較表</h2>
    <p>主要8サービスの料金・無料期間・作品数を、各社の公式発表をもとに比較しました（{DATA_AS_OF}）。サービス名をタップすると個別ページで詳細を確認できます。</p>
    {table}
    <p class="note">料金は税込。月額料金は登録方法（Web／アプリ）で異なる場合があります。作品数が「非公表」のサービスは、公式に本数を発表していません。</p>
  </section>
  <section class="card">
    <h2>目的別のおすすめ</h2>
    {''.join(purpose_html)}
  </section>
  <section class="card">
    <h2>サービス一覧</h2>
    <div class="grid">{''.join(cards)}</div>
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
            f"<td>月額{esc(s['price_monthly'])}</td>"
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
