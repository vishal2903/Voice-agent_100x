# setup_vector_store.py
from dotenv import load_dotenv
load_dotenv()

import os, sys, glob
from openai import OpenAI

# usage: python setup_vector_store.py "C:/Users/visha/Downloads/knowledge"
folder = sys.argv[1] if len(sys.argv) > 1 else None
if not folder or not os.path.isdir(folder):
    print("Usage: python setup_vector_store.py <folder-with-files>")
    sys.exit(1)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 1) create vector store
vs = client.vector_stores.create(name="voice-agent-knowledge")
print("Vector store created:", vs.id)

# 2) upload files in the folder
paths = []
for ext in ("*.pdf", "*.txt", "*.md", "*.docx"):
    paths.extend(glob.glob(os.path.join(folder, ext)))

if not paths:
    print("No files found to upload. Add PDFs/TXT/MD/DOCX to the folder and re-run.")
    sys.exit(0)

for p in paths:
    try:
        f = client.files.create(file=open(p, "rb"), purpose="assistants")
        client.vector_stores.files.create(vector_store_id=vs.id, file_id=f.id)
        print("Uploaded:", os.path.basename(p))
    except Exception as e:
        print("Failed:", p, "-", e)

print("\nDONE. Put this in your .env:\nVECTOR_STORE_ID=" + vs.id)
