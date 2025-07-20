import streamlit as st
import pandas as pd
import os

# --- Config ---
st.set_page_config(page_title="Secret Class Messages", layout="centered")
st.title("💌 Secret Class Messages")

st.markdown("""
Welcome to your class's secret message wall!  
Here, you can:
- ✨ Send **anonymous messages** to your classmates  
- 🔐 Create a **private inbox** that only **you** can unlock  
---
""")

# --- Classmate List ---
students = ["Aarav", "Bela", "Chirag", "Divya", "Eshan", "Farah", "Gautam", "Heena"]  # Customize this

# --- Section: Create Private Inbox ---
st.header("🔐 Step 1: Set Your Private Inbox Password")

st.markdown("**Create your own secret password. Only you will know it. No one else — not even the sender — can access your messages.**")

name_for_code = st.text_input("Enter Your Name", key="name_for_code")
new_password = st.text_input("Set a Secret Password (only once)", type="password", key="new_password")

if st.button("🔒 Lock My Inbox"):
    if name_for_code and new_password:
        if os.path.exists("user_codes.csv"):
            codes_df = pd.read_csv("user_codes.csv")
        else:
            codes_df = pd.DataFrame(columns=["Name", "Code"])

        existing_user = codes_df[codes_df["Name"].str.lower() == name_for_code.lower()]

        if not existing_user.empty:
            st.warning("🔐 You already set a password. Try viewing your messages below.")
        else:
            new_code = pd.DataFrame([[name_for_code, new_password]], columns=["Name", "Code"])
            codes_df = pd.concat([codes_df, new_code], ignore_index=True)
            codes_df.to_csv("user_codes.csv", index=False)
            st.success("✅ Your inbox is locked. Only you can open it now.")
    else:
        st.warning("Please enter both name and password.")

st.markdown("---")

# --- Section: Send Message ---
st.header("✍️ Step 2: Send a Secret Message")

st.markdown("You can send a message to anyone in your class. Your name is **optional**. If you leave it blank, it stays anonymous forever.")

sender = st.text_input("Your Name (leave blank to stay anonymous)", key="sender_name")
receiver = st.selectbox("Choose a classmate to send a message to:", students)
message = st.text_area("Write your message here")

if st.button("📤 Send Message"):
    if not message.strip():
        st.warning("⚠️ You must write something!")
    else:
        new_msg = pd.DataFrame([[receiver, sender, message]], columns=["To", "From", "Message"])
        if os.path.exists("messages.csv"):
            old_msgs = pd.read_csv("messages.csv")
            all_msgs = pd.concat([old_msgs, new_msg], ignore_index=True)
        else:
            all_msgs = new_msg
        all_msgs.to_csv("messages.csv", index=False)
        st.success(f"✅ Your anonymous message was sent to {receiver}!")

st.markdown("---")

# --- Section: View Messages ---
st.header("📬 Step 3: View Your Private Inbox")

st.markdown("Enter your name and secret password to access messages sent only to you.")

your_name = st.text_input("Your Name", key="inbox_name")
code_entered = st.text_input("Enter Your Secret Password", type="password", key="inbox_code")

if st.button("📥 Unlock My Inbox"):
    if os.path.exists("user_codes.csv"):
        codes_df = pd.read_csv("user_codes.csv")
        user_row = codes_df[codes_df["Name"].str.lower() == your_name.lower()]

        if not user_row.empty:
            saved_code = str(user_row.iloc[0]["Code"])
            if code_entered == saved_code:
                # Show messages
                try:
                    df = pd.read_csv("messages.csv")
                    personal_msgs = df[df["To"].str.lower() == your_name.lower()]
                    if not personal_msgs.empty:
                        st.success(f"📫 You have {len(personal_msgs)} message(s):")
                        for _, row in personal_msgs.iterrows():
                            st.markdown(f"**From:** {row['From'] or 'Anonymous'}")
                            st.info(row["Message"])
                    else:
                        st.warning("😔 No messages found for you yet.")
                except FileNotFoundError:
                    st.warning("No messages have been sent yet.")
            else:
                st.error("🚫 Incorrect password. Please try again.")
        else:
            st.error("❌ No inbox found for that name. Please set it up above.")
    else:
        st.warning("🔐 No inboxes exist yet. Be the first to create one!")
