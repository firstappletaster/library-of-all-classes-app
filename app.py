import streamlit as st
import requests

# Sayfa Yapılandırması
st.set_page_config(page_title="Özel Arama Motoru", page_icon="🔍", layout="wide")

st.title("🔍 Akıllı Arama Motoru")
st.markdown("Web üzerinde hızlı, reklamsız ve sade bir arama deneyimi.")

# Kullanıcı Arama Girdisi
query = st.text_input("Aramak istediğiniz konuyu yazın:", placeholder="Örn: Yapay zeka gelişmeleri...")

def search_duckduckgo(keywords):
    url = f"https://api.duckduckgo.com/?q={keywords}&format=json&no_html=1&skip_disambig=1"
    try:
        response = requests.get(url)
        data = response.json()
        results = []
        
        # Abstract / Özet Bilgi
        if data.get("Abstract"):
            results.append({
                "title": data.get("Heading", "Özet Sonuç"),
                "snippet": data.get("Abstract"),
                "url": data.get("AbstractURL")
            })
            
        # İlgili Bağlantılar (Related Topics)
        for topic in data.get("RelatedTopics", []):
            if "Text" in topic and "FirstURL" in topic:
                results.append({
                    "title": topic.get("Text").split(" - ")[0] if " - " in topic.get("Text") else "Sonuç",
                    "snippet": topic.get("Text"),
                    "url": topic.get("FirstURL")
                })
        return results
    except Exception as e:
        return []

if st.button("Ara", type="primary"):
    if not query.strip():
        st.warning("Lütfen aramak için bir kelime yazın.")
    else:
        with st.spinner("Web taranıyor..."):
            results = search_duckduckgo(query)
            
            if results:
                st.subheader(f"🔎 '{query}' için Arama Sonuçları")
                st.divider()
                for item in results:
                    st.markdown(f"### [{item['title']}]({item['url']})")
                    st.write(item['snippet'])
                    st.caption(f"🔗 {item['url']}")
                    st.divider()
            else:
                st.info("Aramanızla ilgili doğrudan bir özet bulunamadı. Lütfen farklı anahtar kelimeler deneyin.")
