import asyncio
import logging
import os
import json
from typing import List, Optional
from dotenv import load_dotenv
from openai import OpenAI
from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions, function_tool, RunContext
from livekit.plugins import openai as lk_openai, noise_cancellation, silero
from datetime import datetime
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
load_dotenv()

# Reduce console warnings
logging.getLogger("livekit.agents").setLevel(logging.WARNING)
logging.getLogger("livekit.plugins.silero").setLevel(logging.ERROR)

VECTOR_STORE_ID = os.getenv("VECTOR_STORE_ID")



def save_report_to_file(content: str, topic: str, file_type: str = "docx") -> str:
    """Saves the content to either .docx or .pdf in the Downloads folder."""
    downloads_folder = r"C:\temp"  # Change to another folder if Downloads is restricted
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    filename = f"research_report-{_slugify(topic)}-{timestamp}"

    if file_type == "docx":
        filename += ".docx"
        file_path = os.path.join(downloads_folder, filename)

        # Save as a DOCX file
        doc = Document()
        doc.add_heading(f"Research Report: {topic}", 0)
        doc.add_paragraph(content)
        doc.save(file_path)

    elif file_type == "pdf":
        filename += ".pdf"
        file_path = os.path.join(downloads_folder, filename)

        # Save as a PDF file
        c = canvas.Canvas(file_path, pagesize=letter)
        c.setFont("Helvetica", 12)
        c.drawString(72, 750, f"Research Report: {topic}")
        text_object = c.beginText(72, 730)
        text_object.textLines(content)
        c.drawText(text_object)
        c.save()

    else:
        return "Invalid file type. Please choose either 'docx' or 'pdf'."

    return file_path
# ---------------- agent ----------------
class VoiceAssistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions="""You are a fast, efficient voice AI assistant for an AI instructor.
Keep answers concise, classroom-ready, and spoken clearly.
Use FILE SEARCH for foundational content from our internal notes.
Use WEB SEARCH for recent developments and news.
Available report formats:
- daily_update: short newsy brief with dates
- lesson_brief: weekly teaching brief (concepts, demos, exercises)
- research_report: deeper dive with landscape + sources

Be direct and friendly; no filler.""")
        self.openai_client = OpenAI()

    # -------- existing tools (kept) --------
    @function_tool(
        description="Search the web for current/recent information and return direct facts."
    )
    async def web_search(self, query: str, ctx: RunContext) -> str:
        #seed_urls = _normalize_seed_urls(_load_seed_urls())  # Load dynamic seed URLs
        try:
            resp = self.openai_client.responses.create(
                model="gpt-4o-mini",
                tools=[{"type": "web_search_preview", "search_context_size": "medium"}],
                input=query,
            )
            return resp.output_text
        except Exception as e:
            return f"Search error: {str(e)}"

    @function_tool(
        description="Search our uploaded documents using File Search (vector store)."
    )
    async def file_search(self, query: str, ctx: RunContext) -> str:
        if not VECTOR_STORE_ID:
            return "File search not configured yet. Set VECTOR_STORE_ID in your .env."
        try:
            resp = self.openai_client.responses.create(
                model="gpt-4o-mini",
                tools=[{"type": "file_search", "vector_store_ids": [VECTOR_STORE_ID]}],
                input=query,
            )
            return resp.output_text
        except Exception as e:
            return f"File search error: {str(e)}"

    # ---------------- deep research report ----------------
    # ---------------- deep research report ----------------
