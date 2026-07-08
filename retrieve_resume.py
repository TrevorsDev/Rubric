import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()

uri = os.getenv("MONGODB_URI")
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["job_fit_analyzer"]
collection = db["resume_chunks"]


def retrieve_chunks(required_skills):
    query = {"skills": {"$in": required_skills}}
    results = list(collection.find(query, {"_id": 0}))
    return results


if __name__ == "__main__":
    test_skills = ["Python", "MongoDB", "AWS Lambda", "OpenAI API"]
    chunks = retrieve_chunks(test_skills)
    for chunk in chunks:
        print(f"\n--- {chunk['title']} ({chunk['type']}) ---")
        print(f"Matched skills: {[s for s in chunk['skills'] if s in test_skills]}")
