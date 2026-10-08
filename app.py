import streamlit as st
from duckduckgo_search import DDGS

# Sayfa Yapılandırması
st.set_page_config(page_title="Özel Arama Motoru", page_icon="🔍", layout="wide")

st.title("🔍 Akıllı Arama Motoru")
st.markdown("Web üzerinde hızlı, reklamsız ve sade bir arama deneyimi.")

# Kullanıcı Arama Girdisi
query = st.text_input("Aramak istediğiniz konuyu yazın:", placeholder="Örn: 11. sınıf TYT kaynak önerileri")

if st.button("Ara", type="primary"):
    if not query.strip():
        st.warning("Lütfen aramak için bir kelime yazın.")
    else:
        with st.spinner("Web taranıyor..."):
            try:
                results = []
                with DDGS() as ddgs:
                    # En alakalı 10 sonucu hızlıca çeker
                    for r in ddgs.text(query, max_results=10):
                        results.append(r)
                
                if results:
                    st.subheader(f"🔎 '{query}' için Arama Sonuçları")
                    st.divider()
                    for item in results:
                        st.markdown(f"### [{item['title']}]({item['href']})")
                        st.write(item['body'])
                        st.caption(f"🔗 {item['href']}")
                        st.divider()
                else:
                    st.info("Aramanızla ilgili sonuç bulunamadı.")
            except Exception as e:
                st.error("Arama yapılırken bir hata oluştu. Lütfen tekrar deneyin.")
