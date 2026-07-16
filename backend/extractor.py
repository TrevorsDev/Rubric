import json
from openai import OpenAI

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


def extract_requirements(client: OpenAI, job_posting: str) -> dict:
    response = client.chat.completions.create(
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
