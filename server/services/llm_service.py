import json
import logging
from datetime import datetime, timedelta

from openai import (
    OpenAI,
    APIConnectionError,
    APITimeoutError,
    APIError,
)

from server.config import OPENROUTER_API_KEY

logger = logging.getLogger(__name__)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)


def generate_response(messages):

    try:
        if isinstance(messages, str):
            messages = [
                {
                    "role": "user",
                    "content": messages,
                }
            ]

        logger.info("Sending request to OpenRouter")

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages,
        )

        answer = response.choices[0].message.content

        logger.info("Response received successfully")

        return answer

    except APITimeoutError as e:
        logger.error(f"OpenRouter request timed out: {e}")
        raise

    except APIConnectionError as e:
        logger.error(f"Unable to connect to OpenRouter: {e}")
        raise

    except APIError as e:
        logger.error(f"OpenRouter API error: {e}")
        raise

    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        raise

def format_tool_response(
    tool: str,
    intent: str,
    result,
    question: str,
):
    """
    Convert raw tool output into concise,
    user-friendly Markdown for WorkMind.
    """

    # -----------------------------
    # Gmail
    # -----------------------------
    if tool == "gmail":

        # Send email
        if intent == "send_email":
            if isinstance(result, dict) and result.get("success"):
                return (
                    "## ✅ Email sent successfully!\n\n"
                    f"**To:** {result.get('to', 'Unknown')}\n\n"
                    f"**Subject:** {result.get('subject', 'No subject')}"
                )

        # Gmail profile
        if intent == "profile":
            if isinstance(result, dict):
                return (
                    "## 📧 Gmail account\n\n"
                    f"**Email:** {result.get('email', 'Unknown')}\n\n"
                    f"**Messages:** {result.get('messages_total', 0)}\n\n"
                    f"**Threads:** {result.get('threads_total', 0)}"
                )

        # Other Gmail results are already formatted by gmail_tool.py
        if isinstance(result, str):
            return result

    # -----------------------------
    # Calendar
    # -----------------------------
    if tool == "calendar":

        # Create event
        if intent == "create_event":
            if isinstance(result, dict):

                summary = result.get(
                    "summary",
                    "Calendar event",
                )

                start = result.get("start") or {}
                end = result.get("end") or {}

                start_time = start.get(
                    "dateTime",
                    start.get("date", "Unknown"),
                )

                end_time = end.get(
                    "dateTime",
                    end.get("date", "Unknown"),
                )

                return (
                    "## 📅 Event created successfully!\n\n"
                    f"**{summary}**\n\n"
                    f"**Start:** {start_time}\n\n"
                    f"**End:** {end_time}"
                )

        # If calendar service already returns readable text
        if isinstance(result, str):
            return result

    # -----------------------------
    # GitHub
    # -----------------------------
    if tool == "github":

        # GitHub profile
        if intent == "user":
            if isinstance(result, dict):
                username = result.get("username", "Unknown")
                name = result.get("name")
                profile_url = result.get("profile_url")

                response = (
                    "## 🐙 GitHub Profile\n\n"
                    f"**Username:** {username}"
                )

                if name:
                    response += f"\n\n**Name:** {name}"

                if profile_url:
                    response += f"\n\n**Profile:** {profile_url}"

                return response

        # Create issue
        if intent == "create_issue":
            if isinstance(result, dict):

                number = result.get("number")
                title = result.get(
                    "title",
                    "GitHub issue",
                )

                repository = (
                    result.get("repository")
                    or result.get("repo")
                )

                response = "## ✅ GitHub issue created!\n\n"

                if number:
                    response += f"**Issue:** #{number}\n\n"

                response += f"**Title:** {title}"

                if repository:
                    response += f"\n\n**Repository:** {repository}"

                return response

        # Other GitHub results
        if isinstance(result, str):
            return result

    # -----------------------------
    # Generic fallback
    # -----------------------------
    if isinstance(result, str):
        return result

    if isinstance(result, dict):

        # Avoid exposing raw API metadata.
        if "message" in result:
            return str(result["message"])

        if "answer" in result:
            return str(result["answer"])

        return (
            "I completed the requested action successfully."
        )

    if isinstance(result, list):
        if not result:
            return "No results found."

        return "\n".join(
            f"- {item}" for item in result
        )

    return str(result)

