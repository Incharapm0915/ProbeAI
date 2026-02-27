"""
ProbeAI — Smart Candidate Screening Chatbot
============================================
Simple, colorful, friendly UI.
Zero API calls. Fully local question bank.

Run: streamlit run app.py
"""

import streamlit as st
from questions  import get_questions
from validators import VALIDATORS
from storage    import save_candidate

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ProbeAI · Candidate Screening",
    page_icon="🔍",
    layout="centered",
)

# ── Colorful friendly CSS ─────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap');

* { font-family: 'Nunito', sans-serif; }

/* Page background */
.stApp { background: linear-gradient(135deg, #f0f4ff 0%, #fef9f0 50%, #f0fff4 100%); }

/* Hide default Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; max-width: 780px; }

/* Top banner */
.probe-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
    border-radius: 20px;
    padding: 28px 32px;
    margin-bottom: 24px;
    color: white;
    text-align: center;
    box-shadow: 0 8px 32px rgba(102,126,234,0.35);
}
.probe-header h1 { font-size: 2.2rem; font-weight: 800; margin: 0; letter-spacing: -0.5px; }
.probe-header p  { font-size: 1rem; margin: 6px 0 0; opacity: 0.9; }

/* Chat messages */
.msg-bot {
    display: flex;
    gap: 12px;
    align-items: flex-start;
    margin: 14px 0;
}
.msg-user {
    display: flex;
    gap: 12px;
    align-items: flex-start;
    justify-content: flex-end;
    margin: 14px 0;
}
.bubble-bot {
    background: white;
    border: 2px solid #e8eeff;
    border-radius: 18px 18px 18px 4px;
    padding: 14px 18px;
    max-width: 82%;
    font-size: 0.97rem;
    line-height: 1.6;
    color: #2d3748;
    box-shadow: 0 2px 12px rgba(102,126,234,0.1);
}
.bubble-user {
    background: linear-gradient(135deg, #667eea, #764ba2);
    border-radius: 18px 18px 4px 18px;
    padding: 14px 18px;
    max-width: 82%;
    font-size: 0.97rem;
    line-height: 1.6;
    color: white;
    box-shadow: 0 2px 12px rgba(102,126,234,0.25);
}
.avatar-bot  { font-size: 1.8rem; flex-shrink: 0; }
.avatar-user { font-size: 1.8rem; flex-shrink: 0; }

/* Progress pills */
.progress-bar {
    display: flex;
    gap: 6px;
    justify-content: center;
    margin: 0 0 20px;
    flex-wrap: wrap;
}
.pill {
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.3px;
}
.pill-done   { background: #c6f6d5; color: #276749; }
.pill-active { background: linear-gradient(135deg, #667eea, #764ba2); color: white; }
.pill-todo   { background: #edf2f7; color: #a0aec0; }

/* Question card */
.q-card {
    background: linear-gradient(135deg, #667eea15, #f093fb10);
    border: 2px solid #667eea30;
    border-left: 5px solid #667eea;
    border-radius: 12px;
    padding: 16px 20px;
    margin: 8px 0;
    font-size: 0.95rem;
    color: #2d3748;
}
.q-tag {
    display: inline-block;
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    padding: 2px 10px;
    border-radius: 10px;
    font-size: 0.72rem;
    font-weight: 700;
    margin-bottom: 8px;
}

/* Summary card */
.summary-card {
    background: white;
    border-radius: 16px;
    padding: 24px 28px;
    border: 2px solid #e8eeff;
    box-shadow: 0 4px 20px rgba(102,126,234,0.12);
}
.summary-row {
    display: flex;
    justify-content: space-between;
    padding: 8px 0;
    border-bottom: 1px solid #f0f4ff;
    font-size: 0.93rem;
}
.summary-label { color: #718096; font-weight: 600; }
.summary-value { color: #2d3748; font-weight: 700; text-align: right; }

/* Tip box */
.tip-box {
    background: #fffbf0;
    border: 1.5px solid #f6e05e;
    border-radius: 10px;
    padding: 10px 16px;
    font-size: 0.85rem;
    color: #744210;
    margin: 12px 0;
}

/* Stagger animation */
@keyframes fadeIn { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }
.msg-bot, .msg-user { animation: fadeIn 0.25s ease; }
</style>
""", unsafe_allow_html=True)

# ── Constants ─────────────────────────────────────────────────────────────────
EXIT_WORDS = {"exit", "quit", "bye", "goodbye", "end", "stop"}

STAGES = [
    ("name",       "👤 Name"),
    ("email",      "📧 Email"),
    ("phone",      "📞 Phone"),
    ("experience", "🗓 Experience"),
    ("position",   "💼 Role"),
    ("location",   "📍 Location"),
    ("tech_stack", "🛠 Tech Stack"),
    ("questions",  "❓ Questions"),
]

PROMPTS = {
    "name":       "What's your **full name**?",
    "email":      "Great! What's your **email address**?",
    "phone":      "Got it! What's your **phone number**? *(with country code)*",
    "experience": "How many **years of experience** do you have?",
    "position":   "What **role** are you applying for? *(e.g. Backend Engineer, Data Scientist)*",
    "location":   "Where are you based? **City and country** please.",
    "tech_stack": "List your **tech stack** — languages, frameworks, databases, tools.\n*(e.g. Python, React, PostgreSQL, Docker)*",
}

ACKS = ["Nice one! 👍", "Got it! ✅", "Perfect! 🎯", "Noted! 📝", "Awesome! 🚀", "Great! ✨", "Thanks! 💪"]


# ── Session state init ────────────────────────────────────────────────────────
def init():
    if "stage" not in st.session_state:
        st.session_state.stage     = "name"
        st.session_state.messages  = []
        st.session_state.profile   = {}
        st.session_state.questions = []
        st.session_state.q_index   = 0
        st.session_state.answers   = []
        st.session_state.done      = False
        st.session_state.greeted   = False


# ── Message helpers ───────────────────────────────────────────────────────────
def bot(text):
    st.session_state.messages.append({"role": "bot", "text": text})

def usr(text):
    st.session_state.messages.append({"role": "user", "text": text})


# ── Render helpers ────────────────────────────────────────────────────────────
def render_message(msg):
    if msg["role"] == "bot":
        st.markdown(
            f'<div class="msg-bot"><div class="avatar-bot">🔍</div>'
            f'<div class="bubble-bot">{msg["text"]}</div></div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<div class="msg-user"><div class="bubble-user">{msg["text"]}</div>'
            f'<div class="avatar-user">🧑</div></div>',
            unsafe_allow_html=True,
        )


def render_progress():
    stage_keys = [s[0] for s in STAGES]
    current    = st.session_state.stage
    pills      = []
    for key, label in STAGES:
        if key == current:
            cls = "pill-active"
        elif stage_keys.index(key) < stage_keys.index(current) if current in stage_keys else True:
            cls = "pill-done"
        else:
            cls = "pill-todo"
        pills.append(f'<span class="pill {cls}">{label}</span>')
    st.markdown(f'<div class="progress-bar">{"".join(pills)}</div>', unsafe_allow_html=True)


def render_q_card(q_num, total, tech, question):
    st.markdown(
        f'<div class="q-card">'
        f'<div class="q-tag">Q{q_num} of {total} · {tech}</div><br>'
        f'{question}'
        f'</div>',
        unsafe_allow_html=True,
    )


def render_summary():
    p = st.session_state.profile
    rows = [
        ("👤 Name",       p.get("name", "—")),
        ("📧 Email",      p.get("email", "—")),
        ("📞 Phone",      p.get("phone", "—")),
        ("🗓 Experience", p.get("experience", "—")),
        ("💼 Role",       p.get("position", "—")),
        ("📍 Location",   p.get("location", "—")),
        ("🛠 Tech Stack", p.get("tech_stack", "—")),
    ]
    html = '<div class="summary-card">'
    for label, value in rows:
        html += (
            f'<div class="summary-row">'
            f'<span class="summary-label">{label}</span>'
            f'<span class="summary-value">{value}</span>'
            f'</div>'
        )
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


# ── Stage logic ───────────────────────────────────────────────────────────────
def handle_input(user_input: str):
    text = user_input.strip()

    # Exit check
    if text.lower() in EXIT_WORDS:
        usr(text)
        bot("Thanks for chatting with **ProbeAI**! 👋 Best of luck with your application! 🌟")
        st.session_state.done = True
        return

    stage = st.session_state.stage

    # ── Collecting profile fields ──────────────────────────────────────────
    if stage in PROMPTS:
        # Validate if validator exists
        if stage in VALIDATORS:
            valid, err_msg = VALIDATORS[stage](text)
            if not valid:
                usr(text)
                bot(f"⚠️ {err_msg} Please try again.")
                return

        usr(text)
        st.session_state.profile[stage] = text

        # Move to next stage
        keys = list(PROMPTS.keys())
        idx  = keys.index(stage)
        name = st.session_state.profile.get("name", "there").split()[0]

        if idx + 1 < len(keys):
            next_stage = keys[idx + 1]
            st.session_state.stage = next_stage
            # Personalise the name prompt acknowledgement
            if stage == "name":
                bot(f"Nice to meet you, **{name}**! 😊\n\n" + PROMPTS[next_stage])
            else:
                bot(f"{ACKS[idx % len(ACKS)]}\n\n" + PROMPTS[next_stage])
        else:
            # All fields collected — load questions
            st.session_state.stage = "questions"
            qs = get_questions(text, n_per_tech=2)
            st.session_state.questions = qs
            st.session_state.q_index   = 0
            techs = list(dict.fromkeys(q["tech"] for q in qs))
            bot(
                f"🎉 All set, **{name}**! I found questions on: **{', '.join(techs)}**\n\n"
                f"You have **{len(qs)} questions** total. Take your time — answer as fully as you like!\n\n"
                "Type `exit` anytime to end the session."
            )
            # Show first question
            q = qs[0]
            bot(f'<div class="q-tag">Q1 of {len(qs)} · {q["tech"]}</div><br>{q["question"]}')

    # ── Q&A phase ─────────────────────────────────────────────────────────
    elif stage == "questions":
        idx  = st.session_state.q_index
        qs   = st.session_state.questions
        total = len(qs)

        usr(text)
        st.session_state.answers.append({
            "question": qs[idx]["question"],
            "answer":   text,
        })

        next_idx = idx + 1
        st.session_state.q_index = next_idx

        if next_idx < total:
            q = qs[next_idx]
            ack = ACKS[idx % len(ACKS)]
            bot(f"{ack}\n\n"
                f'<div class="q-tag">Q{next_idx+1} of {total} · {q["tech"]}</div><br>{q["question"]}')
        else:
            # Done — farewell
            name = st.session_state.profile.get("name", "there").split()[0]
            save_candidate(st.session_state.profile, st.session_state.answers)
            bot(
                f"🎊 **Well done, {name}! Screening complete.**\n\n"
                "Our team will review your responses and get back to you within **3–5 business days**.\n\n"
                "Thank you for taking the time — best of luck! 🚀"
            )
            st.session_state.stage = "done"
            st.session_state.done  = True


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    init()

    # Header
    st.markdown("""
    <div class="probe-header">
        <h1>🔍 ProbeAI</h1>
        <p>Smart Candidate Screening · Powered by local AI · Takes 5–10 minutes</p>
    </div>
    """, unsafe_allow_html=True)

    # Progress bar
    if not st.session_state.done:
        render_progress()

    # Greeting (once)
    if not st.session_state.greeted:
        bot(
            "👋 Hi! Welcome to **ProbeAI** — your smart screening assistant.\n\n"
            "I'll collect some basic info about you, then ask **technical questions** "
            "tailored to your skill set.\n\n"
            "⏱ Takes about **5–10 minutes** · Type `exit` anytime to leave.\n\n"
            "Let's start — " + PROMPTS["name"]
        )
        st.session_state.greeted = True

    # Render chat history
    for msg in st.session_state.messages:
        render_message(msg)

    # Show profile summary when done
    if st.session_state.done and st.session_state.stage in ("done", "questions"):
        st.markdown("---")
        st.markdown("### 📋 Your Profile Summary")
        render_summary()

        _, c, _ = st.columns([1, 2, 1])
        with c:
            if st.button("🔄 Start New Session", use_container_width=True):
                for k in list(st.session_state.keys()):
                    del st.session_state[k]
                st.rerun()
        return

    # Tip during questions
    if st.session_state.stage == "questions" and not st.session_state.done:
        qidx  = st.session_state.q_index
        total = len(st.session_state.questions)
        st.markdown(
            f'<div class="tip-box">💡 Question {qidx + 1} of {total} — '
            'Answer in your own words. There are no trick questions!</div>',
            unsafe_allow_html=True,
        )

    # Input
    placeholder = {
        "name":       "Type your full name…",
        "email":      "your@email.com",
        "phone":      "+91 98765 43210",
        "experience": "e.g. 3 or 3.5",
        "position":   "e.g. Backend Engineer",
        "location":   "e.g. Bengaluru, India",
        "tech_stack": "e.g. Python, React, PostgreSQL, Docker",
        "questions":  "Type your answer here…",
    }.get(st.session_state.stage, "Type here…")

    if user_input := st.chat_input(placeholder):
        handle_input(user_input)
        st.rerun()


if __name__ == "__main__":
    main()