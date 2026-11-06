import itertools
import json
import os
from flask import Flask, jsonify, request, abort

app = Flask(__name__)

FILE_NAME = "notes.json"

if os.path.exists(FILE_NAME):
    with open(FILE_NAME, "r", encoding="utf-8") as f:
        notes = json.load(f)
        if notes:
            max_id = max(n["id"] for n in notes)
            note_ids = itertools.count(max_id + 1)
        else:
            note_ids = itertools.count(1)
else:
    notes = []
    note_ids = itertools.count(1)


def save_notes():
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(notes, f, ensure_ascii=False, indent=4)


def find_note(note_id):
    return next((n for n in notes if n["id"] == note_id), None)


@app.get("/")
def index():
    return "<h1>Гостевая книга</h1>"


@app.get("/notes")
def list_notes():
    author = request.args.get("author")

    limit_str = request.args.get("limit", "10")
    offset_str = request.args.get("offset", "0")

    try:
        limit = int(limit_str)
        offset = int(offset_str)
    except ValueError:
        return jsonify(error="limit and offset must be integers"), 400

    if not (1 <= limit <= 100):
        return jsonify(error="limit must be between 1 and 100"), 400

    if offset < 0:
        return jsonify(error="offset must be >= 0"), 400

    sort_by = request.args.get("sort", "id")
    order = request.args.get("order", "asc")

    if sort_by not in ["id", "likes"]:
        return jsonify(error="sort must be 'id' or 'likes'"), 400
    if order not in ["asc", "desc"]:
        return jsonify(error="order must be 'asc' or 'desc'"), 400

    result = notes
    if author is not None:
        result = [n for n in result if n.get("author") == author]

    reverse = True if order == "desc" else False
    result = sorted(result, key=lambda x: x.get(sort_by, 0), reverse=reverse)

    result = result[offset: offset + limit]
    return jsonify(result)


@app.post("/notes")
def create_note():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify(error="JSON object is required"), 400

    if not isinstance(data.get("text"), str) or not data["text"].strip():
        return jsonify(error="field 'text' (non-empty string) is required"), 400

    if not isinstance(data.get("author"), str) or not data["author"].strip():
        return jsonify(error="field 'author' (non-empty string) is required"), 400

    note = {
        "id": next(note_ids),
        "author": data["author"].strip(),
        "text": data["text"].strip(),
        "likes": 0
    }
    notes.append(note)
    save_notes()
    return jsonify(note), 201


@app.post("/notes/<int:note_id>/like")
def like_note(note_id):
    note = find_note(note_id)
    if note is None:
        abort(404)

    note["likes"] += 1
    save_notes()
    return jsonify(note), 200


@app.put("/notes/<int:note_id>")
def update_note(note_id):
    note = find_note(note_id)
    if note is None:
        abort(404)

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify(error="JSON object is required"), 400

    if not isinstance(data.get("text"), str) or not data["text"].strip():
        return jsonify(error="field 'text' (non-empty string) is required"), 400

    if not isinstance(data.get("author"), str) or not data["author"].strip():
        return jsonify(error="field 'author' (non-empty string) is required"), 400

    note["author"] = data["author"].strip()
    note["text"] = data["text"].strip()
    save_notes()

    return jsonify(note), 200


@app.patch("/notes/<int:note_id>")
def patch_note(note_id):
    note = find_note(note_id)
    if note is None:
        abort(404)

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify(error="JSON object is required"), 400

    if "text" not in data and "author" not in data:
        return jsonify(error="At least 'text' or 'author' is required"), 400

    if "text" in data:
        if not isinstance(data["text"], str) or not data["text"].strip():
            return jsonify(error="field 'text' must be a non-empty string"), 400
        note["text"] = data["text"].strip()

    if "author" in data:
        if not isinstance(data["author"], str) or not data["author"].strip():
            return jsonify(error="field 'author' must be a non-empty string"), 400
        note["author"] = data["author"].strip()

    save_notes()
    return jsonify(note), 200


@app.get("/notes/<int:note_id>")
def get_note(note_id):
    note = find_note(note_id)
    if note is None:
        abort(404)
    return jsonify(note)


@app.delete("/notes/<int:note_id>")
def delete_note(note_id):
    note = find_note(note_id)
    if note is None:
        abort(404)
    notes.remove(note)
    save_notes()
    return "", 204


@app.delete("/notes")
def bulk_delete_notes():
    author = request.args.get("author")

    if not author or not author.strip():
        return jsonify(error="author parameter is required and cannot be empty"), 400

    author = author.strip()
    global notes

    initial_count = len(notes)
    notes = [n for n in notes if n.get("author") != author]

    deleted_count = initial_count - len(notes)
    save_notes()

    return jsonify(deleted=deleted_count), 200


@app.get("/authors")
def get_authors():
    stats = {}

    for n in notes:
        author = n.get("author")
        if author not in stats:
            stats[author] = {"author": author, "notes": 0, "likes": 0}
        stats[author]["notes"] += 1
        stats[author]["likes"] += n.get("likes", 0)

    result = list(stats.values())
    result.sort(key=lambda x: x["author"])

    return jsonify(result)


@app.errorhandler(404)
def not_found(error):
    return jsonify(error="not found"), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify(error="method not allowed"), 405


if __name__ == "__main__":
    app.run(debug=True)