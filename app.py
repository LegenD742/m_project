# from flask import Flask, render_template, request, jsonify
# from backend.detectors.type1_detector import type1_similarity
# from backend.detectors.type2_detector import type2_similarity
# from backend.detectors.type3_detector import type3_similarity

# app = Flask(__name__)


# @app.route('/')
# def home():
#     return render_template('index.html')


# @app.route('/analyze', methods=['POST'])
# def analyze():
#     try:
#         data = request.get_json()

#         user_code = data.get('code', '')
#         compare_code = data.get('compare_code', '')  # (for now, or fetched from GitHub later)
#         clone_types = data.get('clone_types', [])    # ["type1", "type3"] etc.

#         if not user_code.strip():
#             return jsonify({"error": "No code provided"}), 400

#         results = {"type1": 0, "type2": 0, "type3": 0}

       
#         if "type1" in clone_types:
#             results["type1"] = type1_similarity(user_code, compare_code)

#         if "type2" in clone_types:
#             results["type2"] = type2_similarity(user_code, compare_code)

       
#         if "type3" in clone_types:
#             results["type3"] = type3_similarity(user_code, compare_code)

        
#         selected = [results[t] for t in clone_types if results[t] > 0]
#         overall = round(sum(selected) / len(selected), 2) if selected else 0

#         return jsonify({
#             "overall_similarity": overall,
#             **results,
#             "matches": [
#                 {
#                     "repository": "https://github.com/example/demo",
#                     "file": "src/example.py",
#                     "similarity": overall
#                 }
#             ]
#         })

#     except Exception as e:
#         print("Error in /analyze:", str(e))
#         return jsonify({"error": str(e)}), 500


# #runnnnnn.....

# if __name__ == '__main__':
#     app.run(debug=True)






from flask import Flask, render_template, request, jsonify
from backend.detectors.type1_detector import type1_similarity
from backend.detectors.type2_detector import type2_similarity
from backend.utils.github_fetcher import fetch_sourcegraph_candidates, fetch_file_content
import sys

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    user_code = data.get('code', '')
    lang = data.get('language', 'Python')
    clone_types = data.get('clone_types', [])

    candidates = fetch_sourcegraph_candidates(user_code, language=lang, limit=3)

    results_list = []
    sim1, sim2 = 0, 0  # <--- ✅ initialize here

    for c in candidates:
        sample_code = fetch_file_content(c["file_url"])
        if not sample_code:
            continue

        if "type1" in clone_types:
            sim1 = type1_similarity(user_code, sample_code)
        if "type2" in clone_types:
            sim2 = type2_similarity(user_code, sample_code)

        overall = round((sim1 + sim2) / 2, 2) if any([sim1, sim2]) else 0

        results_list.append({
            "repository": c["repo"],
            "file": c["name"],
            "similarity": overall
        })

    overall_similarity = round(sum([r["similarity"] for r in results_list]) / len(results_list), 2) if results_list else 0

    return jsonify({
        "overall_similarity": overall_similarity,
        "type1": sim1 if "type1" in clone_types else 0,
        "type2": sim2 if "type2" in clone_types else 0,
        "matches": results_list
    })

if __name__ == '__main__':
    app.run(debug=True)
