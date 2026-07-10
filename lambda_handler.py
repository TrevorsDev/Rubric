import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from retrieve_resume import retrieve_chunks

load_dotenv()

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

tools = [
    {
        "type": "function",
        "function": {
            "name": "extract_job_requirements",
            "description": "Extract structured hiring requirements from a job posting",
            "parameters": {
                "type": "object",
                "properties": {
                    "required_skills": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Technical skills explicitly required",
                    },
                    "years_experience": {
                        "type": "integer",
                        "description": "Minimum years of experience required",
                    },
                    "tech_stack": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Specific languages, frameworks, or tools mentioned",
                    },
                },
                "required": ["required_skills", "years_experience", "tech_stack"],
            },
        },
    }
]


def extract_requirements(job_posting):
    response = openai_client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[
            {
                "role": "user",
                "content": f"Extract the hiring requirements from this job posting:\n\n{job_posting}",
            }
        ],
        tools=tools,
    )
    tool_call = response.choices[0].message.tool_calls[0]
    return json.loads(tool_call.function.arguments)


def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
        job_posting = body.get("job_posting", "")

        if not job_posting:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "job_posting is required"}),
            }

        requirements = extract_requirements(job_posting)
        skills_to_match = requirements.get("required_skills", []) + requirements.get("tech_stack", [])
        chunks = retrieve_chunks(skills_to_match)

        return {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({
                "requirements": requirements,
                "matching_chunks": chunks,
            }),
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
        }
