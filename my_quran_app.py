import streamlit as st
import os

# --- 1. إعدادات الصفحة والخطوط ---
st.set_page_config(page_title="تجميعة أحمد أبو تركي", layout="centered")

# استدعاء خط "الأميري" للمظهر المصحفي
st.markdown('<link href="https://fonts.googleapis.com/css2?family=Amiri&display=swap" rel="stylesheet">', unsafe_allow_html=True)

# --- 2. دالة قراءة البيانات ---
@st.cache_data
def load_and_clean_data():
    app_data = {}
    if not os.path.exists("data.txt"):
        return None
    with open("data.txt", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or ":" not in line:
                continue
            parts = line.split(":", 1)
            category = parts[0].strip()
            verse = parts[1].strip()
            if category not in app_data:
                app_data[category] = []
            app_data[category].append(verse)
    return app_data

quran_app_data = load_and_clean_data()

# --- 3. القائمة الجانبية (تم تحديث مسار الصورة) ---
with st.sidebar:
    st.markdown("<h3 style='text-align: center; color: #3E5E3D;'>✍️ إعداد وتجميع</h3>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center;'>أحمد أبو تركي</h4>", unsafe_allow_html=True)
    
    # تحديث المسار ليشير لمجلد images
    image_path = "images/ahmad.jpg" 
    
    if os.path.exists(image_path):
        # عرض صورتك الشخصية
        st.image(image_path, use_container_width=True)
    else:
        st.info("💡 لم يتم العثور على ahmad.jpg داخل مجلد images.")

    st.divider()
    st.title("📌 الفهرس")
    choice = st.selectbox("اختر القسم الموضوعي:", list(quran_app_data.keys()))

# --- 4. منطق العرض الرئيسي ---
if 'verse_idx' not in st.session_state or st.session_state.get('last_cat') != choice:
    st.session_state.verse_idx = 0
    st.session_state.last_cat = choice

verses = quran_app_data[choice]
total = len(verses)

st.title("📖 مصحف التصفح الموضوعي")
st.write(f"تجميعة: **{st.session_state.last_cat}**")

# شريط إنجاز يوضح التقدم
progress = (st.session_state.verse_idx + 1) / total
st.progress(progress)

# إطار العرض (نمط السكينة)
st.markdown(f"""
<div style="direction: rtl; background-color: #FDFBF7; padding: 40px; border-radius: 20px; border-right: 15px solid #3E5E3D; text-align: center; box-shadow: 2px 4px 15px rgba(0,0,0,0.05); min-height: 250px;">
    <h1 style="color: #2D3436; font-family: 'Amiri', serif; line-height: 2.0; font-size: 2.2em;">
        ﴿ {verses[st.session_state.verse_idx]} ﴾
    </h1>
    <hr style="border-top: 1px dashed #3E5E3D; margin: 30px 0;">
    <p style="color: #636e72; font-size: 0.9em;">النص رقم {st.session_state.verse_idx + 1} من إجمالي {total}</p>
</div>
""", unsafe_allow_html=True)

# --- 5. أزرار التحكم ---
st.write("")
c1, c2, c3 = st.columns([1,1,1])

with c1:
    if st.button("⬅️ السابق", use_container_width=True) and st.session_state.verse_idx > 0:
        st.session_state.verse_idx -= 1
        st.rerun()

with c2:
    if st.button("🔄 البداية", use_container_width=True):
        st.session_state.verse_idx = 0
        st.rerun()

with c3:
    if st.button("التالي ➡️", use_container_width=True) and st.session_state.verse_idx < total - 1:
        st.session_state.verse_idx += 1
        st.rerun()