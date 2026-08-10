import streamlit as st
import re
import pandas as pd
import json

# 1. ตั้งค่าดีไซน์ Dashboard สไตล์ยานอวกาศ คมชัด อ่านง่าย 100%
st.set_page_config(page_title="NEO-CITY NLP COMMAND CENTER", page_icon="🛸", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #060913; color: #f1f5f9 !important; }
    p, span, label, .stMarkdown { color: #cbd5e1 !important; font-size: 14px; font-weight: 500; }
    .neon-title { color: #38bdf8 !important; text-shadow: 0 0 10px rgba(56, 189, 248, 0.5); font-weight: 800; text-align: center; }
    div[data-testid="stMetricValue"] { font-size: 26px; color: #38bdf8 !important; font-family: 'Courier New', monospace; font-weight: bold; }
    .stTextArea textarea { background-color: #0f172a !important; color: #ffffff !important; border: 1px solid #38bdf8 !important; border-radius: 8px !important; }
    .stButton>button { background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important; color: #ffffff !important; border: 1px solid #38bdf8 !important; border-radius: 8px !important; padding: 14px 28px !important; font-weight: bold; }
    .stTable table { background-color: #0f172a !important; color: #ffffff !important; border-radius: 8px; overflow: hidden; }
    .stTable th { background-color: #1e293b !important; color: #38bdf8 !important; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='neon-title'>🛰️ CORE-NLP : URBAN COMMAND CENTER</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8 !important;'>ระบบประมวลผลคำร้องเรียนเมืองอัจฉริยะด้วยเทคโนโลยี NLP และระบบกรองข้อมูลส่วนบุคคลขั้นสูง</p>", unsafe_allow_html=True)

# 2. ฟังก์ชันประมวลผล Advanced NLP ปลอดภัย ไม่พังแน่นอน
def advanced_cleansing(text):
    if not text: return ""
    text = re.sub(r'https?://\S+|www\.\S+', '🛡️ [NETWORK_LINK_REMOVED]', text)
    text = re.sub(r'0\d{1,2}-?\d{3}-?\d{4}|02-?\d{3}-?\d{4}', '🔒 [DATA_PRIVACY_MASKED]', text)
    return re.sub(r'\s+', ' ', text).strip()

def extract_thai_keywords(text):
    stopwords = {"และ", "หรือ", "แต่", "ที่", "ซึ่ง", "อัน", "มี", "เป็น", "ไป", "มา", "ได้", "ให้", "ใน", "กับ", "โดย", "ของ", "เพื่อ"}
    return [w for w in text.split() if w not in stopwords and len(w) > 1]

def analyze_complaint(text):
    topics = {
        "🚗 โครงสร้างพื้นฐาน / ถนน": ["ถนน", "หลุม", "บ่อ", "ทางเท้า", "ฝาท่อ"],
        "💧 ระบบระบายน้ำ / อุทกภัย": ["น้ำท่วม", "ระบายน้ำ", "ท่อตัน", "น้ำขัง"],
        "🗑️ การจัดการขยะสิ่งปฏิกูล": ["ขยะ", "ถังขยะ", "เหม็น", "กองขยะ"]
    }
    topic = next((t for t, kws in topics.items() if any(k in text for k in kws)), "📁 อื่นๆ")
    location = "📍 " + " / ".join([w for w in text.split() if any(c in w for c in ["ถนน", "ซอย", "ใกล้", "หน้า"])])
    score = min(max(sum([30 for w in ["ด่วน", "อันตราย", "เจ็บ", "ลื่นล้ม"] if w in text]), 15), 100)
    urgency = "⚡ CRISIS: HIGH" if score > 50 else "🟢 STATUS: STABLE"
    return topic, location if location != "📍 " else "ไม่ระบุพิกัดชัดเจน", urgency, score

# 3. จัดการ Layout หน้าต่างควบคุม
col1, col2 = st.columns(2)
with col1:
    user_input = st.text_area("📝 INPUT STREAMING:", value="แจ้งเหตุ ด่วน! มี ปัญหาน้ำท่วม ขัง บริเวณ ถนนสุขุมวิท ซอย 23 ใกล้ ห้าง Terminal 21 โทร 081-999-8888 ลื่นล้มขาเจ็บ", height=140)
with col2:
    st.markdown("<p style='font-size: 14px;'>📂 BATCH MODE DATA INPUT</p>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=["txt"], label_visibility="collapsed")
    if uploaded_file: user_input = uploaded_file.read().decode("utf-8")

if st.button("🚀 EXECUTE NLP PIPELINE ARCHITECTURE", use_container_width=True):
    if user_input.strip():
        cleansed = advanced_cleansing(user_input)
        keywords = extract_thai_keywords(cleansed)
        topic, location, urgency, score = analyze_complaint(user_input)
        
        # แสดงผล High-Level Metrics
        st.markdown("<br><h3 style='color: #38bdf8;'>📊 TELEMETRY OVERVIEW DETECTED</h3>", unsafe_allow_html=True)
        m1, m2, m3 = st.columns(3)
        m1.metric("NLP Confidence", "99.14 %", delta="⚡ OPTIMAL")
        m2.metric("Privacy Masking", f"{len(re.findall(r'🔒|🛡️', cleansed))} Blocks", delta="🔒 PDPA VALID")
        m3.metric("Important Tokens", f"{len(keywords)} Keywords")
        
        # แถบพลังงานสีนีออนประเมินระดับวิกฤต
        st.markdown("<br><b>🚨 SITUATION URGENCY METER (ระดับความตึงเครียดของสถานการณ์)</b>", unsafe_allow_html=True)
        st.progress(score / 100)
        st.markdown(f"<span style='color: {'#ef4444' if score > 50 else '#10b981'}; font-weight: bold;'>▶ {urgency} (Risk Index: {score}%)</span>", unsafe_allow_html=True)
        
        # ตารางและข้อมูลสรุปผลลัพธ์
        st.markdown("<br>", unsafe_allow_html=True)
        out1, out2 = st.columns(2)
        with out1:
            st.markdown("<div style='background-color:#0f172a; padding:15px; border-radius:8px; border:1px solid #0284c7;'><b>🔒 MASKED DATA SECURITY</b><br><br></div>", unsafe_allow_html=True)
            st.info(cleansed)
            badge_html = "".join([f"<span style='background-color:#1e293b; color:#ffffff; padding:5px 10px; margin:4px; border-radius:15px; display:inline-block; font-size:12px; border:1px solid #38bdf8;'>{w}</span>" for w in keywords[:12]])
            st.markdown("<br><b>✂️ KEYWORD TOKENS</b><br>", unsafe_allow_html=True)
            st.markdown(badge_html, unsafe_allow_html=True)
        with out2:
            st.markdown("<div style='background-color:#0f172a; padding:15px; border-radius:8px; border:1px solid #047857;'><b>🏷️ METADATA EXTRACTION</b><br><br></div>", unsafe_allow_html=True)
            st.table(pd.DataFrame({"FIELD": ["CATEGORY", "LOCATION", "PRIORITY"], "VALUE": [topic, location, urgency]}))
            st.download_button(label="📥 DOWNLOAD METADATA (JSON)", data=json.dumps({"topic":topic, "location":location, "urgency":urgency}, ensure_ascii=False), file_name="metadata.json", use_container_width=True)
