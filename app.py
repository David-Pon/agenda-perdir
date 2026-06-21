import streamlit as st
import pandas as pd
from datetime import datetime, time, timedelta

# Configuration optimisée pour Mobile
st.set_page_config(page_title="PerDir Équilibre", page_icon="🧘", layout="centered")

# Style CSS pour masquer les éléments superflus sur téléphone et épurer l'interface
st.markdown("""
    <style>
    .reportview-container .main .block-container { max-width: 400px; padding-top: 1rem; }
    .stMetric { background-color: #f0f2f6; padding: 10px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- NAVIGATION MOBILE ---
onglet = st.sidebar.radio("Navigation", ["📊 Tableau de Bord", "📅 Mon Agenda", "⚙️ Réglages"])

# Simulation de la base de données
if 'evenements' not in st.session_state:
    st.session_state.evenements = [
        {"titre": "Réunion Équipe Direction", "date": "2026-06-22", "heures": 4.0, "type": "💼 Pro"},
        {"titre": "Conseil d'Administration", "date": "2026-06-22", "heures": 3.5, "type": "🌙 Réunion Tardive"},
        {"titre": "Pause Marche / Sport", "date": "2026-06-23", "heures": 1.0, "type": "🌿 Perso"},
    ]

# --- ONGLET 1 : TABLEAU DE BORD (VUE MOBILE CORPS) ---
if onglet == "📊 Tableau de Bord":
    st.title("🧘 Mon Équilibre")
    
    # Calculs rapides
    heures_pro = sum(ev["heures"] for ev in st.session_state.evenements if "Pro" in ev["type"] or "Tardive" in ev["type"])
    heures_perso = sum(ev["heures"] for ev in st.session_state.evenements if "Perso" in ev["type"])
    
    # Affichage en grille verticale (adaptée aux téléphones)
    st.metric("💼 Temps Pro Cumulé", f"{heures_pro} h")
    st.write("")
    st.metric("🌿 Temps Perso Posé", f"{heures_perso} h / 4h mini")
    
    st.subheader("🤖 Assistant Bien-être")
    # Logique d'alerte PerDir
    has_ca = any(ev["type"] == "🌙 Réunion Tardive" for ev in st.session_state.evenements)
    if has_ca:
        st.warning("💡 **Sas requis :** CA détecté. Pensez à décaler votre arrivée à 9h00 demain.")
    if heures_pro > 10:
        st.error("⚠️ **Alerte Surcharge :** Journée de plus de 10h constatée.")

# --- ONGLET 2 : AGENDA ---
elif onglet == "📅 Mon Agenda":
    st.title("📅 Mes Créneaux")
    
    # Bouton d'action rapide mobile
    with st.expander("➕ Bloquer du temps pour soi", expanded=False):
        type_pause = st.selectbox("Activité", ["Marche / Sport", "Rendez-vous Médical", "Déconnexion"])
        duree_pause = st.slider("Durée (heures)", 0.5, 2.0, 1.0, 0.5)
        if st.button("Valider le créneau"):
            st.session_state.evenements.append({"titre": type_pause, "date": "2026-06-23", "heures": duree_pause, "type": "🌿 Perso"})
            st.success("Créneau verrouillé !")
            st.rerun()
            
    # Liste des événements sous forme de "Cartes" lisibles sur mobile
    st.write("---")
    for ev in st.session_state.evenements:
        st.markdown(f"**{ev['type']} - {ev['titre']}**")
        st.caption(f"Date : {ev['date']} | Durée : {ev['heures']}h")
        st.markdown("---")

# --- ONGLET 3 : RÉGLAGES ---
elif onglet == "⚙️ Réglages":
    st.title("⚙️ Seuils PerDir")
    seuil = st.slider("Limite journalière (heures)", 8, 12, 10)
    st.info("Ces paramètres ajustent les alertes de votre assistant sur votre téléphone.")
