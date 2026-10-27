from pydantic import BaseModel, Field

class BlogState(BaseModel):
    topic: str = ""
    audience: str = ""
    raw_context: str = ""

    research: str = ""
    research_feedback: str = ""

    draft: str = ""
    draft_feedback: str = ""

    final_blog: str = ""
    revision_count: int = 0