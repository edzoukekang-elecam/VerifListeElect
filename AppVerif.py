import streamlit as st
import pandas as pd
import unidecode

# Charger le CSV
@st.cache_data
def load_data():
    return pd.read_csv("liste_electorale.csv", encoding="latin1")

data = load_data()

st.title("📋 Vérification de l'inscription sur la liste électorale")

nom = st.text_input("Entrez votre nom de famille (Last Name) :")

if st.button("Vérifier"):
    if nom.strip() == "":
        st.warning("Veuillez entrer un nom avant de vérifier.")
    else:
        nom_saisi = unidecode.unidecode(nom.lower().strip())
        data["Nom_normalise"] = data["Nom"].apply(lambda x: unidecode.unidecode(str(x).lower().strip()))

        # Recherche exacte
        exact_matches = [n for n in data["Nom"] if unidecode.unidecode(n.lower().strip()) == nom_saisi]

        # Recherche partielle
        partial_matches = [n for n in data["Nom"] if nom_saisi in unidecode.unidecode(n.lower().strip())]

        # Fusionner résultats sans doublons
        all_matches = list(set(exact_matches + partial_matches))

        if all_matches:
            st.success(f"✅ {len(all_matches)} résultat(s) trouvé(s) pour : {nom}")
            st.dataframe(pd.DataFrame(all_matches, columns=["Nom"]))
        else:
            st.error("❌ Aucun résultat trouvé. Vérifiez l'orthographe ou contactez le secrétariat.")
