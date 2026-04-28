import streamlit as st
import pandas as pd
import os
import numpy as np

st.title("📊 Analyse des performances des étudiants")

FILE = "data.csv"

# 🔥 Chargement des données
if "data" not in st.session_state:
    if os.path.exists(FILE):
        st.session_state.data = pd.read_csv(FILE).to_dict("records")
    else:
        st.session_state.data = []

# 📥 FORMULAIRE
with st.form("form"):
    nom = st.text_input("Nom")
    age = st.number_input("Âge", 15, 40)
    heures = st.number_input("Heures d'étude", 0, 15)
    telephone = st.number_input("Temps sur téléphone", 0, 15)
    moyenne = st.number_input("Moyenne", 0.0, 20.0)

    submit = st.form_submit_button("Enregistrer")

# 💾 ENREGISTREMENT
if submit:
    new_data = {
        "Nom": nom,
        "Age": age,
        "Heures étude": heures,
        "Téléphone": telephone,
        "Moyenne": moyenne
    }

    st.session_state.data.append(new_data)
    pd.DataFrame(st.session_state.data).to_csv(FILE, index=False)

    st.success("Données enregistrées !")

# 📊 AFFICHAGE
df = pd.DataFrame(st.session_state.data)

st.write("### 📋 Données collectées")
st.dataframe(df)

# 📊 ANALYSE DESCRIPTIVE
if not df.empty:
    st.write("### 📊 Statistiques descriptives")
    st.write(df.describe())

    # 🔗 CORRÉLATION
    st.write("### 🔗 Matrice de corrélation")
    corr = df.corr(numeric_only=True)
    st.write(corr)

    # 📈 GRAPHIQUES
    st.write("### 📈 Graphiques")

    st.write("Relation Heures d'étude vs Moyenne")
    st.line_chart(df[["Heures étude", "Moyenne"]])

    st.write("Téléphone vs Moyenne")
    st.bar_chart(df[["Téléphone", "Moyenne"]])

    # 📉 RÉGRESSION LINÉAIRE SIMPLE
    st.write("### 📉 Régression linéaire (Heures d'étude → Moyenne)")

    if len(df) > 1:
        x = df["Heures étude"]
        y = df["Moyenne"]

        coef = np.polyfit(x, y, 1)
        poly1d_fn = np.poly1d(coef)

        df["Prédiction"] = poly1d_fn(x)

        st.write("Équation : y =", round(coef[0],2), "x +", round(coef[1],2))
        st.line_chart(df[["Moyenne", "Prédiction"]])
