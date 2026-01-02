# multi-agent-reasoning-arena
An interactive, locally-run multi-agent debate system where multiple AI personas continuously clash on a topic, while the user steers the intellectual dynamics in real time.

This project is not a chatbot.
It is a thinking instrument designed to explore perspectives, stress-test ideas, and demonstrate controlled multi-agent reasoning.

# Problem
- Most AI chat interfaces are passive:
- One prompt → one response
- User types, model talks
- No way to steer how thinking unfolds

# Core Idea
- Instead of asking an AI to “think better”, force two AIs to fight — and let the human control how they fight.
- Cognitive Duel creates:
- - Two adversarial agents
  - No long-term memory (prevents convergence)
  - Continuous turn-based debate
- Real-time control over:
- - Aggression
  - Abstraction
  - Novelty pressure
  - Vocabulary complexity
  - Speed

The result is a live reasoning arena, not a Q&A tool.


# What You Can Do
- Enter any debate topic e.g.Everyone must exercise daily, Capitalism is better than communism
- Start a continuous AI-vs-AI argument
- Adjust sliders while the debate is running
- Pause, resume, or reset at any time
- Automatically stop after N turns (soft stop)
- Download full debate logs for analysis (duel_log_YYYY-MM-DD_HH-MM-SS.txt)
- Run everything locally (no API costs, no data leakage)

# How to Run
1. Install dependencies
pip install streamlit ollama

2. Ensure Ollama is running
ollama serve

3. Run the app
streamlit run app.py

4. Open following link in browser:
http://localhost:8501

# Example Use Cases
- Exploring ethical, technical, or philosophical debates
- Stress-testing product ideas from opposing perspectives
- Extracting strong arguments from debate logs


# Limitations
- sequencial execution
- Models may repeat arguments at low novelty settings
- Not intended for factual accuracy — focused on reasoning diversity
- Bugs
  
