# AI Blog Post Generator

This project provides a command-line tool to generate and manage blog posts using Large Language Models (LLMs) via the `litellm` library. It facilitates the drafting, revision, formatting, and committing of blog posts, including Jekyll-compatible frontmatter, directly to a GitHub repository.

## Features

*   **LLM-Powered Drafting:** Generate initial blog post drafts based on a given topic.
*   **Interactive Revision:** Provide feedback to the LLM to iteratively revise and improve the draft.
*   **Content Processing:** Automatically extract core content, suggest a title, and generate a filename slug from the final draft using an LLM.
*   **Jekyll Frontmatter:** Automatically generate YAML frontmatter (title, date, layout, categories) for compatibility with Jekyll or similar static site generators.
*   **GitHub Integration:** Commit the final blog post file directly to a specified GitHub repository using the `tools.py` helper functions.
*   **Customization:** Incorporate a `style_guide.md` and `notes.md` file to guide the LLM's generation.
*   **Visual Feedback:** Includes simple terminal animations during LLM calls.

## Requirements

*   Python 3.7+
*   Access to an LLM API supported by `litellm` (e.g., OpenAI, Gemini, Anthropic, etc.).
*   A GitHub account and a Personal Access Token with repository write permissions.
*   The `tools.py` script (provided in your repository) which handles slugification and GitHub commits.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd <your-repo-directory>
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: You will need to create a `requirements.txt` file containing the necessary libraries. See Configuration below.)*

## Configuration

1.  **Environment Variables:** Create a `.env` file in the root directory of the project to store your API keys and GitHub token.
    ```dotenv
    # Example .env file
    # Replace with your actual keys/tokens and desired model configuration
    OPENAI_API_KEY="sk-..." # Or the API key for your chosen LLM provider
    GITHUB_TOKEN="ghp_..." # Your GitHub Personal Access Token
    # You might need other litellm specific variables depending on your model choice
    # e.g., COHERE_API_KEY, ANTHROPIC_API_KEY, etc.
    ```
    *   **LLM API Key:** `litellm` uses environment variables to find your API keys. The exact variable name depends on the provider (e.g., `OPENAI_API_KEY`, `GEMINI_API_KEY`, `ANTHROPIC_API_KEY`). Refer to the `litellm` documentation for details. The script currently uses `gemini/gemini-2.5-flash-preview-04-17`, so you'll likely need `GEMINI_API_KEY`.
    *   **GitHub Token:** The `tools.py` script requires a `GITHUB_TOKEN` environment variable to authenticate with the GitHub API for committing files.
2.  **`requirements.txt`:** Create a `requirements.txt` file with the required libraries:
    ```
    litellm
    colorama
    PyYAML
    python-slugify # Used by tools.py
    requests # Used by tools.py
    python-dotenv
    ```
3.  **`tools.py` Configuration:** Ensure your `tools.py` script is correctly configured to target your desired GitHub repository (repository owner, name, branch, etc.). The provided `github_commit` function summary suggests it's ready, but you might need to adjust it based on your specific repo setup.

## Usage

1.  **Run the script:**
    ```bash
    python blog_generator.py
    ```
2.  **Enter Topic:** The script will prompt you to enter the topic for the blog post.
3.  **Review and Revise:** The LLM will generate an initial draft. The script will display it and prompt you for feedback.
    *   Enter feedback to request revisions based on your input.
    *   Type `approve` to accept the current draft.
    *   Type `deny` to cancel the operation.
4.  **Finalization:** Once approved, the script will use the LLM again to process the final draft, extract the core content, and suggest a title and filename slug.
5.  **Confirm Title/Filename:** You will be prompted to confirm or override the suggested title and filename slug.
6.  **Enter Categories:** Optionally, enter comma-separated categories for the blog post frontmatter.
7.  **Commit:** The script will then generate the full markdown file (with frontmatter) and attempt to commit it to your configured GitHub repository.

## Optional Files

*   **`style_guide.md`:** If this file exists in the same directory as `blog_generator.py`, its content will be passed to the LLM as a system message to guide the writing style.
*   **`notes.md`:** If this file exists, its content will also be passed to the LLM as a system message, allowing you to provide specific points or requirements to include.

## Contributing

(Add information on how others can contribute if this is an open-source project)

## License

(Add license information, e.g., MIT, Apache 2.0, etc.)
