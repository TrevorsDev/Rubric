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


if __name__ == "__main__":
    JOB_POSTING = """
    We are hiring a Python backend developer to build AI-integrated applications.
    Requirements: Python, MongoDB, AWS Lambda, OpenAI API, REST APIs, Git, Node.js.
    1+ years of experience. Serverless architecture experience preferred.
    Nice to have: React, CI/CD pipelines, Next.js.
    """

    print("=== Step 1: Extracting requirements from job posting ===")
    requirements = extract_requirements(JOB_POSTING)
    print(json.dumps(requirements, indent=2))

    skills_to_match = requirements.get("required_skills", []) + requirements.get("tech_stack", [])

    print("\n=== Step 2: Retrieving matching resume chunks from MongoDB ===")
    chunks = retrieve_chunks(skills_to_match)
    for chunk in chunks:
        matched = [s for s in chunk["skills"] if s in skills_to_match]
        print(f"\n--- {chunk['title']} ({chunk['type']}) ---")
        print(f"Matched on: {matched}")
