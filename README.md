# Voice-agent_100x
# AI Voice Assistant for GenAI Cohort

## Overview

This project is a **voice-driven AI assistant** designed for an AI instructor who teaches a **6-month Applied GenAI Cohort**. The assistant can provide:
- **Daily updates** on AI topics.
- **Lesson briefs** for upcoming sessions.
- **Deep research reports** using both internal knowledge (uploaded course material) and the web.
- **File search functionality** to fetch relevant information from uploaded documents.
- **Web search functionality** to gather the latest information from the web.
- The ability to **save reports** as DOCX, PDF, or text files for future reference.

The assistant is built using **LiveKit**, **OpenAI's GPT-4** API, and **Python**. 

## Features

### 1. **Web Search Tool**
- Allows the assistant to fetch up-to-date information from the web.
- Useful for getting news, stock prices, recent AI developments, etc.

### 2. **File Search Tool**
- Searches through documents uploaded by the instructor, helping the assistant pull relevant content for specific queries.

### 3. **Deep Research Tool**
- Combines both **web search** and **file search** to produce comprehensive research reports.
- The user can request a **daily update**, a **lesson brief**, or a **full research report**.

### 4. **Save Report**
- Saves the generated research or lesson brief in **DOCX** or **PDF** format to the **Downloads** folder.

**Voice Assistant Commands:**
You can interact with the assistant using voice (or text). Here are some example commands:

### A.) Daily Update:
“Daily update on AI agents — save as docx.”

### B.)Lesson Brief:
“Brief me for next week's lesson on ControlNets — save as pdf.”

### C.)Deep Research:
“Deep research on vector databases for RAG — save it as docx.”

The assistant will perform the search, generate the report, and save it as a file in DOCX or PDF format.

## Requirements

Before running the application, you need to install the following dependencies:

### Dependencies:
- `openai`
- `livekit-agents`
- `livekit-plugins-openai`
- `python-docx` (for saving DOCX files)
- `reportlab` (for saving PDF files)

Install them using the following command:

```bash
pip install python-docx reportlab openai livekit-agents livekit-plugins-openai
