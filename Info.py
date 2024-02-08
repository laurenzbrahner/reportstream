import streamlit as st


st.set_page_config(page_title="Spotify Analyse Report",
                   page_icon=":musical_note:")

st.title("Spotify Analyse Report")

st.markdown("""
       Dieser Report dient dazu, die wichtigsten Erkenntnisse meiner Analyse anhand ausgewählter Graphen darzustellen.
Ein detailliertes Dashboard zu diesem Projekt finden sie hier.
            [Dasboard](https://appapp-ka7buefabvnokhdfwhyptg.streamlit.app/)
    """)

st.sidebar.header("Über den Autor")
st.sidebar.markdown("""
        **Name des Autors:**
        - Laurenz Brahner

        **Kontaktinformationen:**
        - [GitHub](https://github.com/laurenzbrahner)
        - lb184@hdm-stuttgart.de    

    """)


st.header("Projektdetails")
st.markdown("""
    - **Datenquellen:** Die analysierten Daten stammen direkt von Kaggle. [Daten](https://www.kaggle.com/datasets/nelgiriyewithana/top-spotify-songs-2023).
    - **Analyseziele:** Identifizierung von Mustern in Musikpräferenzen, Verständnis der Popularität verschiedener Musikgenres, Einfluss von verschiedenen Faktoren auf den Erfolg der Songs.
    - **Technologien:** Python, Pandas, Streamlit, Sklearn und Altair für visuelle Datenanalyse.
    """)

st.header("Weitere Informationen")
st.markdown("""
    Falls Sie weitere Informationen wünschen oder Fragen zum Report haben, können Sie mich gerne über die in der Sidebar aufgeführten Kontaktdaten erreichen.
    """)

# Footer
st.markdown("---")
st.markdown("© 2023 Laurenz Brahner - Alle Rechte vorbehalten.")
