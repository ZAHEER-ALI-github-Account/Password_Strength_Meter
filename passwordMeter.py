import streamlit as st
import re
import random
import string
import pyperclip  # For copying to clipboard

# Custom CSS for styling
st.markdown("""
    <style>
    .stProgress > div > div > div > div {
        background-color: #4CAF50;
    }
    .stTextInput > div > div > input {
        border-radius: 10px;
        padding: 10px;
    }
    .stButton > button {
        border-radius: 10px;
        padding: 10px 20px;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
    .stMarkdown {
        font-family: 'Arial', sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

# Function to calculate password strength
def calculate_strength(password):
    strength = 0
    suggestions = []

    # Check length
    if len(password) >= 8:
        strength += 1
    else:
        suggestions.append("🔒 Use at least 8 characters.")

    # Check for uppercase letters
    if re.search(r'[A-Z]', password):
        strength += 1
    else:
        suggestions.append("🔠 Add uppercase letters.")

    # Check for lowercase letters
    if re.search(r'[a-z]', password):
        strength += 1
    else:
        suggestions.append("🔡 Add lowercase letters.")

    # Check for numbers
    if re.search(r'[0-9]', password):
        strength += 1
    else:
        suggestions.append("🔢 Include numbers.")

    # Check for special characters
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        strength += 1
    else:
        suggestions.append("🔣 Add special characters (!@#$%^&*).")

    return strength, suggestions

# Function to generate a strong password
def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

# Function to display strength meter
def display_strength_meter(strength):
    strength_labels = {
        0: "Very Weak 😱",
        1: "Weak 😟",
        2: "Moderate 😐",
        3: "Strong 😊",
        4: "Very Strong 😎",
        5: "Excellent! 🔥"
    }
    progress = strength / 5
    st.progress(progress)
    st.write(f"**Strength:** {strength_labels.get(strength, 'Unknown')}")

# Streamlit App
def main():
    st.title("🔐 Password Strength Meter")
    st.markdown("Check how strong your password is and get tips to make it stronger!")

    # Dark/Light Mode Toggle
    dark_mode = st.checkbox("🌙 Dark Mode")
    if dark_mode:
        st.markdown("""
            <style>
            .stApp {
                background-color: #1e1e1e;
                color: white;
            }
            </style>
            """, unsafe_allow_html=True)

    # Input field for password
    password = st.text_input("Enter your password:", type="password")

    # Password Generator
    if st.button("🎲 Generate Strong Password"):
        generated_password = generate_password()
        st.text_input("Generated Password:", generated_password)
        if st.button("📋 Copy to Clipboard"):
            pyperclip.copy(generated_password)
            st.success("Copied to clipboard!")

    if password:
        strength, suggestions = calculate_strength(password)
        display_strength_meter(strength)

        if strength < 5:
            st.markdown("### 💡 Suggestions to Improve Your Password:")
            for suggestion in suggestions:
                st.write(suggestion)
        else:
            st.balloons()  # Celebrate if the password is excellent
            st.success("🎉 Your password is strong and secure!")

    # Password History (stored in session state)
    if "password_history" not in st.session_state:
        st.session_state.password_history = []

    if password:
        st.session_state.password_history.append(password)
        st.markdown("### 📜 Password History")
        for idx, pwd in enumerate(st.session_state.password_history[-5:], 1):
            st.write(f"{idx}. {pwd}")

    # Additional Tips Section
    st.markdown("### 📚 Tips for Creating Strong Passwords")
    st.write("""
    - Use a mix of uppercase and lowercase letters.
    - Include numbers and special characters.
    - Avoid using common words or phrases.
    - Make your password at least 12 characters long.
    - Use a passphrase (e.g., `MyDogLoves2Run!`).
    """)

# Run the app
if __name__ == "__main__":
    main()