import re, json, os

base = r'D:\hermes\priblog'

def hexo_quote(s):
    """Percent-encode only non-ASCII chars (UTF-8); preserve / - . _ space."""
    out = []
    for ch in s:
        if ord(ch) > 127:
            for b in ch.encode('utf-8'):
                out.append('%' + format(b, '02X'))
        else:
            out.append(ch)
    return ''.join(out)

# Verify encoding against known MI400 entry
test_path = "2026/09/01/AMD发布Instinct-MI400系列：CDNA-5登陆2nm，432GB-HBM4正面硬刚NVIDIA-Rubin/"
expected = "http://coderedeng.github.io/2026/09/01/AMD%E5%8F%91%E5%B8%83Instinct-MI400%E7%B3%BB%E5%88%97%EF%BC%9ACDNA-5%E7%99%BB%E9%99%862nm%EF%BC%8C432GB-HBM4%E6%AD%A3%E9%9D%A2%E7%A1%AC%E5%88%9ANVIDIA-Rubin/"
got = "http://coderedeng.github.io/" + hexo_quote(test_path)
assert got == expected, f"Encoding mismatch!\n  exp: {expected}\n  got: {got}"
print("✓ Encoding verified against MI400 entry")

title = "NVIDIA发布Vera Rubin NVL72：336B晶体管与20.7TB HBM4的AI工厂革命"
slug = "NVIDIA-Vera-Rubin-NVL72"
date_iso = "2026-09-05T02:00:00.000Z"  # 10:00 CST -> UTC 02:00
path = "2026/09/05/NVIDIA发布Vera Rubin NVL72：336B晶体管与20.7TB HBM4的AI工厂革命/"
permalink = "http://coderedeng.github.io/" + hexo_quote(path)

# Extract article body from built HTML
article_dir = os.path.join(base, '.deploy_git', '2026/09/05/NVIDIA发布Vera Rubin NVL72：336B晶体管与20.7TB HBM4的AI工厂革命')
index_html = os.path.join(article_dir, 'index.html')
html = open(index_html, encoding='utf-8').read()
m = re.search(r'<article[^>]*>(.*?)</article>', html, re.S)
body = m.group(1) if m else ""
print(f"✓ Article body extracted: {len(body)} chars")

entry = {
    "title": title,
    "slug": slug,
    "date": date_iso,
    "updated": date_iso,
    "comments": True,
    "path": path,
    "link": "",
    "permalink": permalink,
    "excerpt": "",
    "text": body,
    "categories": [{"name": "Tech前沿", "permalink": "http://coderedeng.github.io/categories/Tech%E5%89%8D%E6%B2%BF/", "slug": "Tech前沿"}],
    "tags": [
        {"name": "AI芯片", "permalink": "http://coderedeng.github.io/tags/AI%E8%8A%AF%E7%89%87/", "slug": "AI芯片"},
        {"name": "NVIDIA Vera Rubin", "permalink": "http://coderedeng.github.io/tags/NVIDIA-Vera-Rubin/", "slug": "NVIDIA-Vera-Rubin"},
        {"name": "NVL72", "permalink": "http://coderedeng.github.io/tags/NVL72/", "slug": "NVL72"}
    ]
}

cj_path = os.path.join(base, '.deploy_git', 'content.json')
d = json.load(open(cj_path, encoding='utf-8'))
posts = d['posts']  # it's a list

# Check for duplicate by path
dup = [x for x in posts if x.get('path') == path]
if dup:
    print("⚠ NVIDIA entry already present - skipping")
else:
    posts.append(entry)
    with open(cj_path, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False)
    print(f"✓ Added NVIDIA entry. Total posts now: {len(posts)}")

# Verify
d2 = json.load(open(cj_path, encoding='utf-8'))
nvidia = [x for x in d2['posts'] if 'Rubin NVL72' in x.get('title', '')]
print(f"✓ Verified NVIDIA entries: {len(nvidia)}")
if nvidia:
    e = nvidia[0]
    print("  path:", e['path'])
    print("  date:", e['date'])
    print("  permalink:", e['permalink'][:90])
    print("  text length:", len(e.get('text', '')))
