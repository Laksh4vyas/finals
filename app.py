
import streamlit as st
import pickle
import json
import random
import pandas as pd
import re

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="College Admission Chatbot",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,400&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    /* Background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: #e8e8f0;
    }

    /* Main title */
    .main-title {
        font-family: 'Sora', sans-serif;
        font-size: 2.6rem;
        font-weight: 700;
        background: linear-gradient(90deg, #a78bfa, #60a5fa, #34d399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }

    .sub-title {
        font-size: 1rem;
        color: #94a3b8;
        margin-bottom: 1.5rem;
    }

    /* Cards */
    .card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: 1.5rem;
        backdrop-filter: blur(10px);
        margin-bottom: 1rem;
    }

    /* Chat bubble */
    .chat-user {
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        border-radius: 18px 18px 4px 18px;
        padding: 0.8rem 1.2rem;
        margin: 0.5rem 0;
        max-width: 80%;
        margin-left: auto;
        color: white;
        font-size: 0.95rem;
        box-shadow: 0 4px 20px rgba(79, 70, 229, 0.3);
    }

    .chat-bot {
        background: rgba(255,255,255,0.07);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 18px 18px 18px 4px;
        padding: 0.8rem 1.2rem;
        margin: 0.5rem 0;
        max-width: 80%;
        color: #e2e8f0;
        font-size: 0.95rem;
    }

    .chat-label {
        font-size: 0.7rem;
        color: #94a3b8;
        margin-bottom: 0.2rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e1b4b, #0f0c29);
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    [data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }

    .sidebar-header {
        font-family: 'Sora', sans-serif;
        font-size: 1.2rem;
        font-weight: 700;
        color: #a78bfa !important;
        margin-bottom: 1rem;
    }

    /* Model accuracy cards */
    .model-card {
        background: rgba(255,255,255,0.05);
        border-radius: 12px;
        padding: 0.8rem 1rem;
        margin-bottom: 0.6rem;
        border-left: 3px solid;
    }

    .model-nb { border-color: #60a5fa; }
    .model-lr { border-color: #34d399; }
    .model-svm { border-color: #f472b6; }

    .model-name {
        font-weight: 600;
        font-size: 0.85rem;
    }

    .model-acc {
        font-size: 1.4rem;
        font-weight: 700;
    }

    .model-err {
        font-size: 0.72rem;
        color: #94a3b8 !important;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255,255,255,0.05);
        border-radius: 12px;
        padding: 4px;
        gap: 4px;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        color: #94a3b8;
        font-weight: 500;
        padding: 0.5rem 1.5rem;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
        color: white !important;
    }

    /* Input fields */
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.07) !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        border-radius: 12px !important;
        color: #e2e8f0 !important;
        padding: 0.6rem 1rem !important;
        font-family: 'DM Sans', sans-serif !important;
    }

    .stTextInput > div > div > input:focus {
        border-color: #7c3aed !important;
        box-shadow: 0 0 0 2px rgba(124, 58, 237, 0.25) !important;
    }

    /* Selectbox */
    .stSelectbox > div > div {
        background: rgba(255,255,255,0.07) !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        border-radius: 12px !important;
        color: #e2e8f0 !important;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.6rem 2rem !important;
        font-weight: 600 !important;
        font-family: 'Sora', sans-serif !important;
        letter-spacing: 0.03em !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 15px rgba(79, 70, 229, 0.35) !important;
    }

    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(79, 70, 229, 0.5) !important;
    }

    /* Slider */
    .stSlider > div > div > div {
        color: #a78bfa !important;
    }

    /* DataFrame */
    .stDataFrame {
        border-radius: 12px !important;
        overflow: hidden !important;
    }

    /* Section headers */
    .section-header {
        font-family: 'Sora', sans-serif;
        font-size: 1.1rem;
        font-weight: 600;
        color: #a78bfa;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* Divider */
    .divider {
        border: none;
        border-top: 1px solid rgba(255,255,255,0.08);
        margin: 1.2rem 0;
    }

    /* Warning / info boxes */
    .stWarning, .stInfo {
        background: rgba(251, 191, 36, 0.1) !important;
        border: 1px solid rgba(251, 191, 36, 0.3) !important;
        border-radius: 10px !important;
        color: #fbbf24 !important;
    }

    /* Number input */
    .stNumberInput > div > div > input {
        background: rgba(255,255,255,0.07) !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        border-radius: 12px !important;
        color: #e2e8f0 !important;
    }

    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD MODELS ----------------
@st.cache_resource
def load_models():
    nb_model = pickle.load(open('models/nb.pkl', 'rb'))
    lr_model = pickle.load(open('models/lr.pkl', 'rb'))
    svm_model = pickle.load(open('models/svm.pkl', 'rb'))
    vectorizer = pickle.load(open('models/vectorizer.pkl', 'rb'))
    return nb_model, lr_model, svm_model, vectorizer

nb_model, lr_model, svm_model, vectorizer = load_models()

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    with open('data.json') as f:
        data = json.load(f)
    college_df = pd.read_csv("colleges.csv")
    return data, college_df

data, college_df = load_data()

# ---------------- STRIP HTML TAGS ----------------
def strip_html(text):
    """Remove all HTML tags and return clean plain text with newlines preserved."""
    # Replace <br> variants with newlines
    text = re.sub(r'<br\s*/?>', '\n', text, flags=re.IGNORECASE)
    # Replace closing block tags with newlines
    text = re.sub(r'</?(p|div|li|tr)[^>]*>', '\n', text, flags=re.IGNORECASE)
    # Extract href link text format: keep anchor display text only
    text = re.sub(r'<a\s[^>]*href=["\']([^"\']*)["\'][^>]*>(.*?)</a>',
                  lambda m: m.group(2).strip(), text, flags=re.IGNORECASE | re.DOTALL)
    # Remove all remaining HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Decode common HTML entities
    text = text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>') \
               .replace('&nbsp;', ' ').replace('&#39;', "'").replace('&quot;', '"')
    # Clean up excessive whitespace/newlines
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

# ---------------- CHATBOT FUNCTION ----------------
def get_response(user_input, model):
    input_vec = vectorizer.transform([user_input])
    tag = model.predict(input_vec)[0]

    for intent in data['intents']:
        if intent['tag'] == tag:
            raw = random.choice(intent['responses'])
            return strip_html(raw)

    return "Sorry, I didn't understand that. Could you rephrase?"

# ---------------- MODEL SELECT ----------------
def select_model(choice):
    if choice == "Naive Bayes":
        return nb_model
    elif choice == "Logistic Regression":
        return lr_model
    else:
        return svm_model

# ---------------- COLLEGE RECOMMENDER ----------------
def recommend_colleges(marks, location, branch, budget):
    filtered = college_df.copy()
    #filtered = filtered[filtered['cutoff'] <= marks]
    filtered = filtered[filtered['avg_cutoff'] <= marks]
    if location != "Any":
        filtered = filtered[filtered['location'] == location]
    if branch != "Any":
        filtered = filtered[filtered['branch'] == branch]
    filtered = filtered[filtered['fees'] <= budget]
    return filtered.head(5)

# ---------------- SIDEBAR ----------------
# ---------------- LOAD ACCURACY ----------------
with open("models/accuracy.json") as f:
    acc_data = json.load(f)

nb_acc = acc_data["nb"]
lr_acc = acc_data["lr"]
svm_acc = acc_data["svm"]

# convert to percentage string
nb_acc_str = f"{nb_acc*100:.2f}%"
lr_acc_str = f"{lr_acc*100:.2f}%"
svm_acc_str = f"{svm_acc*100:.2f}%"

# auto error labels
def get_error_label(acc):
    if acc >= 0.97:
        return "Minimal Error Rate"
    elif acc >= 0.93:
        return "Very Low Error Rate"
    else:
        return "Low Error Rate"

models_info = [
    {"name": "Naive Bayes", "acc": nb_acc_str, "err": get_error_label(nb_acc), "cls": "model-nb", "color": "#60a5fa"},
    {"name": "Logistic Regression", "acc": lr_acc_str, "err": get_error_label(lr_acc), "cls": "model-lr", "color": "#34d399"},
    {"name": "SVM", "acc": svm_acc_str, "err": get_error_label(svm_acc), "cls": "model-svm", "color": "#f472b6"},
]

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown('<p class="sidebar-header">⚙️ Dashboard</p>', unsafe_allow_html=True)
    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    st.markdown("**📊 Model Accuracy**")
    st.markdown('<div style="height:0.5rem"></div>', unsafe_allow_html=True)

    for m in models_info:
        st.markdown(f"""
        <div class="model-card {m['cls']}">
            <div class="model-name" style="color:{m['color']}">{m['name']}</div>
            <div class="model-acc" style="color:{m['color']}">{m['acc']}</div>
            <div class="model-err">{m['err']}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown("**ℹ️ About**")
    st.markdown('<p style="font-size:0.82rem; color:#94a3b8; line-height:1.6;">AI-powered chatbot trained on college admission FAQs. Switch models to compare performance.</p>', unsafe_allow_html=True)
# ---------------- MAIN HEADER ----------------
st.markdown('<div class="main-title">🎓 College Admission AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Your intelligent guide to college admissions & recommendations</div>', unsafe_allow_html=True)

# ---------------- TABS ----------------
tab1, tab2 = st.tabs(["💬  AI Chatbot", "🎯  College Advisor"])

# ================= CHATBOT TAB =================
with tab1:
    st.markdown('<div class="section-header">💬 Ask Me Anything</div>', unsafe_allow_html=True)

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Model selector + input in columns
    col_inp, col_model, col_btn = st.columns([4, 2, 1])

    with col_inp:
        user_input = st.text_input(
            label="user_input_label",
            placeholder="e.g. What is the fee structure? What are the hostel facilities?",
            label_visibility="collapsed"
        )

    with col_model:
        model_choice = st.selectbox(
            label="model_select_label",
            options=["Naive Bayes", "Logistic Regression", "SVM"],
            label_visibility="collapsed"
        )

    with col_btn:
        ask_clicked = st.button("Ask →", use_container_width=True)

    if ask_clicked:
        if user_input.strip():
            model = select_model(model_choice)
            response = get_response(user_input, model)
            st.session_state.chat_history.append(("user", user_input))
            st.session_state.chat_history.append(("bot", response))
        else:
            st.warning("Please enter a question before clicking Ask.")

    # Render chat history
    if st.session_state.chat_history:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        for role, msg in st.session_state.chat_history:
            if role == "user":
                st.markdown(f'<div class="chat-label" style="text-align:right">You</div>'
                            f'<div class="chat-user">{msg}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-label">🤖 Assistant ({model_choice})</div>'
                            f'<div class="chat-bot">{msg}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()
    else:
        st.markdown("""
        <div class="card" style="text-align:center; padding: 2.5rem; color:#64748b;">
            <div style="font-size:2.5rem; margin-bottom:0.5rem">💬</div>
            <div style="font-size:1rem; font-weight:500;">Start the conversation above!</div>
            <div style="font-size:0.85rem; margin-top:0.3rem;">Ask about fees, admissions, hostel, branches, and more.</div>
        </div>
        """, unsafe_allow_html=True)

# ================= COLLEGE ADVISOR TAB =================
with tab2:
    st.markdown('<div class="section-header">🎯 Find Your Best-Fit College</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        marks = st.slider("📈 Your Marks / Percentile", 0, 100, 75)
        location = st.selectbox(
            "📍 Preferred Location",
            ["Any"] + sorted(college_df['location'].unique().tolist())
        )

    with col2:
        branch = st.selectbox(
            "🔬 Preferred Branch",
            ["Any"] + sorted(college_df['branch'].unique().tolist())
        )
        budget = st.number_input("💰 Max Annual Budget (₹)", min_value=0, value=200000, step=10000)

    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🔍 Get Recommendations"):
        results = recommend_colleges(marks, location, branch, budget)

        if not results.empty:
            st.markdown('<div class="section-header" style="margin-top:1rem">✅ Recommended Colleges</div>', unsafe_allow_html=True)
            st.dataframe(
                results.reset_index(drop=True),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.warning("⚠️ No colleges found matching your criteria. Try relaxing your filters.")


