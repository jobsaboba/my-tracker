import streamlit as st
import requests, re
from bs4 import BeautifulSoup

# Setup the Page for Mobile
st.set_page_config(page_title="10p Tracker", layout="centered")

st.title("🏇 10p Trainer Tracker")

# 1. Initialize the List (Saved in 'Session State' so it stays while you use it)
if 'trainers' not in st.session_state:
    st.session_state.trainers = ["Carroll", "Appleby", "Evans", "Butler", "Watson", "Fahey", "Boughey", "Brittain", "Loughnane", "Haynes", "Channon", "Carr"]

# 2. Sidebar for Adding/Removing (Keeps the main screen clean on phone)
with st.sidebar:
    st.header("Manage List")
    new_name = st.text_input("Add Trainer Surname")
    if st.button("Add"):
        if new_name and new_name.title() not in st.session_state.trainers:
            st.session_state.trainers.append(new_name.title())
            st.success(f"Added {new_name}")
            
    rem_name = st.selectbox("Remove Trainer", sorted(st.session_state.trainers))
    if st.button("Delete"):
        st.session_state.trainers.remove(rem_name)
        st.warning(f"Removed {rem_name}")
        st.rerun()

# 3. The Scan Button
if st.button("🔍 SCAN TODAY'S RUNNERS", use_container_width=True):
    with st.spinner("Checking Sporting Life..."):
        try:
            h = {'User-Agent': 'Mozilla/5.0'}
            req = requests.get("https://www.sportinglife.com/racing/abc-guide/today/trainers", headers=h, timeout=10)
            soup = BeautifulSoup(req.text, 'html.parser')
            
            found = []
            seen = set()
            for row in soup.find_all('tr'):
                txt = row.get_text(" ", strip=True).lower()
                if "entries" in txt:
                    for n in st.session_state.trainers:
                        n_low = n.lower()
                        if n_low not in seen and re.search(r'\b' + re.escape(n_low) + r'\b', txt):
                            found.append(n.upper())
                            seen.add(n_low)
            
            if found:
                for f in sorted(found):
                    st.success(f"✅ {f} - ACTIVE TODAY")
            else:
                st.info("No trainers from your list found today.")
                
        except Exception as e:
            st.error(f"Error: {e}")

# 4. Show Current List at the bottom
with st.expander("Show My Full Trainer List"):
    st.write(", ".join(sorted(st.session_state.trainers)))
