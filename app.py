import streamlit as st
import pandas as pd
import os

st.title("📊 Application de collecte des étudiants")

FILE = "data.csv"

# 🔥 Charger les données au démarrage
if "data" not in st.session_state:
    if os.path.exists(FILE):
        st.session_state.data = pd.read_csv(FILE).to_dict("records")
    else:
        st.session_state.data = []

# FORMULAIRE
with st.form("form"):
    nom = st.text_input("Nom")
    age = st.number_input("Âge", 15, 40)
    heures = st.number_input("Heures d'étude", 0, 15)
    moyenne = st.number_input("Moyenne", 0.0, 20.0)

    submit = st.form_submit_button("Enregistrer")

# 🔥 ENREGISTREMENT
if submit:
    new_data = {
        "Nom": nom,
        "Age": age,
        "Heures étude": heures,
        "Moyenne": moyenne
    }

    st.session_state.data.append(new_data)

    # Sauvegarde dans fichier
    pd.DataFrame(st.session_state.data).to_csv(FILE, index=False)

    st.success("Données enregistrées !")

# 🔥 AFFICHAGE
df = pd.DataFrame(st.session_state.data)

st.write("### 📋 Données")
st.dataframe(df)

# ANALYSE
if not df.empty:
    st.write("### 📊 Statistiques")
    st.write(df.describe())

    st.write("### 📈 Graphique")
    st.bar_chart(df[["Heures étude", "Moyenne"]])
