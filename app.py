import streamlit as st
from duckduckgo_search import DDGS
import google.generativeai as genai

# Sayfa Yapılandırması
st.set_page_config(page_title="AI Web Asistanı", page_icon="🤖", layout="wide")

st.title("🤖 Yapay Zeka Destekli Arama Asistanı")
st.markdown("Soru sorun, web'den güncel bilgileri toplayıp sizin için özetlesin ve yanıtlasın!")

# Yan menüden Gemini API Anahtarı girişi
with st.sidebar:
    st.header("⚙️ Ayarlar")
    api_key = st.text_input("Gemini API Key Girin:", type="password", help="Google AI Studio'dan alabileceğiniz ücretsiz API anahtarı.")
    st.caption("API anahtarınız yoksa [Google AI Studio](https://aistudio.google.com/) üzerinden ücretsiz alabilirsiniz.")

query = st.text_area("Ne öğrenmek istiyorsunuz?", placeholder="Örn: 11. Sınıf 1. Dönem 1. Yazılı için önemli biyoloji kavramlarını ve açıklamalarını özetler misin?", height=100)

if st.button("AI ile Ara & Yanıtla", type="primary"):
    if not api_key:
        st.error("Lütfen sol menüden Gemini API Key anahtarınızı girin.")
    elif not query.strip():
        st.warning("Lütfen bir soru yazın.")
    else:
        with st.spinner("Web taranıyor ve Yapay Zeka yanıtı hazırlanıyor..."):
            try:
                # 1. Web'de arama yap
                search_results = []
                ddg = DDGS()
                results = ddg.text(query, max_results=5)
                
                context_text = ""
                sources = []
                if results:
                    for r in results:
                        context_text += f"- {r.get('title')}: {r.get('body')}\n"
                        sources.append((r.get('title'), r.get('href')))
                
                # 2. Gemini Yapay Zekaya bağlam gönder
                genai.configure(api_key=api_key)
                # En kararlı ve standart model ismi
                model = genai.GenerativeModel("gemini-1.5-pro")
                
                prompt = f"""
Kullanıcı Soru / İstek: {query}

Web'den Toplanan İlgili Bilgiler:
{context_text}

Görevin:
Yukarıdaki web arama sonuçlarını ve kendi kapsamlı akademik/genel bilgini harmanlayarak kullanıcıya son derece detaylı, net, düzenli (maddeler halinde) ve akıcı bir yanıt hazırla. Eğer konu sınav, ders veya kavramsalsa açıklayıcı ve eğitici bir üslup kullan.
"""
                response = model.generate_content(prompt)
                
                # 3. Sonucu Göster
                st.subheader("💡 AI Yanıtı")
                st.write(response.text)
                
                if sources:
                    st.divider()
                    st.caption("🌐 Kullanılan Web Kaynakları:")
                    for title, url in sources:
                        st.markdown(f"- [{title}]({url})")
                        
            except Exception as e:
                st.error(f"Bir hata oluştu: {e}")
