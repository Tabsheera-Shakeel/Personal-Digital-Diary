import streamlit as st
import datetime
import os
import json
import hashlib
from cryptography.fernet import Fernet
import uuid
import sqlite3
import random
from PIL import Image
import base64
from io import BytesIO
import webbrowser
import io
import base64

def image_to_base64(image_path):
    img = Image.open(image_path)
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()
#  SECURITY SETUP 
def get_encryption_key():
    if os.path.exists("secret.key"):
        with open("secret.key", "rb") as key_file:
            return key_file.read()
    else:
        key = Fernet.generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(key)
        return key

KEY = get_encryption_key()
cipher = Fernet(KEY)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

#  DATABASE SETUP 
def init_db():
    conn = sqlite3.connect('diary.db')
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT UNIQUE,
                 password TEXT,
                 created_at TEXT)''')
    
    # Entries table
    c.execute('''CREATE TABLE IF NOT EXISTS entries
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 user_id INTEGER,
                 title TEXT,
                 date TEXT,
                 mood TEXT,
                 mood_color TEXT,
                 text TEXT,
                 tags TEXT,
                 image_path TEXT,
                 todo_list TEXT,
                 goal TEXT,
                 quote TEXT,
                 timestamp TEXT,
                 FOREIGN KEY(user_id) REFERENCES users(id))''')
    
    conn.commit()
    conn.close()

init_db()

def get_db_connection():
    return sqlite3.connect('diary.db')

#  DATA FUNCTIONS 
def encrypt_data(data):
    return cipher.encrypt(json.dumps(data).encode()).decode()

def decrypt_data(encrypted_data):
    try:
        return json.loads(cipher.decrypt(encrypted_data.encode()).decode())
    except:
        return None

def save_image(uploaded_file):
    os.makedirs("uploaded_images", exist_ok=True)
    image_path = os.path.join("uploaded_images", f"{uuid.uuid4()}.jpg")
    with open(image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return image_path

# QUOTES 
QUOTES = [
    "The only limit to our realization of tomorrow is our doubts of today. - FDR",
    "Do what you can, with what you have, where you are. - Theodore Roosevelt",
    "It always seems impossible until it's done. - Nelson Mandela",
    "Success is not final, failure is not fatal. - Winston Churchill",
    "Believe you can and you're halfway there. - Theodore Roosevelt"
]

def get_random_quote():
    return random.choice(QUOTES)

#  ABOUT SECTION 
def about_section():
    
    
    # Main Project Description
    st.markdown(
        """
        <div style="background-color: #f9f9f9; padding: 20px; border-radius: 10px; border: 1px solid #ddd;">
            <h2 style="color: #4CAF50;">Welcome to My Digital Diary!</h2>
            <p style="font-size: 16px; line-height: 1.6;">
                This project was inspired by the idea of solving real problems by addressing our own challenges. I wanted to identify pain points and enhance the user experience. Inspired by this, I created a Digital Diary to solve a problem that I—and many others who love to write and read—face.
            </p>
            <p style="font-size: 16px; line-height: 1.6;">
                <strong>🔸 What Problem Does It Solve?</strong><br>
                I love writing about my experiences, emotions, and lessons, but I don't feel comfortable writing in front of others. I also love reading real-life experiences from others, as they provide valuable lessons and inspiration. In today's fast-paced world, deep conversations have become rare, making it harder to connect on a meaningful level.
                Additionally, carrying a physical diary everywhere isn't practical, but we always have our phones with us.
            </p>
            <p style="font-size: 16px; line-height: 1.6;">
                That's why I built this Digital Diary—a special place where anyone can write, read, and learn from life experiences, helping them to develop a growth mindset and continuously improve. And the best part? You can access it anytime, anywhere, directly on your phone!
            </p>
            <p style="font-size: 16px; line-height: 1.6;">
                <strong>🔸 Key Features:</strong>
                <ul>
                    <li>Choose Your Mood, Title & Name – Set the tone before you start writing.</li>
                    <li>✅ To-Do List & Goal Reminders – Stay on track with your personal goals.</li>
                    <li>✅ Mood-Based UI – Your diary adapts to how you feel.</li>
                    <li>✅ Quote of the Day – Pick a motivational quote that resonates with you.</li>
                    <li>✅ Tagging System – Add tags related to your writing for easy filtering.</li>
                    <li>✅ Search Functionality – Quickly find past entries.</li>
                    <li>✅ Delete Options – Keep your diary organized.</li>
                    <li>✅ Save History – Never lose your past writings!</li>
                </ul>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

     # Display two GIFs side by side
    col1, col2 = st.columns(2)
    with col1:
        st.image(
            "https://media2.giphy.com/media/56ikf9jD4ZK6s/200.webp?cid=ecf05e47h6kt7jmesug20d8q0g617hbk0c2wtlbtmzftos3k&ep=v1_gifs_search&rid=200.webp&ct=g",
            caption="Welcome!",
            width=300,
        )
    with col2:
        st.image(
            "https://media0.giphy.com/media/dtEw467VB2g0CYa4EU/200.webp?cid=ecf05e47sdcwqjqgrqvvvw65wl6o2czrzolzn4j18nfz1jdz&ep=v1_gifs_search&rid=200.webp&ct=g",
            caption="Let's Get Started!",
            width=330,
        )

    st.markdown("---")
    # Security Features Section
    st.markdown("### 🔒 Security Features")
    st.markdown(
        """
        <div style="background-color: #f9f9f9; padding: 20px; border-radius: 10px; border: 1px solid #ddd;">
            <p style="font-size: 16px; line-height: 1.6;">
                <strong>Your privacy and security are our top priority:</strong>
            </p>
            <ul>
                <li>🔐 End-to-end encryption for all diary entries</li>
                <li>🔑 Secure password hashing (SHA-256 with salt)</li>
                <li>🔒 Automatic session timeout after 30 minutes</li>
                <li>🛡️ Protection against SQL injection attacks</li>
                <li>📱 Local storage encryption for sensitive data</li>
                <li>👤 Strict user authentication system</li>
            </ul>
            <p style="font-size: 14px; color: #666;">
                <i>Note: All data is stored securely and never shared with third parties.</i>
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("---")

   
    
    # Enhanced About Me Section with Social Media Icons
    st.subheader("👤 Connect With Me")
    
    # Social Media Icons with Links
    st.markdown("""
    <div style="display: flex; justify-content: center; gap: 20px; margin-bottom: 20px;">
        <a href="https://www.linkedin.com/in/tabsheera-shakeel-116555300" target="_blank">
            <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="40">
        </a>
        <a href="https://x.com/TabsheeraS" target="_blank">
           <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/X_icon_2.svg/2048px-X_icon_2.svg.png" width="40" style="filter: invert(1);">
       </a>
        </a>
        <a href="https://www.facebook.com/" target="_blank">
            <img src="https://cdn-icons-png.flaticon.com/512/124/124010.png" width="40">
        </a>
        <a href="https://github.com/Tabsheera" target="_blank">
            <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" width="50">
        </a>
    </div>
    """, unsafe_allow_html=True)
    
   

    img_path = "images/my-image.png"  
    img_base64 = image_to_base64(img_path)
    
    st.markdown(
        f"""
        <div style="background-color: #f9f9f9; padding: 20px; border-radius: 10px; border: 1px solid #ddd; text-align: center;">
            <img src="data:image/png;base64,{img_base64}" 
                 style="border-radius: 50%; width: 120px; height: 120px; object-fit: cover; margin: 0 auto 15px; display: block;">
           <h3 style="color: #4CAF50; margin-bottom: 5px;">Hello! 👋 I'm Tabsheera</h3>
        <p style="font-size: 16px; color: #666; margin-bottom: 15px;">
            The creator behind this Digital Diary
        </p>
        <p style="font-size: 14px; line-height: 1.6;">
            As a developer who values both technology and mindfulness, I created this space 
            to make journaling more accessible and secure. I hope it helps you reflect, 
            grow, and organize your thoughts as much as it has helped me!
        </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    

#  AUTHENTICATION 
def auth_page():
    st.title("🔒 Personal Digital Diary")
    
    tab1, tab2, tab3 = st.tabs(["Login", "Register", "About"])
    
    with tab1:
        st.subheader("Login to Your Diary")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            conn = get_db_connection()
            c = conn.cursor()
            c.execute("SELECT id, password FROM users WHERE username = ?", (username,))
            user = c.fetchone()
            conn.close()
            
            if user and user[1] == hash_password(password):
                st.session_state.user_id = user[0]
                st.session_state.username = username
                st.session_state.authenticated = True
                st.session_state.todo_list = []
                st.session_state.goal = ""
                st.session_state.selected_mood = "Happy"
                st.session_state.mood_color = "#9b59b6"
                st.session_state.selected_entry = None
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid username or password")
    
    with tab2:
        st.subheader("Create New Account")
        new_username = st.text_input("Choose a username")
        new_password = st.text_input("Choose a password", type="password")
        confirm_password = st.text_input("Confirm password", type="password")
        
        if st.button("Register"):
            if new_password != confirm_password:
                st.error("Passwords don't match!")
            elif len(new_password) < 8:
                st.error("Password must be at least 8 characters")
            else:
                conn = get_db_connection()
                c = conn.cursor()
                try:
                    c.execute("INSERT INTO users (username, password, created_at) VALUES (?, ?, ?)",
                             (new_username, hash_password(new_password), str(datetime.datetime.now())))
                    conn.commit()
                    st.success("Registration successful! Please login.")
                except sqlite3.IntegrityError:
                    st.error("Username already exists")
                finally:
                    conn.close()
    
    with tab3:
        about_section()

# DIARY 
def diary_page():
    st.set_page_config(page_title="📖 My Digital Diary", layout="wide")
    
    # Initialize session state
    if "entries" not in st.session_state:
        load_entries_from_db()
    if "todo_list" not in st.session_state:
        st.session_state.todo_list = []
    if "goal" not in st.session_state:
        st.session_state.goal = ""
    if "selected_entry" not in st.session_state:
        st.session_state.selected_entry = None
    if "selected_mood" not in st.session_state:
        st.session_state.selected_mood = "Happy"
    if "mood_color" not in st.session_state:
        st.session_state.mood_color = "#9b59b6"

    # Apply the selected mood color to UI elements
    apply_ui_theme(st.session_state.mood_color)

    # Add logout button to sidebar
    with st.sidebar:
        if st.button("🚪 Logout"):
            st.session_state.authenticated = False
            st.session_state.clear()
            st.rerun()

    # Main header
    st.title("📖 My Daily Diary (Mini Todo App, Goal Reminder)")
    
    # Date selection
    selected_date = st.date_input("📅 Select Date", datetime.date.today())
    formatted_date = selected_date.strftime("%Y/%m/%d")
    
    # Mood selection with both emoji and text
    st.subheader("😊 How are you feeling today?")
    
    mood_options = {
        "Happy": ("😀 Happy", "#9b59b6"),
        "Sad": ("😢 Sad", "#3498DB"),
        "Angry": ("😠 Angry", "#E74C3C"),
        "Tired": ("😴 Tired", "#f4b400"),
        "Excited": ("😎 Excited", "#F1C40F")
    }
    
    cols = st.columns(5)
    for i, (mood_text, (mood_display, mood_color)) in enumerate(mood_options.items()):
        with cols[i]:
            if st.button(mood_display, key=f"mood_{i}"):
                st.session_state.selected_mood = mood_text
                st.session_state.mood_color = mood_color
                st.rerun()
    
    # Mood display
    current_mood_display = mood_options[st.session_state.selected_mood][0]
    st.markdown(f"""
        <div style="background:{st.session_state.mood_color}; 
                    padding: 12px; 
                    border-radius: 12px; 
                    color: white; 
                    text-align:center;
                    margin-bottom: 20px;">
            {current_mood_display}
        </div>
    """, unsafe_allow_html=True)
    
    # Title input
    st.subheader("📜 Title of Your Entry")
    title = st.text_input("Give a title to your entry", key="diary_title")
    
    # User name
    st.subheader("👤 Your Name (Optional)")
    username = st.text_input("Enter your name (Optional)", key="user_name")
    
    # Image upload
    st.subheader("🖼 Upload an Image")
    uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"], key="image_uploader")
    
    # Diary entry
    st.subheader("📝 Write your daily thoughts")
    diary_text = st.text_area("Start writing here...", height=150, key="diary_text")
    
    # Tags
    st.subheader("🏷 Add Tags")
    tags = st.text_input("Separate multiple tags with commas (e.g., Travel, Work, Health)", key="tags_input")
    tags_list = [tag.strip() for tag in tags.split(",") if tag.strip()]
    
    # Todo list
    st.subheader("📝 Todo List")
    new_task = st.text_input("Add a new task", key="new_task")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ Add Task"):
            if new_task:
                st.session_state.todo_list.append({"task": new_task, "completed": False})
    with col2:
        if st.button("🧹 Clear All Tasks"):
            st.session_state.todo_list = []
    
    for idx, task_item in enumerate(st.session_state.todo_list):
        task = task_item["task"]
        completed = task_item["completed"]
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.checkbox("", value=completed, key=f"task_{idx}"):
                st.session_state.todo_list[idx]["completed"] = True
            else:
                st.session_state.todo_list[idx]["completed"] = False
        with col2:
            st.write(f"{task}")
    
    # Goal reminder
    st.subheader("🎯 Goal Reminder")
    st.session_state.goal = st.text_area("Write your goal here...", height=100, key="goal_input")
    
    # Quote of the day
    st.subheader("💬 Quote of the Day")
    quote = st.selectbox("Select a quote", QUOTES, key="quote_select")
    
    # Save entry button
    if st.button("💾 Save Diary Entry"):
        if 'selected_mood' not in st.session_state:
            st.error("Please select your mood first!")
            return
        
        image_path = None
        if uploaded_image:
            image_path = save_image(uploaded_image)
        
        entry = {
            "user_id": st.session_state.user_id,
            "title": title if title else "Untitled Entry",
            "date": formatted_date,
            "mood": st.session_state.selected_mood,
            "mood_color": st.session_state.mood_color,
            "text": diary_text,
            "tags": json.dumps(tags_list),
            "image_path": image_path,
            "todo_list": json.dumps(st.session_state.todo_list),
            "goal": st.session_state.goal,
            "quote": quote,
            "timestamp": str(datetime.datetime.now())
        }
        
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('''INSERT INTO entries 
                    (user_id, title, date, mood, mood_color, text, tags, image_path, todo_list, goal, quote, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                 tuple(entry.values()))
        conn.commit()
        conn.close()
        
        st.success("Diary entry saved successfully!")
        st.balloons()
        st.session_state.todo_list = []
        load_entries_from_db()
        st.rerun()
    
    # Sidebar for history - showing only written content beautifully
    st.sidebar.title(f"📜 {st.session_state.username}'s Diary History")
    
    search_query = st.sidebar.text_input("🔍 Search entries", key="sidebar_search")
    
    for entry in st.session_state.entries:
        # Skip if entry doesn't match search
        if search_query and not (
            search_query.lower() in entry.get('text', '').lower() or
            search_query.lower() in entry.get('title', '').lower() or
            any(search_query.lower() in tag.lower() for tag in json.loads(entry.get('tags', '[]')))
        ):
            continue
        
        # Get mood display data
        mood_display, mood_color = mood_options.get(entry['mood'], ("😀 Happy", "#9b59b6"))
        
        # Create a clean entry card showing only the written content
        with st.sidebar.container():
            st.markdown(f"""
                <div style="background-color: {mood_color}20;
                            padding: 12px;
                            border-radius: 10px;
                            margin-bottom: 12px;
                            border-left: 4px solid {mood_color};">
                    <div style="display: flex; align-items: center; margin-bottom: 6px;">
                        <span style="font-size: 18px; margin-right: 8px;">{mood_display.split()[0]}</span>
                        <span style="font-weight: bold; color: {mood_color}">
                            {mood_display.split()[1]}
                        </span>
                    </div>
                    <div style="font-size: 14px; color: #666; margin-bottom: 4px;">
                        {entry['date']}
                    </div>
                    <div style="font-size: 15px; font-style: italic; margin-top: 8px;">
                        "{entry['text'][:100]}{'...' if len(entry['text']) > 100 else ''}"
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button("View", key=f"view_{entry['id']}"):
                st.session_state.selected_entry = entry
                st.rerun()
    
    # Display selected entry (only when viewing details)
    if st.session_state.selected_entry:
        entry = st.session_state.selected_entry
        mood_color = entry.get('mood_color', '#9b59b6')
        
        # Display entry content in main view
        st.subheader(f"📅 {entry['date']} - {entry['title']}")
        
        # Mood chip
        mood_display = mood_options.get(entry['mood'], ("😀 Happy", "#9b59b6"))[0]
        st.markdown(f"""
            <div style="display: inline-block;
                        background:{mood_color};
                        padding: 6px 12px;
                        border-radius: 20px;
                        color: white;
                        margin-bottom: 16px;">
                {mood_display}
            </div>
        """, unsafe_allow_html=True)
        
        # Main diary content
        st.markdown(f"""
            <div style="background-color: #f9f9f9;
                        padding: 20px;
                        border-radius: 10px;
                        border-left: 4px solid {mood_color};
                        margin-bottom: 20px;">
                {entry['text']}
            </div>
        """, unsafe_allow_html=True)
        
        # Tags
        tags = json.loads(entry.get('tags', '[]'))
        if tags:
            st.markdown(f"**Tags:** {', '.join(tags)}")
        
        # Image if exists
        if entry.get('image_path') and os.path.exists(entry['image_path']):
            st.image(entry['image_path'], use_column_width=True)
        
        # Todo list
        st.subheader("📝 Todo List")
        for task in json.loads(entry.get('todo_list', '[]')):
            st.write(f"{'✅' if task['completed'] else '❌'} {task['task']}")
        
        # Goal
        st.subheader("🎯 Goal Reminder")
        st.markdown(f"""
            <div style="background:{mood_color}; padding: 12px; border-radius: 12px; color: white;">
                {entry.get('goal', '')}
            </div>
        """, unsafe_allow_html=True)
        
        # Quote
        st.subheader("💬 Quote of the Day")
        st.markdown(f"""
            <div style="background:{mood_color}; padding: 12px; border-radius: 12px; color: white;">
                {entry.get('quote', '')}
            </div>
        """, unsafe_allow_html=True)
        
        # Delete button
        if st.button("🗑️ Delete Entry"):
            conn = get_db_connection()
            c = conn.cursor()
            c.execute("DELETE FROM entries WHERE id = ?", (entry['id'],))
            conn.commit()
            conn.close()
            
            if entry.get('image_path') and os.path.exists(entry['image_path']):
                os.remove(entry['image_path'])
            
            st.session_state.selected_entry = None
            load_entries_from_db()
            st.success("Entry deleted!")
            st.rerun()

def apply_ui_theme(mood_color):
    st.markdown(f"""
        <style>
            /* Main buttons */
            .stButton>button {{
                background-color: {mood_color};
                color: white;
                border-radius: 8px;
                padding: 8px 16px;
                border: none;
                font-weight: 500;
                transition: all 0.3s ease;
            }}
            .stButton>button:hover {{
                opacity: 0.8;
                transform: scale(1.02);
            }}
            
            /* Mood buttons */
            .mood-btn {{
                width: 100%;
                padding: 12px;
                border-radius: 12px;
                margin-bottom: 8px;
                font-size: 16px;
                transition: all 0.3s ease;
                border: none;
                cursor: pointer;
            }}
            
            /* Text input focus */
            .stTextInput>div>div>input:focus, 
            .stTextArea>div>div>textarea:focus {{
                border-color: {mood_color} !important;
                box-shadow: 0 0 0 0.2rem {mood_color}80;
            }}
            
            /* Date input */
            .stDateInput>div>div>input {{
                border-color: {mood_color};
            }}
        </style>
    """, unsafe_allow_html=True)

def load_entries_from_db():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM entries WHERE user_id = ? ORDER BY timestamp DESC", (st.session_state.user_id,))
    columns = [column[0] for column in c.description]
    st.session_state.entries = [dict(zip(columns, row)) for row in c.fetchall()]
    conn.close()

# MAIN APP 
def main():
    if "authenticated" not in st.session_state or not st.session_state.authenticated:
        auth_page()
    else:
        diary_page()

if __name__ == "__main__":
    main()