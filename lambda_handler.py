import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from retrieve_resume import retrieve_chunks

load_dotenv()

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

extraction_tools = [
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

synthesis_tools = [
    {
        "type": "function",
        "function": {
            "name": "generate_fit_report",
            "description": "Generate an honest job fit analysis comparing job requirements to a candidate's resume",
            "parameters": {
                "type": "object",
                "properties": {
                    "fit_level": {
                        "type": "string",
                        "enum": ["strong", "partial", "poor"],
                        "description": "Overall fit assessment",
                    },
                    "fit_summary": {
                        "type": "string",
                        "description": "2-3 sentence honest assessment of overall fit for this specific role",
                    },
                    "strengths": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Specific ways the candidate's background matches what this job requires",
                    },
                    "gaps": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Specific requirements the job lists that the candidate does not clearly meet",
                    },
                    "talking_points": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Key points the candidate should lead with in a cover letter or interview for this role",
                    },
                },
                "required": ["fit_level", "fit_summary", "strengths", "gaps", "talking_points"],
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
        tools=extraction_tools,
    )
    tool_call = response.choices[0].message.tool_calls[0]
    return json.loads(tool_call.function.arguments)


def synthesize_fit(requirements, chunks):
    resume_context = "\n\n".join(
        [f"{c['title']}:\n{c['content']}" for c in chunks]
    )
    response = openai_client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[
            {
                "role": "user",
                "content": (
                    f"Analyze job fit for a software developer candidate.\n\n"
                    f"Job Requirements:\n"
                    f"- Required Skills: {requirements.get('required_skills', [])}\n"
                    f"- Tech Stack: {requirements.get('tech_stack', [])}\n"
                    f"- Years of Experience Required: {requirements.get('years_experience', 0)}\n\n"
                    f"Candidate's Relevant Resume Sections:\n{resume_context}\n\n"
                    f"Be honest and specific. If the candidate is missing key requirements, say so clearly."
                ),
            }
        ],
        tools=synthesis_tools,
        tool_choice={"type": "function", "function": {"name": "generate_fit_report"}},
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
        fit_report = synthesize_fit(requirements, chunks)

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
