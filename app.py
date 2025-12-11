import streamlit as st
import datetime
import re

# ---------------------------------------------------------
# 1. CSS & STYLING (PURE BLACK UI ⚫)
# ---------------------------------------------------------
st.set_page_config(page_title="Eligibility Dashboard", layout="wide", page_icon="💎")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; }
    .stApp { background-color: #000000; }
    .main-title { text-align: center; background: -webkit-linear-gradient(45deg, #00c853, #64ffda); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3rem; font-weight: 800; margin-bottom: 10px; text-shadow: 0 10px 30px rgba(0, 200, 83, 0.2); }
    .glass-card { background: rgba(22, 27, 34, 0.8); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 16px; padding: 24px; margin-bottom: 24px; box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5); transition: transform 0.3s ease, box-shadow 0.3s ease; height: 100%; display: flex; flex-direction: column; position: relative; }
    .glass-card:hover { transform: translateY(-5px); box-shadow: 0 12px 40px 0 rgba(0, 255, 127, 0.1); border-color: rgba(0, 230, 118, 0.3); }
    .card-title { color: #ffffff; margin: 0; text-align: center; font-size: 1.4rem; font-weight: 700; letter-spacing: 0.5px; margin-bottom: 15px; }
    .summary-box { text-align: center; background: rgba(33, 150, 243, 0.15); border: 1px solid #2196f3; color: #ffffff; padding: 15px; border-radius: 12px; font-size: 1.2rem; font-weight: 700; margin-bottom: 30px; box-shadow: 0 0 20px rgba(33, 150, 243, 0.2); }
    .badge { display: block; margin: 0 auto 20px auto; padding: 8px 16px; border-radius: 50px; text-align: center; font-weight: 800; font-size: 1rem; letter-spacing: 1px; width: fit-content; box-shadow: 0 4px 15px rgba(0,0,0,0.2); }
    .badge-success { background: linear-gradient(135deg, #00c853, #00e676); color: #003300; box-shadow: 0 0 15px rgba(0, 230, 118, 0.4); }
    .badge-error { background: linear-gradient(135deg, #d32f2f, #ff5252); color: #ffffff; box-shadow: 0 0 15px rgba(255, 82, 82, 0.4); }
    .check-item { display: flex; justify-content: space-between; align-items: center; padding: 8px 0; border-bottom: 1px solid rgba(255, 255, 255, 0.08); font-size: 0.95rem; color: #eceff1; }
    .check-label { font-weight: 600; color: #90a4ae; }
    .val-success { color: #69f0ae; font-weight: bold; text-shadow: 0 0 8px rgba(105, 240, 174, 0.3); }
    .val-error { color: #ff8a80; font-weight: bold; text-shadow: 0 0 8px rgba(255, 138, 128, 0.3); }
    .val-neutral { color: #b0bec5; }
    .val-list { color: #fff59d; font-size: 0.9rem; font-weight: 600; text-align: right; flex: 1; margin-left: 10px; line-height: 1.3; }
    .combo-box { margin-top: 15px; padding: 12px; border-radius: 10px; font-size: 0.9rem; font-weight: 700; display: flex; align-items: center; gap: 10px; }
    .combo-green { background: rgba(27, 94, 32, 0.4); border: 1px solid #00e676; color: #b9f6ca; }
    .combo-orange { background: #FFC50F; border: 1px solid #FFD740; color: #000000; box-shadow: 0 0 10px rgba(255, 197, 15, 0.2); }
    .combo-blue { background: rgba(2, 119, 189, 0.4); border: 1px solid #29b6f6; color: #e1f5fe; }
    .reason-text { margin-top: 15px; font-size: 0.85rem; color: #b0bec5; background: rgba(255, 255, 255, 0.05); padding: 10px; border-radius: 8px; border-left: 3px solid #607d8b; line-height: 1.5; }
    .portal-link { display: block; margin-top: 20px; padding: 12px; background: linear-gradient(90deg, #2196f3, #21cbf3); color: white !important; text-align: center; text-decoration: none; border-radius: 50px; font-weight: bold; transition: 0.3s; box-shadow: 0 4px 15px rgba(33, 203, 243, 0.3); }
    .portal-link:hover { transform: scale(1.02); box-shadow: 0 6px 20px rgba(33, 203, 243, 0.5); }
    .stButton>button { width: 100%; background: linear-gradient(90deg, #00c853, #00e676); color: #003300; font-size: 1.3rem; border-radius: 12px; padding: 14px; border: none; font-weight: 800; box-shadow: 0 4px 15px rgba(0, 230, 118, 0.3); transition: 0.3s; }
    .stButton>button:hover { transform: scale(1.01); box-shadow: 0 6px 25px rgba(0, 230, 118, 0.5); color: #000; }
    .stTextInput>div>div>input { background-color: #161b22; border: 1px solid rgba(255, 255, 255, 0.2); color: white; border-radius: 10px; padding: 10px; font-size: 1.1rem; }
    .stTextInput>div>div>input:focus { border-color: #00e676; box-shadow: 0 0 10px rgba(0, 230, 118, 0.2); }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. RULE-BASED DATABASE
# ---------------------------------------------------------
# Full State List for matching
ALL_STATES = ["AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY","DC"]

PC_STATES = ["DE", "ME", "MD", "MA", "NJ", "NY", "PA", "VT", "IL", "MI", "OH", "WI", "FL", "MS", "NC", "VA", "WV", "AZ", "KS", "SD", "WA", "WY"]
DL_STATES = ["AK", "AR", "AZ", "CA", "DC", "DE", "FL", "GA", "IA", "ID", "IL", "IN", "KS", "KY", "LA", "MA", "ME", "MI", "MN", "MO", "MS", "MT", "NC", "NE", "NH", "NJ", "NM", "NY", "OH", "OR", "PA", "PR", "RI", "SC", "SD", "TN", "TX", "UT", "VA", "VT", "VI", "WA", "WI", "WV", "WY"]
MEDX_STATES = ["AK", "AR", "AZ", "CA", "DC", "DE", "FL", "GA", "IA", "IL", "IN", "KS", "KY", "LA", "MA", "ME", "MI", "MN", "MS", "MT", "NE", "NH", "NJ", "NM", "NC", "OH", "NY", "RI", "SC", "ID", "TN", "TX", "VA", "VT", "SD", "UT", "WI", "WY", "WV", "WA", "OR", "MO"]
WE_STATES = ["VT", "NH", "ME", "MA", "RI", "DE", "NY", "ID", "UT", "MT", "WY", "SD", "NE", "KS", "IA", "CA", "MO", "AZ", "WA", "LA", "WI", "MS", "IN", "WV", "VA", "SC", "MI", "TX", "NC", "AK", "NM"]

CAMPAIGNS = [
    {
        "name": "PC-Telemed",
        "link": "https://sites.google.com/outsourcingskill-teams.com/closing-portal-/clients-menu/1-pc-telemed?authuser=0",
        "provided": "BB, BKB, BB + Single Knee",
        "combo_type": "accepted",
        "combo_list": ["BB", "Both Knees", "BB + Single Knee"],
        "states": PC_STATES,
        "min_age": 65,
        "max_age": 84
    },
    {
        "name": "DL-PCP",
        "link": "https://sites.google.com/outsourcingskill-teams.com/closing-portal-/clients-menu/1-dl-pcp?authuser=0",
        "provided": "Back, Knee, Wrist, Shoulder, Ankle, Neck, Elbow",
        "combo_type": "none",
        "states": DL_STATES,
        "min_age": 0,
        "max_age": 200
    },
    {
        "name": "MEDX-PCP",
        "link": "https://sites.google.com/outsourcingskill-teams.com/closing-portal-/clients-menu/1-medx-chasing?authuser=0",
        "provided": "Back, Knee, Wrist, Shoulder, Ankle, Neck, Elbow",
        "combo_type": "none",
        "states": MEDX_STATES,
        "min_age": 0,
        "max_age": 200
    },
    {
        "name": "WE-PCP",
        "link": "https://sites.google.com/outsourcingskill-teams.com/closing-portal-/clients-menu/2-we-pcp?authuser=0",
        "provided": "Back, Knee, Wrist, Shoulder, Elbow, Ankle, Neck",
        "combo_type": "not_accepted",
        "combo_list": ["WRISTS + ANKLES", "ELBOWS + ANKLES", "WRISTS + ELBOWS", "WRISTS + SHOULDERS", "ELBOWS + SHOULDERS", "NECK + SHOULDER"],
        "states": WE_STATES,
        "min_age": 0,
        "max_age": 90
    },
    {
        "name": "CGM-PCP",
        "link": "https://sites.google.com/outsourcingskill-teams.com/closing-portal-/clients-menu/3-cgm-pcp?authuser=0",
        "provided": "Dexcom (CGM)",
        "combo_type": "none",
        "states": ALL_STATES,
        "min_age": 0,
        "max_age": 200
    }
]

# ---------------------------------------------------------
# 3. HELPER FUNCTIONS (The Smart Logic 🧠)
# ---------------------------------------------------------
def parse_input(user_input):
    """
    Super robust parser:
    1. Finds year (19xx or 20xx) regardless of position.
    2. Finds state (2 letters from ALL_STATES list) regardless of case/position.
    3. Anything else is considered 'Combo'.
    """
    clean_text = user_input.upper() # To uppercase
    
    # 1. FIND YEAR (Strict 4 digits starting with 19 or 20)
    year_match = re.search(r'(19|20)\d{2}', clean_text)
    year = int(year_match.group(0)) if year_match else None
    
    # Remove year from text to avoid confusion (e.g. CA1990 -> CA)
    text_without_year = clean_text
    if year:
        text_without_year = text_without_year.replace(str(year), " ")

    # 2. FIND STATE (Check against valid list)
    state = None
    # We split by non-alpha characters to check tokens, 
    # BUT we also handle "PA1968" case where space is missing.
    # Logic: Look for any 2-letter substring that matches a state code
    found_states = []
    for s in ALL_STATES:
        # Check if state exists as a distinct word OR inside the string if strictly 2 chars
        # Simplest robust way: if the state code exists in the string (after year removal)
        if s in text_without_year:
            found_states.append(s)
            
    # Heuristic: Pick the first valid state found (or longest match if needed, but states are all 2 chars)
    if found_states:
        # Preference logic: if multiple found (rare like "AL" inside "WALKER"), usually 
        # the user input is short. Let's pick the one that matches strict word boundary if possible
        best_state = None
        for s in found_states:
            if re.search(r'\b' + s + r'\b', text_without_year):
                best_state = s
                break
        state = best_state if best_state else found_states[0] # Fallback to first found

    # 3. EXTRACT COMBO
    # Remove State and Year from Original text
    combo_text = clean_text
    if state: combo_text = combo_text.replace(state, "")
    if year: combo_text = combo_text.replace(str(year), "")
    
    # Cleanup extra symbols
    combo_text = re.sub(r'[^A-Z0-9\+]', ' ', combo_text) # Keep letters, numbers, +
    combo_text = re.sub(r'\s+', ' ', combo_text).strip() # Merge spaces
    
    if not combo_text: combo_text = "None"
    
    return state, year, combo_text

def calculate_age(birth_year):
    current_year = datetime.datetime.now().year
    return current_year - birth_year

def check_campaign_eligibility(campaign, state, age):
    reasons = []
    is_eligible = True
    
    if state not in campaign["states"]:
        is_eligible = False
        reasons.append(f"State {state} is NOT in approved list.")
    
    if age < campaign["min_age"] or age > campaign["max_age"]:
        is_eligible = False
        if campaign["max_age"] < 150:
            reasons.append(f"Age {age} is out of range ({campaign['min_age']}-{campaign['max_age']}).")
        else:
            reasons.append(f"Age {age} is invalid.")
            
    if is_eligible:
        return True, "Patient meets all demographics criteria (State & Age)."
    else:
        return False, " & ".join(reasons)

def format_combo_rule(campaign):
    ctype = campaign["combo_type"]
    clist = campaign.get("combo_list", [])
    
    if ctype == "accepted":
        text = f"Accepted: {', '.join(clist)}"
        css = "combo-green"
        icon = "✅"
    elif ctype == "not_accepted":
        text = f"Not Accepted: {', '.join(clist)}"
        css = "combo-orange"
        icon = "⚠️"
    else:
        text = "no combo"
        css = "combo-blue"
        icon = "ℹ️"
        
    return text, css, icon

# ---------------------------------------------------------
# 4. UI RENDERER
# ---------------------------------------------------------
st.markdown('<div class="main-title">Eligibility Hub 💎</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    user_input = st.text_input("Search Patient", placeholder="e.g.NY 1950 ")
    check_btn = st.button("Check Eligibility Now")

if check_btn and user_input:
    with st.spinner("Analyzing Rules..."):
        state, year, combo_raw = parse_input(user_input)
        
        if not state or not year:
            st.error("❌ Could not detect State (e.g. NY) or Birth Year (e.g. 1950). Please check format.")
        else:
            age = calculate_age(year)
            st.markdown(f"""<div class="summary-box">📋 Patient Profile: Age {age} | State {state} | Input: {combo_raw}</div>""", unsafe_allow_html=True)
            
            cols = st.columns(3)
            for idx, campaign in enumerate(CAMPAIGNS):
                is_eligible, reason_summary = check_campaign_eligibility(campaign, state, age)
                
                if is_eligible:
                    status_html = '<span class="badge badge-success">✅ ELIGIBLE</span>'
                    border_style = "border-top: 5px solid #00e676;"
                    state_valid = True
                    age_valid = True
                else:
                    status_html = '<span class="badge badge-error">❌ NOT ELIGIBLE</span>'
                    border_style = "border-top: 5px solid #ff5252;"
                    state_valid = state in campaign["states"]
                    age_valid = campaign["min_age"] <= age <= campaign["max_age"]

                def get_row_html(label, val, is_valid):
                    icon = "✅" if is_valid else "❌"
                    color_class = "val-success" if is_valid else "val-error"
                    return f'<div class="check-item"><span class="check-label">{label}</span><span class="{color_class}">{val} {icon}</span></div>'

                rows_html = ""
                rows_html += get_row_html("🗺️ State", state, state_valid)
                rows_html += get_row_html("🎂 Age", age, age_valid)
                rows_html += f'<div class="check-item"><span class="check-label">🦿 Provided</span><span class="val-list">{campaign["provided"]}</span></div>'

                combo_text, combo_css, combo_icon = format_combo_rule(campaign)
                combo_html = f'<div class="combo-box {combo_css}">{combo_icon} {combo_text}</div>'

                with cols[idx % 3]:
                    html_card = f"""
<div class="glass-card" style="{border_style}">
    <h3 class="card-title">{campaign['name']}</h3>
    {status_html}
    <div style="margin-bottom: 10px;">{rows_html}</div>
    {combo_html}
    <div class="reason-text">💡 {reason_summary}</div>
    <a href="{campaign['link']}" target="_blank" class="portal-link">🔗 Open Portal</a>
</div>
"""
                    st.markdown(html_card, unsafe_allow_html=True)