@function_tool(
    description=(
        "Deep research: combine file_search (internal notes) and web_search (recent) to produce a formatted brief. "
        "Args: topic (str), format ('daily_update'|'lesson_brief'|'research_report', default 'lesson_brief'), "
        "max_sources (int, default 6), recency_hint (str, default 'last 30 days' - used only in the prompt)."
    )
)
async def deep_research_report(
    self,
    ctx: RunContext,
    topic: str,
    format: str = "lesson_brief",
    max_sources: int = 6,
    recency_hint: str = "last 30 days",
) -> str:
    if not VECTOR_STORE_ID:
        return "File search not configured yet. Set VECTOR_STORE_ID in your .env."

    # Format-specific instructions (pure prompt control; no tool params)
    format_instructions = {
        "daily_update": (
            "Return a DAILY UPDATE for an AI instructor:\n"
            "1) TL;DR — 3 concise bullets with dates\n"
            f"2) What changed in {recency_hint} — 3–5 items, dated\n"
            "3) Teaching angle — how to mention this in class (1–2 bullets)\n"
            f"4) Must-know links — up to {max_sources} URLs"
        ),
        "lesson_brief": (
            "Return a LESSON BRIEF for the next cohort session:\n"
            "1) TL;DR — what to teach & why (3 bullets)\n"
            "2) Core concepts & definitions — PULL FROM INTERNAL FILES FIRST\n"
            f"3) What’s new on the web ({recency_hint}) — 3–5 dated points\n"
            "4) Demo ideas — one no-code (Bubble/TensorArt) and one code (Python/FastAPI)\n"
            "5) Exercises — 2–3 mini projects (~60–90 minutes)\n"
            f"6) Reading list — up to {max_sources} links (mix: internal + web)"
        ),
        "research_report": (
            "Return a RESEARCH REPORT:\n"
            "1) TL;DR — 5 bullets\n"
            "2) Landscape — key approaches & players\n"
            f"3) State of the art ({recency_hint}) — dated\n"
            "4) Risks / pitfalls\n"
            "5) Teaching recommendations — lecture flow for the cohort\n"
            f"6) Sources — up to {max_sources} URLs with dates"
        ),
    }.get(format, "")

    # Single Responses call with BOTH tools enabled; recency + seeds via prompt only
    prompt = [
        {
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": (
                        "You are assisting an AI instructor planning and teaching a 6-month GenAI cohort.\n"
                        "Use FILE SEARCH for foundational definitions/frameworks from our internal notes.\n"
                        f"Use WEB SEARCH for recent developments ({recency_hint}).\n"
                        "Always include source URLs and dates where possible. Keep it concise and classroom-ready.\n\n"
                        f"FORMAT:\n{format_instructions}\n\n"
                        f"TOPIC:\n{topic}\n"
                    ),
                }
            ],
        }
    ]

    try:
        resp = self.openai_client.responses.create(
            model="gpt-4o-mini",
            tools=[
                {"type": "file_search", "vector_store_ids": [VECTOR_STORE_ID]},
                {"type": "web_search_preview", "search_context_size": "medium"},
            ],
            input=prompt,
        )
        short = resp.output_text.splitlines()[0][:220] if resp.output_text else "Research ready."
        await ctx.session.say(short)
        return resp.output_text
    except Exception as e:
        return f"Deep research error: {str(e)}"


    # ---------------- save_report ----------------------
@function_tool(
    description="Save the generated report to a file in the Downloads folder (docx or pdf)."
)
async def save_report(self, ctx: RunContext, content: str, topic: str, file_type: str = "docx") -> str:
    try:
        file_path = save_report_to_file(content, topic, file_type)
        await ctx.session.say(f"I've saved your research report to: {file_path}")
        return f"Report saved at {file_path}"
    except Exception as e:
        return f"Error: {str(e)}"

# ---------------- livekit entry ----------------
async def entrypoint(ctx: agents.JobContext):
    await ctx.connect()

    session = AgentSession(
        stt=lk_openai.STT(model="gpt-4o-transcribe"),
        llm=lk_openai.LLM(model="gpt-4o-mini"),
        tts=lk_openai.TTS(
            model="gpt-4o-mini-tts",
            voice="ash",
            instructions=(
                "Speak quickly and efficiently with clear pronunciation. "
                "Be direct and concise. Sound sweet, confident and decisive."
            ),
            speed=1.2,
        ),
        vad=silero.VAD.load(),
        turn_detection="vad",
    )

    await session.start(
        room=ctx.room,
        agent=VoiceAssistant(),
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    await session.generate_reply(
        instructions=(
            "Greet the user. Mention you can produce daily updates, lesson briefs, "
            "and deep research reports using our internal notes and the web."
        )
    )

if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
