import json
from openai import OpenAI

tools = [
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


def synthesize_fit(client: OpenAI, requirements: dict, chunks: list[dict]) -> dict:
    resume_context = "\n\n".join(
        [f"{c['title']}:\n{c['content']}" for c in chunks]
    )
    response = client.chat.completions.create(
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
        tools=tools,
        tool_choice={"type": "function", "function": {"name": "generate_fit_report"}},
    )
    tool_call = response.choices[0].message.tool_calls[0]
    return json.loads(tool_call.function.arguments)
