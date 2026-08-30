import os
import json
import random
import streamlit as st
from groq import Groq
import copy
# إعداد الصفحة
st.set_page_config(
    page_title="الموسوعة الفقهية والحديثية الذكية",
    page_icon="🕌",
    layout="wide",
    initial_sidebar_state="expanded"
)
# تخصيص واجهة المستخدم: متجاوبة 100% مع الهواتف والشاشات الكبيرة + ثيم أندلسي ملكي
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Amiri:ital,wght@0,400;0,700;1,400&family=Aref+Ruqaa:wght@700&family=Cairo:wght@400;600;700;800;900&display=swap');
    
    * {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
        box-sizing: border-box;
    }
    
    .stApp {
        background: radial-gradient(circle at 50% 0%, #0b1528 0%, #050b14 65%, #02050a 100%);
        color: #ffffff;
        overflow-x: hidden !important;
    }
    /* الشريط العلوي */
    .ticker-wrap {
        width: 100%;
        overflow: hidden;
        background: linear-gradient(90deg, rgba(234, 179, 8, 0.05) 0%, rgba(234, 179, 8, 0.22) 50%, rgba(234, 179, 8, 0.05) 100%);
        border: 1.5px solid rgba(234, 179, 8, 0.5);
        border-radius: 50px;
        padding: 0.6rem 0;
        margin-bottom: 1.5rem;
        box-shadow: 0 0 20px rgba(234, 179, 8, 0.15);
        position: relative;
        white-space: nowrap;
    }
    .ticker-move {
        display: inline-block;
        white-space: nowrap;
        animation: tickerAnim 30s linear infinite;
    }
    .ticker-item {
        display: inline-block;
        font-family: 'Amiri', serif;
        font-size: 1.25rem;
        font-weight: 700;
        color: #fef08a;
        margin: 0 1.5rem;
    }
    .ticker-bullet {
        color: #38bdf8;
        margin: 0 0.5rem;
    }
    @keyframes tickerAnim {
        0% { transform: translateX(0); }
        100% { transform: translateX(50%); }
    }
    /* الهيدر الملكي المتجاوب */
    .royal-hero {
        background: linear-gradient(135deg, rgba(15, 29, 54, 0.85) 0%, rgba(8, 16, 32, 0.95) 100%);
        border: 2px solid rgba(234, 179, 8, 0.5);
        border-radius: 20px;
        padding: 2rem 1.2rem;
        margin-bottom: 1.5rem;
        text-align: center;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.7);
    }
    .royal-hero h1 {
        font-family: 'Aref Ruqaa', serif;
        color: #fbbf24;
        font-size: 2.3rem;
        margin-bottom: 0.5rem;
        line-height: 1.3;
    }
    .royal-hero p {
        color: #93c5fd;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0;
    }
    /* تحسين علامات التبويب للهاتف */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(15, 29, 54, 0.6);
        padding: 6px;
        border-radius: 14px;
        border: 1px solid rgba(234, 179, 8, 0.3);
        flex-wrap: wrap;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        color: #cbd5e1;
        font-weight: 700;
        font-size: 1.05rem;
        padding: 8px 14px;
        white-space: normal;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(234, 179, 8, 0.3) 0%, rgba(234, 179, 8, 0.12) 100%) !important;
        color: #fbbf24 !important;
        border: 1px solid rgba(234, 179, 8, 0.6) !important;
    }
    /* تحسين نصوص الإدخال والأزرار للهاتف */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background: rgba(15, 29, 54, 0.9) !important;
        color: #ffffff !important;
        border: 1.5px solid rgba(234, 179, 8, 0.5) !important;
        border-radius: 12px !important;
        padding: 0.8rem 1rem !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
    }
    .stRadio label {
        font-size: 1.15rem !important;
        font-weight: 600 !important;
        color: #f1f5f9 !important;
        padding: 4px 0;
    }
    .stSelectbox label, .stMultiSelect label, .stSlider label {
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        color: #facc15 !important;
    }
    .stButton>button {
        background: linear-gradient(135deg, #f59e0b 0%, #b45309 100%) !important;
        color: #ffffff !important;
        font-weight: 800 !important;
        font-size: 1.15rem !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.5rem !important;
        width: 100%;
        margin-top: 0.5rem;
    }
    /* نصوص الفتاوى والنتائج */
    .stMarkdown {
        font-size: 1.15rem !important;
        line-height: 2 !important;
        color: #f8fafc !important;
    }
    .stMarkdown h1 {
        font-family: 'Amiri', serif !important;
        color: #fbbf24 !important;
        font-size: 1.8rem !important;
        border-bottom: 1.5px solid rgba(234, 179, 8, 0.4) !important;
        padding-bottom: 0.4rem !important;
        margin-top: 1.5rem !important;
    }
    .stMarkdown h2, .stMarkdown h3 {
        font-family: 'Amiri', serif !important;
        color: #38bdf8 !important;
        font-size: 1.45rem !important;
    }
    /* الجداول */
    table {
        width: 100% !important;
        overflow-x: auto;
        display: block;
        margin: 1.5rem 0 !important;
        background: rgba(15, 29, 54, 0.8) !important;
        border: 1px solid rgba(234, 179, 8, 0.45) !important;
        border-radius: 12px !important;
    }
    th, td {
        padding: 10px 14px !important;
        font-size: 1rem !important;
    }
    .quiz-card {
        background: rgba(15, 29, 54, 0.95);
        border: 1.5px solid #eab308;
        border-radius: 16px;
        padding: 1.4rem;
        margin-bottom: 1rem;
    }
    .royal-footer {
        margin-top: 3rem;
        padding: 1.5rem 1rem;
        border-top: 1px solid rgba(234, 179, 8, 0.35);
        background: linear-gradient(180deg, transparent 0%, rgba(11, 21, 40, 0.95) 100%);
        border-radius: 16px 16px 0 0;
        text-align: center;
    }
    .dev-badge {
        display: inline-block;
        background: rgba(234, 179, 8, 0.18);
        border: 1px solid rgba(234, 179, 8, 0.5);
        padding: 0.3rem 1rem;
        border-radius: 15px;
        color: #facc15;
        font-weight: 800;
        font-size: 1rem;
    }
</style>
""", unsafe_allow_html=True)
# بنك الأسئلة الموسع
EXPANDED_QUIZ_DATABASE = {
    "المستوى الأول: المبتدئ (فقه العبادات الأساسي) 🟢": [
        {"question": "ما حكم قراءة سورة الفاتحة للإمام والمنفرد في الصلاة المفروضة؟", "options": ["ركن لا تصح الصلاة إلا به", "سنة مستحبة وتصح الصلاة بدونها", "واجب يجبره سجود السهو"], "correct": "ركن لا تصح الصلاة إلا به", "proof": "لقول النبي ﷺ: «لا صلاةَ لمَن لم يقرَأْ بفاتحةِ الكتابِ» (متفق عليه)."},
        {"question": "ما هو الحد الأدنى لنصاب الذهب الذي تجب فيه الزكاة بالجرامات؟", "options": ["85 جراماً من الذهب الخالص", "50 جراماً", "120 جراماً"], "correct": "85 جراماً من الذهب الخالص", "proof": "النصاب الشرعي للذهب عشرون ديناراً، وتساوي 85 جراماً من الذهب عيار 24."},
        {"question": "ما حكم صيام يومي عيدي الفطر والأضحى؟", "options": ["محرم باتفاق العلماء", "مكروه كراهة تنزيه", "مباح لمن كان عليه قضاء"], "correct": "محرم باتفاق العلماء", "proof": "نهى رسول الله ﷺ عن صيام يومين: يوم الفطر، ويوم النحر (صحيح البخاري)."},
        {"question": "ما الحكم إذا نوى المسلم الصيام المفروض بعد طلوع الفجر؟", "options": ["لا يصح صومه ويجب تبييت النية من الليل", "يصح صومه كصيام التطوع", "يصح وعليه كفارة"], "correct": "لا يصح صومه ويجب تبييت النية من الليل", "proof": "لقوله ﷺ: «من لم يُبيّتِ الصيامَ قبلَ الفجرِ، فلا صيامَ له» (رواه أصحاب السنن)."},
        {"question": "كم عدد التكبيرات الزوائد في الركعة الأولى من صلاة العيد عند جمهور العلماء؟", "options": ["سبع تكبيرات مع تكبيرة الإحرام", "ثلاث تكبيرات فقط", "خمس تكبيرات"], "correct": "سبع تكبيرات مع تكبيرة الإحرام", "proof": "ثبت عن النبي ﷺ أنه كبّر في العيدين في الأولى سبعاً وفي الثانية خمساً."},
        {"question": "ما هو الركن الأعظم في الحج الذي يفوت الحج بفواته؟", "options": ["الوقوف بعرفة", "طواف الإفاضة", "السعي بين الصفا والمروة"], "correct": "الوقوف بعرفة", "proof": "لقوله ﷺ الصريح: «الحجُّ عرفةُ» (رواه الترمذي وأحمد)."},
        {"question": "ما حكم الوضوء من أكل لحم الإبل؟", "options": ["ينقض الوضوء عند الحنابلة ومذهب الحديث", "لا ينقض الوضوء عند جميع المذاهب", "مستحب فقط"], "correct": "ينقض الوضوء عند الحنابلة ومذهب الحديث", "proof": "لحديث جابر بن سمرة رضي الله عنه: أن رجلاً سأل النبي ﷺ: أنتوضأ من لحوم الإبل؟ قال: «نعم» (صحيح مسلم)."},
        {"question": "ما هو أقل مدة للاعتكاف المسنون في المسجد؟", "options": ["لحظة أو ساعة بنية الاعتكاف عند الجمهور", "يوم وليلة كاملين حتماً", "عشرة أيام كاملة"], "correct": "لحظة أو ساعة بنية الاعتكاف عند الجمهور", "proof": "يصح الاعتكاف عند الشافعية والحنابلة ولو زمناً يسيراً مع النية في المسجد."},
        {"question": "ما حكم من نسي التسمية في أول الوضوء وتذكر في أثنائه؟", "options": ["يسمي ويكمل وضوءه ولا يعيد", "يبطل وضوءه ويجب أن يعيده", "الوضوء صحيح ولا يلزمه شيء"], "correct": "يسمي ويكمل وضوءه ولا يعيد", "proof": "التسمية سنة مؤكدة، وإن نسيها وتذكر في الأثناء سمى وأكمل."},
        {"question": "أين يكون موضع اليدين في السجود الصحيح؟", "options": ["حذو المنكبين أو فروع الأذنين", "أمام الرأس بكثير", "ملاصقة للركبتين"], "correct": "حذو المنكبين أو فروع الأذنين", "proof": "هكذا وصف الصحابة سجود النبي ﷺ كما في حديث وائل بن حجر وغيره."}
    ],
    "المستوى الثاني: المتوسط (فقه المعاملات ودقائق العبادات) 🟡": [
        {"question": "ما حكم سجود السهو إذا سلّم المصلي عن نقص في صلاته وتذكر بعد لحظات يسيرة؟", "options": ["يأتي بما فاته ثم يسجد للسهو ويسلم", "تبطل صلاته ويعيدها كاملة", "يسجد للسهو فقط وتجزئه"], "correct": "يأتي بما فاته ثم يسجد للسهو ويسلم", "proof": "لحديث ذي اليدين؛ حيث أتم النبي ﷺ الركعتين ثم سلم، ثم سجد سجدتي السهو وسلّم."},
        {"question": "ما هو بيع العينة المنهي عنه شرعاً؟", "options": ["أن يبيع سلعة بثمن مؤجل ثم يشتريها نقداً بأقل", "بيع الثمار قبل بدو صلاحها", "بيع ما لا يملك الإنسان"], "correct": "أن يبيع سلعة بثمن مؤجل ثم يشتريها نقداً بأقل", "proof": "لقوله ﷺ: «إذا تبايعتُم بالعِينَةِ... سلَّطَ اللهُ عليكُمْ ذُلاً» (رواه أبو داود)."},
        {"question": "ما حكم مسح الخفين للمسافر والمقيم من حيث المدة؟", "options": ["يوم وليلة للمقيم، وثلاثة أيام بلياليها للمسافر", "يومان للمقيم، وأربعة للمسافر", "يوم وليلة للجميع بلا تفريق"], "correct": "يوم وليلة للمقيم، وثلاثة أيام بلياليها للمسافر", "proof": "لحديث علي بن أبي طالب رضي الله عنه في صحيح مسلم بتحديد هذه المدد."},
        {"question": "ما حكم الإحرام بالحج أو العمرة قبل الميقات المكاني؟", "options": ["ينعقد إحرامه مع الكراهة عند الجمهور", "باطل ويجب الرجوع للميقات", "لا ينعقد وتلزمه شاة"], "correct": "ينعقد إحرامه مع الكراهة عند الجمهور", "proof": "يكره الإحرام قبل الميقات لمخالفة هدي النبي ﷺ، لكن ينعقد إحرامه شرعاً."},
        {"question": "ما هو خيار المجلس في البيوع الشرعية؟", "options": ["حق العاقدين في فسخ البيع ما داما في مكان التبايع ولم يتفرقا", "خيار المشتري في إرجاع السلعة خلال 3 أيام", "خيار البائع في زيادة السعر"], "correct": "حق العاقدين في فسخ البيع ما داما في مكان التبايع ولم يتفرقا", "proof": "لقوله ﷺ: «البيعانِ بالخيارِ ما لم يتفرَّقا» (متفق عليه)."},
        {"question": "ما حكم الجمع بين صلاتي الظهر والعصر تقديماً أو تأخيراً للمسافر؟", "options": ["سنة ورخصة جائزة باتفاق الجمهور", "واجب يأثم بتركه", "خاص بصلاة الخوف فقط"], "correct": "سنة ورخصة جائزة باتفاق الجمهور", "proof": "كان النبي ﷺ إذا ارتحل قبل أن تزيغ الشمس أخّر الظهر إلى العصر ثم جمع بينهما."}
    ],
    "المستوى الثالث: المتقدم (أصول الفقه، مصطلح الحديث، والخلاف العالي) 🔴": [
        {"question": "ما هو الحديث المرسل عند جمهور المحدثين؟", "options": ["ما سقط من إسناده الصحابي ورفعه التابعي مباشرة", "ما سقط من وسط سنده راويان على التوالي", "الحديث الذي انفرد بروايته شخص واحد"], "correct": "ما سقط من إسناده الصحابي ورفعه التابعي مباشرة", "proof": "المرسل هو قول التابعي صغيراً كان أو كبيراً: قال رسول الله ﷺ كذا."},
        {"question": "ما هو مذهب جمهور الأصوليين في حجية 'قول الصحابي' إذا انتشر ولم يُعلم له مخالف؟", "options": ["إجماع سكوتي وهو حجة عند الجمهور", "ليس بحجة مطلقاً", "حجة خاصة بأهل المدينة فقط"], "correct": "إجماع سكوتي وهو حجة عند الجمهور", "proof": "يعتبر إجماعاً سكوتياً وظنياً معتبراً لدى غالبية الأصوليين وفقهاء المذاهب."},
        {"question": "ما الفرق بين 'الفرض' و'الواجب' عند السادة الحنفية؟", "options": ["الفرض ما ثبت بدليل قطعي، والواجب ما ثبت بدليل ظني", "الفرض والواجب مترادفان تماماً", "الواجب آكد من الفرض في العقيدة"], "correct": "الفرض ما ثبت بدليل قطعي، والواجب ما ثبت بدليل ظني", "proof": "يميز الحنفية بين الفرض (كالصلاة بالدليل القطعي) والواجب (كالوتر بالدليل الظني)."},
        {"question": "ما المقصود بقاعدة 'العام يبقى على عمومه حتى يرد دليل التخصيص'؟", "options": ["أن النص العام يشمل كل أفراده حتى يأتي نص خاص يقيده", "أن النص العام ينسخ كل النصوص السابقة", "أن النص العام لا يعمل به إلا بإجماع"], "correct": "أن النص العام يشمل كل أفراده حتى يأتي نص خاص يقيده", "proof": "من القواعد الأصولية القطعية المقررة عند الأئمة الأربعة في دلالات الألفاظ."}
    ]
}
# قراءة مفتاح Groq بأمان
# قراءة المفتاح بأمان محلياً وسحابياً دون أخطاء
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except Exception:
    GROQ_API_KEY = "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"
def get_working_groq_models():
    client = Groq(api_key=GROQ_API_KEY.strip())
    try:
        models_data = client.models.list()
        return [m.id for m in models_data.data if m.active]
    except Exception:
        return ["llama3-70b-8192", "llama3-8b-8192", "gemma2-9b-it"]
def execute_groq_prompt(prompt, system_inst, output_container):
    client = Groq(api_key=GROQ_API_KEY.strip())
    models_to_try = get_working_groq_models()
    
    full_text = ""
    for model_choice in models_to_try:
        try:
            completion = client.chat.completions.create(
                model=model_choice,
                messages=[
                    {"role": "system", "content": system_inst},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                stream=True
            )
            for chunk in completion:
                chunk_content = chunk.choices[0].delta.content
                if chunk_content:
                    full_text += chunk_content
                    output_container.markdown(f"<br>{full_text}▌", unsafe_allow_html=True)
            output_container.markdown(f"<br>{full_text}", unsafe_allow_html=True)
            return full_text
        except Exception:
            continue
    return None
def generate_dynamic_quiz_questions(level_name):
    client = Groq(api_key=GROQ_API_KEY.strip())
    models_to_try = get_working_groq_models()
    
    sys_prompt = """أنت محرك فقهي ومحدث محقق. ولد 10 أسئلة شرعية جديدة ومتنوعة تماماً بصيغة اختيار من متعدد بالعربية.
اكتب كل سؤال في سطر منفصل بالضبط وفق هذا النموذج مستخدماً الرمز ||| للفصل:
نص السؤال ||| الإجابة الصحيحة ||| الخيار الخطأ الأول ||| الخيار الخطأ الثاني ||| الدليل والتخريج الشرعي
تنبيه: لا تكتب أي مقدمات أو أرقام، فقط الأسطر المفصولة بالعلامة |||."""
    for model_choice in models_to_try:
        try:
            completion = client.chat.completions.create(
                model=model_choice,
                messages=[
                    {"role": "system", "content": sys_prompt},
                    {"role": "user", "content": f"ولد 10 أسئلة شرعية جديدة تماماً للمستوى: {level_name}"}
                ],
                temperature=0.7
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
# إدارة حالة الأسئلة والجلسة
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
def prepare_new_round(level):
    pool = st.session_state["quiz_pool"][level]
    unseen = [q for q in pool if q["question"] not in st.session_state["seen_questions"]]
    
    if len(unseen) < 5:
        st.session_state["seen_questions"] = set()
        unseen = pool
        
    random.shuffle(unseen)
    selected_round = unseen[:10]
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
# ملف حفظ السجل المحلي
HISTORY_FILE = "search_history.json"
def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f: return json.load(f)
        except Exception: return []
    return []
def save_history(hl):
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f: json.dump(hl, f, ensure_ascii=False, indent=2)
    except Exception: pass
if "history" not in st.session_state: st.session_state["history"] = load_history()
if "current_question" not in st.session_state: st.session_state["current_question"] = ""
if "current_answer" not in st.session_state: st.session_state["current_answer"] = ""
# القائمة الجانبية
with st.sidebar:
    st.markdown("<h3 style='color:#fbbf24; text-align:center;'>📜 سجل الاستفسارات</h3>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color: rgba(234,179,8,0.3);'>", unsafe_allow_html=True)
    
    if st.session_state["history"]:
        if st.button("🗑️ مسح السجل بالكامل", use_container_width=True):
            st.session_state["history"] = []
            save_history([])
            st.session_state["current_question"] = ""
            st.session_state["current_answer"] = ""
            st.rerun()
        st.markdown("<br>", unsafe_allow_html=True)
        for idx, item in enumerate(st.session_state["history"]):
            btn_label = f"📌 {item['question'][:24]}..." if len(item['question']) > 24 else f"📌 {item['question']}"
            if st.button(btn_label, key=f"hist_{idx}", use_container_width=True):
                st.session_state["current_question"] = item["question"]
                st.session_state["current_answer"] = item["answer"]
                st.rerun()
    else:
        st.info("لا توجد استفسارات محفوظة بعد.")
# الشريط العلوي
st.markdown("""
<div class="ticker-wrap">
    <div class="ticker-move">
        <span class="ticker-item">✨ لَا إِلَٰهَ إِلَّا ٱللَّٰهُ مُحَمَّدٌ رَسُولُ ٱللَّٰهِ ✨</span>
        <span class="ticker-bullet">✦</span>
        <span class="ticker-item">🌸 اللَّهُمَّ صَلِّ وَسَلِّمْ وَبَارِكْ عَلَىٰ سَيِّدِنَا مُحَمَّدٍ وَعَلَىٰ آلِهِ وَصَحْبِهِ أَجْمَعِينَ 🌸</span>
        <span class="ticker-bullet">✦</span>
        <span class="ticker-item">🌿 سُبْحَانَ اللَّهِ وَبِحَمْدِهِ ، سُبْحَانَ اللَّهِ الْعَظِيمِ 🌿</span>
        <span class="ticker-bullet">✦</span>
        <span class="ticker-item">💎 أَسْتَغْفِرُ اللَّهَ الْعَظِيمَ وَأَتُوبُ إِلَيْهِ 💎</span>
        <span class="ticker-bullet">✦</span>
        <span class="ticker-item">🤍 لَا حَوْلَ وَلَا قُوَّةَ إِلَّا بِاللَّهِ الْعَلِيِّ الْعَظِيمِ 🤍</span>
    </div>
</div>
""", unsafe_allow_html=True)
# الهيدر الترحيبي
st.markdown("""
<div class="royal-hero">
    <h1>🕌 الموسوعة الفقهية والحديثية الذكية</h1>
    <p>استعراض الأحكام الشرعية • الاستدلال القرآني • تخريج الأحاديث • بنك تحديات عشوائي</p>
</div>
""", unsafe_allow_html=True)
# علامات التبويب الرئيسية
tab_main, tab_hadith, tab_dict, tab_interactive = st.tabs([
    "🏛️ المحرك الفقهي والمقارن",
    "📜 التحقيق الحديثي المباشر",
    "📖 معجم غريب الألفاظ",
    "🏆 بنك المسابقات والتحديات"
])
# ----------------- التبويب 1: المحرك الفقهي -----------------
with tab_main:
    col_opt1, col_opt2 = st.columns(2)
    with col_opt1:
        selected_madhab = st.selectbox("🏛️ اختر المذهب المطلوب عرضه:", [
            "مقارنة المذاهب الأربعة كاملة (الحنفي، المالكي، الشافعي، الحنبلي)", "المذهب الحنفي فقط", "المذهب المالكي فقط", "المذهب الشافعي فقط", "المذهب الحنبلي فقط"
        ])
    with col_opt2:
        depth_level = st.select_slider("🎚️ مستوى تفصيل الإجابة الشرعية:", options=["موجز ميسر (للمستفتي)", "متوسط وتأصيلي (مع الأدلة)", "بحث فقهي موسع (لطلاب العلم)"], value="متوسط وتأصيلي (مع الأدلة)")
    col_sub1, col_sub2 = st.columns([2, 1])
    with col_sub1:
        selected_hadith_levels = st.multiselect("📜 درجات الحديث في التخريج:", ["الأحاديث الصحيحة", "الأحاديث الحسنة", "الأحاديث الضعيفة والمشتهرة (للتنبيه)"], default=["الأحاديث الصحيحة", "الأحاديث الحسنة"])
    with col_sub2:
        include_quran = st.checkbox("📖 الاستدلال بالقرآن", value=True)
    user_query = st.text_input("اكتب استفسارك الشرعي:", value=st.session_state["current_question"], placeholder="مثال: حكم صلاة الوتر وصفتها، وهل تجوز بركعة واحدة؟...", key="main_query_input")
    submit_btn = st.button("✨ استخراج الحكم والتحقيق", use_container_width=True)
    output_area = st.empty()
    if st.session_state["current_answer"] and not submit_btn:
        output_area.markdown(f"<br>{st.session_state['current_answer']}", unsafe_allow_html=True)
    if submit_btn:
        query_text = user_query.strip()
        if not query_text:
            st.warning("⚠️ يرجى كتابة المسألة أو السؤال أولاً.")
        else:
            if selected_madhab == "مقارنة المذاهب الأربعة كاملة (الحنفي، المالكي، الشافعي، الحنبلي)":
                madhab_instruction = """
# 🏛️ مقارنة أقوال ومذاهب الأئمة الأربعة

| المذهب الفقهي | المعتمد في المذهب | المستند والدليل من المذهب |
| :--- | :--- | :--- |
| **المذهب الحنفي** | الحكم المعتمد | المستند الشرعي |
| **المذهب المالكي** | الحكم المعتمد | المستند الشرعي |
| **المذهب الشافعي** | الحكم المعتمد | المستند الشرعي |
| **المذهب الحنبلي** | الحكم المعتمد | المستند الشرعي |

"""
            else:
                madhab_name = selected_madhab.replace(" فقط", "")
                madhab_instruction = f"""
# 🏛️ الحكم الفقهي المعتمد في {madhab_name}
- **الحكم المعتمد**: (اكتب بالتفصيل قول أئمة {madhab_name} المعتمد في الفتوى).
- **أدلة المذهب ومستنده**: (اذكر القواعد والأدلة التي بنى عليها علماء {madhab_name} هذا الحكم).
*(تنبيه: التزم بعرض {madhab_name} فقط).*
"""
            hadith_filter = "، ".join(selected_hadith_levels) if selected_hadith_levels else "الأحاديث الصحيحة والحسنة فقط"
            dynamic_system_instruction = f"""
أنت محرك فقهي محقق. دورك تفصيل المسائل بدقة وبمستوى: ({depth_level}).
التزم بالهيكل التالي:
# 📌 خلاصة المسألة
{"# 📖 الاستدلال من القرآن الكريم" if include_quran else ""}
{"- **الآية الكريمة**: «نص الآية» - **السورة والآية** - **وجه الاستدلال**" if include_quran else ""}
# 🤝 المتفق عليه بين الأئمة
---
# 📜 التحقيق الحديثي وتفصيل الأسانيد
التزم بإيراد ({hadith_filter}):
- 🔹 **نص المتن**: «...» * 👤 **الراوي**: ... * 📚 **المصدر**: ... * ⚖️ **الدرجة**: ... * 💡 **الشرح**: ...
---
{madhab_instruction}
---
# 💡 توجيه وإرشاد شرعي
"""
            result = execute_groq_prompt(query_text, dynamic_system_instruction, output_area)
            if result:
                st.session_state["current_question"] = query_text
                st.session_state["current_answer"] = result
                updated_hist = [h for h in st.session_state["history"] if h["question"] != query_text]
                updated_hist.insert(0, {"question": query_text, "answer": result})
                st.session_state["history"] = updated_hist
                save_history(updated_hist)
# ----------------- التبويب 2: التحقيق الحديثي -----------------
with tab_hadith:
    st.markdown("<div class='feature-box'><h4>🔍 التحقيق الحديثي المباشر وتخريج الأسانيد</h4><p style='color:#94a3b8;'>اكتب أي حديث أو جزء من المتن للتحقق من صحته، راويه، أصله في كتب السنة، وحكم المحدثين عليه.</p></div>", unsafe_allow_html=True)
    hadith_input = st.text_input("اكتب نص الحديث المراد تخريجه:", placeholder="مثال: إنما الأعمال بالنيات...")
    if st.button("🔎 تخريج وتحقيق الحديث", use_container_width=True):
        if hadith_input.strip():
            h_output = st.empty()
            h_sys = """
أنت عالم ومحدث محقق متمكن في علوم الجرح والتعديل.
قم بتحقيق الحديث المدخل:
# 📜 تحقيق الحديث النبوي
- **نص المتن الكامل**: «النص مع الضبط»
- 👤 **الصحابي الراوي**:
- 📚 **المصادر وكتب السنة**:
- ⚖️ **حكم المحدثين ورتبته**:
- 💡 **الفائدة المستنبطة من الحديث**:
"""
            execute_groq_prompt(hadith_input, h_sys, h_output)
# ----------------- التبويب 3: معجم غريب الألفاظ -----------------
with tab_dict:
    st.markdown("<div class='feature-box'><h4>📖 معجم غريب الألفاظ والمصطلحات</h4><p style='color:#94a3b8;'>شرح دقيق للمصطلحات القديمة، المقادير الشرعية، والألفاظ التراثية الصعبة.</p></div>", unsafe_allow_html=True)
    term_input = st.text_input("اكتب اللفظ أو المصطلح الشرعي:", placeholder="مثال: الصاع، العول، الكلالة، القسامة...")
    if st.button("📚 شرح وتفسير المصطلح", use_container_width=True):
        if term_input.strip():
            t_output = st.empty()
            t_sys = """
أنت معجمي وفقهي محقق.
اشرح المصطلح الشرعي:
# 📖 بيان المصطلح الشرعي
- **المعنى اللغوي والاصطلاحي**:
- **المقدار المعاصر (إن وجد)**:
- **أمثلة وتطبيقات فقهية**:
"""
            execute_groq_prompt(term_input, t_sys, t_output)
# ----------------- التبويب 4: بنك المسابقات والتحديات -----------------
with tab_interactive:
    st.markdown("<h3 style='color:#fbbf24; font-size:1.8rem;'>🏆 بنك المسابقات والتحديات الفقهية</h3>", unsafe_allow_html=True)
    
    selected_level = st.selectbox(
        "🎯 حدد مستوى التحدي:",
        list(st.session_state["quiz_pool"].keys()),
        index=list(st.session_state["quiz_pool"].keys()).index(st.session_state["quiz_level"])
    )
    if selected_level != st.session_state["quiz_level"]:
        st.session_state["quiz_level"] = selected_level
        prepare_new_round(selected_level)
        st.rerun()
    if st.button("⚡ توليد وتجديد أسئلة غير مكررة بالذكاء الاصطناعي", use_container_width=True):
        with st.spinner("جاري استحضار أسئلة فقهية جديدة وإضافتها للموسوعة..."):
            new_q = generate_dynamic_quiz_questions(st.session_state["quiz_level"])
            if new_q and len(new_q) > 0:
                st.session_state["quiz_pool"][st.session_state["quiz_level"]].extend(new_q)
                prepare_new_round(st.session_state["quiz_level"])
                st.success(f"🎉 تم توليد وإضافة {len(new_q)} أسئلة فقهية جديدة بنجاح!")
                st.rerun()
            else:
                prepare_new_round(st.session_state["quiz_level"])
                st.info("🔄 تم تجديد الأسئلة وبدء جولة غير مكررة من بنك الأسئلة الموسع!")
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
        col_sc1, col_sc2 = st.columns([2, 1])
        with col_sc1:
            progress_val = current_idx / total_q
            st.progress(progress_val)
            st.write(f"📌 **السؤال {current_idx + 1} من {total_q} في هذه الجولة**")
        with col_sc2:
            st.markdown(f"<div style='text-align:left; color:#facc15; font-size:1.3rem; font-weight:bold;'>⭐ النقاط: {st.session_state['quiz_score']}/{total_q}</div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="quiz-card">
            <h3 style="color:#ffffff; line-height:1.6; font-size:1.35rem;">{q_data['question']}</h3>
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
            check_btn = st.button("✅ تأكيد الإجابة والتحقق", use_container_width=True, disabled=st.session_state["quiz_answered"])
        
        with col_qbtn2:
            next_btn = st.button("➡️ الانتقال للسؤال التالي", use_container_width=True, disabled=not st.session_state["quiz_answered"])
        if check_btn:
            if chosen_answer is None:
                st.warning("⚠️ يرجى اختيار إحدى الإجابات أولاً قبل التأكيد.")
            else:
                st.session_state["quiz_answered"] = True
                if chosen_answer == q_data["correct"]:
                    st.session_state["quiz_score"] += 1
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
            <h2 style="color:#fbbf24; font-size:1.8rem;">🎉 بارك الله فيك! أكملت هذه الجولة بنجاح</h2>
            <p style="font-size:1.4rem; color:#ffffff; margin: 1rem 0;">نتيجتك الإجمالية: <strong>{st.session_state['quiz_score']} من {total_q}</strong></p>
        </div>
        """, unsafe_allow_html=True)
        
        col_end1, col_end2 = st.columns(2)
        with col_end1:
            if st.button("🚀 بدء جولة عشوائية جديدة بأسئلة غير مكررة", use_container_width=True):
                prepare_new_round(st.session_state["quiz_level"])
                st.rerun()
        with col_end2:
             if st.button("⚡ جلب أسئلة جديدة كلياً بالذكاء الاصطناعي", use_container_width=True):
                with st.spinner("جاري استحضار تحديات فقهية جديدة..."):
                    new_q = generate_dynamic_quiz_questions(st.session_state["quiz_level"])
                    if new_q and len(new_q) > 0:
                        st.session_state["quiz_pool"][st.session_state["quiz_level"]].extend(new_q)
                    prepare_new_round(st.session_state["quiz_level"])
                    st.rerun()
# التذييل
st.markdown("""
<div class="royal-footer">
    <div class="footer-text">نظام فقهي استدلالي وتوثيقي مقارن مبني بنماذج الذكاء الاصطناعي المتقدمة</div>
    <div>تطوير بواسطة <span class="dev-badge">Eng. Abdelfttah Ragheb</span> © 2026</div>
</div>
""", unsafe_allow_html=True)
