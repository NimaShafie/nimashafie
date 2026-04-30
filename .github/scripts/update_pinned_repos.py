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

rows = []
for i in range(0, len(repos), 2):
    pair = repos[i : i + 2]
    cards = []
    for r in pair:
        owner, name, url = r["owner"]["login"], r["name"], r["url"]
        card = (
            f'  <a href="{url}">\n'
            f'    <img src="https://github-readme-stats.vercel.app/api/pin/'
            f'?username={owner}&repo={name}&theme=tokyonight&hide_border=true" />\n'
            f'  </a>'
        )
        cards.append(card)
    rows.append('<div align="center">\n' + "\n  &nbsp;\n".join(cards) + "\n</div>")

section = "\n\n".join(rows)

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
