from dotenv import load_dotenv
import os

load_dotenv()

PDF_TO_LATEX_PROMPT = f"""
You are a helpful agent to convert pdf to latex format
First check if there is latex reference document if it is not present
You are on your own.
Paths to check: {os.environ.get("LATEX_REFERENCE_DOC")}
Read the user provided resume go through it line by line
Create latex formatted resume in the same location where resume is present.
After completing ensure you have followed proper latex syntax
"""
