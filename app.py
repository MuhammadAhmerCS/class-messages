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
        # First time user — show info and register
        if code_entered:
            new_code = pd.DataFrame([[your_name, code_entered]], columns=["Name", "Code"])
            codes_df = pd.concat([codes_df, new_code], ignore_index=True)
            codes_df.to_csv("user_codes.csv", index=False)
            st.success("🔐 Secret code created!")
            st.info("✅ You’ve now locked your inbox. Only YOU can view your messages.")
        else:
            st.info("🔒 First time here? Set a secret password to protect your messages so no one else can view them.")
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
