"""
Halle's Visualizations
TODO: Halle - Implement your 2 visualizations here
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import sys

sys.path.append('..')
from utils.db_connection import execute_query

# Page config
st.set_page_config(page_title="Halle's Visualizations", page_icon="🎭", layout="wide")

st.title("🎭 Halle's Visualizations")
st.markdown("---")

# ============================================
# VISUALIZATION 1 - TODO: HALLE
# ============================================

st.header("📊 Visualization 1")
st.info("TODO: Halle - Implement your first visualization here")
st.markdown("Check `utils/queries.py` for available query functions")

st.markdown("---")

# ============================================
# VISUALIZATION 2 - TODO: HALLE
# ============================================

st.header("📊 Visualization 2")
st.info("TODO: Halle - Implement your second visualization here")
st.markdown("Check `utils/queries.py` for available query functions")

st.markdown("---")
st.caption("Halle's Visualizations | DMQL Phase 3")
