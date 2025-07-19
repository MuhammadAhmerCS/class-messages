import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Secret Class Messages", layout="centered")
st.title("💌 Secret Class Messages")

# --- List of classmates (edit this with your full class list) ---
students = ["Aarav", "Bela", "Chirag", "Divya", "Eshan", "Farah", "Gautam", "Heena"]

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

# --- View Messages With Self-Set Secret Code ---
st.header("🔐 View Your Messages")

your_name = st.text_input("Your Name", key="view_name")
code_entered = st.text_input("Enter your secret code (or create one)", type="password", key="view_code")

if st.button("Access Messages"):
    # Load or create code storage file
    if os.path.exists("user_codes.csv"):
        codes_df = pd.read_csv("user_codes.csv")
    else:
        codes_df = pd.DataFrame(columns=["Name", "Code"])

    # Check if user already set a code
    existing = codes_df[codes_df["Name"].str.lower() == your_name.lower()]

    if existing.empty:
        # First time user — create new code
        if code_entered:
            new_code = pd.DataFrame([[your_name, code_entered]], columns=["Name", "Code"])
            codes_df = pd.concat([codes_df, new_code], ignore_index=True)
            codes_df.to_csv("user_codes.csv", index=False)
            st.success("✅ Secret code created! You can now view your messages.")
        else:
            st.warning("Please enter a secret code to register.")
    else:
        # Returning user — check if code matches
        real_code = str(existing.iloc[0]["Code"])
        if code_entered == real_code:
            try:
                df = pd.read_csv("messages.csv")
                personal_msgs = df[df["To"].str.lower() == your_name.lower()]
                if not personal_msgs.empty:
                    st.success(f"📬 Found {len(personal_msgs)} message(s) for {your_name}")
                    for _, row in personal_msgs.iterrows():
                        st.markdown(f"**From:** {row['From'] or 'Anonymous'}")
                        st.info(row["Message"])
                else:
                    st.warning("😔 No messages found for you yet.")
            except FileNotFoundError:
                st.error("No messages have been sent yet.")
        else:
            st.error("🚫 Incorrect secret code.")
