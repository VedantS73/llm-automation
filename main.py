from fastapi import FastAPI, HTTPException, Body, Request
import os
import uvicorn
import json
import sqlite3
import subprocess
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI
import numpy as np
from PIL import Image
import requests
import re
import shutil
import sys

load_dotenv()
app = FastAPI()
client = OpenAI()

def install_uv_and_run_datagen(user_email: str):
    print("Running install_uv_and_run_datagen")    
    try:
        # Check if uv is installed
        if not shutil.which("uv"):
            print("Installing uv...")
            subprocess.run([sys.executable, "-m", "pip", "install", "uv"], check=True)
        else:
            print("uv is already installed.")
        
        # Run the datagen.py script with the provided email
        print("Running datagen.py with email:", user_email)
        subprocess.run(["uv", "run", "https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py", user_email], check=True)

        return "Data generation completed successfully."
    
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")

def format_markdown(file_path: str) -> None:
    """Format markdown file using prettier."""
    subprocess.run(['npx', 'prettier@3.4.2', '--write', file_path], check=True)

def parse_task(task: str):
    """Parse task description using LLM to identify operation and parameters."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """Analyze the task and return a string representing the operation to be performed. String should be one of [install_script, format_markdown, count_weekday, sort_contacts, recent_logs, markdown_index, extract_email, extract_card, similar_comments, ticket_sales]"""
            },
            {"role": "user", "content": task}
        ]
    )
    
    to_execute = str(response.choices[0].message.content)
    # convert to string
    to_execute = to_execute.replace('[','').replace(']','').replace('\'','').replace(' ','')
    print(to_execute)
    if to_execute == 'install_script':
        return install_uv_and_run_datagen('23f1002365@ds.study.iitm.ac.in')
    elif to_execute == 'format_markdown':
        return format_markdown('/data/format.md')
    else:
        return "Operation not recognized."

@app.post("/run")
async def run_task(request: Request):
    try:
        task = request.query_params.get("task")
        output = parse_task(task)
        return {"status": "success", "output": output}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@app.get("/read")
def read_file(path: str):
    """Read a file's content and return it."""
    if ".." in path or path.startswith("/"):
        raise HTTPException(status_code=400, detail="Invalid file path.")

    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found.")

    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        return {"status": "success", "content": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")