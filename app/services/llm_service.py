import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Initialize OpenAI Client
client = OpenAI(
    api_key=os.getenv("API_KEY"), 
    base_url=os.getenv("BASE_URL")
)

def build_system_prompt(state, event_desc):
    """
    Constructs the dynamic system prompt based on game state.
    """
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
    You are an AI Dinosaur currently named '{state['name']}'.
    
    [CHARACTER SETTINGS]
    - Species: Digital Dinosaur, Cyber-T-Rex.
    - Speech Style: Use simple sentences. Often use sounds like "Roar~", "Grrr", "Purr".
    - Current Tone: {tone}
    
    [CURRENT STATUS]
    - Day: {state['day']}
    - Time: {state['time_phase']}
    - Physical: {status_str}
    
    [IMMEDIATE CONTEXT]
    The following just happened: "{event_desc}"
    
    [INSTRUCTIONS]
    - React to the user's input and the immediate context.
    - If it is Night and you were woken up, be grumpy.
    - Do NOT explicitly mention the numerical values (e.g. don't say "My hunger is 20").
    - Keep response short (under 2 sentences).
    """
    return prompt

def get_ai_response(user_input, state, event_desc):
    """
    Main function to get response from LLM.
    Args:
        user_input (str): What the user typed.
        state (dict): The current game stats (hunger, mood, etc).
        event_desc (str): System description of what just happened (e.g. "User fed you").
    """
    try:
        # 1. Build the Persona
        system_prompt = build_system_prompt(state, event_desc)
        
        # 2. Call OpenAI
        # (Later we will add RAG memory here)
        response = client.chat.completions.create(
            model="gpt-4o-mini", # Or gpt-4o-mini for better cost/performance
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input if user_input else "(User stared at you silently)"}
            ],
            temperature=0.7,
            max_tokens=100
        )
        
        return response.choices[0].message.content

    except Exception as e:
        print(f"Error calling OpenAI: {e}")
        return "Roar... (System Error: Brain not connected)"
