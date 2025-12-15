import os
from dashscope import Generation

# Check for Qwen API Key
if 'DASHSCOPE_API_KEY' not in os.environ:
    print("Error: DASHSCOPE_API_KEY is not set.")
    exit()

# File paths
input_file = "specs/project.md"
output_file = "docs/output.md"

# Read specification
try:
    with open(input_file, 'r', encoding='utf-8') as f:
        spec_content = f.read()
except FileNotFoundError:
    print(f"Error: Input file {input_file} not found.")
    exit()

# Prompt for Qwen
prompt = f"""
You are an expert technical author tasked with writing a chapter of a book based on the provided specification.
Your goal is to generate the next section or chapter content.

SPECIFICATION (Start with the next logical section based on this plan):
---
{spec_content}
---

Continue the book generation process. Do not include notes or summaries, only the book content.
"""

# Call Qwen API
print("--- Qwen Book Generation Started ---")
response = Generation.call(
    model='qwen-turbo',
    prompt=prompt
)

# Save output
output_dir = os.path.dirname(output_file)
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(response.output['text'])

print(f"--- Generation Complete! Output saved to {output_file} ---")