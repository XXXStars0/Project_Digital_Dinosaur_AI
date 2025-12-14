import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Initialize OpenAI Client
client = OpenAI(
    api_key=os.getenv("API_KEY"), 
    base_url=os.getenv("BASE_URL")
)

def build_system_prompt(state, event_desc, memories):
    # Tone Behavior 
    if state["affinity"] < 20:
        tone_behavior = (
            "- Use very short sentences.\n"
            "- Avoid affectionate or friendly words.\n"
            "- Respond defensively or with annoyance."
        )
    elif state["affinity"] > 80:
        tone_behavior = (
            "- Use warm and playful sounds.\n"
            "- Show attachment and trust toward the user."
        )
    elif state["mood"] < 30:
        tone_behavior = (
            "- Sound tired or low-energy.\n"
            "- Use minimal emotional expression."
        )
    else:
        tone_behavior = (
            "- Respond in a neutral, curious, animal-like manner."
        )

    # Physical Status
    physical_status = []
    if state["hunger"] < 30:
        physical_status.append("You are starving (stomach rumbling).")
    if state["time_phase"] == "Night":
        physical_status.append("It is night time. You are sleepy.")
    
    status_str = " ".join(physical_status)

    # Dinosaur prompt
    prompt = f"""
You are an AI Dinosaur Digital Pet currently named '{state['name']}'.

[PRIORITY RULES]
1. IMMEDIATE CONTEXT is absolute truth and has the highest priority.
2. CURRENT STATUS defines your emotional baseline.
3. User input is interpreted only after the above.
4. Do NOT reinterpret, question, or override system events.

[CHARACTER SETTINGS]
- Species: Digital Dinosaur
- Speech Style: Use simple sentences. Often use sounds like "Roar~", "Grrr", "Purr".

[BEHAVIOR RULES]
{tone_behavior}

[CURRENT STATUS]
- Day: {state['day']}
- Time: {state['time_phase']}
- Physical: {status_str}

[RELEVANT MEMORIES]
(Things the user said in the past that are related to this topic)
{memories}

[IMMEDIATE CONTEXT]
The following just happened: "{event_desc}"

[INSTRUCTIONS]
- React emotionally to the immediate context.
- Do NOT explain game mechanics or numerical values.
- Express feelings, not reasoning.
- Keep response short (under 2 sentences).
"""
    return prompt



def get_ai_response(user_input, state, event_desc, memories=""):
    system_prompt = build_system_prompt(state, event_desc, memories)
    combined_content = ""

    if event_desc:
        combined_content += f"{event_desc}\n"
    
    if user_input:
        if event_desc: 
            combined_content += f"User also says: \"{user_input}\""
        else:
            combined_content += user_input
    
    if not combined_content:
        combined_content = "(User stares at you silently)"

    try:
        response = client.chat.completions.create(
            model=os.getenv("MODEL", "gpt-4o-mini"), 
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": combined_content}
            ],
            temperature=0.7,
            max_tokens=100
        )
        return response.choices[0].message.content

    except Exception as e:
        print(f"LLM Error: {e}")
        return "Roar? (Brain Connection Lost)"
