
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

    title = "今日のおすすめ商品"
    content = ""

    if selected:
        product_title = html.escape(str(selected.get("title", "おすすめ商品")))
        description = html.escape(str(selected.get("description", "")))
        url = html.escape(str(selected["affiliate_url"]), quote=True)

        content = f"""
        <article class="product">
          <h2>{product_title}</h2>
          <p>{description}</p>
          <a class="button" href="{url}" rel="nofollow sponsored noopener" target="_blank">
            商品の詳細を見る
          </a>
        </article>
        """
    else:
        content = """
        <p>現在、準備中です。おすすめ商品を順次追加します。</p>
        """

    page = f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="毎日チェックしたいおすすめ商品を紹介します。">
<style>
body {{ font-family: sans-serif; line-height: 1.8; margin: 0; background: #f5f5f5; color: #222; }}
main {{ max-width: 720px; margin: 0 auto; padding: 24px 16px; }}
header, .product {{ background: white; padding: 24px; border-radius: 12px; margin-bottom: 20px; }}
.button {{ display: inline-block; background: #1769aa; color: white; padding: 12px 20px; border-radius: 8px; text-decoration: none; }}
footer {{ color: #666; font-size: 13px; }}
</style>
</head>
<body>
<main>
<header>
<h1>{title}</h1>
<p>気になる商品を見つけるためのおすすめ情報サイトです。</p>
</header>
{content}
<footer>
<p>※商品リンクにはアフィリエイトリンクが含まれる場合があります。</p>
<p>掲載情報は購入前に販売元のページでご確認ください。</p>
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
