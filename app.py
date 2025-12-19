import streamlit as st
import datetime
import re
import pandas as pd

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
    .age-note { font-size: 0.75rem; color: #ffab91; text-align: right; margin-top: -5px; font-style: italic;}
    .special-note { font-size: 0.85rem; color: #ff80ab; text-align: center; margin-top: 10px; font-weight: bold; background: rgba(255, 64, 129, 0.1); padding: 5px; border-radius: 5px; border: 1px dashed #ff80ab; }
    .combo-box { margin-top: 15px; padding: 12px; border-radius: 10px; font-size: 0.9rem; font-weight: 700; display: flex; align-items: center; gap: 10px; }
    .combo-green { background: rgba(27, 94, 32, 0.4); border: 1px solid #00e676; color: #b9f6ca; }
    .combo-orange { background: #FFC50F; border: 1px solid #FFD740; color: #000000; box-shadow: 0 0 10px rgba(255, 197, 15, 0.2); }
    .combo-blue { background: rgba(2, 119, 189, 0.4); border: 1px solid #29b6f6; color: #e1f5fe; }
    .reason-text { margin-top: 15px; font-size: 0.85rem; color: #b0bec5; background: rgba(255, 255, 255, 0.05); padding: 10px; border-radius: 8px; border-left: 3px solid #607d8b; line-height: 1.5; }
    
    /* Links Container styling */
    .links-container { display: flex; gap: 10px; margin-top: 20px; }
    .portal-link { flex: 1; padding: 10px; background: linear-gradient(90deg, #2196f3, #21cbf3); color: white !important; text-align: center; text-decoration: none; border-radius: 50px; font-weight: bold; font-size: 0.9rem; transition: 0.3s; box-shadow: 0 4px 15px rgba(33, 203, 243, 0.3); }
    .extra-link { flex: 1; padding: 10px; background: linear-gradient(90deg, #7b1fa2, #ab47bc); color: white !important; text-align: center; text-decoration: none; border-radius: 50px; font-weight: bold; font-size: 0.9rem; transition: 0.3s; box-shadow: 0 4px 15px rgba(171, 71, 188, 0.3); }
    .portal-link:hover, .extra-link:hover { transform: scale(1.05); }
    
    .stButton>button { width: 100%; background: linear-gradient(90deg, #00c853, #00e676); color: #003300; font-size: 1.3rem; border-radius: 12px; padding: 14px; border: none; font-weight: 800; box-shadow: 0 4px 15px rgba(0, 230, 118, 0.3); transition: 0.3s; }
    .stButton>button:hover { transform: scale(1.01); box-shadow: 0 6px 25px rgba(0, 230, 118, 0.5); color: #000; }
    .stTextInput>div>div>input { background-color: #161b22; border: 1px solid rgba(255, 255, 255, 0.2); color: white; border-radius: 10px; padding: 10px; font-size: 1.1rem; }
    .stTextInput>div>div>input:focus { border-color: #00e676; box-shadow: 0 0 10px rgba(0, 230, 118, 0.2); }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. DATA ENGINE (Google Sheets - CSV Link) 🌐
# ---------------------------------------------------------
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQythtQBUCbRZAw54i_5x1uSz0NI9aA5O6GpYaKU6h_twzBGsJeu7PiJTjmUd4_xVGon4lHhSoQ7KZ7/pub?output=csv"

ALL_STATES = ["AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY","DC"]

@st.cache_data(ttl=60)
def load_campaigns():
    try:
        # Load Data
        df = pd.read_csv(SHEET_URL, dtype=str, engine='python', on_bad_lines='skip')
        df = df.fillna("") 
        df.columns = [c.strip() for c in df.columns]

        campaigns = []
        for _, row in df.iterrows():
            def clean_str(val): return str(val).strip()
            
            # Status Normalization
            status_raw = clean_str(row.get('status', 'Inactive')).title()
            
            # Lists
            states_list = [s.strip().upper() for s in str(row.get('states', '')).split(',')] if row.get('states') else []
            combos_list = [c.strip() for c in str(row.get('combo_list', '')).split(',')] if row.get('combo_list') else []
            
            def safe_int(val):
                try: return int(float(val))
                except: return 0

            campaign = {
                "name": clean_str(row.get('name', 'Unknown')),
                "status": status_raw,
                "link": clean_str(row.get('link', '#')),
                "resource_link": clean_str(row.get('resource_link', '')), # Keep raw for checking later
                "resource_label": clean_str(row.get('resource_label', 'Check Tool')),
                "provided": clean_str(row.get('provided', '')),
                "special_note": clean_str(row.get('special_note', '')) if row.get('special_note') else None,
                "combo_type": clean_str(row.get('combo_type', 'none')),
                "combo_list": combos_list,
                "states": states_list,
                "min_age": safe_int(row.get('min_age', 0)),
                "max_age": safe_int(row.get('max_age', 200)),
                "age_note": clean_str(row.get('age_note', '')) if row.get('age_note') else None
            }
            campaigns.append(campaign)
            
        return campaigns
    except Exception as e:
        st.error(f"❌ Error loading data from sheet: {e}")
        return []

CAMPAIGNS = load_campaigns()

# ---------------------------------------------------------
# 3. HELPER FUNCTIONS
# ---------------------------------------------------------
def parse_input(user_input):
    clean_text = user_input.upper()
    year, month = None, 1 
    date_match = re.search(r'\b(0?[1-9]|1[0-2])[-/](19|20)\d{2}\b', clean_text)
    if date_match:
        date_str = date_match.group(0)
        parts = date_str.split('-') if '-' in date_str else date_str.split('/')
        month, year = int(parts[0]), int(parts[1])
        text_without_date = clean_text.replace(date_str, " ")
    else:
        year_match = re.search(r'(19|20)\d{2}', clean_text)
        if year_match:
            year = int(year_match.group(0))
            text_without_date = clean_text.replace(str(year), " ")
        else:
            text_without_date = clean_text

    state = None
    found_states = []
    for s in ALL_STATES:
        if s in text_without_date:
            found_states.append(s)
            
    if found_states:
        best_state = None
        for s in found_states:
            if re.search(r'\b' + s + r'\b', text_without_date):
                best_state = s; break
        state = best_state if best_state else found_states[0]

    combo_text = clean_text
    if state: combo_text = combo_text.replace(state, "")
    if date_match: combo_text = combo_text.replace(date_match.group(0), "")
    elif year: combo_text = combo_text.replace(str(year), "")
    
    combo_text = re.sub(r'[^A-Z0-9\+]', ' ', combo_text).strip()
    return state, year, month, (combo_text if combo_text else "None")

def calculate_precise_age(birth_year, birth_month):
    today = datetime.date.today()
    age_years = today.year - birth_year
    if today.month < birth_month:
        age_years -= 1
        age_months = 12 - (birth_month - today.month)
    else:
        age_months = today.month - birth_month
    return age_years, age_months

def check_campaign_eligibility(campaign, state, age_y, age_m):
    reasons = []
    is_eligible = True
    
    if state not in campaign["states"]:
        is_eligible = False
        reasons.append(f"State {state} is NOT in approved list.")
    
    if campaign["name"] == "WE-PCP":
        limit_months = (89 * 12) + 11
        if (age_y * 12) + age_m > limit_months:
            is_eligible = False
            reasons.append(f"Age exceeds limit (Max 89y 11m).")
    else:
        if age_y < campaign["min_age"] or age_y > campaign["max_age"]:
            is_eligible = False
            if campaign["max_age"] < 150:
                reasons.append(f"Age {age_y} is out of range ({campaign['min_age']}-{campaign['max_age']}).")
            else:
                reasons.append(f"Age {age_y} is invalid.")
            
    if is_eligible:
        return True, "Patient meets all demographics criteria (State & Age)."
    return False, " & ".join(reasons)

def format_combo_rule(campaign):
    ctype = campaign["combo_type"]
    clist = campaign.get("combo_list", [])
    if ctype == "accepted":
        return f"Accepted: {', '.join(clist)}", "combo-green", "✅"
    elif ctype == "not_accepted":
        return f"Not Accepted: {', '.join(clist)}", "combo-orange", "⚠️"
    return "no combo", "combo-blue", "ℹ️"

# ---------------------------------------------------------
# 4. UI RENDERER (Indentation Fixed)
# ---------------------------------------------------------
st.markdown('<div class="main-title">Eligibility Hub 💎</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    user_input = st.text_input("Search Patient", placeholder="e.g. 11-1938 NY BB (or just 1938)")
    check_btn = st.button("Check Eligibility Now")

if check_btn and user_input:
    with st.spinner("Syncing Data & Analyzing..."):
        state, year, month, combo_raw = parse_input(user_input)
        
        if not state or not year:
            st.error("❌ Could not detect State (e.g. NY) or Year (e.g. 1950). Check format.")
        else:
            age_y, age_m = calculate_precise_age(year, month)
            combo_display = f" | Combo: {combo_raw}" if combo_raw and combo_raw != "None" else ""
            st.markdown(f"""<div class="summary-box">📋 Patient Profile: Age {age_y}y {age_m}m | State {state}{combo_display}</div>""", unsafe_allow_html=True)
            
            # Filter Active Campaigns
            active_campaigns = [c for c in CAMPAIGNS if str(c.get("status")).lower() == "active"]
            
            if not active_campaigns:
                st.warning("⚠️ No active campaigns found. Please check your Google Sheet.")
            else:
                cols = st.columns(3)
                for idx, campaign in enumerate(active_campaigns):
                    is_eligible, reason_summary = check_campaign_eligibility(campaign, state, age_y, age_m)
                    
                    if is_eligible:
                        status_html = '<span class="badge badge-success">✅ ELIGIBLE</span>'
                        border_style = "border-top: 5px solid #00e676;"
                        state_valid, age_valid = True, True
                    else:
                        status_html = '<span class="badge badge-error">❌ NOT ELIGIBLE</span>'
                        border_style = "border-top: 5px solid #ff5252;"
                        state_valid = state in campaign["states"]
                        if campaign["name"] == "WE-PCP":
                            age_valid = ((age_y * 12) + age_m) <= ((89 * 12) + 11)
                        else:
                            age_valid = campaign["min_age"] <= age_y <= campaign["max_age"]

                    def get_row_html(label, val, is_valid):
                        icon, color = ("✅", "val-success") if is_valid else ("❌", "val-error")
                        return f'<div class="check-item"><span class="check-label">{label}</span><span class="{color}">{val} {icon}</span></div>'

                    rows_html = ""
                    rows_html += get_row_html("🗺️ State", state, state_valid)
                    rows_html += get_row_html("🎂 Age", f"{age_y}y {age_m}m", age_valid)
                    
                    if campaign["age_note"]: rows_html += f'<div class="age-note">⚠️ {campaign["age_note"]}</div>'
                    rows_html += f'<div class="check-item"><span class="check-label">🦿 Provided</span><span class="val-list">{campaign["provided"]}</span></div>'
                    if campaign["special_note"]: rows_html += f'<div class="special-note">⚠️ {campaign["special_note"]}</div>'

                    combo_text, combo_css, combo_icon = format_combo_rule(campaign)
                    combo_html = f'<div class="combo-box {combo_css}">{combo_icon} {combo_text}</div>'

                    # 🔥 SMART BUTTON LOGIC (Fixed)
                    raw_res_link = str(campaign.get("resource_link", "")).strip()
                    raw_res_label = str(campaign.get("resource_label", "Check Tool")).strip()
                    
                    extra_btn_html = ""
                    # Check if link exists AND is not "nan" or "none"
                    if (len(raw_res_link) > 0 and 
                        raw_res_link.lower() != "nan" and 
                        raw_res_link.lower() != "none"):
                        extra_btn_html = f'<a href="{raw_res_link}" target="_blank" class="extra-link">{raw_res_label}</a>'

                    main_link = str(campaign.get('link', '#')).strip()

                    # ⚠️ CRITICAL FIX: HTML String is NOT indented to avoid Markdown code blocks
                    html_card = f"""<div class="glass-card" style="{border_style}"><h3 class="card-title">{campaign['name']}</h3>{status_html}<div style="margin-bottom: 10px;">{rows_html}</div>{combo_html}<div class="reason-text">💡 {reason_summary}</div><div class="links-container"><a href="{main_link}" target="_blank" class="portal-link">🔗 Open Client Page</a>{extra_btn_html}</div></div>"""

                    with cols[idx % 3]:
                        st.markdown(html_card, unsafe_allow_html=True)
