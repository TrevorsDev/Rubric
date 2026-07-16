import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from pymongo import MongoClient
from pymongo.server_api import ServerApi

from backend.extractor import extract_requirements
from backend.retriever import retrieve_chunks
from backend.synthesizer import synthesize_fit

load_dotenv()

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

mongo_client = MongoClient(os.getenv("MONGODB_URI"), server_api=ServerApi("1"))
collection = mongo_client["job_fit_analyzer"]["resume_chunks"]


def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
        job_posting = body.get("job_posting", "")

        if not job_posting or not job_posting.strip():
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "job_posting is required"}),
            }

        requirements = extract_requirements(openai_client, job_posting)
        skills_to_match = requirements.get("required_skills", []) + requirements.get("tech_stack", [])
        chunks = retrieve_chunks(collection, skills_to_match)
        fit_report = synthesize_fit(openai_client, requirements, chunks)

        return {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({
                "requirements": requirements,
                "matching_chunks": chunks,
                "fit_report": fit_report,
            }),
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
        }
