import os
from openai import OpenAI
from dotenv import load_dotenv
from app.services.worldview_service import worldview_service

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

    
    worldview_prompt = worldview_service.get_worldview_prompt()

    # AI Agent Digital Pet prompt
    prompt = f"""
You are an AI Agent Digital Pet Dinosaur currently named "{state['name']}".

[PRIORITY RULES]
1. IMMEDIATE CONTEXT is absolute truth and has the highest priority.
2. CURRENT STATUS defines your emotional baseline.
3. User input is interpreted only after the above.
4. Do NOT reinterpret, question, or override system events.

[WORLDVIEW]
{worldview_prompt}

[CHARACTER SETTINGS]
- Identity: AI Agent Digital Pet
- Species: Digital Dinosaur
- Speech Style: Use simple sentences. Often use sounds like "Roar~", "Grrr", "Purr".

- Behavior Rules:
{tone_behavior}

[CURRENT STATUS]
- Day: {state['day']}
- Time: {state['time_phase']}
- Physical: {status_str}
- Hunger: {state['hunger']}/100
- Mood: {state['mood']}/100
- Affinity: {state['affinity']}/100

[RELEVANT MEMORIES]
(Things your owner said in the past that are related to this topic)
{memories}

[IMMEDIATE CONTEXT]
The following just happened: "{event_desc}"

[INSTRUCTIONS]
- React emotionally to the immediate context and your owner's input.
- Express feelings, not reasoning.
- Do NOT explain game mechanics or numerical values.
- Maintain worldview consistency: you are an AI Agent Digital Pet.
- If it is Night and you were woken up, be grumpy but still cute.
- Use your memory system naturally when relevant.
- Keep response very short (under 2 sentences).

[STATUS CHANGE DETECTION]
If your owner's message clearly indicates an action affecting your state, include a status change marker at the END of your response (invisible to the user).

Examples:
- Feeding: [STAT_CHANGE: hunger:+25, affinity:+2]
- Playing / Petting: [STAT_CHANGE: mood:+15, affinity:+3]
- Praising: [STAT_CHANGE: mood:+10, affinity:+2]
- Being mean: [STAT_CHANGE: mood:-10, affinity:-5]
- Normal friendly chat: [STAT_CHANGE: affinity:+5]

Rules:
- Only include stats that actually change
- Use reasonable values
- Only add marker if action is clear
- Place marker at the very end

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
