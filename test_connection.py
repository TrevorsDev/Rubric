import json
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
# client is an OpenAI SDK object, not just the key — it stores the key internally
# and exposes methods (e.g. .chat.completions.create) that make the actual API calls
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

JOB_POSTING = """About Vendra
We are building an AI-native manufacturing marketplace, transforming how the best companies get custom parts manufactured in the U.S. There aren’t many early stage companies where you’ll get work with industry titans like Apple, Anduril and NASA, solving their critical production challenges, but you will at Vendra. We accelerate lead times, de-risk supply chains, and on-shore production, especially across aerospace, defense, and other critical industries.

Our vision is to become the only resource a hardware company ever turns to when they need hardware manufactured. We’re backed by Y Combinator and top investors, and we’re building a team to ship fast and solve hard problems as we continue to scale fast.

Vendra is registered under the International Traffic in Arms Regulations (ITAR) and supports U.S. government and defense programs. This role is restricted to U.S. Persons (22 CFR §120.62) located in the United States.

About the role
Vendra is building the AI-native operating system for manufacturing procurement and supply chain. Our goal is simple: build platforms, both external and internal, that allow fewer people to accomplish dramatically more. Think about what Claude Code did for engineers. We are doing that for supply chain (and are well on our way).

You will be part of the core engineering team at Vendra. This is a high-ownership role where you will help shape everything from our architecture across multiple connected platforms to the product experiences our customers rely on every day.

As an SDE here, you will work across the backend, APIs, frontend, and core AI workflows that power our manufacturing marketplace. You will collaborate directly with the founders, move fast, and work closely with customers building some of the most advanced hardware in the world.

We are already working with some of the most ambitious companies in aerospace, defense, robotics, and advanced manufacturing, including teams at Anduril, Mach Industries, Relativity Space, and more. Click here to see some of those names

This is a role for builders who want to work on products that are used by the companies building the future of hardware. We are growing faster than anyone in this space, and the only way to keep up with the demand in front of us is to build faster, think bigger, and raise the bar on what one great engineer can ship.

What You Will Do
Within days

Take ownership of a real production workflow across our marketplace, supplier portal, internal tools, or AI automation systems
Ship improvements used directly by customers, suppliers, or the Vendra team
Work directly with Anish and the founding team to support our newest product lines
Within weeks

Become responsible for one of our core platforms
Suggest, plan, and execute product and engineering improvements
Help us design and build the next product in our stack
Improve backend systems, APIs, internal tools, and AI workflows that directly impact customers
Within months

Help define product and technical vision
Build new platforms and products that support our mission
Develop a deep understanding of supply chain, procurement, and custom part manufacturing
Work with us to automate more of the manufacturing procurement lifecycle from RFQ to supplier matching, quoting, ordering, tracking, and fulfillment using Agentic Workflows
Who You Are
You have 1+ years of experience building and shipping real products
We don't care about your degree; we care about the systems you've put into production. Tell us about those in the message you send over
You understand software engineering principles. You also understand that they could be wrong at this stage. You know when to follow them and when to break past them. Confused? You should be. That’s what makes this fun.
You DO NOT need experience in Supply chain or Hardware. You just need to be a really good engineer
You are a US Person (Greencard works too)
You are strong in at least one part of the stack and excited to work across the rest: frontend, backend, APIs, data systems, infrastructure, and AI workflows
You can take ambiguous product or customer problems and turn them into working software quickly
You are comfortable working directly with founders, customers, and suppliers to understand what needs to be built
You are excited by AI, automation, marketplaces, infrastructure, and the opportunity to transform a massive offline industry
You want a high-ownership role where your work ships fast and matters immediately
You are willing to learn fast. Requirements change, processes change. We iterate at lightspeed and prioritize on a case by case basis.
Our Tech Stack
Frontend: React, Next.js, TypeScript

Backend: Node.js, Python

AI Stack: OpenAI models, Anthropic models, custom fine-tuned models, agentic workflows

Infrastructure: AWS, Postgres, Redis, S3, MongoDB

Data: Real-time quote intelligence, supplier availability, historical manufacturing performance, customer and supplier workflow data

How We Work
We plan, push, and ship features many times in a single day. You will not be stuck waiting weeks to see your work matter. At Vendra, the feedback loop is immediate: you build, customers use it, and the product gets better.

This role is a fit for someone who wants ownership, speed, ambiguity, and direct impact. You should be excited to work across the stack, talk to customers, make product decisions, and build systems that become the backbone of modern manufacturing procurement.

Why we started Vendra
Vendra started from a simple realization: the hardest part of building hardware is not just managing suppliers. It is finding the right suppliers in the first place.

Before launching this version of Vendra one year ago, we spent six months building productivity tools for hardware teams working with manufacturers. But the deeper we got into the problem, the clearer it became that the real bottleneck was supplier discovery, quoting, and procurement

So we pivoted. Within two weeks of the idea, we launched the first version of Vendra. Apple became our first customer, and we have been growing at lightspeed ever since.

The Founders
Shan, CEO, designed camera systems at Microsoft and Apple for AR hardware, including HoloLens 2 and Vision Pro. He later led product development at Skydio for the X10 camera systems and NightSense modules, with thousands of drones and modules deployed around the world. He also holds multiple patents across product design and manufacturing design.

Anish, CTO, comes from a machine learning research and applied AI background across computer vision, NLP, logistics, and defense. After his stint in the research space, he became a Founding ML Engineer at Ship Angel, where he led development of autonomous logistics systems, and built satellite-data tracking systems for open-water intelligence at General Atomics.

Technology
Frontend: React, TypeScript. Backend: Node.js, Python. ML and Agents: OpenAI, Claude, fine tuned models, custom LLM orchestration. Infra: AWS, Postgres, Redis, S3, Vercel, Docker. Data: Real time quote intelligence, supplier availability, historical manufacturing performance.

Interview Process
Interview Process
Founder intro call (10 min)
Casual conversation with a founder. We want to understand how you think, what you’ve built, and what you’re excited about.
Take home assignment (2 days)
Take home assignment related to our day to day tasks. You will have 2 days to complete this. Use everything.
Take home walkthrough (Same or next day)
We will walk through your submission as soon as 1 hour after you’ve done it
Vibe Check (30 minutes)
Quick conversation with both founders to see if the culture fits
We can go through the entire process in 3 days and start you off if things go well (Obviously dependent on your speed in the take home challenge)"""

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
                        "description": "Specific languages, frameworkds, or tools mentioned",
                    },
                },
                "required": ["required_skills", "years_experience", "tech_stack"],
            },
        },
    }
]

response = client.chat.completions.create(
    model="gpt-4.1-nano",
    messages=[
        {
            "role": "user",
            "content": f"Extract the hiring requirements from this job posting:\n\n{JOB_POSTING}",
        }
    ],
    tools=tools,
)

tool_call = response.choices[0].message.tool_calls[0]
arguments = json.loads(tool_call.function.arguments)
print(arguments)
