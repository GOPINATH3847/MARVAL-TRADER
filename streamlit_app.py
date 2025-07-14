import streamlit as st
import os
import datetime

st.set_page_config(page_title="MARVEL-TRADER", layout="wide")
st.title("💥 MARVEL TRADER DASHBOARD")

if "bot_active" not in st.session_state:
    st.session_state.bot_active = False

st.markdown("### Status: " + ("🟢 Bot Running" if st.session_state.bot_active else "🔴 Bot Stopped"))

if st.button("▶️ Start Bot"):
    st.session_state.bot_active = True
    st.success("Bot Started")

if st.button("⏹ Stop Bot"):
    st.session_state.bot_active = False
    st.warning("Bot Stopped")

st.markdown("---")
st.markdown("**Time:** " + str(datetime.datetime.now()))
st.markdown("**Version:** SMC + Wyckoff + ICT")

st.markdown("---")
st.caption("© 2025 Gopi's MARVEL-TRADER powered by Streamlit + MT5 + Telegram")
