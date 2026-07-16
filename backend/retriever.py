from pymongo.collection import Collection


def retrieve_chunks(collection: Collection, skills: list[str]) -> list[dict]:
    query = {"skills": {"$in": skills}}
    return list(collection.find(query, {"_id": 0}))
