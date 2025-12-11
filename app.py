import streamlit as st
import json
import datetime
import re
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

# ---------------------------------------------------------
# 1. CSS & STYLING (PURE BLACK UI ⚫)
# ---------------------------------------------------------
st.set_page_config(page_title="Eligibility Dashboard", layout="wide", page_icon="💎")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
    }
    
    .stApp {
        background-color: #000000;
    }

    .main-title {
        text-align: center;
        background: -webkit-linear-gradient(45deg, #00c853, #64ffda);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 10px;
        text-shadow: 0 10px 30px rgba(0, 200, 83, 0.2);
    }

    .glass-card {
        background: rgba(22, 27, 34, 0.8);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
        position: relative;
    }

    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(0, 255, 127, 0.1);
        border-color: rgba(0, 230, 118, 0.3);
    }

    .card-title {
        color: #ffffff;
        margin: 0;
        text-align: center;
        font-size: 1.4rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        margin-bottom: 15px;
    }

    .summary-box {
        text-align: center;
        background: rgba(33, 150, 243, 0.15);
        border: 1px solid #2196f3;
        color: #ffffff;
        padding: 15px;
        border-radius: 12px;
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 30px;
        box-shadow: 0 0 20px rgba(33, 150, 243, 0.2);
    }

    .badge {
        display: block;
        margin: 0 auto 20px auto;
        padding: 8px 16px;
        border-radius: 50px;
        text-align: center;
        font-weight: 800;
        font-size: 1rem;
        letter-spacing: 1px;
        width: fit-content;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .badge-success {
        background: linear-gradient(135deg, #00c853, #00e676);
        color: #003300;
        box-shadow: 0 0 15px rgba(0, 230, 118, 0.4);
    }
    .badge-error {
        background: linear-gradient(135deg, #d32f2f, #ff5252);
        color: #ffffff;
        box-shadow: 0 0 15px rgba(255, 82, 82, 0.4);
    }

    .check-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 8px 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        font-size: 0.95rem;
        color: #eceff1;
    }
    .check-label { font-weight: 600; color: #90a4ae; }
    .val-success { color: #69f0ae; font-weight: bold; text-shadow: 0 0 8px rgba(105, 240, 174, 0.3); }
    .val-error { color: #ff8a80; font-weight: bold; text-shadow: 0 0 8px rgba(255, 138, 128, 0.3); }
    .val-neutral { color: #b0bec5; }
    .val-list { color: #fff59d; font-size: 0.9rem; font-weight: 600; text-align: right; flex: 1; margin-left: 10px; line-height: 1.3; }

    .combo-box {
        margin-top: 15px;
        padding: 12px;
        border-radius: 10px;
        font-size: 0.9rem;
        font-weight: 700;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .combo-green { background: rgba(27, 94, 32, 0.4); border: 1px solid #00e676; color: #b9f6ca; }
    .combo-orange { background: #FFC50F; border: 1px solid #FFD740; color: #000000; box-shadow: 0 0 10px rgba(255, 197, 15, 0.2); }
    .combo-blue { background: rgba(2, 119, 189, 0.4); border: 1px solid #29b6f6; color: #e1f5fe; }

    .reason-text {
        margin-top: 15px;
        font-size: 0.85rem;
        color: #b0bec5;
        background: rgba(255, 255, 255, 0.05);
        padding: 10px;
        border-radius: 8px;
        border-left: 3px solid #607d8b;
        line-height: 1.5;
    }

    .portal-link {
        display: block;
        margin-top: 20px;
        padding: 12px;
        background: linear-gradient(90deg, #2196f3, #21cbf3);
        color: white !important;
        text-align: center;
        text-decoration: none;
        border-radius: 50px;
        font-weight: bold;
        transition: 0.3s;
        box-shadow: 0 4px 15px rgba(33, 203, 243, 0.3);
    }
    .portal-link:hover { transform: scale(1.02); box-shadow: 0 6px 20px rgba(33, 203, 243, 0.5); }

    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #00c853, #00e676);
        color: #003300;
        font-size: 1.3rem;
        border-radius: 12px;
        padding: 14px;
        border: none;
        font-weight: 800;
        box-shadow: 0 4px 15px rgba(0, 230, 118, 0.3);
        transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.01); box-shadow: 0 6px 25px rgba(0, 230, 118, 0.5); color: #000; }
    
    .stTextInput>div>div>input {
        background-color: #161b22;
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
        border-radius: 10px;
        padding: 10px;
        font-size: 1.1rem;
    }
    .stTextInput>div>div>input:focus { border-color: #00e676; box-shadow: 0 0 10px rgba(0, 230, 118, 0.2); }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. FULL DATABASE
# ---------------------------------------------------------
campaigns_data = [
    {
        "name": "PC-Telemed",
        "status": "Active",
        "link": "https://sites.google.com/outsourcingskill-teams.com/closing-portal-/clients-menu/1-pc-telemed?authuser=0", 
        "criteria": {
            "age_limit": "65-84 years old",
            "dob_range": "1941 - 1960",
            "good_states": ["DE", "ME", "MD", "MA", "NJ", "NY", "PA", "VT", "IL", "MI", "OH", "WI", "FL", "MS", "NC", "VA", "WV", "AZ", "KS", "SD", "WA", "WY"],
            "provided_braces": "BB, BKB, BB + Single Knee",
            "accepted_combos": ["BB", "Both Knees", "BB + Single Knee"]
        }
    },
    {
        "name": "DL-PCP",
        "status": "Active",
        "link": "https://sites.google.com/outsourcingskill-teams.com/closing-portal-/clients-menu/1-dl-pcp?authuser=0", 
        "criteria": {
            "age_limit": "None (No age limit)",
            "good_states": ["AK", "AR", "AZ", "CA", "DC", "DE", "FL", "GA", "IA", "ID", "IL", "IN", "KS", "KY", "LA", "MA", "ME", "MI", "MN", "MO", "MS", "MT", "NC", "NE", "NH", "NJ", "NM", "NY", "OH", "OR", "PA", "PR", "RI", "SC", "SD", "TN", "TX", "UT", "VA", "VT", "VI", "WA", "WI", "WV", "WY"],
            "provided_braces": "Back, Knee, Wrist, Shoulder, Ankle, Neck, Elbow"
        }
    },
    {
        "name": "MEDX-PCP",
        "status": "Active",
        "link": "https://sites.google.com/outsourcingskill-teams.com/closing-portal-/clients-menu/1-medx-chasing?authuser=0", 
        "criteria": {
            "age_limit": "None (No age limit)",
            "good_states": ["AK", "AR", "AZ", "CA", "DC", "DE", "FL", "GA", "IA", "IL", "IN", "KS", "KY", "LA", "MA", "ME", "MI", "MN", "MS", "MT", "NE", "NH", "NJ", "NM", "NC", "OH", "NY", "RI", "SC", "ID", "TN", "TX", "VA", "VT", "SD", "UT", "WI", "WY", "WV", "WA", "OR", "MO"],
            "provided_braces": "Back, Knee, Wrist, Shoulder, Ankle, Neck, Elbow"
        }
    },
    {
        "name": "WE-PCP",
        "status": "Active",
        "link": "https://sites.google.com/outsourcingskill-teams.com/closing-portal-/clients-menu/2-we-pcp?authuser=0",
        "criteria": {
            "age_limit": "Max 90 years",
            "good_states": ["VT", "NH", "ME", "MA", "RI", "DE", "NY", "ID", "UT", "MT", "WY", "SD", "NE", "KS", "IA", "CA", "MO", "AZ", "WA", "LA", "WI", "MS", "IN", "WV", "VA", "SC", "MI", "TX", "NC", "AK", "NM"],
            "provided_braces": "Back, Knee, Wrist, Shoulder, Elbow, Ankle, Neck",
            "not_accepted_combos": ["WRISTS + ANKLES", "ELBOWS + ANKLES", "WRISTS + ELBOWS", "WRISTS + SHOULDERS", "ELBOWS + SHOULDERS", "NECK + SHOULDER"]
        }
    },
    {
        "name": "CGM-PCP",
        "status": "Active",
        "link": "https://sites.google.com/outsourcingskill-teams.com/closing-portal-/clients-menu/3-cgm-pcp?authuser=0",
        "criteria": {
            "age_limit": "None",
            "good_states": "All States",
            "provided_braces": "Dexcom (CGM)",
            "provided_cgm": "Dexcom"
        }
    },
    {"name": "Medicare-Fit", "status": "Inactive", "criteria": {}},
    {"name": "PPO-CGM", "status": "Inactive", "criteria": {}},
    {"name": "Fast-Telemed", "status": "Inactive", "criteria": {}}
]

# ---------------------------------------------------------
# 3. HELPER FUNCTION
# ---------------------------------------------------------
def clean_and_parse_json(text):
    try:
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        return None
    except:
        return None

# ---------------------------------------------------------
# 4. API & HYBRID LOGIC
# ---------------------------------------------------------
groq_key = st.secrets.get("GROQ_API_KEY")
google_key = st.secrets.get("GOOGLE_API_KEY")

if not groq_key or not google_key:
    with st.sidebar:
        st.header("⚙️ API Keys")
        st.caption("For deployment, use Secrets.")
        if not groq_key: groq_key = st.text_input("Groq API Key", type="password")
        if not google_key: google_key = st.text_input("Google API Key", type="password")

if not groq_key and not google_key:
    st.warning("⚠️ Please enter at least one API Key to proceed.")
    st.stop()

current_year = datetime.datetime.now().year
data_context = json.dumps(campaigns_data)

# --- STRICT MATH PROMPT ---
system_prompt = f"""
You are a Medical Eligibility API.
Context: Current Year is {current_year}.
Database: {data_context}

INSTRUCTIONS:
1. Ignore "Inactive" campaigns.
2. **STRICT AGE CALCULATION:** Age = {current_year} - Birth Year. Example: 1938 -> Age 87. If Age > Max Limit -> `age_valid` FALSE.
3. **ELIGIBILITY LOGIC:** `is_eligible` is TRUE ONLY IF `state_valid` is true AND `age_valid` is true.
4. **DATA OUTPUT:** Extract `link` & `provided_braces` exactly from DB.
5. **COMBO INFO:** If "accepted_combos" -> "Accepted: [...]". If "not_accepted_combos" -> "Not Accepted: [...]". Else -> "no combo".
6. **Output Format:** JSON Object.

JSON Structure:
{{
    "summary": "Patient Summary (calculated age)",
    "results": [
        {{
            "campaign": "Campaign Name",
            "link": "URL",
            "provided_braces": "String",
            "is_eligible": true/false,
            "breakdown": {{
                "state": {{ "text": "NY", "valid": true }},
                "age": {{ "text": "87", "valid": false }} 
            }},
            "combo_info_text": "Rules text",
            "reason_summary": "Explanation"
        }}
    ]
}}
"""

def get_hybrid_response(messages):
    # 1. Try Groq First (Faster)
    if groq_key:
        try:
            llm = ChatGroq(temperature=0, groq_api_key=groq_key, model_name="llama-3.3-70b-versatile")
            return llm.invoke(messages), "Groq"
        except Exception as e:
            pass 
    
    # 2. Try Google Gemini (Backup)
    if google_key:
        try:
            llm = ChatGoogleGenerativeAI(temperature=0, google_api_key=google_key, model="gemini-1.5-flash")
            return llm.invoke(messages), "Gemini"
        except Exception as e:
            return None, str(e)
            
    return None, "No valid API keys"

# ---------------------------------------------------------
# 5. UI RENDERER
# ---------------------------------------------------------
st.markdown('<div class="main-title">Eligibility Hub 💎</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    user_input = st.text_input("Search Patient", placeholder="e.g. NY 1938 wants BB")
    check_btn = st.button("Check Eligibility Now")

if check_btn and user_input:
    with st.spinner("Processing Data..."):
        try:
            messages = [SystemMessage(content=system_prompt), HumanMessage(content=user_input)]
            
            response, source = get_hybrid_response(messages)
            
            if response:
                result_json = clean_and_parse_json(response.content)

                if result_json:
                    st.markdown(f"""<div class="summary-box">📋 {result_json.get('summary', 'Report')}</div>""", unsafe_allow_html=True)

                    results = result_json.get("results", [])
                    cols = st.columns(3)
                    
                    for idx, item in enumerate(results):
                        # 1. Status Badge
                        if item["is_eligible"]:
                            status_html = '<span class="badge badge-success">✅ ELIGIBLE</span>'
                            border_style = "border-top: 5px solid #00e676;" 
                        else:
                            status_html = '<span class="badge badge-error">❌ NOT ELIGIBLE</span>'
                            border_style = "border-top: 5px solid #ff5252;" 

                        # 2. Rows
                        bd = item['breakdown']
                        provided_items = item.get('provided_braces', 'N/A')
                        link_url = item.get('link', '#')
                        
                        def format_row(label, data):
                            text = str(data.get('text', 'N/A'))
                            is_valid = data.get('valid')
                            if is_valid is True:
                                val_html = f'<span class="val-success">{text} ✅</span>'
                            elif is_valid is False:
                                val_html = f'<span class="val-error">{text} ❌</span>'
                            else:
                                val_html = f'<span class="val-neutral">{text} ➖</span>'
                            return f'<div class="check-item"><span class="check-label">{label}</span>{val_html}</div>'

                        rows_html = ""
                        rows_html += format_row("🗺️ State", bd.get('state', {}))
                        rows_html += format_row("🎂 Age", bd.get('age', {}))
                        rows_html += f'<div class="check-item"><span class="check-label">🦿 Provided</span><span class="val-list">{provided_items}</span></div>'

                        # 3. Combo Rules (3 Colors)
                        combo_text = item.get("combo_info_text", "no combo")
                        
                        if "not accepted" in combo_text.lower():
                            css_class = "combo-orange"
                            icon = "⚠️"
                        elif "no combo" in combo_text.lower():
                            css_class = "combo-blue"
                            icon = "ℹ️"
                        else:
                            css_class = "combo-green"
                            icon = "✅"
                            
                        combo_html = f'<div class="combo-box {css_class}">{icon} {combo_text}</div>'

                        # 4. Render Glass Card
                        with cols[idx % 3]:
                            html_card = f"""
    <div class="glass-card" style="{border_style}">
        <h3 class="card-title">{item['campaign']}</h3>
        {status_html}
        <div style="margin-bottom: 10px;">{rows_html}</div>
        {combo_html}
        <div class="reason-text">💡 {item['reason_summary']}</div>
        <a href="{link_url}" target="_blank" class="portal-link">🔗 Open Portal</a>
    </div>
    """
                            st.markdown(html_card, unsafe_allow_html=True)
                else:
                    st.warning("⚠️ Please provide a valid API Key to continue.")
            else:
                st.warning("⚠️ Please provide a valid API Key to continue.")
        except Exception as e:
            st.error(f"Error: {e}")
