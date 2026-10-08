import streamlit as st
from duckduckgo_search import DDGS
from google import genai

# Sayfa Yapılandırması
st.set_page_config(page_title="AI Search Assistant", page_icon="✨", layout="centered")

# Özel CSS ile Modern ve Şık Tasarım
st.markdown("""
    <style>
    /* Ana Sayfa Arka Planı */
    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
    }
    
    /* Başlık Stilizasyonu (Mor/Mavi Degrade) */
    .main-title {
        font-size: 2.3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #a855f7 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        text-align: center;
    }
    
    /* Alt Başlık */
    .sub-title {
        color: #94a3b8;
        font-size: 1rem;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    /* Mor/İndigo Buton Tasarımı */
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
    
    /* Soru Kutusu Stili */
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
    </style>
""", unsafe_allow_html=True)

# Başlık Alanı
st.markdown('<div class="main-title">✨ Akıllı Arama Asistanı</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Web verileriyle desteklenmiş kişisel yapay zeka arama motorunuz.</div>', unsafe_allow_html=True)

# Streamlit Secrets'tan API Anahtarını Çekiyoruz
api_key = st.secrets.get("GEMINI_API_KEY")

query = st.text_area("🔍 Ne öğrenmek istiyorsunuz?", placeholder="Örn: 11. Sınıf Biyoloji dersinin en kritik sınav kavramları nelerdir?", height=110)

if st.button("AI ile Ara & Yanıtla"):
    if not api_key:
        st.error("Sistemde API anahtarı bulunamadı. Lütfen Streamlit Settings > Secrets alanına GEMINI_API_KEY ekleyin.")
    elif not query.strip():
        st.warning("Lütfen aramak istediğiniz konuyu yazın.")
    else:
        with st.spinner("🌐 Web taranıyor ve yapay zeka yanıtı hazırlanıyor..."):
            try:
                # 1. Web Araması Yap
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

Web'den Toplanan Güncel Bilgiler:
{context_text}

Görevin:
Yukarıdaki web arama sonuçlarını ve kendi kapsamlı akademik/genel kültür bilgini harmanlayarak kullanıcıya son derece detaylı, net, düzenli (maddeler halinde) ve akıcı bir yanıt hazırla. Eğer konu sınav, ders veya kavramsalsa açıklayıcı ve eğitici bir üslup kullan.
"""
                # Hata vermeyen garantili model deneme sırası
                candidate_models = [
                    'models/gemini-2.5-flash',
                    'models/gemini-2.5-pro',
                    'models/gemini-1.5-flash',
                    'models/gemini-1.5-pro'
                ]
                
                response = None
                for m in candidate_models:
                    try:
                        response = client.models.generate_content(
                            model=m,
                            contents=prompt,
                        )
                        if response:
                            break
                    except Exception:
                        continue
                
                if response and response.text:
                    # 3. Yanıtı Göster
                    st.markdown("### 💡 AI Yanıtı")
                    st.markdown(response.text)
                    
                    if sources:
                        st.divider()
                        st.markdown("##### 🌐 Kullanılan Web Kaynakları:")
                        for title, url in sources:
                            st.markdown(f"- [{title}]({url})")
                else:
                    st.error("Şu an modeller yanıt veremedi, lütfen birkaç saniye sonra tekrar deneyin.")
                        
            except Exception as e:
                st.error(f"Bir sorun oluştu: {e}")
