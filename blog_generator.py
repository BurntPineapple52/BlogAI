from litellm import completion
import os
from datetime import datetime
from tools import slugify_title, github_commit
import json
from pathlib import Path

def get_current_date():
    return datetime.now().strftime("%Y-%m-%d")

def generate_blog_post(topic, style_guide=None, notes=None):
    messages = [
        {"role": "system", "content": "You are a professional blog writer."},
        {"role": "user", "content": f"Write a comprehensive blog post about: {topic}"}
    ]
    
    if style_guide:
        messages.append({"role": "system", "content": f"Follow this style guide: {style_guide}"})
    if notes:
        messages.append({"role": "system", "content": f"Incorporate these notes: {notes}"})

    response = completion(
        model="gemini/gemini-2.0-flash",
        messages=messages
    )
    return response.choices[0].message.content

def main():
    topic = input("Enter blog post topic: ")
    
    # Load style guide and notes if available
    style_guide = None
    notes = None
    if Path("style_guide.md").exists():
        with open("style_guide.md", "r") as f:
            style_guide = f.read()
    if Path("notes.md").exists():
        with open("notes.md", "r") as f:
            notes = f.read()
    
    draft = generate_blog_post(topic, style_guide, notes)
    print("\nGenerated Draft:\n")
    print(draft)
    
    while True:
        feedback = input("\nEnter feedback (or 'approve'/'deny'): ")
        if feedback.lower() == 'approve':
            break
        elif feedback.lower() == 'deny':
            print("Operation cancelled.")
            return
        
        # Revise based on feedback
        draft = generate_blog_post(
            f"Revise this blog post based on feedback: {feedback}\n\n{draft}",
            style_guide,
            notes
        )
        print("\nRevised Draft:\n")
        print(draft)
    
    # Commit to GitHub
    date = get_current_date()
    title = draft.split('\n')[0].replace('#', '').strip()
    filename = f"{date}-{slugify_title(title)}.md"
    
    commit_message = f"Add new blog post: {title}"
    result = github_commit(filename, draft, commit_message)
    print(result)

if __name__ == "__main__":
    main()
