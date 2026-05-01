import os
import re
import requests

USERNAME = "NimaShafie"
TOKEN = os.environ["GH_TOKEN"]

QUERY = """
{
  user(login: "%s") {
    pinnedItems(first: 6, types: [REPOSITORY]) {
      nodes {
        ... on Repository {
          name
          owner { login }
          url
          description
          primaryLanguage { name color }
        }
      }
    }
  }
}
""" % USERNAME

response = requests.post(
    "https://api.github.com/graphql",
    json={"query": QUERY},
    headers={"Authorization": f"bearer {TOKEN}"},
)
response.raise_for_status()

repos = response.json()["data"]["user"]["pinnedItems"]["nodes"]

LANG_LOGOS = {
    "Rust":           ("000",    "rust",       "white"),
    "Python":         ("3776AB", "python",     "white"),
    "JavaScript":     ("F7DF1E", "javascript", "black"),
    "TypeScript":     ("3178C6", "typescript", "white"),
    "C++":            ("00599C", "cplusplus",  "white"),
    "C#":             ("239120", "csharp",     "white"),
    "C":              ("A8B9CC", "c",          "black"),
    "HTML":           ("E34F26", "html5",      "white"),
    "Go":             ("00ADD8", "go",         "white"),
    "Java":           ("ED8B00", "openjdk",    "white"),
    "Swift":          ("F54A2A", "swift",      "white"),
    "Kotlin":         ("7F52FF", "kotlin",     "white"),
    "Ruby":           ("CC342D", "ruby",       "white"),
    "Shell":          ("121011", "gnubash",    "white"),
    "Jupyter Notebook": ("F37626", "jupyter",  "white"),
}

ICONS = ["🔷", "📡", "🤖", "🎯", "❄️", "🏨"]

rows = ["| | Project | Description | Language | Stars |", "|:---:|---|---|:---:|:---:|"]

for i, repo in enumerate(repos):
    owner  = repo["owner"]["login"]
    name   = repo["name"]
    url    = repo["url"]
    desc   = (repo["description"] or "").replace("|", "\\|")
    lang   = (repo.get("primaryLanguage") or {}).get("name", "")
    icon   = ICONS[i] if i < len(ICONS) else "📁"

    if lang in LANG_LOGOS:
        color, logo, text = LANG_LOGOS[lang]
        lang_badge = (
            f"![{lang}](https://img.shields.io/badge/"
            f"{lang.replace(' ', '%20').replace('#', '%23').replace('+', '%2B')}"
            f"-{color}?style=flat-square&logo={logo}&logoColor={text})"
        )
    elif lang:
        lang_badge = f"`{lang}`"
    else:
        lang_badge = ""

    stars_badge = (
        f"![](https://img.shields.io/github/stars/{owner}/{name}"
        f"?style=flat-square&color=gold&labelColor=1a1b27)"
    )

    rows.append(f"| {icon} | [{name}]({url}) | {desc} | {lang_badge} | {stars_badge} |")

section = "\n".join(rows)

readme_path = "README.md"
with open(readme_path, "r", encoding="utf-8") as f:
    content = f.read()

new_content = re.sub(
    r"<!-- PINNED-REPOS:START -->.*?<!-- PINNED-REPOS:END -->",
    f"<!-- PINNED-REPOS:START -->\n{section}\n<!-- PINNED-REPOS:END -->",
    content,
    flags=re.DOTALL,
)

with open(readme_path, "w", encoding="utf-8") as f:
    f.write(new_content)

print(f"Updated README with {len(repos)} pinned repos.")
