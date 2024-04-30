"""
SQL Optimizer App

This Streamlit app allows users to optimize SQL queries using predefined optimization rules.
Users can select optimization rules, choose to remove common table expressions (CTEs), and
optionally format the optimized query using sqlfmt. The original and optimized queries are
displayed side by side for comparison. Additionally, users can view the source code on GitHub.

Author: [Your Name]

"""

import os
import streamlit as st
from streamlit_ace import st_ace
from util import RULE_MAPPING, SAMPLE_QUERY, apply_optimizations, format_sql_with_sqlfmt

# Set custom Streamlit page configuration
st.set_page_config(
    page_title="SQL Optimizer",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Hide Streamlit default menu and footer
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# Custom CSS styling
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600&display=swap');

    body {
        font-family: 'Open Sans', sans-serif;
        background-color: #f8f9fa; /* Light background */
        color: #333; /* Dark grey text */
    }

    .stButton {
        background-color: #007bff; /* Primary color */
        color: #fff; /* White text */
        padding: 10px 24px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        text-align: center;
        transition: background-color 0.3s ease; /* Smooth color transition */
    }

    .stButton:hover {
        background-color: #0056b3; /* Darker hover color */
    }

    /* Editor styling */
    .ace_editor {
        border-radius: 4px; /* Rounded corners */
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Add subtle box shadow */
    }

    /* Error message styling */
    .stMarkdown.stException {
        padding: 1rem; /* Add padding to error messages */
        background-color: #f8d7da; /* Light red background */
        color: #721c24; /* Dark red text */
        border-radius: 4px; /* Rounded corners */
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Add subtle box shadow */
    }

    /* Success message styling */
    .stMarkdown.stSuccess {
        padding: 1rem; /* Add padding to success messages */
        background-color: #d4edda; /* Light green background */
        color: #155724; /* Dark green text */
        border-radius: 4px; /* Rounded corners */
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Add subtle box shadow */
    }

    /* GitHub link styling */
    .github-link {
        text-align: center;
        margin-top: 2rem;
    }

    .github-link a {
        color: #007bff; /* Primary color */
        text-decoration: none;
        transition: color 0.3s ease; /* Smooth color transition */
    }

    .github-link a:hover {
        color: #0056b3; /* Darker hover color */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Title container
st.markdown(
    """
    <div style="text-align: center;">
        <h1>SQL Optimizer</h1>
    </div>
    """,
    unsafe_allow_html=True,
)

# Rule selector
selected_rules = st.multiselect(
    'Optimization rules:',
    list(RULE_MAPPING.keys()),
    default=list(RULE_MAPPING.keys()),
    key="rules_multiselect",
)

# Checkboxes and button
cols = st.columns(3)
remove_ctes = cols[0].checkbox("Remove CTEs", on_change=None, key="remove_ctes_checkbox")
format_with_sqlfmt = cols[1].checkbox("Lint with sqlfmt", on_change=None, key="format_with_sqlfmt_checkbox")
optimize_button = cols[2].button("Optimize SQL", key="optimize_button")

# Initialize session state
if "new_query" not in st.session_state:
    st.session_state.new_query = ""
if "state" not in st.session_state:
    st.session_state.state = 0

# Input editor
def _generate_editor_widget(value: str, **kwargs) -> str:
    return st_ace(
        value=value,
        height=300,
        theme="twilight",
        language="sql",
        font_size=16,
        wrap=True,
        auto_update=True,
        **kwargs,
    )

left, right = st.columns(2)

with left:
    sql_input = _generate_editor_widget(SAMPLE_QUERY, key="input_editor")

# Optimize and lint query
if optimize_button:
    try:
        rules = [RULE_MAPPING[rule] for rule in selected_rules]
        new_query = apply_optimizations(sql_input, rules, remove_ctes).sql(pretty=True)
        if format_with_sqlfmt:
            new_query = format_sql_with_sqlfmt(new_query)
        st.session_state.new_query = new_query
        st.session_state.state += 1
        st.success("SQL query optimized successfully!")
    except Exception as e:
        st.error(f"Error: {e}")

# Output editor
with right:
    _generate_editor_widget(
        st.session_state.new_query, readonly=True, key=f"ace-{st.session_state.state}"
    )

# Include Font Awesome CSS
st.markdown(
    """
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" rel="stylesheet">
    """,
    unsafe_allow_html=True,
)

# GitHub link
st.markdown(
    """
    <div class="github-link">
        <a href="https://github.com/shubhusion/sql-optimizer-app-main" target="_blank">
            <i class="fab fa-github"></i> View on GitHub
        </a>
    </div>
    """,
    unsafe_allow_html=True,
)
