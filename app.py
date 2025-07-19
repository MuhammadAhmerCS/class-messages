import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Secret Class Messages", layout="centered")
st.title("💌 Secret Class Messages")

# --- List of classmates (example: add all 30) ---
students = ["Aarav", "Bela", "Chirag", "Divya", "Eshan", "Farah", "Gautam", "Heena"]

# --- Secret codes for each student (private) ---
codes = {
    "Aarav": "1234",
    "Bela": "5678",
    "Chirag": "abcd",
    "Divya": "4444",
    "Eshan": "5555",
    "Farah": "6666",
    "Gautam": "7777",
    "Heena": "8888"
}

# --- Message Form ---
st.header("✍️ Send a Message")
sender = st.text_input("Your Name (or leave blank for anonymous)", key="sender")
receiver = st.selectbox("Choose a classmate to send a message to:", students, key="receiver")
message = st.text_area("Write your message here", key="message")

if st.button("Send Message"):
    if not message.strip():
        st.warning("⚠️ Please write something before sending.")
    else:
        new_msg = pd.DataFrame([[receiver, sender, message]], columns=["To", "From", "Message"])
        if os.path.exists("messages.csv"):
            old_msgs = pd.read_csv("messages.csv")
            all_msgs = pd.concat([old_msgs, new_msg], ignore_index=True)
        else:
            all_msgs = new_msg
        all_msgs.to_csv("messages.csv", index=False)
        st.success(f"✅ Message sent to {receiver}!")

# --- Divider ---
st.markdown("---")

# --- View Messages ---
st.header("🔐 View Your Messages")

col1, col2 = st.columns(2)
with col1:
    name_input = st.text_input("Your Name", key="name_input")
with col2:
    code_input = st.text_input("Your Secret Code", type="password", key="code_input")

if st.button("Unlock My Messages"):
    if codes.get(name_input) == code_input:
        try:
            df = pd.read_csv("messages.csv")
            my_msgs = df[df["To"].str.lower() == name_input.lower()]
            if not my_msgs.empty:
                st.success(f"📬 Found {len(my_msgs)} message(s) for {name_input}")
                for i, row in my_msgs.iterrows():
                    st.markdown(f"**From:** {row['From'] or 'Anonymous'}")
                    st.info(row["Message"])
            else:
                st.warning("😔 No messages found for you yet.")
        except FileNotFoundError:
            st.error("📂 No message file found yet. Be the first to send one!")
    else:
        st.error("🚫 Incorrect name or secret code.")
