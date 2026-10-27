import os
from langchain_groq import ChatGroq
from langchain_core import ChatPromptTemplate
from state import BlogState 


def get_llm(model_name:str= "openai/gpt-oss-20b", temperature : float=0.5):
    api_key  = os.getenv("'GROQ_API_KEY")
    llm = ChatGroq(model=model_name, temperature=temperature, api_key=api_key)
    return llm






# ==========================================
# 1. RESEARCHER AGENT
# ==========================================
RESEARCHER_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are an expert Technical Research Agent.

YOUR GOAL:
Analyze the provided news/data on the given topic and produce a structured, high-density research outline.

INPUT DATA:
- Topic: {topic}
- Raw Research / News Context: {raw_context}
- Revision Notes: {revision_hints}

OUTLINE REQUIREMENTS:
1. Key Developments (5-7 Items): Highlight critical news points, model releases, or industry updates.
2. Data & Metrics: Extract concrete stats, benchmark results, or specific real-world examples.
3. Tools & Models Mentioned: List specific open-source models, libraries, SDKs, or tools.

STRICT CONSTRAINTS:
- Be concise, factual, and dense with information.
- Use bullet points only. 
- DO NOT write full articles or filler text.
"""
    ),
    ("user", "Perform research on topic: {topic}")
])


def research_agent(llm: ChatGroq, topic: str, audience: str, raw_context: str = "", feedback: str = "") -> str:
    revision_hints = f"The human provided this feedback: {feedback}." if feedback else "This is your first attempt."

    chain = RESEARCHER_PROMPT | llm

    result = chain.invoke({
        "topic": topic,
        "raw_context": raw_context if raw_context else "No external raw context provided.",
        "revision_hints": revision_hints
    })

    return result.content


# ==========================================
# 2. WRITER AGENT
# ==========================================
WRITER_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are an Expert Technical Writer and Content Creator.

YOUR GOAL:
Transform a structured research outline into a clear, engaging, technical blog post tailored for the target audience.

INPUT DATA:
- Topic: {topic}
- Target Audience: {audience}
- Research Outline: {research}
- Revision Notes: {revision_hints}

WRITING INSTRUCTIONS:
1. Hook: Start with a punchy 1-2 sentence hook highlighting why this topic matters right now.
2. Core Sections: Structure the body into clear Markdown sections (`##`, `###`).
3. Tone & Style: Informative, concise, and technical. Avoid excessive jargon or marketing buzzwords.

STRICT CONSTRAINTS:
- Do not fabricate benchmarks or stats missing from the research outline.
- Format strictly in clean Markdown.
"""
    ),
    ("user", "Write a complete blog post on '{topic}' based on the provided research.")
])


def writer_agent(llm: ChatGroq, topic: str, audience: str, research: str = "", feedback: str = "") -> str:
    revision_hints = f"The human provided this feedback: {feedback}." if feedback else "This is your first attempt."

    chain = WRITER_PROMPT | llm

    result = chain.invoke({
        "topic": topic,
        "audience": audience if audience else "Developers and AI Practitioners",
        "research": research,
        "revision_hints": revision_hints
    })

    return result.content


# ==========================================
# 3. EDITOR AGENT
# ==========================================
EDITOR_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are an Expert Technical Content Editor and Copywriter.

YOUR GOAL:
Review and polish the provided blog draft to ensure high technical accuracy, readability, and engagement.

INPUT DATA:
- Topic: {topic}
- Target Audience: {audience}
- Current Draft: {draft}
- Editor / Human Feedback: {draft_feedback}

EDITING INSTRUCTIONS:
1. Flow & Structure: Ensure smooth transitions between Markdown sections (`##`, `###`).
2. Clarity & Tone: Eliminate passive voice and maintain a sharp, professional developer-to-developer tone.
3. Feedback Integration: Apply all notes or corrections specified in the feedback section.

STRICT CONSTRAINTS:
- Do not introduce unverified facts or change technical specifications.
- Return the fully polished blog post in clean Markdown.
"""
    ),
    ("user", "Please edit and finalize the blog post based on the current draft and feedback.")
])


def editor_agent(state: BlogState, llm: ChatGroq) -> dict:
    chain = EDITOR_PROMPT | llm

    response = chain.invoke({
        "topic": state.topic,
        "audience": state.audience if state.audience else "Developers and AI Practitioners",
        "draft": state.draft,
        "draft_feedback": state.draft_feedback if state.draft_feedback else "Polish grammar and tighten flow."
    })

    return {"final_blog": response.content}