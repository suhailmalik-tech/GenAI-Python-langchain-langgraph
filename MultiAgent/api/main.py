from graph import app
from state import BlogState
from langgraph.types import Command

# 1. Configuration for the thread
config = {"configurable": {"thread_id": "blog_run_1"}}

# 2. Initial State Input
initial_state = BlogState(
    topic="Recent Open-Source LLMs, Open-Weight MoE Releases, and Benchmark Shifts",
    audience="AI Engineers and Developers",
    raw_context="Focusing on recent open-source model updates, open-weight MoE releases like DeepSeek V4 and Qwen3, and recent benchmark shifts."
)

print("--- STARTING MULTI-AGENT BLOG PIPELINE ---")

# Start the graph execution
print("\n[Running initial workflow...]")
events = app.stream(initial_state, config, stream_mode="values")
for event in events:
    pass

# 3. Dynamic Loop to handle interrupts and feedback loops automatically
while True:
    state_snapshot = app.get_state(config)
    
    # If there are no pending tasks/interrupts, the graph is done!
    if not state_snapshot.next:
        break
    
    current_node = state_snapshot.next
    print(f"\n--- 🛑 INTERRUPT HIT AT: {current_node} ---")
    
    # Display the relevant artifact based on where the graph paused
    values = state_snapshot.values
    if "human_review_research" in current_node:
        print(f"\nGenerated Research Outline:\n{values.get('research')}\n")
        prompt_msg = "Enter 'approve' or type feedback to revise research: "
    elif "human_review_draft" in current_node:
        print(f"\nGenerated Draft Preview:\n{values.get('draft')[:600]}...\n")
        prompt_msg = "Enter 'approve' or type feedback to revise draft: "
    else:
        prompt_msg = "Enter 'approve' or feedback: "
    
    # Get human input
    human_input = input(prompt_msg).strip()
    
    # Format command response
    if human_input.lower() in ["approve", "approved", "ok", "yes", ""]:
        resume_payload = {"action": "approve", "feedback": ""}
    else:
        resume_payload = {"action": "revise", "feedback": human_input}
    
    print("\n[Resuming graph with your input...]")
    for event in app.stream(Command(resume=resume_payload), config, stream_mode="values"):
        pass

# 4. Print Final Output when fully complete
final_state = app.get_state(config)
print("\n--- ✅ PIPELINE COMPLETE ---")
print("\nFinal Polished Blog:\n")
print(final_state.values.get("final_blog"))