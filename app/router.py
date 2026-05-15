def route(query):
    q = query.lower()

    if "excel" in q:
        return "excel"
    elif "image" in q:
        return "image"
    else:
        return "rag"