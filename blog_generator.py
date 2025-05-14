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
import random
from colorama import init, Fore, Style

class TextGlitchAnimator:
    """Handles text glitch animations"""
    def __init__(self, message="Processing"):
        self.message = message
        self.stop_event = threading.Event()
        self.thread = None
        self.glitch_chars = ['#', '$', '%', '&', '*', '@', '!', '?', '~', '/', '\\', '|', '_', '+', '-']
        self.colors = [
            Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, 
            Fore.MAGENTA, Fore.CYAN, Fore.WHITE,
            Fore.LIGHTRED_EX, Fore.LIGHTGREEN_EX, Fore.LIGHTYELLOW_EX,
            Fore.LIGHTBLUE_EX, Fore.LIGHTMAGENTA_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTWHITE_EX
        ]
        
    def _animate(self):
        """Internal animation loop"""
        original_text = list(self.message)
        text_len = len(original_text)
        
        try:
            while not self.stop_event.is_set():
                display_text_list = list(original_text)
                num_glitches = random.randint(1, max(1, text_len // 3)) 

                for _ in range(num_glitches):
                    idx_to_glitch = random.randint(0, text_len - 1)
                    if original_text[idx_to_glitch] != ' ': 
                        chosen_color = random.choice(self.colors)
                        if random.random() < 0.6: 
                            display_text_list[idx_to_glitch] = f"{chosen_color}{random.choice(self.glitch_chars)}{Style.RESET_ALL}"
                        else:
                            display_text_list[idx_to_glitch] = f"{chosen_color}{original_text[idx_to_glitch]}{Style.RESET_ALL}"
                
                output = "\r" + "".join(display_text_list) + "..."
                sys.stdout.write(output.ljust(text_len + 25))
                sys.stdout.flush()
                time.sleep(0.05)
        finally:
            sys.stdout.write("\r" + " " * (text_len + 25) + "\r")
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

    animator = TextGlitchAnimator("Generating Blog Post")
    animator.start()

    try:
        response = completion(
            model="gemini/gemini-2.5-flash-preview-04-17",
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
        animator = TextGlitchAnimator("Revising Content")
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
