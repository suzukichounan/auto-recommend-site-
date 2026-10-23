
import json
import html
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent
DATA_FILE = ROOT / "products.json"
OUTPUT_DIR = ROOT / "public"
OUTPUT_FILE = OUTPUT_DIR / "index.html"


def main():
    with DATA_FILE.open("r", encoding="utf-8") as f:
        products = json.load(f)

    enabled = [
        p for p in products
        if p.get("enabled") is True
        and str(p.get("affiliate_url", "")).startswith("https://")
    ]

    today = date.today()
    selected = None

    if enabled:
        index = today.toordinal() % len(enabled)
        selected = enabled[index]

    title = "きょうのおすすめ帖"
    content = ""

    if selected:
        product_title = html.escape(
            str(selected.get("title", "おすすめ商品"))
        )
        description = html.escape(
            str(selected.get("description", ""))
        )
        url = html.escape(
            str(selected["affiliate_url"]), quote=True
        )

        content = f"""
        <article class="product">
          <h2>{product_title}</h2>
          <p>{description}</p>
          <a class="button"
             href="{url}"
             rel="nofollow sponsored noopener"
             target="_blank">
            商品の詳細を見る
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
<meta name="description" content="アニメ・漫画関連の商品から、日常生活に役立つ便利なアイテムまで紹介します。">
<style>
* {{ box-sizing: border-box; }}
body {{
    font-family: sans-serif;
    line-height: 1.8;
    margin: 0;
    background: #f5f5f5;
    color: #222;
}}
main {{
    max-width: 720px;
    margin: 0 auto;
    padding: 20px 16px;
}}
header, .product {{
    background: white;
    padding: 24px;
    border-radius: 12px;
    margin-bottom: 20px;
}}
header h1 {{
    margin-top: 12px;
}}
.pr-notice {{
    background: #fff3cd;
    border: 1px solid #ead28a;
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 14px;
    margin-bottom: 16px;
}}
.button {{
    display: inline-block;
    background: #1769aa;
    color: white;
    padding: 12px 20px;
    border-radius: 8px;
    text-decoration: none;
}}
footer {{
    color: #666;
    font-size: 13px;
    padding: 8px;
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
<p>毎日の暮らしや趣味に役立つ、おすすめ商品を紹介します。</p>
</header>

{content}

<footer>
<p>※商品リンクにはアフィリエイト広告が含まれています。</p>
<p>商品の価格・在庫・詳細は、リンク先の販売元サイトでご確認ください。</p>
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
