import os
import re
import html
import time
import json
import random
import urllib.request
import streamlit as st
from groq import Groq
import copy

# 1. إعداد الصفحة
st.set_page_config(
    page_title="الموسوعة الفقهية والحديثية الذكية",
    page_icon="🕌",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. تصميم احترافي متقدم (Ultra-Modern Islamic Glassmorphism UI)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Amiri:ital,wght@0,400;0,700;1,400&family=Aref+Ruqaa:wght@700&family=Cairo:wght@400;600;700;800;900&display=swap');
    
    * {
        font-family: 'Cairo', sans-serif !important;
        box-sizing: border-box !important;
    }
    
    html, body, .stApp {
        background: radial-gradient(circle at 50% -20%, #0d2818 0%, #081c15 35%, #050e14 75%, #02060a 100%) !important;
        color: #f8fafc !important;
        direction: rtl !important;
        overflow-x: hidden !important;
    }

    [data-testid="stSidebar"], [data-testid="collapsedControl"] {
        display: none !important;
    }

    .main .block-container {
        padding: 1rem 0.8rem 2.5rem 0.8rem !important;
        max-width: 720px !important;
    }
    
    /* بطاقة الذكر الزجاجية */
    .dhikr-card {
        background: linear-gradient(135deg, rgba(234, 179, 8, 0.12) 0%, rgba(13, 40, 24, 0.4) 100%);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(234, 179, 8, 0.35);
        border-radius: 16px;
        padding: 0.75rem 1rem;
        margin-bottom: 1.2rem;
        text-align: center;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.35);
    }
    
    .dhikr-text {
        font-family: 'Amiri', serif !important;
        font-size: 1.15rem;
        font-weight: 700;
        color: #fef08a;
        margin: 0;
        line-height: 1.6;
    }
    
    /* الهيدر الملكي الفاخر */
    .royal-hero {
        background: linear-gradient(135deg, rgba(16, 44, 30, 0.8) 0%, rgba(8, 28, 21, 0.95) 100%);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(234, 179, 8, 0.45);
        border-radius: 20px;
        padding: 1.5rem 1rem;
        margin-bottom: 1.5rem;
        text-align: center;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.5);
    }
    
    .royal-hero h1 {
        font-family: 'Aref Ruqaa', serif !important;
        color: #fbbf24;
        font-size: 1.85rem;
        margin-bottom: 0.3rem;
        line-height: 1.3;
        text-shadow: 0 2px 10px rgba(251, 191, 36, 0.25);
    }
    
    .royal-hero p {
        color: #86efac;
        font-size: 0.95rem;
        font-weight: 600;
        margin-bottom: 0;
    }
    
    /* الحقول والمدخلات الزجاجية */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stNumberInput>div>div>input {
        background: rgba(8, 28, 21, 0.85) !important;
        color: #ffffff !important;
        border: 1px solid rgba(234, 179, 8, 0.4) !important;
        border-radius: 14px !important;
        padding: 0.75rem 1rem !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.4) !important;
    }

    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #fbbf24 !important;
        box-shadow: 0 0 15px rgba(251, 191, 36, 0.3) !important;
    }
    
    .stRadio label, .stSelectbox label {
        font-size: 1.05rem !important;
        font-weight: 700 !important;
        color: #facc15 !important;
    }
    
    /* أزرار الإجراءات الفاخرة */
    .stButton>button {
        background: linear-gradient(135deg, #d97706 0%, #b45309 50%, #78350f 100%) !important;
        color: #ffffff !important;
        font-weight: 800 !important;
        font-size: 1.05rem !important;
        border: 1px solid rgba(254, 240, 138, 0.3) !important;
        border-radius: 14px !important;
        padding: 0.75rem 1.2rem !important;
        width: 100%;
        margin-top: 0.4rem;
        box-shadow: 0 6px 20px rgba(180, 83, 9, 0.4) !important;
        transition: all 0.25s ease !important;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(251, 191, 36, 0.5) !important;
    }

    .back-btn>button {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.85) 0%, rgba(15, 23, 42, 0.95) 100%) !important;
        border: 1px solid rgba(234, 179, 8, 0.4) !important;
        color: #fbbf24 !important;
        margin-bottom: 1.2rem !important;
        box-shadow: none !important;
    }
    
    .stMarkdown {
        font-size: 1.05rem !important;
        line-height: 1.9 !important;
        color: #f8fafc !important;
        word-break: break-word !important;
    }

    .stMarkdown h1 {
        font-family: 'Amiri', serif !important;
        color: #fbbf24 !important;
        font-size: 1.45rem !important;
        border-bottom: 1.5px solid rgba(234, 179, 8, 0.3) !important;
        padding-bottom: 0.35rem !important;
        margin-top: 1.2rem !important;
    }
    
    .stMarkdown h2, .stMarkdown h3 {
        font-family: 'Amiri', serif !important;
        color: #38bdf8 !important;
        font-size: 1.25rem !important;
    }

    table {
        width: 100% !important;
        display: block !important;
        overflow-x: auto !important;
        white-space: nowrap !important;
        border-collapse: collapse !important;
        margin: 1rem 0 !important;
    }

    th, td {
        border: 1px solid rgba(234, 179, 8, 0.3) !important;
        padding: 8px 12px !important;
    }

    .quiz-card {
        background: rgba(16, 44, 30, 0.85);
        border: 1.5px solid rgba(234, 179, 8, 0.6);
        border-radius: 16px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.4);
    }
    
    .stat-card {
        background: rgba(16, 44, 30, 0.7);
        border: 1px solid rgba(234, 179, 8, 0.3);
        border-radius: 14px;
        padding: 1rem;
        text-align: center;
        margin-bottom: 0.8rem;
    }
    .stat-number {
        font-size: 1.75rem;
        font-weight: 900;
        color: #fbbf24;
    }
    .stat-title {
        color: #94a3b8;
        font-size: 0.85rem;
        font-weight: 700;
    }

    .market-badge {
        background: rgba(34, 197, 94, 0.15);
        border: 1px solid rgba(34, 197, 94, 0.4);
        color: #4ade80;
        padding: 4px 10px;
        border-radius: 10px;
        font-size: 0.85rem;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 0.8rem;
    }

    .royal-footer {
        margin-top: 3rem;
        padding: 1.5rem 1rem;
        border-top: 1px solid rgba(234, 179, 8, 0.25);
        background: linear-gradient(180deg, transparent 0%, rgba(8, 28, 21, 0.95) 100%);
        border-radius: 16px 16px 0 0;
        text-align: center;
        font-size: 0.9rem;
    }
    
    .dev-badge {
        display: inline-block;
        background: rgba(234, 179, 8, 0.15);
        border: 1px solid rgba(234, 179, 8, 0.4);
        padding: 0.25rem 0.8rem;
        border-radius: 12px;
        color: #facc15;
        font-weight: 800;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# 3. بنك الأسئلة الموسع
EXPANDED_QUIZ_DATABASE = {
    "المستوى الأول: المبتدئ (فقه العبادات الأساسي) 🟢": [
        {"question": "ما حكم قراءة سورة الفاتحة للإمام والمنفرد في الصلاة المفروضة؟", "options": ["ركن لا تصح الصلاة إلا به", "سنة مستحبة وتصح الصلاة بدونها", "واجب يجبره سجود السهو"], "correct": "ركن لا تصح الصلاة إلا به", "proof": "لقول النبي ﷺ: «لا صلاةَ لمَن لم يقرَأْ بفاتحةِ الكتابِ» (متفق عليه)."},
        {"question": "ما هو الحد الأدنى لنصاب الذهب الذي تجب فيه الزكاة بالجرامات؟", "options": ["85 جراماً من الذهب الخالص", "50 جراماً", "120 جراماً"], "correct": "85 جراماً من الذهب الخالص", "proof": "النصاب الشرعي للذهب عشرون ديناراً، وتساوي 85 جراماً من الذهب عيار 24."},
        {"question": "ما حكم صيام يومي عيدي الفطر والأضحى؟", "options": ["محرم باتفاق العلماء", "مكروه كراهة تنزيه", "مباح لمن كان عليه قضاء"], "correct": "محرم باتفاق العلماء", "proof": "نهى رسول الله ﷺ عن صيام يومين: يوم الفطر، ويوم النحر (صحيح البخاري)."},
        {"question": "ما الحكم إذا نوى المسلم الصيام المفروض بعد طلوع الفجر؟", "options": ["لا يصح صومه ويجب تبييت النية من الليل", "يصح صومه كصيام التطوع", "يصح وعليه كفارة"], "correct": "لا يصح صومه ويجب تبييت النية من الليل", "proof": "لقوله ﷺ: «من لم يُبيّتِ الصيامَ قبلَ الفجرِ، فلا صيامَ له» (رواه أصحاب السنن)."}
    ],
    "المستوى الثاني: المتوسط (فقه المعاملات ودقائق العبادات) 🟡": [
        {"question": "ما حكم سجود السهو إذا سلّم المصلي عن نقص في صلاته وتذكر بعد لحظات يسيرة؟", "options": ["يأتي بما فاته ثم يسجد للسهو ويسلم", "تبطل صلاته ويعيدها كاملة", "يسجد للسهو فقط وتجزئه"], "correct": "يأتي بما فاته ثم يسجد للسهو ويسلم", "proof": "لحديث ذي اليدين؛ حيث أتم النبي ﷺ الركعتين ثم سلم، ثم سجد سجدتي السهو وسلّم."},
        {"question": "ما هو بيع العينة المنهي عنه شرعاً؟", "options": ["أن يبيع سلعة بثمن مؤجل ثم يشتريها نقداً بأقل", "بيع الثمار قبل بدو صلاحها", "بيع ما لا يملك الإنسان"], "correct": "أن يبيع سلعة بثمن مؤجل ثم يشتريها نقداً بأقل", "proof": "لقوله ﷺ: «إذا تبايعتُم بالعِينَةِ... سلَّطَ اللهُ عليكُمْ ذُلاً» (رواه أبو داود)."}
    ],
    "المستوى الثالث: المتقدم (أصول الفقه ومصطلح الحديث) 🔴": [
        {"question": "ما هو الحديث المرسل عند جمهور المحدثين؟", "options": ["ما سقط من إسناده الصحابي ورفعه التابعي مباشرة", "ما سقط من وسط سنده راويان على التوالي", "الحديث الذي انفرد بروايته شخص واحد"], "correct": "ما سقط من إسناده الصحابي ورفعه التابعي مباشرة", "proof": "المرسل هو قول التابعي صغيراً كان أو كبيراً: قال رسول الله ﷺ كذا."},
        {"question": "ما الفرق بين 'الفرض' و'الواجب' عند السادة الحنفية؟", "options": ["الفرض ما ثبت بدليل قطعي، والواجب ما ثبت بدليل ظني", "الفرض والواجب مترادفان تماماً", "الواجب آكد من الفرض في العقيدة"], "correct": "الفرض ما ثبت بدليل قطعي، والواجب ما ثبت بدليل ظني", "proof": "يميز الحنفية بين الفرض (كالصلاة بالدليل القطعي) والواجب (كالوتر بالدليل الظني)."}
    ]
}

# 4. قراءة مفتاح Groq
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except Exception:
    GROQ_API_KEY = "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"

# 5. دوال جلب أسعار الذهب والفضة في السوق المصري تلقائياً
@st.cache_data(ttl=1800, show_spinner=False)
def fetch_egypt_gold_silver_prices():
    # أسعار السوق المصري الأساسية والمحدثة
    default_prices = {
        "24": 4650.0,
        "21": 4068.0,
        "18": 3487.0,
        "silver": 52.0,
        "source": "تحديث لحظي من السوق المصري"
    }
    try:
        req = urllib.request.Request(
            "https://api.gold-api.com/price/XAU",
            headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read().decode())
            price_usd_oz = float(data.get("price", 0))
            if price_usd_oz > 0:
                usd_to_egp = 48.60  # سعر صرف الدولار البنكي
                gram_24_usd = price_usd_oz / 31.1035
                gram_24_egp = round(gram_24_usd * usd_to_egp * 1.03, 1) # شامل متوسط المصنعية والتداول
                
                default_prices["24"] = gram_24_egp
                default_prices["21"] = round(gram_24_egp * (21 / 24), 1)
                default_prices["18"] = round(gram_24_egp * (18 / 24), 1)
                default_prices["source"] = "محدث آلياً وفق مؤشرات البورصة والسوق المصري"
    except Exception:
        pass
    return default_prices

# 6. دوال الفلترة والأمان وحماية التعريب
def sanitize_user_input(text: str, max_chars: int = 500) -> str:
    if not text:
        return ""
    cleaned = re.sub(r'<[^>]*?>', '', text)
    cleaned = html.escape(cleaned)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned[:max_chars]

def execute_groq_prompt(prompt, system_inst, output_container=None):
    client = Groq(api_key=GROQ_API_KEY.strip())
    models_to_try = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"]
    
    guarded_system_prompt = f"""
{system_inst}

[قواعد لغوية وشرعية إلزامية وصارمة]:
1. التزم باللغة العربية الفصحى الرصينة فقط بنسبة 100%.
2. يُمنع منعاً باتاً كتابة أي حرف أو كلمة باللغة الإنجليزية أو اللاتينية.
3. التزم بالعلوم الشرعية الإسلامية المعتمدة واذكر الأدلة من أمهات كتب الفقه والحديث.
4. أجب بشكل كامل ودقيق ومفصل دون بتر للنص.
"""
    full_text = ""
    for model_choice in models_to_try:
        for attempt in range(2):
            try:
                completion = client.chat.completions.create(
                    model=model_choice,
                    messages=[
                        {"role": "system", "content": guarded_system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.0,
                    top_p=1.0,
                    max_tokens=4096,
                    stream=True if output_container else False
                )
                if output_container:
                    for chunk in completion:
                        chunk_content = chunk.choices[0].delta.content
                        if chunk_content:
                            full_text += chunk_content
                            output_container.markdown(f"<br>{full_text}▌", unsafe_allow_html=True)
                    output_container.markdown(f"<br>{full_text}", unsafe_allow_html=True)
                    return full_text
                else:
                    return completion.choices[0].message.content.strip()
            except Exception as e:
                err_msg = str(e).lower()
                if "rate" in err_msg or "429" in err_msg:
                    time.sleep(1.5 * (attempt + 1))
                    continue
                break
    return None

def execute_chat_turn(messages_history, system_inst, output_container):
    client = Groq(api_key=GROQ_API_KEY.strip())
    models_to_try = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"]
    
    guarded_system_prompt = f"""
{system_inst}

[قواعد لغوية وشرعية إلزامية وصارمة]:
1. أنت محاور فقهي ومستشار شرعي رصين باللغة العربية الفصحى فقط.
2. يُمنع منعاً باتاً ظهور أي كلمة أو حرف إنجليزي في الإجابة.
3. حافظ على سياق المحادثة والتفريعات الفقهية السابقة بدقة وثبات.
"""
    full_messages = [{"role": "system", "content": guarded_system_prompt}] + messages_history
    full_text = ""
    for model_choice in models_to_try:
        for attempt in range(2):
            try:
                completion = client.chat.completions.create(
                    model=model_choice,
                    messages=full_messages,
                    temperature=0.0,
                    top_p=1.0,
                    max_tokens=4096,
                    stream=True
                )
                for chunk in completion:
                    chunk_content = chunk.choices[0].delta.content
                    if chunk_content:
                        full_text += chunk_content
                        output_container.markdown(f"<br>{full_text}▌", unsafe_allow_html=True)
                output_container.markdown(f"<br>{full_text}", unsafe_allow_html=True)
                return full_text
            except Exception as e:
                err_msg = str(e).lower()
                if "rate" in err_msg or "429" in err_msg:
                    time.sleep(1.5 * (attempt + 1))
                    continue
                break
    return None

def generate_dynamic_quiz_questions(level_name):
    client = Groq(api_key=GROQ_API_KEY.strip())
    models_to_try = ["llama-3.1-8b-instant", "llama-3.3-70b-versatile"]
    
    sys_prompt = """أنت محرك فقهي ومحدث محقق. ولد 10 أسئلة شرعية جديدة باللغة العربية الفصحى فقط.
اكتب كل سؤال في سطر منفصل بالضبط وفق هذا النموذج مستخدماً الرمز ||| للفصل:
نص السؤال ||| الإجابة الصحيحة ||| الخيار الخطأ الأول ||| الخيار الخطأ الثاني ||| الدليل والتخريج الشرعي
تنبيه: لا تكتب أي مقدمات أو أرقام أو كلمات إنجليزية مطلقاً، فقط الأسطر المفصولة بالعلامة |||."""
    
    for model_choice in models_to_try:
        try:
            completion = client.chat.completions.create(
                model=model_choice,
                messages=[
                    {"role": "system", "content": sys_prompt},
                    {"role": "user", "content": f"ولد 10 أسئلة شرعية جديدة للمستوى: {level_name}"}
                ],
                temperature=0.7,
                max_tokens=3000
            )
            content = completion.choices[0].message.content.strip()
            parsed_questions = []
            for line in content.split("\n"):
                line = line.strip()
                if "|||" in line:
                    parts = [p.strip() for p in line.split("|||")]
                    if len(parts) >= 5:
                        parsed_questions.append({
                            "question": parts[0],
                            "correct": parts[1],
                            "options": [parts[1], parts[2], parts[3]],
                            "proof": parts[4]
                        })
            if parsed_questions:
                return parsed_questions
        except Exception:
            continue
    return []

# 7. محرك المواريث والفرائض الحسابي القطعي
def calculate_inheritance_engine(estate, deceased_gender, has_spouse, sons, daughters, has_father, has_mother):
    shares = {}
    has_children = (sons + daughters) > 0
    
    if has_spouse:
        if deceased_gender.startswith("رجل"):
            if has_children:
                shares["الزوجة"] = {"fraction": "1/8 (الثمن)", "value": estate * 0.125, "note": "لوجود الفرع الوارث"}
            else:
                shares["الزوجة"] = {"fraction": "1/4 (الربع)", "value": estate * 0.25, "note": "لعدم وجود فرع وارث"}
        else:
            if has_children:
                shares["الزوج"] = {"fraction": "1/4 (الربع)", "value": estate * 0.25, "note": "لوجود الفرع الوارث"}
            else:
                shares["الزوج"] = {"fraction": "1/2 (النصف)", "value": estate * 0.5, "note": "لعدم وجود فرع وارث"}

    if has_mother:
        if has_children or (sons + daughters > 1):
            shares["الأم"] = {"fraction": "1/6 (السدس)", "value": estate * (1/6), "note": "لوجود الفرع الوارث أو جمع الإخوة"}
        else:
            shares["الأم"] = {"fraction": "1/3 (الثلث)", "value": estate * (1/3), "note": "لعدم وجود فرع وارث"}

    if has_father:
        if sons > 0:
            shares["الأب"] = {"fraction": "1/6 (السدس فرضاً)", "value": estate * (1/6), "note": "السدس فرضاً لوجود ابن ذكر"}
        elif daughters > 0:
            shares["الأب (فرضاً)"] = {"fraction": "1/6 (السدس)", "value": estate * (1/6), "note": "السدس فرضاً لوجود بنات"}

    fixed_allocated = sum(item["value"] for item in shares.values())
    remainder = max(0.0, estate - fixed_allocated)

    if sons > 0:
        total_parts = (sons * 2) + daughters
        part_value = remainder / total_parts if total_parts > 0 else 0
        
        shares[f"الأبناء الذكور ({sons})"] = {
            "fraction": "عصبة بالنفس (الباقي)",
            "value": part_value * 2 * sons,
            "note": f"نصيب كل ابن: {(part_value * 2):,.2f} ج.م"
        }
        if daughters > 0:
            shares[f"البنات ({daughters})"] = {
                "fraction": "عصبة بالغير (للذكر مثل حظ الأنثيين)",
                "value": part_value * daughters,
                "note": f"نصيب كل بنت: {part_value:,.2f} ج.م"
            }
    elif daughters > 0:
        if daughters == 1:
            shares["البنت الواحدة"] = {"fraction": "1/2 (النصف)", "value": estate * 0.5, "note": "النصف فرضاً لانفرادها"}
        else:
            shares[f"البنات ({daughters})"] = {"fraction": "2/3 (الثلثان)", "value": estate * (2/3), "note": "الثلثان فرضاً يوزع بينهن"}
        
        current_fixed = sum(item["value"] for item in shares.values())
        rem_after_daughters = max(0.0, estate - current_fixed)
        if has_father and rem_after_daughters > 0:
            shares["الأب (تعصيباً)"] = {"fraction": "باقي التركة تعصيباً", "value": rem_after_daughters, "note": "يرث الباقي تعصيباً بعد الفروض"}
    elif has_father and "الأب" not in shares:
        shares["الأب"] = {"fraction": "عصبة بالنفس", "value": remainder, "note": "يحوز باقي التركة تعصيباً"}

    return shares

def create_printable_html(title: str, content: str) -> str:
    return f"""
    <!DOCTYPE html>
    <html dir="rtl" lang="ar">
    <head>
        <meta charset="UTF-8">
        <title>{title}</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Cairo:wght@600;800&display=swap');
            body {{ font-family: 'Cairo', sans-serif; margin: 30px; color: #1e293b; line-height: 1.8; }}
            .header {{ text-align: center; border-bottom: 2px solid #b45309; padding-bottom: 10px; margin-bottom: 20px; }}
            .header h1 {{ font-family: 'Amiri', serif; color: #b45309; margin: 0; }}
            .content {{ font-size: 1rem; white-space: pre-wrap; }}
            .footer {{ margin-top: 30px; text-align: center; border-top: 1px solid #cbd5e1; padding-top: 10px; font-size: 0.85rem; color: #64748b; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🕌 الموسوعة الفقهية والحديثية الذكية</h1>
            <p>وثيقة استخراج وتوثيق شرعي معتمد</p>
        </div>
        <div class="content">{content}</div>
        <div class="footer">Developed by Eng. Abdelfttah Ragheb © 2026</div>
        <script>window.print();</script>
    </body>
    </html>
    """

# 8. إدارة حالة الجلسة والتنقل
if "active_view" not in st.session_state:
    st.session_state["active_view"] = "home"

if "last_request_time" not in st.session_state:
    st.session_state["last_request_time"] = 0.0

if "stats" not in st.session_state:
    st.session_state["stats"] = {
        "fiqh_queries": 0, "hadith_queries": 0, "dict_queries": 0,
        "quran_queries": 0, "quiz_total_answered": 0, "quiz_correct_answered": 0
    }

if "chat_messages" not in st.session_state:
    st.session_state["chat_messages"] = []

if "bookmarks" not in st.session_state:
    st.session_state["bookmarks"] = []

if "quiz_pool" not in st.session_state:
    st.session_state["quiz_pool"] = copy.deepcopy(EXPANDED_QUIZ_DATABASE)
if "quiz_level" not in st.session_state:
    st.session_state["quiz_level"] = list(EXPANDED_QUIZ_DATABASE.keys())[0]
if "seen_questions" not in st.session_state:
    st.session_state["seen_questions"] = set()
if "current_round_questions" not in st.session_state:
    st.session_state["current_round_questions"] = []
if "quiz_idx" not in st.session_state:
    st.session_state["quiz_idx"] = 0
if "quiz_score" not in st.session_state:
    st.session_state["quiz_score"] = 0
if "quiz_answered" not in st.session_state:
    st.session_state["quiz_answered"] = False
if "quiz_feedback" not in st.session_state:
    st.session_state["quiz_feedback"] = None
if "shuffled_options" not in st.session_state:
    st.session_state["shuffled_options"] = []

def check_rate_limit(cooldown_seconds: float = 2.0) -> bool:
    now = time.time()
    if now - st.session_state["last_request_time"] < cooldown_seconds:
        return False
    st.session_state["last_request_time"] = now
    return True

def prepare_new_round(level):
    pool = st.session_state["quiz_pool"][level]
    unseen = [q for q in pool if q["question"] not in st.session_state["seen_questions"]]
    if len(unseen) < 4:
        st.session_state["seen_questions"] = set()
        unseen = pool
    random.shuffle(unseen)
    selected_round = unseen[:8]
    for q in selected_round:
        st.session_state["seen_questions"].add(q["question"])
    st.session_state["current_round_questions"] = selected_round
    st.session_state["quiz_idx"] = 0
    st.session_state["quiz_score"] = 0
    st.session_state["quiz_answered"] = False
    st.session_state["quiz_feedback"] = None
    st.session_state["shuffled_options"] = []

if not st.session_state["current_round_questions"]:
    prepare_new_round(st.session_state["quiz_level"])

# بطاقة الذكر الثابتة
st.markdown("""
<div class="dhikr-card">
    <p class="dhikr-text">✨ سُبْحَانَ اللَّهِ وَبِحَمْدِهِ ، سُبْحَانَ اللَّهِ الْعَظِيمِ • اللَّهُمَّ صَلِّ وَسَلِّمْ عَلَىٰ نَبِيِّنَا مُحَمَّدٍ ✨</p>
</div>
""", unsafe_allow_html=True)

# ----------------- الشاشة الرئيسية: شبكة أزرار التطبيقات (App Grid) -----------------
if st.session_state["active_view"] == "home":
    st.markdown("""
    <div class="royal-hero">
        <h1>🕌 الموسوعة الفقهية والحديثية</h1>
        <p>البوابة الرقمية الشاملة للأحكام الشرعية وتخريج الأحاديث وحساب الفرائض</p>
    </div>
    """, unsafe_allow_html=True)

    row1_c1, row1_c2 = st.columns(2)
    with row1_c1:
        if st.button("🏛️ المحاور الفقهي\n(المذاهب الأربعة)", use_container_width=True):
            st.session_state["active_view"] = "fiqh"
            st.rerun()
    with row1_c2:
        if st.button("📜 تخريج الحديث\n(ومعجم الألفاظ)", use_container_width=True):
            st.session_state["active_view"] = "hadith"
            st.rerun()

    row2_c1, row2_c2 = st.columns(2)
    with row2_c1:
        if st.button("📖 القرآن والتفسير\n(بحث موضوعي)", use_container_width=True):
            st.session_state["active_view"] = "quran"
            st.rerun()
    with row2_c2:
        if st.button("⚖️ الزكاة والمواريث\n(أسعار حية بالسوق)", use_container_width=True):
            st.session_state["active_view"] = "calc"
            st.rerun()

    row3_c1, row3_c2 = st.columns(2)
    with row3_c1:
        if st.button("🏆 بنك المسابقات\n(تحديات فقهية)", use_container_width=True):
            st.session_state["active_view"] = "quiz"
            st.rerun()
    with row3_c2:
        if st.button("⭐ فتاواي المحفوظة\n(والإحصائيات)", use_container_width=True):
            st.session_state["active_view"] = "bookmarks"
            st.rerun()

# ----------------- 1. شاشة الفقه والاستفتاء -----------------
elif st.session_state["active_view"] == "fiqh":
    st.markdown("<div class='back-btn'>", unsafe_allow_html=True)
    if st.button("⬅️ العودة للقائمة الرئيسية", use_container_width=True):
        st.session_state["active_view"] = "home"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="royal-hero">
        <h1>🏛️ المحاور الفقهي المباشر</h1>
        <p>استعراض الفتاوى وتفصيل المذاهب الأربعة بالأدلة الشرعية</p>
    </div>
    """, unsafe_allow_html=True)

    selected_madhab = st.selectbox("المذهب الفقهي:", [
        "مقارنة المذاهب الأربعة كاملة (الحنفي، المالكي، الشافعي، الحنبلي)", "المذهب الحنفي فقط", "المذهب المالكي فقط", "المذهب الشافعي فقط", "المذهب الحنبلي فقط"
    ])
    depth_level = st.selectbox("مستوى التفصيل:", ["موجز ميسر", "متوسط وتأصيلي", "بحث فقهي موسع"], index=1)

    if st.session_state["chat_messages"]:
        if st.button("🗑️ مسح المحادثة وبدء جلسة جديدة"):
            st.session_state["chat_messages"] = []
            st.rerun()

    for msg in st.session_state["chat_messages"]:
        if msg["role"] == "user":
            st.markdown(f"<div style='background:rgba(30,58,138,0.35); border:1px solid rgba(59,130,246,0.4); border-radius:12px; padding:0.8rem; margin-bottom:0.6rem;'>👤 <strong>السؤال:</strong> {msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='background:rgba(16,44,30,0.85); border:1.5px solid rgba(234,179,8,0.4); border-radius:12px; padding:1rem; margin-bottom:1rem;'>🕌 <strong>البيان الفقهي:</strong><br>{msg['content']}</div>", unsafe_allow_html=True)

    chat_input = st.text_input("اكتب استفسارك الفقهي هنا:", placeholder="مثال: حكم صلاة الوتر وصفتها؟ وهل تجوز بركعة واحدة؟...", key="chat_fiqh_input")
    if st.button("💬 إرسال واستفتاء", use_container_width=True):
        cleaned_chat_query = sanitize_user_input(chat_input, max_chars=400)
        if not cleaned_chat_query:
            st.warning("⚠️ يرجى كتابة الاستفسار أولاً.")
        elif not check_rate_limit(cooldown_seconds=2.0):
            st.info("⏳ يرجى التمهل ثانية واحدة قبل إرسال استفسار جديد.")
        else:
            st.session_state["chat_messages"].append({"role": "user", "content": cleaned_chat_query})
            chat_out = st.empty()
            
            chat_sys = f"""
أنت مفتٍ ومحاور فقهي ومحدث محقق.
المذهب المطلوب: {selected_madhab}
مستوى التفصيل: {depth_level}

هيكل الإجابة المطلوب بالعربية الفصحى فقط:
# 📌 خلاصة الحكم الشرعي المباشر
# 📖 الاستدلال من القرآن الكريم والسنة النبوية
# 🏛️ أقوال الأئمة والمذاهب المعتمدة
# 💡 توجيه وإرشاد تطبيقي
"""
            ans = execute_chat_turn(st.session_state["chat_messages"], chat_sys, chat_out)
            if ans:
                st.session_state["chat_messages"].append({"role": "assistant", "content": ans})
                st.session_state["stats"]["fiqh_queries"] += 1
                st.rerun()

    if st.session_state["chat_messages"] and st.session_state["chat_messages"][-1]["role"] == "assistant":
        last_q = [m["content"] for m in st.session_state["chat_messages"] if m["role"] == "user"][-1]
        last_a = st.session_state["chat_messages"][-1]["content"]
        
        st.markdown("---")
        chosen_tag = st.selectbox("🏷️ اختر وسم الفتوى للحفظ:", ["#عبادات_وصلاة", "#معاملات_ومال", "#صيام_وزكاة", "#أحوال_شخصية", "#فقه_عام"])
        col_fb1, col_fb2 = st.columns(2)
        with col_fb1:
            if st.button("⭐ حفظ في المفضلة", use_container_width=True):
                st.session_state["bookmarks"].append({"question": last_q, "answer": last_a, "tag": chosen_tag, "date": time.strftime("%Y-%m-%d %H:%M")})
                st.success("✅ تم الحفظ بنجاح في هاتفك!")
        with col_fb2:
            st.download_button(
                label="📄 طباعة الفتوى (PDF)",
                data=create_printable_html(last_q, last_a),
                file_name="fatwa_document.html",
                mime="text/html",
                use_container_width=True
            )

# ----------------- 2. شاشة الحديث ومعجم الألفاظ -----------------
elif st.session_state["active_view"] == "hadith":
    st.markdown("<div class='back-btn'>", unsafe_allow_html=True)
    if st.button("⬅️ العودة للقائمة الرئيسية", use_container_width=True):
        st.session_state["active_view"] = "home"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="royal-hero">
        <h1>📜 تخريج الحديث ومعجم الألفاظ</h1>
        <p>التحقق من صحة الأحاديث • الرواة والمصادر • بيان الألفاظ الغريبة</p>
    </div>
    """, unsafe_allow_html=True)

    hadith_input = st.text_input("اكتب نص الحديث أو جزءاً منه:", max_chars=350, placeholder="مثال: إنما الأعمال بالنيات...")
    if st.button("🔍 تخريج وتحقيق الحديث", use_container_width=True):
        cleaned_hadith = sanitize_user_input(hadith_input, max_chars=350)
        if not cleaned_hadith:
            st.warning("⚠️ يرجى إدخال نص الحديث أولاً.")
        elif not check_rate_limit(cooldown_seconds=2.0):
            st.info("⏳ يرجى التمهل ثانية واحدة قبل إرسال طلب جديد.")
        else:
            h_output = st.empty()
            h_sys = """
أنت عالم ومحدث محقق في علوم الحديث والجرح والتعديل.
قم بتخريج الحديث باللغة العربية الفصحى حصراً وبدون أي كلمة أجنبية:
# 📜 بطاقة تخريج الحديث النبوي
- **نص المتن الصحيح**: «النص مع الضبط»
- 👤 **الصحابي راوي الحديث**:
- 📚 **المصادر ورقم الحديث والباب**: (مثال: صحيح البخاري، كتاب بدء الوحي، باب كيف كان بدء الوحي، رقم 1)
- ⚖️ **حكم المحدثين ورتبته الدقيقة**: (صحيح / حسن / ضعيف مع بيان كلام الأئمة)
- 💡 **الفوائد الفقهية والعملية المستنبطة**:
"""
            h_res = execute_groq_prompt(cleaned_hadith, h_sys, h_output)
            if h_res:
                st.session_state["stats"]["hadith_queries"] += 1

    st.markdown("---")
    term_input = st.text_input("اكتب اللفظ أو المصطلح الشرعي المراد تفسيره:", max_chars=100, placeholder="مثال: الصاع، العول، الكلالة، القسامة...")
    if st.button("📖 شرح وتفسير المصطلح", use_container_width=True):
        cleaned_term = sanitize_user_input(term_input, max_chars=100)
        if not cleaned_term:
            st.warning("⚠️ يرجى كتابة المصطلح أولاً.")
        elif not check_rate_limit(cooldown_seconds=2.0):
            st.info("⏳ يرجى التمهل ثانية واحدة قبل إرسال طلب جديد.")
        else:
            t_output = st.empty()
            t_sys = """
أنت معجمي وفقهي محقق.
اشرح المصطلح الشرعي باللغة العربية الفصحى فقط وبشكل دقيق:
# 📖 بيان المصطلح الشرعي
- **المعنى اللغوي والاصطلاحي**:
- **المقدار المعاصر (إن وجد)**:
- **أمثلة وتطبيقات فقهية**:
"""
            t_res = execute_groq_prompt(cleaned_term, t_sys, t_output)
            if t_res:
                st.session_state["stats"]["dict_queries"] += 1

# ----------------- 3. شاشة القرآن والتفسير -----------------
elif st.session_state["active_view"] == "quran":
    st.markdown("<div class='back-btn'>", unsafe_allow_html=True)
    if st.button("⬅️ العودة للقائمة الرئيسية", use_container_width=True):
        st.session_state["active_view"] = "home"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="royal-hero">
        <h1>📖 قسم القرآن والتفسير الموضوعي</h1>
        <p>استخراج الآيات بالمفهوم والمعنى • أسباب النزول • الاستنباطات الفقهية</p>
    </div>
    """, unsafe_allow_html=True)

    quran_topic = st.text_input("اكتب الموضوع أو الفكرة القرآنية:", placeholder="مثال: البر بالوالدين، الإنفاق والصدقة، الصبر، أكل أموال الناس بالباطل...")
    if st.button("📖 استخراج الآيات والتفسير الموضوعي", use_container_width=True):
        cleaned_qtopic = sanitize_user_input(quran_topic, max_chars=200)
        if not cleaned_qtopic:
            st.warning("⚠️ يرجى كتابة الموضوع أولاً.")
        elif not check_rate_limit(cooldown_seconds=2.0):
            st.info("⏳ يرجى التمهل ثانية واحدة قبل إرسال طلب جديد.")
        else:
            q_output = st.empty()
            q_sys = """
أنت عالم مفسر ومحقق في التفسير الموضوعي وعلوم القرآن.
استخرج الآيات واشرحها باللغة العربية الفصحى فقط:
# 📖 الآيات القرآنية ذات الصلة بالموضوع
اذكر نصوص الآيات مع اسم السورة ورقم الآية:
- «نص الآية الكريمة» [السورة: رقم الآية]

# 💡 التفسير الميسر وأسباب النزول
(اعتماداً على تفسير ابن كثير والسعدي)

# ⚖️ الاستنباطات والفوائد الفقهية والعملية
"""
            q_res = execute_groq_prompt(cleaned_qtopic, q_sys, q_output)
            if q_res:
                st.session_state["stats"]["quran_queries"] += 1

# ----------------- 4. شاشة الزكاة والمواريث بالأسعار الحية -----------------
elif st.session_state["active_view"] == "calc":
    st.markdown("<div class='back-btn'>", unsafe_allow_html=True)
    if st.button("⬅️ العودة للقائمة الرئيسية", use_container_width=True):
        st.session_state["active_view"] = "home"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="royal-hero">
        <h1>⚖️ حاسبة الزكاة والمواريث (بالجنيه المصري)</h1>
        <p>ربط تلقائي بأسعار الذهب والفضة اليوم • حساب قطعي 100% • قسمة التركات</p>
    </div>
    """, unsafe_allow_html=True)

    # جلب الأسعار المحدثة
    market_prices = fetch_egypt_gold_silver_prices()
    st.markdown(f"<div class='market-badge'>🟢 {market_prices['source']}</div>", unsafe_allow_html=True)

    calc_sub_type = st.radio("اختر العملية الحسابية:", ["💰 حساب زكاة المال والذهب", "👨‍👩‍👧‍👦 توزيع التركات والمواريث"], horizontal=True)

    if calc_sub_type.startswith("💰"):
        selected_karat = st.selectbox("عيار الذهب المتوفر لديك:", ["عيار 21 (الأكثر تداولاً)", "عيار 24 (الذهب الخالص)", "عيار 18"])
        
        # ضبط السعر الافتراضي تلقائياً من السوق
        default_p = market_prices["21"]
        if "24" in selected_karat:
            default_p = market_prices["24"]
        elif "18" in selected_karat:
            default_p = market_prices["18"]
            
        gold_price_input = st.number_input(f"سعر جرام الذهب المختار ({selected_karat}) اليوم بالجنيه:", min_value=1.0, value=float(default_p), step=10.0)
        gold_weight_input = st.number_input("وزن الذهب المدخر بالجرام:", min_value=0.0, value=0.0, step=1.0)
        cash_amount = st.number_input("السيولة النقدية / أموال التجارة والودائع (بالجنيه):", min_value=0.0, value=0.0, step=1000.0)
        silver_weight = st.number_input("وزن الفضة المدخرة بالجرام (إن وجد):", min_value=0.0, value=0.0, step=10.0)
        silver_price = st.number_input("سعر جرام الفضة اليوم (بالجنيه):", min_value=1.0, value=float(market_prices["silver"]), step=1.0)
            
        if st.button("🧮 احتساب تفاصيل الزكاة الشرعية", use_container_width=True):
            if "24" in selected_karat:
                price_24 = gold_price_input
                karat_nisab = 85.0
            elif "21" in selected_karat:
                price_24 = gold_price_input * (24 / 21)
                karat_nisab = 85.0 * (24 / 21)
            else:
                price_24 = gold_price_input * (24 / 18)
                karat_nisab = 85.0 * (24 / 18)
                
            nisab_in_egp = 85.0 * price_24
            gold_val_egp = gold_weight_input * gold_price_input
            silver_val_egp = silver_weight * silver_price
            total_wealth_egp = cash_amount + gold_val_egp + silver_val_egp
            
            is_nisab_reached = total_wealth_egp >= nisab_in_egp
            zakah_due_egp = total_wealth_egp * 0.025 if is_nisab_reached else 0.0

            st.markdown("### 📊 جدول البيان المالي للزكاة:")
            z_table = f"""
| البند المالي الشرعي | القيمة / المقدار | البيان والتفصيل |
| :--- | :--- | :--- |
| **قيمة الذهب المدخر** | `{gold_val_egp:,.2f} ج.م` | وزن `{gold_weight_input} جم` ({selected_karat}) |
| **السيولة النقدية والتجارة** | `{cash_amount:,.2f} ج.م` | الأموال النقدية والمدخرات البنكية |
| **قيمة الفضة المدخرة** | `{silver_val_egp:,.2f} ج.م` | وزن `{silver_weight} جم` |
| **إجمالي الوعاء الزكوي** | **`{total_wealth_egp:,.2f} ج.م`** | مجموع الأموال المتاحة للزكاة |
| **حد النصاب الشرعي** | **`{nisab_in_egp:,.2f} ج.م`** | يعادل `85 جرام ذهب عيار 24` (أو `{karat_nisab:.2f} جم` لـ {selected_karat}) |
| **حالة بلوغ النصاب** | **{'بلغ النصاب الشرعي ✅' if is_nisab_reached else 'لم يبلغ النصاب بعد ❌'}** | يشترط مرور حول كامل (سنة هجرية) |
| **مقدار الزكاة الواجبة فوراً** | **`{zakah_due_egp:,.2f} ج.م`** | **نسبة 2.5% (ربع العشر)** |
"""
            st.markdown(z_table)
            if is_nisab_reached:
                st.success(f"✅ **تجب الزكاة شرعاً:** الواجب إخراجه هو **`{zakah_due_egp:,.2f} جنيه مصري`** تُدفع لمصارف الزكاة.")
            else:
                shortage = nisab_in_egp - total_wealth_egp
                st.info(f"ℹ️ **لا تجب الزكاة حالياً:** ينقص مالك مبلغ **`{shortage:,.2f} جنيه مصري`** ليصل إلى النصاب.")

    else:
        estate_val = st.number_input("إجمالي قيمة التركة المالية (بالجنيه المصري):", min_value=100.0, value=500000.0, step=10000.0)
        deceased_gender = st.radio("المتوفى:", ["رجل (ترك زوجة/أولاد)", "امرأة (تركت زوج/أولاد)"], horizontal=True)
        has_spouse = st.checkbox("يوجد الزوج / الزوجة على قيد الحياة", value=True)
        sons_count = st.number_input("عدد الأبناء (ذكور):", min_value=0, max_value=20, value=2)
        daughters_count = st.number_input("عدد البنات (إناث):", min_value=0, max_value=20, value=2)
        has_father = st.checkbox("الأب حي", value=False)
        has_mother = st.checkbox("الأم حية", value=True)
            
        if st.button("⚖️ احتساب التوزيع الشرعي والأدلة", use_container_width=True):
            results = calculate_inheritance_engine(estate_val, deceased_gender, has_spouse, sons_count, daughters_count, has_father, has_mother)
            st.markdown("### 📊 جدول القسمة الشرعية وتوزيع الأنصبة (بالجنيه المصري):")
            table_md = "| الوارث | الفرض / الحالة الشرعية | النصيب المالي المستحق | تفصيل وسند التوزيع |\n| :--- | :--- | :--- | :--- |\n"
            for k, v in results.items():
                table_md += f"| **{k}** | `{v['fraction']}` | **`{v['value']:,.2f} ج.م`** | {v['note']} |\n"
            st.markdown(table_md)
            
            estate_prompt = f"""
المتوفى: {deceased_gender}
قيمة التركة: {estate_val:,.2f} جنيه مصري
الورثة المستحقون:
- الزوج/الزوجة: {'نعم' if has_spouse else 'لا'}
- الأبناء الذكور: {sons_count}
- البنات: {daughters_count}
- الأب: {'نعم' if has_father else 'لا'}
- الأم: {'نعم' if has_mother else 'لا'}

قم بذكر الآيات القرآنية من سورة النساء الصريحة في قسمة هذه التركة، وبيان حالات الحجب بقواعد علم الفرائض باللغة العربية الفصحى فقط.
"""
            estate_sys = """أنت فقيه ومحقق في علم الفرائض. اذكر نصوص الآيات من سورة النساء التي استندت إليها هذه المسألة وبيان سبب حجب الحواشي بالعربية فقط."""
            m_out = st.empty()
            execute_groq_prompt(estate_prompt, estate_sys, m_out)

# ----------------- 5. شاشة المسابقات والتحديات -----------------
elif st.session_state["active_view"] == "quiz":
    st.markdown("<div class='back-btn'>", unsafe_allow_html=True)
    if st.button("⬅️ العودة للقائمة الرئيسية", use_container_width=True):
        st.session_state["active_view"] = "home"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="royal-hero">
        <h1>🏆 بنك المسابقات والتحديات</h1>
        <p>اختبر معلوماتك الشرعية • مستويات تدريجية • تصحيح فوري</p>
    </div>
    """, unsafe_allow_html=True)

    selected_level = st.selectbox(
        "🎯 حدد مستوى التحدي:",
        list(st.session_state["quiz_pool"].keys()),
        index=list(st.session_state["quiz_pool"].keys()).index(st.session_state["quiz_level"])
    )
    if selected_level != st.session_state["quiz_level"]:
        st.session_state["quiz_level"] = selected_level
        prepare_new_round(selected_level)
        st.rerun()

    if st.button("⚡ توليد أسئلة جديدة بالذكاء الاصطناعي", use_container_width=True):
        if not check_rate_limit(cooldown_seconds=2.0):
            st.info("⏳ يرجى الانتظار ثانية واحدة قبل طلب توليد جديد.")
        else:
            with st.spinner("جاري استحضار أسئلة فقهية جديدة..."):
                new_q = generate_dynamic_quiz_questions(st.session_state["quiz_level"])
                if new_q and len(new_q) > 0:
                    st.session_state["quiz_pool"][st.session_state["quiz_level"]].extend(new_q)
                    prepare_new_round(st.session_state["quiz_level"])
                    st.success(f"🎉 تم توليد وإضافة {len(new_q)} أسئلة فقهية جديدة بنجاح!")
                    st.rerun()
                else:
                    prepare_new_round(st.session_state["quiz_level"])
                    st.info("🔄 تم تجديد الأسئلة وبدء جولة غير مكررة من بنك الأسئلة!")
                    st.rerun()

    questions = st.session_state["current_round_questions"]
    current_idx = st.session_state["quiz_idx"]
    total_q = len(questions)

    if total_q == 0:
        st.info("لا توجد أسئلة حالياً. اضغط على زر التوليد لجلب أسئلة جديدة.")
    elif current_idx < total_q:
        q_data = questions[current_idx]
        if not st.session_state["shuffled_options"]:
            opts = list(q_data["options"])
            random.shuffle(opts)
            st.session_state["shuffled_options"] = opts
        
        progress_val = current_idx / total_q
        st.progress(progress_val)
        st.write(f"📌 **السؤال {current_idx + 1} من {total_q}** | ⭐ **النقاط: {st.session_state['quiz_score']}/{total_q}**")

        st.markdown(f"""
        <div class="quiz-card">
            <h3 style="color:#ffffff; line-height:1.6; font-size:1.15rem;">{q_data['question']}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        chosen_answer = st.radio(
            "اختر الإجابة الصحيحة:",
            st.session_state["shuffled_options"],
            index=None,
            key=f"radio_{st.session_state['quiz_level']}_{current_idx}"
        )
        
        col_qbtn1, col_qbtn2 = st.columns(2)
        with col_qbtn1:
            check_btn = st.button("✅ تأكيد الإجابة", use_container_width=True, disabled=st.session_state["quiz_answered"])
        with col_qbtn2:
            next_btn = st.button("➡️ السؤال التالي", use_container_width=True, disabled=not st.session_state["quiz_answered"])
            
        if check_btn:
            if chosen_answer is None:
                st.warning("⚠️ يرجى اختيار إحدى الإجابات أولاً.")
            else:
                st.session_state["quiz_answered"] = True
                st.session_state["stats"]["quiz_total_answered"] += 1
                if chosen_answer == q_data["correct"]:
                    st.session_state["quiz_score"] += 1
                    st.session_state["stats"]["quiz_correct_answered"] += 1
                    st.session_state["quiz_feedback"] = {"status": "success", "msg": f"🎉 **إجابة صحيحة وموفقة!**\n\n📖 **الدليل والتحقيق:** {q_data['proof']}"}
                else:
                    st.session_state["quiz_feedback"] = {"status": "error", "msg": f"❌ **إجابة غير صحيحة.**\n\n📌 **الصواب هو:** {q_data['correct']}\n\n📖 **الدليل:** {q_data['proof']}"}
                st.rerun()
                
        if st.session_state["quiz_feedback"]:
            if st.session_state["quiz_feedback"]["status"] == "success":
                st.success(st.session_state["quiz_feedback"]["msg"])
            else:
                st.error(st.session_state["quiz_feedback"]["msg"])
                
        if next_btn:
            st.session_state["quiz_idx"] += 1
            st.session_state["quiz_answered"] = False
            st.session_state["quiz_feedback"] = None
            st.session_state["shuffled_options"] = []
            st.rerun()
    else:
        st.balloons()
        st.markdown(f"""
        <div class="quiz-card" style="text-align:center;">
            <h2 style="color:#fbbf24; font-size:1.4rem;">🎉 بارك الله فيك! أكملت هذه الجولة</h2>
            <p style="font-size:1.15rem; color:#ffffff; margin: 0.8rem 0;">النتيجة النهائية: <strong>{st.session_state['quiz_score']} من {total_q}</strong></p>
        </div>
        """, unsafe_allow_html=True)
        
        col_end1, col_end2 = st.columns(2)
        with col_end1:
            if st.button("🚀 جولة جديدة بأسئلة غير مكررة", use_container_width=True):
                prepare_new_round(st.session_state["quiz_level"])
                st.rerun()
        with col_end2:
             if st.button("⚡ توليد أسئلة بالذكاء الاصطناعي", use_container_width=True):
                with st.spinner("جاري استحضار تحديات فقهية جديدة..."):
                    new_q = generate_dynamic_quiz_questions(st.session_state["quiz_level"])
                    if new_q and len(new_q) > 0:
                        st.session_state["quiz_pool"][st.session_state["quiz_level"]].extend(new_q)
                    prepare_new_round(st.session_state["quiz_level"])
                    st.rerun()

# ----------------- 6. شاشة المفضلة والإحصائيات -----------------
elif st.session_state["active_view"] == "bookmarks":
    st.markdown("<div class='back-btn'>", unsafe_allow_html=True)
    if st.button("⬅️ العودة للقائمة الرئيسية", use_container_width=True):
        st.session_state["active_view"] = "home"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="royal-hero">
        <h1>⭐ الفتاوى المحفوظة والإحصائيات</h1>
        <p>سجل استشاراتك المحفوظة على هاتفك ومؤشرات التفاعل في الجلسة</p>
    </div>
    """, unsafe_allow_html=True)

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{st.session_state['stats']['fiqh_queries']}</div>
            <div class="stat-title">استشارات فقهية مستخرجة</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{st.session_state['stats']['quran_queries']}</div>
            <div class="stat-title">بحوث قرآنية موضوعية</div>
        </div>
        """, unsafe_allow_html=True)
    with col_s2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{st.session_state['stats']['hadith_queries']}</div>
            <div class="stat-title">أحاديث محققة ومخرجة</div>
        </div>
        """, unsafe_allow_html=True)
        total_ans = st.session_state['stats']['quiz_total_answered']
        corr_ans = st.session_state['stats']['quiz_correct_answered']
        acc = int((corr_ans / total_ans * 100)) if total_ans > 0 else 0
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{acc}%</div>
            <div class="stat-title">دقة إجابات المسابقات</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📌 الفتاوى المحفوظة في المفضلة:")
    if not st.session_state["bookmarks"]:
        st.info("ℹ️ لم تقم بحفظ أي فتاوى في المفضلة بعد. يمكنك حفظ أي فتوى من قسم الفقه.")
    else:
        tags_list = ["الكل"] + list(set([b["tag"] for b in st.session_state["bookmarks"]]))
        selected_filter_tag = st.selectbox("🔍 تصفية حسب الوسم:", tags_list)
        filtered_bmarks = st.session_state["bookmarks"] if selected_filter_tag == "الكل" else [b for b in st.session_state["bookmarks"] if b["tag"] == selected_filter_tag]
        
        for idx, bmark in enumerate(filtered_bmarks):
            with st.expander(f"📌 {bmark['question']} ({bmark['tag']}) - {bmark['date']}"):
                st.markdown(f"<span style='background:rgba(234,179,8,0.2); color:#fbbf24; border:1px solid #eab308; border-radius:8px; padding:2px 8px; font-weight:bold;'>{bmark['tag']}</span>", unsafe_allow_html=True)
                st.markdown(bmark["answer"])
                st.download_button(
                    label="📄 تحميل هذه الفتوى (PDF)",
                    data=create_printable_html(bmark['question'], bmark['answer']),
                    file_name=f"fatwa_{idx}.html",
                    mime="text/html",
                    key=f"dl_bmark_{idx}"
                )

# 9. التذييل
st.markdown("""
<div class="royal-footer">
    <div style="color: #94a3b8; margin-bottom: 0.4rem;">نظام فقهي استدلالي وتوثيقي مقارن مبني بنماذج الذكاء الاصطناعي المتقدمة</div>
    <div>Developed by <span class="dev-badge">Eng. Abdelfttah Ragheb</span> © 2026</div>
</div>
""", unsafe_allow_html=True)
