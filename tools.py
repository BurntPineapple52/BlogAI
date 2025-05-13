import subprocess
import re
from pathlib import Path

def slugify_title(title):
    """Convert title to URL-friendly slug"""
    slug = re.sub(r'[^\w\s-]', '', title.lower())
    slug = re.sub(r'[\s_-]+', '-', slug)
    slug = re.sub(r'^-+|-+$', '', slug)
    return slug

def github_commit(filename, content, commit_message):
    """Commit file to GitHub repository"""
    try:
        # Ensure directory exists
        Path("blog_posts").mkdir(exist_ok=True)
        filepath = Path("blog_posts") / filename
        
        # Write content to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Git commands
        subprocess.run(['git', 'add', str(filepath)], check=True)
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        subprocess.run(['git', 'push'], check=True)
        
        return f"Successfully committed and pushed: {filename}"
    except subprocess.CalledProcessError as e:
        return f"Error committing to GitHub: {e}"
