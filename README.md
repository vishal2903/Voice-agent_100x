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
- The assistant can search for up-to-date information on the web related to any AI topic or current events.
- It can fetch:
  - Latest research articles on AI.
  - News on advancements in AI technology.
  - Real-time data such as stock prices, weather updates, or sports scores.
  
### 2. **File Search Tool**
- Searches through documents uploaded by the instructor, helping the assistant pull relevant content for specific queries.

### 3. **Deep Research Tool**
- Combines both **web search** and **file search** to produce comprehensive research reports.
- The user can request a **daily update**, a **lesson brief**, or a **full research report**.

### 4. **Save Report**
- Saves the generated research or lesson brief in **DOCX** or **PDF** format to the **Downloads** folder.

## Use Cases

### **1. Daily Updates on AI Topics**

**Use Case**: The AI instructor needs to stay up-to-date with the latest trends and developments in the AI field, especially in areas like **AI agents**, **LLMs**, or **image generation**.

- **Example Prompt**: 
  - **User**: "Give me a daily update on AI agents. Save this as a docx file."
  - **Assistant**: The assistant will provide a summary of the latest advancements in AI agents, including recent articles, research, and developments. It will generate a report and save it as a **DOCX** file for easy reference.

**Benefit**: The instructor can get a daily digest of key updates, which is helpful for integrating new information into the course curriculum.

---

### **2. Lesson Briefs for Upcoming Sessions**

**Use Case**: The AI instructor wants a summary of the next lesson's key concepts, demo ideas, exercises, and recent developments. This brief helps them plan the session efficiently.

- **Example Prompt**:
  - **User**: "Brief me for next week's lesson on ControlNets. Use internal notes and add recent updates from the web."
  - **Assistant**: The assistant pulls the lesson details from the instructor’s internal course materials (uploaded in the Vector Store) and integrates recent updates from the web to create a **lesson brief**. This is saved in **PDF** or **DOCX** format.

**Benefit**: The instructor gets a structured lesson plan that includes core concepts, examples, and any recent changes or trends related to the topic.

---

### **3. Deep Research Reports**

**Use Case**: The AI instructor wants a deep dive into a specific topic for either personal preparation or as reference material for their cohort. The report should pull information from both the instructor's notes and recent updates from the web.

- **Example Prompt**:
  - **User**: "Deep research on vector databases for RAG. Use the sources `anthropic.com` and `openai.com`."
  - **Assistant**: The assistant combines internal notes (from the Vector Store) and web sources to produce a **research report** on vector databases for **retrieval-augmented generation (RAG)**. This report is saved in **DOCX** or **PDF** format.

**Benefit**: The instructor can quickly gather the most relevant, comprehensive information on a specific subject, which helps them refine the curriculum or prepare lecture content.

---

### **4. File Search for Specific Content in Course Notes**

**Use Case**: The AI instructor wants to retrieve specific definitions, examples, or case studies directly from the course notes. This tool is particularly useful for pulling out teaching material from previous lectures or lecture slides.

- **Example Prompt**:
  - **User**: "Search our course notes for the definition of LLM and save the relevant content."
  - **Assistant**: The assistant searches the uploaded course notes for the definition of **Large Language Models (LLMs)**, extracts the relevant content, and presents it to the user. It can also save the results in **PDF** or **DOCX**.

**Benefit**: This tool helps instructors find the exact information they need from a large collection of course materials quickly.

---

### **5. Web Search for Real-Time Data and Trends**

**Use Case**: The AI instructor needs real-time information about the latest trends, news, or research papers related to AI technologies.

- **Example Prompt**:
  - **User**: "Search the web for the latest trends in AI image generation."
  - **Assistant**: The assistant will search the web (across seed URLs or other sources) and provide a summary of the most recent trends in AI image generation.

**Benefit**: The instructor gets the latest updates in real-time, which helps in staying current and modifying lesson content accordingly.

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
