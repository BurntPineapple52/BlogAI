from litellm import completion
import os
from datetime import datetime
from tools import slugify_title, github_commit
import json
import yaml
from pathlib import Path
import threading
import time
import sys
from colorama import init, Fore, Style

class ColorAnimator:
    """Handles colorful loading animations with multiple styles"""
    COLOR_SCHEMES = {
        'ocean': [Fore.CYAN, Fore.BLUE, Fore.MAGENTA],
        'fire': [Fore.RED, Fore.YELLOW, Fore.MAGENTA],
        'forest': [Fore.GREEN, Fore.YELLOW, Fore.CYAN],
        'rainbow': [Fore.RED, Fore.YELLOW, Fore.GREEN, 
                   Fore.CYAN, Fore.BLUE, Fore.MAGENTA]
    }
    
    def __init__(self, message="Processing", style='ocean'):
        self.message = f"[ {message} ]"
        self.colors = self.COLOR_SCHEMES.get(style, self.COLOR_SCHEMES['ocean'])
        self.stop_event = threading.Event()
        self.thread = None
        self.current_frame = 0
        
    def _animate(self):
        """Internal animation loop"""
        while not self.stop_event.is_set():
            colored_text = []
            for i, char in enumerate(self.message):
                color_idx = (i + self.current_frame) % len(self.colors)
                colored_text.append(f"{self.colors[color_idx]}{char}")
            
            sys.stdout.write('\r' + ''.join(colored_text) + Style.RESET_ALL)
            sys.stdout.flush()
            time.sleep(0.08)
            self.current_frame += 1
        
        sys.stdout.write('\r' + ' ' * len(self.message) + '\r')
        sys.stdout.flush()
    
    def start(self):
        """Begin the animation in a background thread"""
        self.thread = threading.Thread(target=self._animate, daemon=True)
        self.thread.start()
    
    def stop(self):
        """Stop the animation and clean up"""
        self.stop_event.set()
        if self.thread:
            self.thread.join(timeout=0.5)

def generate_frontmatter(title, date, categories=None):
    """Generate Jekyll frontmatter in YAML format"""
    frontmatter = {
        'title': title,
        'date': date,
        'layout': 'post'
    }
    if categories:
        frontmatter['categories'] = categories
    return "---\n" + yaml.dump(frontmatter) + "---\n"

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

    animator = ColorAnimator("Generating Blog Post", style='rainbow')
    animator.start()

    try:
        response = completion(
            model="gemini/gemini-2.5-flash",
            messages=messages
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"\nError during generation: {str(e)}", file=sys.stderr)
        return None
    finally:
        animator.stop()

def main():
    init()  # Initialize colorama
    
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
        animator = ColorAnimator("Revising Content", style='fire')
        animator.start()
        try:
            draft = generate_blog_post(
                f"Revise this blog post based on feedback: {feedback}\n\n{draft}",
                style_guide,
                notes
            )
            if not draft:
                print("Failed to revise draft.")
                return
        finally:
            animator.stop()
            
        print("\nRevised Draft:\n")
        print(draft)
    
    # Commit to GitHub
    date = get_current_date()
    title = draft.split('\n')[0].replace('#', '').strip()
    filename = f"{date}-{slugify_title(title)}.md"
    
    # Get categories from user
    categories = input("Enter categories/tags (comma separated, optional): ").strip()
    categories = [c.strip() for c in categories.split(',')] if categories else None
    
    # Add frontmatter to content
    frontmatter = generate_frontmatter(title, date, categories)
    full_content = frontmatter + "\n" + draft
    
    commit_message = f"Add new blog post: {title}"
    result = github_commit(filename, full_content, commit_message)
    print(result)

if __name__ == "__main__":
    main()
