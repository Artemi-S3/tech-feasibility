from flask import Flask, request, jsonify, abort
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

ITEMS = [
    {"id": 0, "name": "mars images 2020", "path": "path/to/mars"}, 
    {"id": 1, "name": "europa images 1987", "path": "path/to/europa"}, 
    {"id": 2, "name": "mars rover soil samples", "path": "path/to/rover/soilsamples"}
]

# curl "http://127.0.0.1:5000/"
@app.get("/")
def root():
    # return homepage metadata
    return jsonify({"message": "Here's the Flask root"}), 200

# curl "http://127.0.0.1:5000/search/europa%20images%201987"
@app.get("/search/<item>")
def search(item: str):
    # return item requested from URL
    return jsonify({"message": f"You searched for: '{item}'"}), 200

# curl "http://127.0.0.1:5000/all" or 
# curl "http://127.0.0.1:5000/all?limit=2"
@app.get("/all")
def list_all():
    try:
        # optional query parameter
        limit = int(request.args.get("limit", len(ITEMS)))
    except ValueError:
        abort(400, description="Limit must be an integer")

    return jsonify(ITEMS[:limit])

""" 
curl -X POST "http://127.0.0.1:5000/new-item" \
     -H "Content-Type: application/json" \
     -d '{"name":"moon base schematics 2028","path":"path/to/moon/base/schematics"}'
"""
@app.post("/new-item")
def create_item():
    data = request.get_json(silent=True) or {}
    if not isinstance(data.get("name"), str):
        abort(400, description="'name' is required and must be a string")
    if not isinstance(data.get("path"), str) or "/" not in data.get("path"):
        abort(400, description="'path' is required, must be a string, and must contain '/' delimeters")

    new_id = max(i["id"] for i in ITEMS) + 1 if ITEMS else 0
    new_item = {"id": new_id, "name": data["name"], "path": data["path"]}
    ITEMS.append(new_item)
    return jsonify(new_item), 201

@app.errorhandler(400)
def bad_request(error):
    return jsonify(error="bad_request", detail=str(error.description)), 400

if __name__ == "__main__":
    app.run(debug=True)
