import streamlit as st
import pandas as pd
import os

st.title("💌 Secret Class Messages")

# --- List of classmates ---
students = ["Aarav", "Bela", "Chirag", "Divya", "Eshan", "Farah", "Gautam", "Heena"]  # Add your 30 names here

# --- Message Form ---
st.subheader("✍️ Send a message to a classmate")

sender = st.text_input("Your Name (can be anonymous)")
receiver = st.selectbox("Choose a classmate to send a message to:", students)
message = st.text_area("Write your message here")

if st.button("Send Message"):
    if not message:
        st.warning("Please write a message before sending.")
    else:
        # Save message to CSV
        new_msg = pd.DataFrame([[receiver, sender, message]], columns=["To", "From", "Message"])
        if os.path.exists("messages.csv"):
            old = pd.read_csv("messages.csv")
            all_msgs = pd.concat([old, new_msg], ignore_index=True)
        else:
            all_msgs = new_msg
        all_msgs.to_csv("messages.csv", index=False)
        st.success("✅ Your message has been sent anonymously!")
