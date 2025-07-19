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
# --- View Messages ---
st.markdown("---")
st.subheader("🔐 View Messages Sent to You")

your_name = st.text_input("Enter your name to view your messages")

if st.button("Show My Messages"):
    try:
        df = pd.read_csv("messages.csv")
        my_msgs = df[df["To"].str.lower() == your_name.lower()]

        if not my_msgs.empty:
            for i, row in my_msgs.iterrows():
                st.markdown(f"📨 **From:** {row['From'] or 'Anonymous'}")
                st.info(row["Message"])
        else:
            st.warning("😔 No messages found for you yet.")
    except FileNotFoundError:
        st.error("No messages have been sent yet.")
# Add this near the 'view messages' section
codes = {"Aarav": "1234", "Bela": "5678", "Chirag": "abcd"}  # Add your class here

name = st.text_input("Your Name")
code = st.text_input("Your Secret Code", type="password")

if st.button("Unlock My Messages"):
    if codes.get(name) == code:
        # Show messages as before
        ...
    else:
        st.error("Incorrect code.")

