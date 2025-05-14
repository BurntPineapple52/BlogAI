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

def generate_blog_post(topic, style_guide=None, notes=None, current_draft=None):
    """Generates or revises a blog post draft using LLM."""
    messages = [
        {"role": "system", "content": "You clean up notes and turn them into a blog post. You don't remove content, but you fill in any context holes and fix narrative flow."},
    ]

    if current_draft:
         # This is a revision request
         messages.append({"role": "user", "content": f"Revise this blog post based on feedback: {topic}\n\n{current_draft}"})
    else:
        # This is an initial generation request
        messages.append({"role": "user", "content": f"Write a Jekyll markdown post about the following: {topic}"})


    if style_guide:
        messages.append({"role": "system", "content": f"Follow this style guide: {style_guide}"})
    if notes:
        messages.append({"role": "system", "content": f"Incorporate these notes and tone: {notes}"})

    animator = TextGlitchAnimator("Generating Blog Post" if not current_draft else "Revising Content")
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

def process_and_title_post(draft):
    """Uses LLM to extract core content and suggest title/filename."""
    messages = [
        {"role": "system", "content": "You are a blog post formatter and title generator. Your task is to take the provided text, which is a blog post draft, and perform two actions: 1. Extract only the core blog post content, removing any introductory/concluding remarks or conversational text from the previous interaction. 2. Suggest a concise and relevant title for the blog post. 3. Suggest a suitable filename slug based on the suggested title. Provide the output as a JSON object with keys 'content', 'title', and 'filename'. Ensure the JSON is valid and contains only these three keys."},
        {"role": "user", "content": f"Process this blog post draft:\n\n{draft}\n\nProvide the output as a JSON object."}
    ]

    animator = TextGlitchAnimator("Finalizing Content and Title")
    animator.start()

    try:
        response = completion(
            model="gemini/gemini-2.5-flash-preview-04-17", # Or another suitable model
            messages=messages,
            response_format={"type": "json_object"} # Request JSON output if model supports it
        )
        content = response.choices[0].message.content
        # Attempt to parse the JSON response
        try:
            processed_data = json.loads(content)
            # Basic validation
            if 'content' in processed_data and 'title' in processed_data and 'filename' in processed_data:
                 return processed_data
            else:
                 print("\nWarning: LLM response JSON missing expected keys.", file=sys.stderr)
                 print(f"Raw response: {content}", file=sys.stderr)
                 return None # Indicate failure
        except json.JSONDecodeError:
            print("\nError: Failed to parse JSON response from LLM.", file=sys.stderr)
            print(f"Raw response: {content}", file=sys.stderr)
            return None # Indicate failure

    except Exception as e:
        print(f"\nError during content processing and titling: {str(e)}", file=sys.stderr)
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

    if not draft:
        print("Initial draft generation failed. Exiting.")
        return

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
            feedback, # Feedback is the new 'topic' for revision
            style_guide,
            notes,
            current_draft=draft # Pass the current draft for revision
        )
        if not draft:
            print("Failed to revise draft.")
            return

        print("\nRevised Draft:\n")
        print(draft)

    # --- NEW STEP: Process content and get title/filename ---
    print("\nProcessing final draft and suggesting title/filename...")
    processed_data = process_and_title_post(draft)

    if not processed_data:
        print("Failed to process content and get title/filename. Exiting.")
        return

    final_content = processed_data['content']
    suggested_title = processed_data['title']
    suggested_filename_slug = processed_data['filename']

    print("\n--- Final Content ---")
    print(final_content)
    print("---------------------\n")

    # --- User confirmation/override for title and filename ---
    print(f"Suggested Title: {suggested_title}")
    user_title = input(f"Enter final title (or press Enter to use suggested): ").strip()
    title = user_title if user_title else suggested_title

    print(f"Suggested Filename Slug: {suggested_filename_slug}")
    user_filename_slug = input(f"Enter final filename slug (or press Enter to use suggested): ").strip()
    filename_slug = user_filename_slug if user_filename_slug else suggested_filename_slug

    # Ensure filename slug is valid if user overrode it
    if user_filename_slug:
         filename_slug = slugify_title(filename_slug) # Re-slugify user input just in case

    # --- Commit to GitHub ---
    date = get_current_date()
    filename = f"{date}-{filename_slug}.md"

    # Get categories from user
    categories = input("Enter categories/tags (comma separated, optional): ").strip()
    categories = [c.strip() for c in categories.split(',')] if categories else None

    # Add frontmatter to content
    frontmatter = generate_frontmatter(title, date, categories)
    full_content = frontmatter + "\n" + final_content # Use final_content here

    commit_message = f"Add new blog post: {title}"
    print(f"\nCommitting to GitHub as {filename}...")
    result = github_commit(filename, full_content, commit_message)
    print(result)

if __name__ == "__main__":
    main()
