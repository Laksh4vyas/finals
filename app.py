"""

import streamlit as st
import pickle
import json
import random
import pandas as pd
import re

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="College Admission System", layout="wide")

# ---------------- LOAD MODELS ----------------
nb_model = pickle.load(open('models/nb.pkl', 'rb'))
lr_model = pickle.load(open('models/lr.pkl', 'rb'))
svm_model = pickle.load(open('models/svm.pkl', 'rb'))
vectorizer = pickle.load(open('models/vectorizer.pkl', 'rb'))

# ---------------- LOAD DATA ----------------
with open('data.json') as f:
    data = json.load(f)

college_df = pd.read_csv("colleges.csv")

# clean column names
college_df.columns = college_df.columns.str.strip().str.lower()

# ---------------- CLEAN HTML ----------------
def clean_response(text):
    return re.sub('<.*?>', '', text)

# ---------------- CHATBOT ----------------
def get_response(user_input, model):
    input_vec = vectorizer.transform([user_input])
    tag = model.predict(input_vec)[0]

    for intent in data['intents']:
        if intent['tag'] == tag:
            return clean_response(random.choice(intent['responses']))

    return "Sorry, I didn't understand."

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
    df = college_df.copy()

    # ✅ FIXED COLUMN NAME
    df = df[df['avg_cutoff'] <= marks]

    if location != "Any":
        df = df[df['location'] == location]

    if branch != "Any":
        df = df[df['branch'] == branch]

    df = df[df['fees'] <= budget]

    return df.head(5)

# ---------------- SIDEBAR ----------------
st.sidebar.title("📊 Model Dashboard")

# 👉 Replace with your real values
# load accuracies
with open("models/accuracy.json") as f:
    acc_data = json.load(f)

nb_acc = acc_data["nb"]
lr_acc = acc_data["lr"]
svm_acc = acc_data["svm"]

st.sidebar.metric("Naive Bayes", f"{nb_acc*100:.2f}%")
st.sidebar.metric("Logistic Regression", f"{lr_acc*100:.2f}%")
st.sidebar.metric("SVM", f"{svm_acc*100:.2f}%")

st.sidebar.success("Best Model: SVM")

# ---------------- MAIN UI ----------------
st.title("🎓 College Admission System")
st.caption("Chatbot + College Recommendation")

# ---------------- TABS ----------------
tab1, tab2 = st.tabs(["💬 Chatbot", "🎯 College Advisor"])

# ================= CHATBOT =================
with tab1:
    st.subheader("Ask Questions")

    col1, col2 = st.columns([3,1])

    with col1:
        user_input = st.text_input("Enter your question")

    with col2:
        model_choice = st.selectbox(
            "Model",
            ["Naive Bayes", "Logistic Regression", "SVM"]
        )

    if st.button("Ask"):
        if user_input.strip():
            model = select_model(model_choice)
            response = get_response(user_input, model)

            st.chat_message("user").write(user_input)
            st.chat_message("assistant").write(response)
        else:
            st.warning("Please enter a question")

# ================= COLLEGE ADVISOR =================
with tab2:
    st.subheader("Find Colleges")

    col1, col2 = st.columns(2)

    with col1:
        marks = st.slider("Marks / Percentile", 0, 100, 75)
        location = st.selectbox(
            "Location",
            ["Any"] + sorted(college_df['location'].unique())
        )

    with col2:
        branch = st.selectbox(
            "Branch",
            ["Any"] + sorted(college_df['branch'].unique())
        )
        budget = st.number_input("Budget (₹)", value=200000)

    if st.button("Get Colleges"):
        results = recommend_colleges(marks, location, branch, budget)

        if not results.empty:
            st.success("Recommended Colleges")
            st.dataframe(results)
        else:
            st.warning("No matching colleges found")


"""






import streamlit as st
import pickle
import json
import random
import pandas as pd
import re
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="College Admission System", layout="wide")

# ---------------- BASE DIR ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------------- LOAD MODELS ----------------
@st.cache_resource
def load_models():
    nb_model = pickle.load(open(os.path.join(BASE_DIR, "models/nb.pkl"), "rb"))
    lr_model = pickle.load(open(os.path.join(BASE_DIR, "models/lr.pkl"), "rb"))
    svm_model = pickle.load(open(os.path.join(BASE_DIR, "models/svm.pkl"), "rb"))
    vectorizer = pickle.load(open(os.path.join(BASE_DIR, "models/vectorizer.pkl"), "rb"))
    return nb_model, lr_model, svm_model, vectorizer

nb_model, lr_model, svm_model, vectorizer = load_models()

# ---------------- LOAD DATA ----------------
with open(os.path.join(BASE_DIR, "data.json")) as f:
    data = json.load(f)

college_df = pd.read_csv(os.path.join(BASE_DIR, "colleges.csv"))
college_df.columns = college_df.columns.str.strip().str.lower()

# ---------------- CLEAN TEXT ----------------
def clean_response(text):
    return re.sub('<.*?>', '', text)

# ---------------- CHATBOT ----------------
def get_response(user_input, model):
    input_vec = vectorizer.transform([user_input])
    tag = model.predict(input_vec)[0]

    for intent in data['intents']:
        if intent['tag'] == tag:
            return clean_response(random.choice(intent['responses']))

    return "Sorry, I didn't understand."

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
    df = college_df.copy()

    df = df[df['avg_cutoff'] <= marks]

    if location != "Any":
        df = df[df['location'] == location]

    if branch != "Any":
        df = df[df['branch'] == branch]

    df = df[df['fees'] <= budget]

    return df.head(5)

# ---------------- SIDEBAR ----------------
st.sidebar.title("📊 Model Dashboard")

with open(os.path.join(BASE_DIR, "models/accuracy.json")) as f:
    acc_data = json.load(f)

st.sidebar.metric("Naive Bayes", f"{acc_data['nb']*100:.2f}%")
st.sidebar.metric("Logistic Regression", f"{acc_data['lr']*100:.2f}%")
st.sidebar.metric("SVM", f"{acc_data['svm']*100:.2f}%")

st.sidebar.success("Best Model: SVM")

# ---------------- MAIN UI ----------------
st.title("🎓 College Admission System")
st.caption("Chatbot + College Recommendation")

tab1, tab2 = st.tabs(["💬 Chatbot", "🎯 College Advisor"])

# ================= CHATBOT =================
with tab1:
    st.subheader("Ask Questions")

    col1, col2 = st.columns([3, 1])

    with col1:
        user_input = st.text_input("Enter your question")

    with col2:
        model_choice = st.selectbox(
            "Model",
            ["Naive Bayes", "Logistic Regression", "SVM"]
        )

    if st.button("Ask"):
        if user_input.strip():
            model = select_model(model_choice)
            response = get_response(user_input, model)

            st.chat_message("user").write(user_input)
            st.chat_message("assistant").write(response)
        else:
            st.warning("Please enter a question")

# ================= COLLEGE ADVISOR =================
with tab2:
    st.subheader("Find Colleges")

    col1, col2 = st.columns(2)

    with col1:
        marks = st.slider("Marks / Percentile", 0, 100, 75)
        location = st.selectbox(
            "Location",
            ["Any"] + sorted(college_df['location'].unique())
        )

    with col2:
        branch = st.selectbox(
            "Branch",
            ["Any"] + sorted(college_df['branch'].unique())
        )
        budget = st.number_input("Budget (₹)", value=200000)

    if st.button("Get Colleges"):
        results = recommend_colleges(marks, location, branch, budget)

        if not results.empty:
            st.success("Recommended Colleges")
            st.dataframe(results)
        else:
            st.warning("No matching colleges found")