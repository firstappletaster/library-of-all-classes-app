import streamlit as st
from duckduckgo_search import DDGS
from google import genai

# Sayfa Yapılandırması
st.set_page_config(page_title="AI Search Assistant", page_icon="✨", layout="centered")

# Özel CSS ile Estetik Tasarım Özelleştirmesi
st.markdown("""
    <style>
    /* Ana Sayfa Arka Planı ve Yazı Tipleri */
    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
    }
    
    /* Başlık Stilizasyonu */
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #a855f7 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    /* Alt Başlık / Açıklama */
    .sub-title {
        color: #94a3b8;
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    
    /* Buton Tasarımı (Kırmızı Yerine Indigo/Mor Degrade) */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-size: 1rem;
        font-weight: 600;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 14px 0 rgba(99, 102, 241, 0.39);
    }
    div.stButton > button:first-child:hover {
        background: linear-gradient(135deg, #4f46e5 0%, #9333ea 100%);
        box-shadow: 0 6px 20px 0 rgba(99, 102, 241, 0.55);
        transform: translateY(-2px);
    }
    
    /* Metin Kutusu Stilizasyonu */
    .stTextArea textarea {
        background-color: #1e293b;
        color: #f8fafc;
        border: 1px solid #334155;
        border-radius: 12px;
    }
    .stTextArea textarea:focus {
        border-color: #818cf8;
        box-shadow: 0 0 0 2px rgba(129, 140, 248, 0.2);
    }
    
    /* Şifre / API Giriş Kutusu */
    .stTextInput input {
        background-color: #1e293b;
        color: #f8fafc;
        border: 1px solid #334155;
        border-radius: 10px;
    }
    
    /* Bilgi Kartları */
    .result-card {
        background-color: #1e293b;
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid #334155;
        margin-top: 1.5rem;
    }
    </style>
""", unsafe_style_html=True)

# Başlık Alanı
st.markdown('<div class="main-title">✨ Akıllı AI Arama Asistanı</div>', unsafe_style_html=True)
st.markdown('<div class="sub-title">Web verileriyle desteklenmiş kişisel yapay zeka arama ve öğrenme asistanınız.</div>', unsafe_style_html=True)

# API Key Giriş Alanı (Daha estetik bir görünüm)
api_key = st.text_input("🔑 Gemini API Anahtarınız:", type="password", placeholder="AIzaSy...")

query = st.text_area("🔍 Ne öğrenmek istiyorsunuz?", placeholder="Örn: 11. Sınıf Biyoloji dersinin ilk dönemi için en kritik sınav kavramları nelerdir?", height=120)

if st.button("AI ile Derinlemesine Ara & Yanıtla"):
    if not api_key:
        st.error("Lütfen devam etmek için geçerli bir Gemini API Anahtarı girin.")
    elif not query.strip():
        st.warning("Lütfen aramak veya öğrenmek istediğiniz konuyu yazın.")
    else:
        with st.spinner("🌐 Web taranıyor ve analiz yapılıyor..."):
            try:
                # 1. Web Araması
                ddg = DDGS()
                results = ddg.text(query, max_results=5)
                
                context_text = ""
                sources = []
                if results:
                    for r in results:
                        context_text += f"- {r.get('title')}: {r.get('body')}\n"
                        sources.append((r.get('title'), r.get('href')))
                
                # 2. Gemini Yapay Zeka Sorgusu
                client = genai.Client(api_key=api_key)
                
                prompt = f"""
Kullanıcı Soru / İstek: {query}

Web'den Toplanan Güncel Kaynaklar:
{context_text}

Görevin:
Yukarıdaki bilgileri ve kendi geniş akademik/genel kültür bilgini kullanarak kullanıcıya son derece estetik, akıcı, net ve maddeler halinde yapılandırılmış bir yanıt sun.
"""
                response = client.models.generate_content(
                    model='gemini-3.8-flash',
                    contents=prompt,
                )
                
                # 3. Sonuç Kartı
                st.markdown("### 💡 Yapay Zeka Yanıtı")
                st.markdown(response.text)
                
                if sources:
                    st.divider()
                    st.markdown("##### 🔗 Yararlanılan Kaynaklar")
                    for title, url in sources:
                        st.markdown(f"- [{title}]({url})")
                        
            except Exception as e:
                st.error(f"Bir sorun oluştu: {e}")