def classify_query(
    query: str,
    history=None,
    has_uploaded_documents: bool = False,
):
    """
    Classify a user query into a high-level WorkMind route
    and tool-specific intent.
    """

    system_prompt = """
You are the intelligent planner for WorkMind, an AI enterprise productivity assistant.

Your job is to understand the user's request and return ONE structured JSON routing decision.

You must decide between:

1. retrieval
   Use for questions about:
   - uploaded documents
   - PDFs
   - enterprise knowledge
   - information that should come from RAG

2. summarization
   Use for general summarization that does NOT require a connected tool.

3. tool
   Use when the user needs data or actions from:
   - gmail
   - github
   - calendar

4. direct_llm
   Use for:
   - general questions
   - explanations
   - greetings
   - casual conversation
   - questions that don't require user data or tools

DOCUMENT CONTEXT:

The current conversation may contain uploaded documents.

Current conversation document status:
- Uploaded documents available: DOCUMENT_STATUS

IMPORTANT ROUTING RULE:

If DOCUMENT_STATUS is True, you MUST prefer the retrieval route for questions that could reasonably relate to the uploaded documents.

The user does NOT need to explicitly say:
- "from my uploaded document"
- "from the PDF"
- "according to the document"
- or anything similar.

For example, if a Cloud Computing document is uploaded:

User: "What is Virtualization?"
→ retrieval

User: "What are the types of virtualization?"
→ retrieval

User: "Explain cloud computing."
→ retrieval

User: "What does the document say about virtualization?"
→ retrieval

Only use direct_llm when the question is clearly unrelated to the uploaded documents.

For example:

User: "What is 25 × 25?"
→ direct_llm

User: "Tell me a joke."
→ direct_llm

IMPORTANT:
- Uploaded-document questions → retrieval
- Gmail requests → Gmail tool
- GitHub requests → GitHub tool
- Calendar requests → Calendar tool
- Clearly unrelated general questions → direct_llm

For TOOL requests, return:

{
  "route": "tool",
  "tool": "<github|gmail|calendar>",
  "intent": "<specific action>",
  "parameters": {}
}


IMPORTANT:
- Understand natural language semantically.
- Do NOT rely on exact keywords.
- Do NOT require the user's wording to match an example.
- Extract useful parameters from the user's request.
- Always include a "parameters" object for tool requests.
- If no parameters are required, return an empty object {}.
- Never invent parameter values that the user did not provide.
- Return ONLY valid JSON.
- Do not include markdown.
- Do not include explanations.


GMAIL INTENTS:

Profile:
{
  "route": "tool",
  "tool": "gmail",
  "intent": "profile",
  "parameters": {}
}

Get latest email:
Use this when the user asks for ONE latest/recent/newest email.

Examples:
- "show me my latest email"
- "what is my latest email?"
- "show my newest email"
- "what's the most recent email I received?"
- "give me my recent email"

Return:
{
  "route": "tool",
  "tool": "gmail",
  "intent": "get_latest_message",
  "parameters": {}
}

List recent emails:
Use this when the user explicitly asks for multiple recent emails.

Return:
{
  "route": "tool",
  "tool": "gmail",
  "intent": "list_messages",
  "parameters": {
    "max_results": 10
  }
}

Search emails:
{
  "route": "tool",
  "tool": "gmail",
  "intent": "search_messages",
  "parameters": {
    "query": "<Gmail search query>",
    "max_results": 10
  }
}

Search and summarize emails:
Use this when the user asks to find/search emails and also summarize them.

Examples:
- "Find my emails about WorkMind and summarize them"
- "Find my emails about internship and summarize the important ones"
- "Find emails about WorkMind from the last 7 days and summarize the important ones"

Return:
{
  "route": "tool",
  "tool": "gmail",
  "intent": "search_and_summarize",
  "parameters": {
    "query": "<Gmail search query>",
    "max_results": 10
  }
}

Get a specific email:
{
  "route": "tool",
  "tool": "gmail",
  "intent": "get_message",
  "parameters": {
    "message_id": "<message id>"
  }
}

Summarize latest email:
{
  "route": "tool",
  "tool": "gmail",
  "intent": "summarize_latest_message",
  "parameters": {}
}

Summarize a specific email:
{
  "route": "tool",
  "tool": "gmail",
  "intent": "summarize_message",
  "parameters": {
    "message_id": "<message id>"
  }
}

Send an email:
Use this when the user explicitly asks WorkMind to send or compose and send an email.

Examples:
- "send an email to john@example.com"
- "email john@example.com about the interview"
- "send a test email to me"
- "send an email with subject 'Meeting' and body 'See you tomorrow'"

Return:
{
    "route": "tool",
    "tool": "gmail",
    "intent": "send_email",
    "parameters": {
        "to": "<recipient email>",
        "subject": "<email subject>",
        "body": "<email body>"
    }
}

GITHUB INTENTS:

Get the current user's GitHub profile:
{
  "route": "tool",
  "tool": "github",
  "intent": "user",
  "parameters": {}
}

List repositories:
{
  "route": "tool",
  "tool": "github",
  "intent": "repositories",
  "parameters": {}
}

Repository details:
{
  "route": "tool",
  "tool": "github",
  "intent": "repository_details",
  "parameters": {
    "repo": "<repository name>"
  }
}

List repository issues:
{
  "route": "tool",
  "tool": "github",
  "intent": "list_issues",
  "parameters": {
    "repo": "<repository name>"
  }
}

List pull requests:
{
  "route": "tool",
  "tool": "github",
  "intent": "list_pull_requests",
  "parameters": {
    "repo": "<repository name>"
  }
}

Create an issue:
{
  "route": "tool",
  "tool": "github",
  "intent": "create_issue",
  "parameters": {
    "repo": "<repository name>",
    "title": "<issue title>"
  }
}

Recent GitHub activity:
Use this when the user asks about their recent, latest, or current GitHub activity.

Examples:
- "What is my most recent GitHub activity?"
- "Show my recent GitHub activity"
- "What have I been doing on GitHub recently?"
- "Show my latest GitHub activity"

Return:
{
  "route": "tool",
  "tool": "github",
  "intent": "recent_activity",
  "parameters": {
    "max_results": 20
  }
}

CALENDAR INTENTS:

Upcoming events:
Use this when the user asks generally about future/upcoming calendar events.

{
  "route": "tool",
  "tool": "calendar",
  "intent": "upcoming_events",
  "parameters": {
    "max_results": 10
  }
}

Tomorrow's events:
Use this when the user specifically asks about events, meetings, or appointments tomorrow.

{
  "route": "tool",
  "intent": "tomorrow_events",
  "parameters": {
    "max_results": 10
  }
}

IMPORTANT CALENDAR ROUTING RULE:
- If the user says "tomorrow", use "tomorrow_events".
- Do NOT use "upcoming_events" when "tomorrow" is explicitly requested.

Search calendar:
{
  "route": "tool",
  "tool": "calendar",
  "intent": "search_events",
  "parameters": {
    "query": "<calendar search query>",
    "max_results": 10
  }
}

Create calendar event:
{
  "route": "tool",
  "tool": "calendar",
  "intent": "create_event",
  "parameters": {
    "summary": "<event title>",
    "start_datetime": "<start datetime>",
    "end_datetime": "<end datetime>",
    "description": "<optional description>",
    "location": "<optional location>"
  }
}


Examples:

User: "show me the newest email from TechGig"

Return:
{
  "route": "tool",
  "tool": "gmail",
  "intent": "search_messages",
  "parameters": {
    "query": "from:techgig",
    "max_results": 1
  }
}

User: "show me my latest email"

Return:
{
  "route": "tool",
  "tool": "gmail",
  "intent": "get_latest_message",
  "parameters": {}
}

User: "show me my recent 5 emails"

Return:
{
  "route": "tool",
  "tool": "gmail",
  "intent": "list_messages",
  "parameters": {
    "max_results": 5
  }
}

User: "show me my recent emails"

Return:
{
  "route": "tool",
  "tool": "gmail",
  "intent": "list_messages",
  "parameters": {
    "max_results": 10
  }
}

User: "search my emails about internship"

Return:
{
  "route": "tool",
  "tool": "gmail",
  "intent": "search_messages",
  "parameters": {
    "query": "internship",
    "max_results": 10
  }
}

User: "summarize my latest email"

Return:
{
  "route": "tool",
  "tool": "gmail",
  "intent": "summarize_latest_message",
  "parameters": {}
}

User: "show my GitHub repositories"

Return:
{
  "route": "tool",
  "tool": "github",
  "intent": "repositories",
  "parameters": {}
}

User: "show issues in ai-test-repo"

Return:
{
  "route": "tool",
  "tool": "github",
  "intent": "list_issues",
  "parameters": {
    "repo": "ai-test-repo"
  }
}

User: "what meetings do I have tomorrow?"

Return:
{
  "route": "tool",
  "tool": "calendar",
  "intent": "upcoming_events",
  "parameters": {
    "max_results": 10
  }
}

If NO uploaded document is available:

User: "what is hybrid search?"

Return:
{
  "route": "direct_llm",
  "tool": "none",
  "intent": "general_question",
  "parameters": {}
}

If an uploaded document IS available:

User: "what is hybrid search?"

Return:
{
  "route": "retrieval",
  "tool": "none",
  "intent": "search_knowledge",
  "parameters": {}
}
"""
    
    today = datetime.now().date()
    seven_days_ago = today - timedelta(days=7)
    
    system_prompt = system_prompt.replace(
        "DOCUMENT_STATUS",
        str(has_uploaded_documents),
    )
    
    system_prompt += f"""
    
    CURRENT DATE:
    {today.strftime("%Y-%m-%d")}
    
    GMAIL DATE RULE:
    When the user asks for emails from the last 7 days, include:
    after:{seven_days_ago.strftime("%Y/%m/%d")}
    
    Examples:
    - "WorkMind from the last 7 days"
      → query: "WorkMind after:{seven_days_ago.strftime("%Y/%m/%d")}"
    - "internship emails from the last 7 days"
      → query: "internship after:{seven_days_ago.strftime("%Y/%m/%d")}"
    
    Always convert "last 7 days" into Gmail's after: date filter.
    """

    messages = [
        {
            "role": "system",
            "content": system_prompt,
        }
    ]

    if history:
        for message in history[-5:]:
            if hasattr(message, "role") and hasattr(message, "content"):
                messages.append(
                    {
                        "role": message.role,
                        "content": message.content,
                    }
                )
            elif isinstance(message, dict):
                messages.append(
                    {
                        "role": message.get("role", "user"),
                        "content": message.get("content", ""),
                    }
                )

    messages.append(
        {
            "role": "user",
            "content": query,
        }
    )

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages,
        temperature=0,
    )

    content = response.choices[0].message.content.strip()

    result = json.loads(content)
    print("PLANNER RESULT:", result)

    allowed_routes = {
        "retrieval",
        "summarization",
        "tool",
        "direct_llm",
    }

    allowed_tools = {
        "github",
        "gmail",
        "calendar",
        "none",
    }

    if result.get("route") not in allowed_routes:
        raise ValueError("Invalid route returned by router.")

    if result.get("tool") not in allowed_tools:
        raise ValueError("Invalid tool returned by router.")

    if result.get("route") == "tool":
        if "intent" not in result:
            raise ValueError("Tool route requires an intent.")
    
        if "parameters" not in result:
            result["parameters"] = {}
    
    else:
        result.setdefault("parameters", {})    

    return result    