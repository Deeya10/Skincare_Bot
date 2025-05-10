from dotenv import load_dotenv
from openai import OpenAI
import pandas as pd
import shelve
import streamlit as stream
import os
import time

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


stream.title("SlayBot")

USER_AVATAR = "user"
BOT_AVATAR = "Bot"

def load_chat_history():
    with shelve.open("chat_history") as db:
        return db.get("messages", [])

def save_chat_history(messages):
    with shelve.open("chat_history") as db:
        db["messages"] = messages

if "messages" not in stream.session_state:
    stream.session_state.messages = load_chat_history()

with stream.sidebar:
    if stream.button("Delete Chat History"):
        stream.session_state.messages = []
        save_chat_history([])
        stream.session_state.skin_type = None

# Initial message displayed 
if len(stream.session_state.messages) == 0:
    welcome = (
        "I'm here to help you with your skincare needs. "
        "Please select your skin type so I can provide you with personalized recommendations."
    )
    stream.session_state.messages.append({"role": "assistant", "content": welcome})

# Display chat history | Method called later during main chat 
for msg in stream.session_state.messages:
    with stream.chat_message(USER_AVATAR if msg["role"] == "user" else BOT_AVATAR):
        stream.markdown(msg["content"])

# Letting user select the skin type 
if "user_profile_completed" not in stream.session_state:
    stream.session_state.user_profile_completed = False

if not stream.session_state.user_profile_completed:
    stream.subheader("Let's get to know your skin better!")

    skin_type = stream.selectbox("What is your skin type?", ["Oily", "Dry", "Combination", "Normal", "Sensitive"])
    age_range = stream.selectbox("Your age range:", ["<20", "20–30", "30–40", "40+"])
    concern = stream.selectbox("What is your main skin concern?", ["Acne", "Dryness", "Wrinkles", "Dark spots", "Redness", "Other"])
    routine_time = stream.selectbox("Preferred skincare routine time?", ["Morning", "Evening", "Both"])
    budget = stream.selectbox("What is your skincare budget?", ["Low", "Medium", "High"])
    preferences = stream.multiselect("Product preferences (optional):", ["Fragrance-free", "Vegan", "Cruelty-free", "Alcohol-free"])

    if stream.button("Submit"):
        stream.session_state.skin_type = skin_type
        stream.session_state.age = age_range
        stream.session_state.concern = concern
        stream.session_state.routine_time = routine_time
        stream.session_state.budget = budget
        stream.session_state.preferences = preferences
        stream.session_state.User_profile_completed = True


        # Update the profile display
        stream.subheader("Here's your profile:")
        stream.markdown(f"**Skin Type:** {stream.session_state.skin_type}")
        stream.markdown(f"**Age Range:** {stream.session_state.age}")
        stream.markdown(f"**Main Concern:** {stream.session_state.concern}")
        stream.markdown(f"**Routine Time:** {stream.session_state.routine_time}")
        stream.markdown(f"**Budget:** {stream.session_state.budget}")
        stream.markdown(f"**Preferences:** {', '.join(stream.session_state.preferences)}")
        # stream.session_state.messages.append({"role": "user", "content": f"My skin type is {skin_type}, age {age_range}, concern: {concern}"})
        # stream.session_state.messages.append({"role": "assistant", "content": "Thanks! I’ve noted your preferences. Let me know how I can help you today."})
        save_chat_history(stream.session_state.messages)

        # Display the "How can I help you?" chat bubble after profile is shown
        #stream.text_input("How can I help you?")  # Placeholder for the user's next message

        # stream.rerun()

# Main Chat Logic
# if stream.session_state.user_profile_completed:
    # Main chat input logic
    # stream.text_input("How can I help you?")
    if prompt := stream.chat_input("How can I help you?"):
        stream.session_state.messages.append({"role": "user", "content": prompt})
        with stream.chat_message("user"):
            stream.markdown(prompt)    

        # Construct prompt with user profile
        full_prompt = (
            f"You are a helpful skincare advisor called SlayBot.\n\n"
            f"User Profile:\n"
            f"- Skin Type: {stream.session_state.skin_type}\n"
            f"- Age: {stream.session_state.age}\n"
            f"- Concern: {stream.session_state.concern}\n"
            f"- Routine Time: {stream.session_state.routine_time}\n"
            f"- Budget: {stream.session_state.budget}\n"
            f"- Preferences: {', '.join(stream.session_state.preferences)}\n\n"
        )

        for msg in stream.session_state.messages:
            role = "User" if msg["role"] == "user" else "Assistant"
            full_prompt += f"{role}: {msg['content']}\n"
        full_prompt += "Assistant:"

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": full_prompt}],
                max_tokens=500,
                temperature=0.7,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            assistant_reply = response.choices[0].message.content.strip()

            # with stream.chat_message("assistant"):
            #     message_placeholder = stream.empty()
            #     message_placeholder.markdown("SlayBot is thinking...")
            #     time.sleep(1.5)
            #     message_placeholder.markdown(assistant_reply)

            stream.session_state.messages.append({"role": "assistant", "content": assistant_reply})
            save_chat_history(stream.session_state.messages)

        except Exception as e:
            stream.error(f"Error generating response: {e}")