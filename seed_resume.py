import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()

uri = os.getenv("MONGODB_URI")
client = MongoClient(uri, server_api=ServerApi('1'))

db = client["job_fit_analyzer"]
collection = db["resume_chunks"]

resume_chunks = [
    {
        "type": "summary",
        "title": "Professional Summary",
        "content": (
            "Full-stack software developer with hands-on experience designing, developing, and deploying "
            "applications across JavaScript, React, Python, and Node.js. Currently building Rubric, a "
            "Python/OpenAI API tool demonstrating applied AI engineering across serverless compute, structured "
            "data extraction, and document retrieval. Integrates AI development tools (Claude Code, Cursor) as "
            "a primary engineering workflow across architecture, debugging, and rapid prototyping. Quick to pick "
            "up new languages and frameworks. US Citizen with ability to obtain and maintain a Public Trust clearance."
        ),
        "skills": ["Python", "JavaScript", "React", "Node.js", "OpenAI API", "serverless", "AI-assisted development"]
    },
    {
        "type": "skills",
        "title": "Technical Skills",
        "content": (
            "Languages & Frameworks: JavaScript, React, Node.js, Python, HTML5, CSS3, Tailwind, SQL. "
            "Databases: MS SQL Server, PostgreSQL, Supabase, MongoDB. "
            "Cloud & Deployment: Netlify, Vercel, AWS Lambda, API Gateway, Google Cloud Platform, Heroku, serverless functions. "
            "Tools & Workflow: Git/GitHub, VS Code, Agile/Scrum, RESTful APIs, JSON, CI/CD Pipelines. "
            "Generative AI: Hands-on experience building with OpenAI API (function-calling, chat completions), "
            "Claude, Cursor, GitHub Copilot, V0. Applying AI-assisted workflows across architecture design, "
            "debugging, and rapid prototyping to accelerate delivery."
        ),
        "skills": [
            "JavaScript", "React", "Node.js", "Python", "HTML5", "CSS3", "Tailwind", "SQL",
            "PostgreSQL", "MS SQL Server", "Supabase", "MongoDB",
            "AWS Lambda", "API Gateway", "Netlify", "Vercel", "GCP", "Heroku", "serverless",
            "Git", "GitHub", "Agile", "Scrum", "REST APIs", "JSON", "CI/CD",
            "OpenAI API", "function-calling", "Claude", "Cursor", "GitHub Copilot"
        ]
    },
    {
        "type": "project",
        "title": "Rubric – Job-Fit Analyzer",
        "content": (
            "Building a full-stack job-fit analysis tool in Python that extracts structured requirements from a "
            "job posting using OpenAI function-calling, retrieves resume content from a MongoDB knowledge base, "
            "and generates a structured gap and fit report. Spans a Python serverless backend on AWS Lambda, "
            "a MongoDB Atlas document retrieval layer, and a planned Next.js frontend deployed on Vercel. "
            "Uses OpenAI function-calling to return validated JSON output from unstructured job postings. "
            "Designed the MongoDB Atlas knowledge base to store resume content as retrievable chunks for RAG-based retrieval."
        ),
        "skills": [
            "Python", "OpenAI API", "function-calling", "MongoDB Atlas", "AWS Lambda", "serverless",
            "Next.js", "Vercel", "RAG", "document retrieval", "JSON", "API Gateway"
        ]
    },
    {
        "type": "experience",
        "title": "IT Internship – Pima County ITD",
        "content": (
            "Independently designed and developed a full-stack asset tracking application in React and PostgreSQL "
            "to manage 15,000+ county IT assets with a normalized relational schema, full CRUD operations, "
            "client-side validation, and pre-flight duplicate detection. "
            "Implemented Row Level Security policies and database-level constraints to enforce access control "
            "and data governance independent of application logic. "
            "Participated in cross-functional Agile workflows across warehouse, NOC, software, and operations teams. "
            "Authored SOPs, installation guides, and troubleshooting references, reducing onboarding time for new staff. "
            "Deployed to production on Vercel and presented to Pima County IT management; proposed for departmental adoption. "
            "Built CSV bulk import and export with conflict detection and live preview to replace manual entry for large datasets. "
            "Executed large-scale imaging and workstation deployments using MECM across 1,800+ countywide devices. "
            "Leveraged AI-assisted development tools (Claude, Cursor) throughout the build."
        ),
        "skills": [
            "React", "PostgreSQL", "SQL", "CRUD", "Row Level Security", "data governance",
            "Agile", "Scrum", "Vercel", "CI/CD", "MECM", "CSV import/export",
            "stakeholder communication", "technical documentation", "Claude", "Cursor"
        ]
    },
    {
        "type": "experience",
        "title": "Freelance Web Developer – Iron John's Brewing",
        "content": (
            "Designed and developed a production website for a local business as sole developer, with ongoing "
            "iteration on architecture, design system, and responsive mobile-first layout. "
            "Configured a GitHub to Netlify CI/CD pipeline and established a scalable CSS design system "
            "using BEM methodology and CSS custom properties. "
            "Built a component injection system using vanilla JavaScript — shared elements live in single source "
            "files and are fetched dynamically so a single edit propagates site-wide. "
            "Integrated Google Maps JavaScript API with custom dark-mode styling, replacing an embedded iFrame "
            "for full programmatic control. "
            "Progressively simplified Maps API key security from an Express.js/Heroku proxy to a Netlify "
            "serverless function to client-side calls protected via Google Cloud domain restrictions. "
            "Managed client communication and incorporated stakeholder feedback."
        ),
        "skills": [
            "JavaScript", "Node.js", "Express.js", "Netlify", "CI/CD", "BEM", "CSS",
            "Google Maps API", "GCP", "serverless functions", "Heroku", "GitHub",
            "client communication", "mobile-first design", "responsive design"
        ]
    },
    {
        "type": "background",
        "title": "Additional Background & Education",
        "content": (
            "Arizona State University – Full-Stack Web Development Bootcamp Certificate (2024). "
            "Cabrillo College – AS Psychology, AS Health Science, AS Liberal Arts and Science (2020). "
            "Background in high-volume hospitality as bartender, server, and barista — strong communicator, "
            "composed under pressure in fast-paced team-dependent environments."
        ),
        "skills": ["communication", "teamwork", "fast-paced environments", "full-stack web development"]
    }
]

try:
    collection.delete_many({})
    result = collection.insert_many(resume_chunks)
    print(f"Inserted {len(result.inserted_ids)} resume chunks into 'resume_chunks' collection.")
except Exception as e:
    print(e)
