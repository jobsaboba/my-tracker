import streamlit as st
import requests, re, os
from bs4 import BeautifulSoup

# Setup for laptop screen
st.set_page_config(page_title="Linux Horse Tracker", layout="wide")

# --- 1. FILE HANDLER (Local Linux Edition) ---
# This looks for 'trainers.txt' in the same folder as this script
FILE_PATH = "trainers.txt"

def load_trainers():
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r") as f:
            # Reads the file and makes sure there are no extra spaces
            return [n.strip() for n in f.read().split(",") if n.strip()]
    return ["goonmyson"] # Defaults if file is missing

def save_trainers(list_to_save):
    with open(FILE_PATH, "w") as f:
        f.write(", ".join(list_to_save))

# Load the names into memory when the app starts
if 'trainers' not in st.session_state:
    st.session_state.trainers = load_trainers()

st.title("🏇 Linux Trainer Tracker (Local Version)")

# --- 2. SIDEBAR (The Control Panel) ---
with st.sidebar:
    st.header("Manage My List")
    new_name = st.text_input("Add Trainer Surname")
    if st.button("Add"):
        if new_name and new_name.title() not in st.session_state.trainers:
            st.session_state.trainers.append(new_name.title())
            save_trainers(st.session_state.trainers) # PERMANENTLY SAVES TO DISK
            st.rerun()
            
    st.divider()
    rem_name = st.selectbox("Remove Trainer", sorted(st.session_state.trainers))
    if st.button("DELETE PERMANENTLY"):
        st.session_state.trainers.remove(rem_name)
        save_trainers(st.session_state.trainers) # PERMANENTLY ERASES FROM DISK
        st.rerun()

# --- 3. THE SCANNER ---
if st.button("🔍 SCAN SPORTING LIFE", use_container_width=True):
    with st.spinner("Checking today's runners..."):
        try:
            h = {'User-Agent': 'Mozilla/5.0'}
            req = requests.get("https://www.sportinglife.com/racing/abc-guide/today/trainers", headers=h, timeout=10)
            soup = BeautifulSoup(req.text, 'html.parser')
            
            found = []
            for row in soup.find_all('tr'):
                txt = row.get_text(" ", strip=True).lower()
                if "entries" in txt:
                    for n in st.session_state.trainers:
                        if re.search(r'\b' + re.escape(n.lower()) + r'\b', txt):
                            found.append(n.upper())
            
            found = sorted(list(set(found))) # Remove duplicates
            
            if found:
                st.balloons()
                c1, c2 = st.columns(2)
                c1.metric("Runners", len(found))
                c2.metric("Total Stake", f"£{len(found)*0.10:.2f}")
                
                for f in found:
                    st.success(f"✅ {f} is active today!")
            else:
                st.info("No trainers found from your list.")
        except Exception as e:
            st.error(f"Error: {e}")

st.write("---")
st.write(f"Current List ({len(st.session_state.trainers)}):", ", ".join(sorted(st.session_state.trainers)))
