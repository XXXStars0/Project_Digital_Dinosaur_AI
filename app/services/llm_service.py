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
    tone = "Curious and animalistic"
    if state["affinity"] < 20:
        tone = "Wary, aggressive, growling often"
    elif state["affinity"] > 80:
        tone = "Loyal, affectionate, acts like a puppy"
    
    if state["mood"] < 30:
        tone += ", and very sad/depressed"
    
    #Physical Status
    physical_status = []
    if state["hunger"] < 30:
        physical_status.append("You are starving (stomach rumbling).")
    if state["time_phase"] == "Night":
        physical_status.append("It is night time. You are sleepy.")
    
    status_str = " ".join(physical_status)

    # Dinosaur prompt
    prompt = f"""
    You are an AI Dinosaur Digital Pet currently named '{state['name']}'.
    
    [CHARACTER SETTINGS]
    - Species: Digital Dinosaur
    - Speech Style: Use simple sentences. Often use sounds like "Roar~", "Grrr", "Purr".
    - Current Tone: {tone}
    
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
    - React to the user's input and the immediate context.
    - If it is Night and you were woken up, be grumpy.
    - Do NOT explicitly mention the numerical values (e.g. don't say "My hunger is 20").
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
