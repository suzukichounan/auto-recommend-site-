
import json
import html
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent
DATA_FILE = ROOT / "products.json"
OUTPUT_DIR = ROOT / "public"
OUTPUT_FILE = OUTPUT_DIR / "index.html"


def esc(value):
    return html.escape(str(value), quote=True)


def main():
    with DATA_FILE.open("r", encoding="utf-8") as f:
        products = json.load(f)

    enabled = [
        p for p in products
        if p.get("enabled") is True
        and str(p.get("affiliate_url", "")).startswith("https://")
    ]

    selected = None

    if enabled:
        selected = enabled[date.today().toordinal() % len(enabled)]

    title = "きょうのおすすめ帖"

    if selected:
        product_title = esc(selected.get("title", "おすすめ商品"))
        description = esc(selected.get("description", ""))
        url = esc(selected.get("affiliate_url", ""))

        recommended_for = selected.get("recommended_for", [])
        check_points = selected.get("check_points", [])

        recommended_html = "".join(
            f"<li>{esc(item)}</li>"
            for item in recommended_for
        )

        check_html = "".join(
            f"<li>{esc(item)}</li>"
            for item in check_points
        )

        content = f"""
        <article class="product">
          <p class="category">今回のおすすめ</p>
          <h2>{product_title}</h2>

          <h3>どんな商品・サービス？</h3>
          <p>{description}</p>

          <h3>こんな人におすすめ</h3>
          <ul>{recommended_html}</ul>

          <h3>購入前に確認したいこと</h3>
          <ul>{check_html}</ul>

          <p class="note">
            価格・送料・在庫・配送日などは、
            販売元のページで確認してください。
          </p>

          <a class="button"
             href="{url}"
             rel="nofollow sponsored noopener"
             target="_blank">
            商品の詳細を確認する →
          </a>
        </article>
        """
    else:
        content = """
        <section class="product">
          <h2>おすすめ商品を準備中です</h2>
          <p>これからおすすめ商品を順次紹介していきます。</p>
        </section>
        """

    page = f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="暮らしや趣味に役立つ商品を、選ぶときのポイントと一緒に紹介します。">
<style>
* {{ box-sizing: border-box; }}

body {{
    font-family: sans-serif;
    line-height: 1.9;
    margin: 0;
    background: #f6f7f9;
    color: #292929;
}}

main {{
    max-width: 760px;
    margin: 0 auto;
    padding: 18px 14px 32px;
}}

.pr-notice {{
    background: #fff3cd;
    border: 1px solid #ead28a;
    border-radius: 8px;
    padding: 9px 12px;
    font-size: 13px;
    margin-bottom: 16px;
}}

header, .product {{
    background: #fff;
    padding: 22px;
    border-radius: 14px;
    margin-bottom: 18px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}}

header h1 {{
    font-size: 26px;
    margin: 0;
}}

header p {{
    margin-bottom: 0;
    color: #555;
}}

.category {{
    color: #1769aa;
    font-size: 13px;
    font-weight: bold;
}}

.product h2 {{
    font-size: 22px;
    line-height: 1.5;
}}

.product h3 {{
    font-size: 17px;
    margin-top: 26px;
    border-left: 4px solid #1769aa;
    padding-left: 10px;
}}

.product li {{
    margin-bottom: 7px;
}}

.note {{
    background: #f3f5f7;
    padding: 12px;
    border-radius: 8px;
    font-size: 13px;
}}

.button {{
    display: block;
    text-align: center;
    background: #1769aa;
    color: white;
    padding: 15px 12px;
    border-radius: 9px;
    text-decoration: none;
    font-weight: bold;
    margin-top: 22px;
}}

.button:hover {{
    opacity: 0.9;
}}

footer {{
    color: #666;
    font-size: 12px;
    padding: 8px;
}}

@media (max-width: 480px) {{
    header, .product {{
        padding: 18px;
    }}

    header h1 {{
        font-size: 23px;
    }}

    .product h2 {{
        font-size: 20px;
    }}
}}
</style>
</head>
<body>
<main>
  <div class="pr-notice">
    <strong>PR：</strong>当サイトはアフィリエイト広告を利用しています。
  </div>

  <header>
    <h1>{title}</h1>
    <p>商品選びの参考になる情報をお届けします。</p>
  </header>

  {content}

  <footer>
    <p>※当サイトはアフィリエイト広告を利用しています。</p>
    <p>商品の価格・在庫・送料・詳細は販売元のページでご確認ください。</p>
  </footer>
</main>
</body>
</html>
"""

    OUTPUT_DIR.mkdir(exist_ok=True)
    OUTPUT_FILE.write_text(page, encoding="utf-8")
    print(f"サイトを生成しました: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
