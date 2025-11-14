import requests
import re
import sys

# -------------------------------
# 🔐 Add your GitHub personal access token here
# -------------------------------
# You can generate one at: https://github.com/settings/tokens
# Give it at least "public_repo" and "code" read permissions
GITHUB_TOKEN = "process.env.code"  # <-- put token here
GITHUB_API = "https://api.github.com/search/code"
# -------------------------------


def extract_keywords_from_code(code: str) -> str:
    """Extract meaningful identifiers from code snippet."""
    tokens = re.findall(r"[A-Za-z_]{3,}", code)
    stopwords = {
        "for", "if", "else", "elif", "while", "int", "float", "var",
        "def", "print", "return", "main", "public", "static", "void",
        "class", "new"
    }
    keywords = [t for t in tokens if t.lower() not in stopwords]
    if not keywords:
        keywords = ["example", "function"]
    query = "+".join(list(dict.fromkeys(keywords))[:5])
    return query


import requests
import re
import sys
import os

# Optional GitHub token (not required for Sourcegraph)
GITHUB_TOKEN = ""

# ✅ Sourcegraph fallback for code search
def fetch_sourcegraph_candidates(code, language="Python", limit=3):
    """Search Sourcegraph for similar code snippets."""
    query = extract_keywords_from_code(code)
    print(f"🔎 Querying Sourcegraph with query: {query}", file=sys.stderr)

    url = "https://sourcegraph.com/.api/graphql"
    graphql_query = {
        "query": f"""
        {{
          search(query: "{query} lang:{language}", first: {limit}) {{
            results {{
              results {{
                ... on FileMatch {{
                  file {{
                    path
                  }}
                  repository {{
                    name
                    url
                  }}
                  lineMatches {{
                    preview
                  }}
                }}
              }}
            }}
          }}
        }}
        """
    }

    try:
        res = requests.post(url, json=graphql_query, timeout=15)
        if res.status_code != 200:
            print(f"⚠️ Sourcegraph API error: {res.status_code} {res.text}", file=sys.stderr)
            return []

        data = res.json()
        matches = data.get("data", {}).get("search", {}).get("results", {}).get("results", [])
        results = []

        for m in matches:
            repo = m["repository"]["url"]
            path = m["file"]["path"]
            results.append({
                "repo": repo,
                "file_url": repo + "/-/blob/" + path,
                "name": path.split("/")[-1]
            })

        print(f"✅ Found {len(results)} code files from Sourcegraph", file=sys.stderr)
        return results
    except Exception as e:
        print("❌ Sourcegraph fetch error:", e, file=sys.stderr)
        return []


def fetch_file_content(raw_url):
    """Download raw file content from GitHub."""
    try:
        r = requests.get(raw_url)
        if r.status_code == 200:
            return r.text
        else:
            print(f"⚠️ Failed to fetch file: {raw_url} ({r.status_code})", file=sys.stderr)
    except Exception as e:
        print("Error fetching file:", e, file=sys.stderr)
    return ""
