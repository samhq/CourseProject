from firebase_admin import db
from search import search_query
from contents import final_content


def add_to_bookmark(bookmark_title, bookmark_url, user_id):
    error = False
    msg = "Bookmark added"
    new_bookmark_id = None

    try:
        parsed_content = final_content(bookmark_url)

        ref = db.reference("/"+user_id+"/bookmarks/")
        content = {
            "title": bookmark_title,
            "url": bookmark_url,
            "content": parsed_content,
        }
        p = ref.push(content)
        new_bookmark_id = p.key
    except Exception as e:
        error = True
        msg = str(e)

    return {
        "error": error,
        "message": msg,
        "bookmark_id": new_bookmark_id
    }


def delete_from_bookmark(bookmark_id, user_id):
    error = False
    msg = "Bookmark deleted"

    try:
        ref = db.reference("/"+user_id+"/bookmarks/")

        ref.child(bookmark_id).set({})
    except Exception as e:
        error = True
        msg = str(e)

    return {
        "error": error,
        "message": msg
    }


def search_with_query(query, top_n, user_id):
    all_b = get_user_bookmarks(user_id)
    if (all_b["error"]):
        return all_b

    bookmarks = all_b["bookmarks"]
    if(bookmarks is None or len(bookmarks) == 0):
        return {
            "error": True,
            "message": f"No bookmarks to search in",
            "bookmarks": {}
        }

    corpus = []
    ids = []
    for key, value in bookmarks.items():
        corpus.append(value["content"])
        ids.append(key)

    try:
        res_ids = search_query(query, top_n, corpus)
        result = {}
        for k, v in res_ids.items():
            rid = ids[k]
            result[rid] = bookmarks[rid]
            result[rid]["score"] = v

        b_dict = {}
        if (res_ids is not None and len(res_ids) > 0):
            b_dict = clean_bookmarks_content(result, True)

        return {
            "error": False,
            "message": "Searched successfully",
            "bookmarks": b_dict
        }
    except Exception as e:
        return {
            "error": True,
            "message": str(e),
            "bookmarks": {}
        }


def all_bookmarks(user_id):
    error = False
    msg = "Fetched successfully"

    res = get_user_bookmarks(user_id)
    if (res["error"]):
        return {
            "error": True,
            "message": res["message"],
            "bookmarks": {}
        }

    b_dict = {}
    if (res["bookmarks"] is not None and len(res["bookmarks"]) > 0):
        b_dict = clean_bookmarks_content(res["bookmarks"])

    return {
        "error": error,
        "message": msg,
        "bookmarks": b_dict
    }


def get_user_bookmarks(user_id):
    error = False
    msg = "Fetched successfully"
    bookmarks = {}

    try:
        ref = db.reference("/"+user_id+"/bookmarks/")

        bookmarks = ref.get()
    except Exception as e:
        error = True
        msg = str(e)

    return {
        "error": error,
        "message": msg,
        "bookmarks": bookmarks
    }


def clean_bookmarks_content(bookmarks, score=False):
    b_dict = {}
    for k, v in bookmarks.items():
        b_dict[k] = {
            "title": v["title"],
            "url": v["url"]
        }
        if (score):
            b_dict[k]["score"] = float("{:.4f}".format(v["score"]))

    return b_dict
