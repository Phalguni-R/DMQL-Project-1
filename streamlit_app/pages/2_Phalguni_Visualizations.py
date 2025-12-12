"""
Phalguni's Visualizations
TODO: Phalguni - Implement your 2 visualizations here
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import sys
sys.path.append('..')
from utils.db_connection import execute_query

# Page config
st.set_page_config(page_title="Phalguni's Visualizations", page_icon="🎨", layout="wide")

st.title("🎨 Phalguni's Visualizations")
st.markdown("---")

# ============================================
# VISUALIZATION 1 - TODO: PHALGUNI
# ============================================

st.header("📊 Visualization 1")
st.info("TODO: Phalguni - Implement your first visualization here")
st.markdown("Check `utils/queries.py` for available query functions")

st.markdown("---")

# ============================================
# VISUALIZATION 2 - TODO: PHALGUNI
# ============================================

st.header("📊 Visualization 2")
st.info("TODO: Phalguni - Implement your second visualization here")
st.markdown("Check `utils/queries.py` for available query functions")

st.markdown("---")
st.caption("Phalguni's Visualizations | DMQL Phase 3")
