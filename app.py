import pandas as pd
import streamlit as st

from llm import call_llm_json, model_label
from prompts import ANALYZE_TEMPLATE, SYSTEM

st.set_page_config(page_title="WTQ 2026 Project", page_icon="✨", layout="wide")

st.title("✨ Project Title Here")
st.caption("One-line value statement: who it helps, what problem it solves, what it saves.")

with st.sidebar:
    st.header("Settings")
    st.write(f"Model: `{model_label()}`")
    uploaded = st.file_uploader("Upload dataset (CSV)", type=["csv"])
    st.divider()
    st.write("Tip: add example inputs below for one-click demos.")

df = pd.read_csv(uploaded) if uploaded else None
if df is not None:
    with st.expander("Dataset preview", expanded=False):
        st.dataframe(df.head(50), use_container_width=True)

EXAMPLES = ["Example input 1", "Example input 2"]
example = st.selectbox("Try an example", [""] + EXAMPLES)
user_input = st.text_area("Your input", value=example, height=140)

if st.button("Analyze", type="primary"):
    if not user_input.strip():
        st.warning("Please enter some input first.")
    else:
        context = df.head(20).to_csv(index=False) if df is not None else "No dataset loaded."
        with st.spinner("Thinking..."):
            try:
                result = call_llm_json(
                    ANALYZE_TEMPLATE.format(user_input=user_input, context=context),
                    system=SYSTEM,
                )
            except Exception as e:
                st.error(f"Something went wrong: {e}. Please try again.")
                st.stop()

        c1, c2 = st.columns([2, 1])
        with c1:
            st.subheader("Summary")
            st.write(result.get("summary", ""))
            st.subheader("Key points")
            for p in result.get("key_points", []):
                st.markdown(f"- {p}")
        with c2:
            st.metric("Score", result.get("risk_or_score", "N/A"))
            st.info(result.get("recommended_action", ""))
        with st.expander("Raw JSON"):
            st.json(result)
