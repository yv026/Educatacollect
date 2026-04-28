import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import io
from datetime import datetime

st.set_page_config(
    page_title="EduData Insight",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #f8fafc;
    color: #1e293b;
}
[data-testid="stSidebar"] { background-color: #1e293b !important; }
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
.app-header {
    background: linear-gradient(90deg, #1e293b 0%, #334155 100%);
    color: white; padding: 1.8rem 2rem; border-radius: 12px; margin-bottom: 1.8rem;
}
.app-header h1 { font-size: 1.9rem; font-weight: 700; margin: 0; }
.app-header p  { margin: 0.2rem 0 0; font-size: 0.88rem; opacity: 0.6; }
.sec-header {
    font-size: 1.35rem; font-weight: 700; color: #1e293b;
    margin: 1.2rem 0 1rem; padding-bottom: 0.6rem;
    border-bottom: 2px solid #e2e8f0;
}
.kpi-card {
    background: white; border: 1px solid #e2e8f0; border-radius: 12px;
    padding: 1.3rem 1.4rem; border-left: 4px solid #3b82f6;
    box-shadow: 0 1px 6px rgba(0,0,0,0.05);
}
.kpi-val { font-size: 1.8rem; font-weight: 700; color: #1e293b; }
.kpi-lbl { font-size: 0.73rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px; margin-top: 0.3rem; }
.stButton > button {
    background: #3b82f6 !important; color: white !important;
    border: none !important; border-radius: 8px !important; font-weight: 600 !important;
}
.stTabs [data-baseweb="tab-list"] { gap: 4px; background: #f1f5f9; padding: 6px; border-radius: 10px; }
.stTabs [data-baseweb="tab"] { border-radius: 7px; font-weight: 500; font-size: 0.88rem; color: #64748b; }
.stTabs [aria-selected="true"] { background: white !important; color: #1e293b !important; }
.info-box {
    background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 10px;
    padding: 0.9rem 1.2rem; font-size: 0.9rem; color: #1d4ed8; margin-bottom: 1rem;
}
.divider { height: 1px; background: #e2e8f0; margin: 1.2rem 0; }
</style>
""", unsafe_allow_html=True)

COLS = [
    "Horodatage","Nom","Filière","Niveau","Genre","Âge","Région",
    "Bourse","Accès_internet","Travail_partiel","Mode_études",
    "Note_Maths","Note_Physique","Note_Info","Note_Français","Note_Anglais",
    "Heures_étude_jour","Heures_sommeil","Absences_semaine","Satisfaction",
    "Objectif_professionnel"
]
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=COLS)

st.markdown("""
<div class="app-header">
    <h1>🎓 EduData Insight</h1>
    <p>Application de collecte et d'analyse des performances des étudiants · INF 232 EC2</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🎓 EduData Insight")
    st.markdown("---")
    page = st.radio("Navigation", [
        "📋 Collecte des données",
        "📊 Tableau de bord",
        "🔍 Analyse descriptive",
        "📁 Données brutes"
    ])
    st.markdown("---")
    st.markdown(f"**Enregistrements :** `{len(st.session_state.data)}`")
    st.markdown("**Cours :** INF 232 EC2")
    st.markdown("**Auteur :** Kenne Mbasso Yvan")
    st.markdown("**Matricule :** 24F2736")

df = st.session_state.data

if page == "📋 Collecte des données":
    st.markdown('<div class="sec-header">📋 Collecte des données</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-box">📌 Remplissez les informations puis cliquez sur <strong>Enregistrer</strong>.</div>', unsafe_allow_html=True)
    with st.form("form_collecte", clear_on_submit=True):
        st.markdown("**👤 Identité**")
        c1, c2, c3 = st.columns(3)
        nom    = c1.text_input("Nom de l'étudiant *")
        genre  = c2.selectbox("Genre", ["Masculin","Féminin","Autre"])
        age    = c3.number_input("Âge", 15, 60, 20)
        c4, c5 = st.columns(2)
        region = c4.selectbox("Région", ["Adamaoua","Centre","Est","Extrême-Nord","Littoral","Nord","Nord-Ouest","Ouest","Sud","Sud-Ouest"])
        objectif = c5.text_input("Objectif professionnel")
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown("**🏫 Parcours académique**")
        c6, c7, c8, c9, c10 = st.columns(5)
        filiere = c6.selectbox("Filière", ["Informatique","Génie Civil","Électronique","Économie","Médecine","Droit","Lettres","Autre"])
        niveau  = c7.selectbox("Niveau", ["Licence 1","Licence 2","Licence 3","Master 1","Master 2","Doctorat"])
        mode    = c8.selectbox("Mode", ["Présentiel","À distance","Hybride"])
        bourse  = c9.selectbox("Bourse ?", ["Non","Oui - Nationale","Oui - Internationale"])
        travail = c10.selectbox("Travail ?", ["Non","Oui"])
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown("**📝 Notes (sur 20)**")
        n1, n2, n3, n4, n5 = st.columns(5)
        n_math = n1.number_input("Maths", 0.0, 20.0, 10.0, 0.5)
        n_phy  = n2.number_input("Physique", 0.0, 20.0, 10.0, 0.5)
        n_info = n3.number_input("Informatique", 0.0, 20.0, 10.0, 0.5)
        n_fr   = n4.number_input("Français", 0.0, 20.0, 10.0, 0.5)
        n_en   = n5.number_input("Anglais", 0.0, 20.0, 10.0, 0.5)
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown("**📌 Habitudes**")
        h1, h2, h3, h4, h5 = st.columns(5)
        heures_etude   = h1.number_input("Heures étude/jour", 0, 24, 3)
        heures_sommeil = h2.number_input("Heures sommeil", 0, 24, 7)
        absences       = h3.number_input("Absences/semaine", 0, 40, 2)
        satisfaction   = h4.slider("Satisfaction /10", 1, 10, 6)
        internet       = h5.selectbox("Internet ?", ["Oui","Non"])
        submitted = st.form_submit_button("✅ Enregistrer l'étudiant")
        if submitted:
            if not nom.strip():
                st.error("⚠️ Le nom est obligatoire.")
            else:
                row = {
                    "Horodatage": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Nom": nom.strip(), "Filière": filiere, "Niveau": niveau,
                    "Genre": genre, "Âge": age, "Région": region,
                    "Bourse": bourse, "Accès_internet": internet,
                    "Travail_partiel": travail, "Mode_études": mode,
                    "Note_Maths": n_math, "Note_Physique": n_phy,
                    "Note_Info": n_info, "Note_Français": n_fr, "Note_Anglais": n_en,
                    "Heures_étude_jour": heures_etude, "Heures_sommeil": heures_sommeil,
                    "Absences_semaine": absences, "Satisfaction": satisfaction,
                    "Objectif_professionnel": objectif
                }
                st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([row])], ignore_index=True)
                st.success(f"✅ {nom.strip()} enregistré(e) ! Total : {len(st.session_state.data)}")
                st.balloons()

elif page == "📊 Tableau de bord":
    st.markdown('<div class="sec-header">📊 Tableau de bord</div>', unsafe_allow_html=True)
    if df.empty:
        st.info("ℹ️ Aucune donnée. Allez sur Collecte des données.")
    else:
        df = df.copy()
        notes = ["Note_Maths","Note_Physique","Note_Info","Note_Français","Note_Anglais"]
        df["Moyenne"] = df[notes].mean(axis=1).round(2)
        k1, k2, k3, k4 = st.columns(4)
        admis = (df["Moyenne"] >= 10).sum()
        with k1: st.markdown(f'<div class="kpi-card"><div class="kpi-val">{len(df)}</div><div class="kpi-lbl">Étudiants</div></div>', unsafe_allow_html=True)
        with k2: st.markdown(f'<div class="kpi-card"><div class="kpi-val">{df["Moyenne"].mean():.2f}/20</div><div class="kpi-lbl">Moyenne générale</div></div>', unsafe_allow_html=True)
        with k3: st.markdown(f'<div class="kpi-card"><div class="kpi-val">{df["Absences_semaine"].mean():.1f}h</div><div class="kpi-lbl">Absences moy.</div></div>', unsafe_allow_html=True)
        with k4: st.markdown(f'<div class="kpi-card"><div class="kpi-val">{admis}/{len(df)}</div><div class="kpi-lbl">Admis (≥10)</div></div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            gc = df["Genre"].value_counts().reset_index(); gc.columns = ["Genre","N"]
            fig = px.pie(gc, names="Genre", values="N", title="Répartition par genre", color_discrete_sequence=["#3b82f6","#f59e0b","#10b981"])
            fig.update_layout(paper_bgcolor="white"); st.plotly_chart(fig, use_container_width=True)
        with col2:
            nc = df["Niveau"].value_counts().reset_index(); nc.columns = ["Niveau","N"]
            fig2 = px.bar(nc, x="Niveau", y="N", title="Par niveau", color_discrete_sequence=["#3b82f6"])
            fig2.update_layout(paper_bgcolor="white", showlegend=False); st.plotly_chart(fig2, use_container_width=True)
        col3, col4 = st.columns(2)
        with col3:
            fig3 = go.Figure()
            for note, color in zip(notes, ["#3b82f6","#f59e0b","#10b981","#ef4444","#8b5cf6"]):
                fig3.add_trace(go.Box(y=df[note], name=note.replace("Note_",""), marker_color=color))
            fig3.update_layout(title="Notes par matière", paper_bgcolor="white"); st.plotly_chart(fig3, use_container_width=True)
        with col4:
            rc = df["Région"].value_counts().reset_index(); rc.columns = ["Région","N"]
            fig4 = px.bar(rc, x="N", y="Région", orientation="h", title="Par région", color_discrete_sequence=["#10b981"])
            fig4.update_layout(paper_bgcolor="white"); st.plotly_chart(fig4, use_container_width=True)

elif page == "🔍 Analyse descriptive":
    st.markdown('<div class="sec-header">🔍 Analyse descriptive</div>', unsafe_allow_html=True)
    if df.empty:
        st.info("ℹ️ Aucune donnée disponible.")
    else:
        df = df.copy()
        notes = ["Note_Maths","Note_Physique","Note_Info","Note_Français","Note_Anglais"]
        df["Moyenne"] = df[notes].mean(axis=1).round(2)
        tab1, tab2, tab3 = st.tabs(["📈 Statistiques","🔗 Corrélations","📊 Comparaisons"])
        with tab1:
            num_cols = notes + ["Heures_étude_jour","Heures_sommeil","Absences_semaine","Satisfaction","Âge","Moyenne"]
            stats = df[num_cols].describe().T.round(2)
            stats.columns = ["N","Moyenne","Écart-type","Min","Q1","Médiane","Q3","Max"]
            st.dataframe(stats, use_container_width=True)
            fig = px.histogram(df, x="Moyenne", nbins=15, color_discrete_sequence=["#3b82f6"], title="Distribution des moyennes")
            fig.add_vline(x=10, line_dash="dash", line_color="#ef4444", annotation_text="Seuil (10)")
            fig.update_layout(paper_bgcolor="white"); st.plotly_chart(fig, use_container_width=True)
        with tab2:
            corr = df[notes + ["Heures_étude_jour","Heures_sommeil","Absences_semaine","Satisfaction"]].dropna().corr().round(2)
            fig2 = px.imshow(corr, text_auto=True, color_continuous_scale="Blues", title="Matrice de corrélation", aspect="auto")
            fig2.update_layout(paper_bgcolor="white"); st.plotly_chart(fig2, use_container_width=True)
        with tab3:
            by_fil = df.groupby("Filière")["Moyenne"].mean().reset_index().sort_values("Moyenne", ascending=False)
            fig3 = px.bar(by_fil, x="Filière", y="Moyenne", title="Moyenne par filière", color_discrete_sequence=["#3b82f6"])
            fig3.add_hline(y=10, line_dash="dash", line_color="#ef4444")
            fig3.update_layout(paper_bgcolor="white"); st.plotly_chart(fig3, use_container_width=True)

elif page == "📁 Données brutes":
    st.markdown('<div class="sec-header">📁 Données brutes</div>', unsafe_allow_html=True)
    if df.empty:
        st.info("ℹ️ Aucune donnée disponible.")
    else:
        search = st.text_input("🔎 Rechercher un étudiant")
        disp = df[df["Nom"].str.contains(search, case=False, na=False)] if search else df
        st.dataframe(disp, use_container_width=True, height=420)
        col_a, col_b = st.columns(2)
        col_a.download_button("⬇️ CSV", data=df.to_csv(index=False).encode("utf-8"),
                              file_name="EduData.csv", mime="text/csv")
        buf = io.BytesIO(); df.to_excel(buf, index=False, engine="openpyxl")
        col_b.download_button("⬇️ Excel", data=buf.getvalue(),
                              file_name="EduData.xlsx",
                              mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        if st.button("🗑️ Supprimer toutes les données"):
            st.session_state.data = pd.DataFrame(columns=COLS)
            st.success("✅ Données supprimées."); st.rerun()

