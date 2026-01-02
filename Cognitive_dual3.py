import streamlit as st
import ollama
import time
import random
from datetime import datetime

# -------------------------------------
# CONFIG
# -------------------------------------
MODEL_NAME = "llama3:8b"
TURN_DELAY_BASE = 0.3

# PERSONAS = [
#     "Economist", "Psychologist", "Philosopher", "Realist", "Visionary",
#     "Minimalist", "Capitalist", "Artist", "Engineer", "Nihilist",
#     "Strategist", "Anarchist", "Stoic", "Humanist", "Hedonist",
# ]

PERSONAS = [
    "Psychologist", "Philosopher",  
     "Capitalist", "Artist", "Engineer", "Nihilist",
    "Stoic", "Hedonist"
]

# -------------------------------------
# STREAMLIT SETTINGS
# -------------------------------------
st.set_page_config(page_title="Cognitive Duel", layout="wide")
st.title("⚔️ Cognitive Duel — Infinite Intellectual Battle")

# State init
if "running" not in st.session_state:
    st.session_state.running = False

if "dialogue" not in st.session_state:
    st.session_state.dialogue = []

if "log_file" not in st.session_state:
    st.session_state.log_file = None

if "turn_count" not in st.session_state:
    st.session_state.turn_count = 0


# Topic Input
topic = st.text_input("Debate Topic:", value="")
st.caption("Topic changes apply only after Reset.")

# Sidebar Sliders
st.sidebar.header("Duel Controls")
aggression = st.sidebar.slider("Aggression", 0, 10, 5)
abstraction = st.sidebar.slider("Abstraction", 0, 10, 5)
novelty = st.sidebar.slider("Novelty Pressure", 0, 10, 5)
complexity = st.sidebar.slider("Vocabulary Complexity", 0, 10, 4)
speed = st.sidebar.slider("Speed", 1, 10, 6)

start_btn = st.sidebar.button("▶️ Start")
pause_btn = st.sidebar.button("⏸️ Pause")
reset_btn = st.sidebar.button("🔄 Reset")

download_slot = st.sidebar.empty()
chat_box = st.container()

if start_btn:
    st.session_state.running = True
    st.session_state.turn_count = 0
    st.session_state.show_warning = False


if pause_btn:
    st.session_state.running = False

if reset_btn:
    st.session_state.running = False
    st.session_state.dialogue = []
    st.session_state.turn_count = 0
    st.session_state.show_warning = False

    st.session_state.log_file = f"duel_log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
    open(st.session_state.log_file, "w", encoding="utf-8").close()

# Ensure log file exists
if st.session_state.log_file is None:
    st.session_state.log_file = f"duel_log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
    open(st.session_state.log_file, "w", encoding="utf-8").close()

# -------------------------------------
# LLM CALL
# -------------------------------------
def generate_response(persona, opponent_msg):
    sophistication = ["simple", "plain", "normal", "educated", "advanced",
                       "refined", "technical", "academic", "philosophical",
                       "elite", "ultra-intellectual"]
    vocab_style = sophistication[min(max(complexity, 0), 10)]

    prompt = f"""
You are a {persona}. Topic: "{topic}".
Use {vocab_style} vocabulary.
Keep it short: 1-2 sentences max.
Never agree. Always counter or attack.
Aggression: {aggression}/10
Abstraction: {abstraction}/10
Novelty Pressure: {novelty}/10

Opponent said:
{opponent_msg}

Respond labeled like this:
**{persona}:** your statement
"""
    response = ollama.generate(model=MODEL_NAME, prompt=prompt)["response"]
    return response.strip()

# -------------------------------------
# DISPLAY helper
# -------------------------------------

def append_and_display(text):
    # Add to memory
    st.session_state.dialogue.append(text)

    # Write to log
    with open(st.session_state.log_file, "a", encoding="utf-8") as f:
        f.write(text + "\n")

    # Re-render entire conversation
    chat_box.empty()
    with chat_box:
        for line in st.session_state.dialogue:
            st.markdown(line)


# -------------------------------------
# MAIN LOOP
# -------------------------------------
if st.session_state.running:

    if len(st.session_state.dialogue) == 0:
        persona = random.choice(PERSONAS)
        msg = generate_response(persona, "Start the debate.")
        timestamp = datetime.now().strftime("%H:%M:%S")
        append_and_display(f"[{timestamp}] {msg}")

    else:
        last_msg = st.session_state.dialogue[-1]
        persona = random.choice(PERSONAS)
        msg = generate_response(persona, last_msg)
        timestamp = datetime.now().strftime("%H:%M:%S")
        append_and_display(f"[{timestamp}] {msg}")
        
    # Count turns
    st.session_state.turn_count += 1

    # Soft Stop after 100 turns
    if st.session_state.turn_count >= 100:
        st.session_state.running = False
        st.session_state.turn_count = 0
        st.session_state.show_warning = True
        if st.session_state.show_warning:
            st.warning("⚠️ Turn Limit Reached — Press Start to continue the duel.")

        st.stop()

    # Speed affects loop pace
    time.sleep((11 - speed) * TURN_DELAY_BASE)
    st.rerun()
    # 
 







# -------------------------------------
# Download Log Option
# -------------------------------------
with open(st.session_state.log_file, "rb") as f:
    download_slot.download_button(
        label="⬇️ Download Full Duel Log",
        data=f,
        file_name=st.session_state.log_file,
        mime="text/plain"
    )
