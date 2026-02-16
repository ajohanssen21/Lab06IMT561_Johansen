import pandas as pd
import streamlit as st


def render_filters(df: pd.DataFrame) -> dict:
    """Rendering filter widgets and returning the chosen values."""
    st.sidebar.header("Filters")

    boroughs = ["All"] + sorted(df["borough"].unique().tolist())
    channels = ["All"] + sorted(df["channel"].unique().tolist())
    complaint_types = sorted(df["complaint_type"].unique().tolist())

    borough = st.sidebar.selectbox("Borough", boroughs, index=0)
    channel = st.sidebar.selectbox("Channel", channels, index=0)

    # TODO (DEMO): Convert this selectbox to a multiselect (and update filtering logic)-- DONE

    #Given Code
    #complaint = st.sidebar.selectbox("Complaint Type", ["All"] + complaint_types, index=0)

    #New Code
    complaint_multiselect = st.sidebar.multiselect(
        'Complaint Type',
        complaint_types,
        default=complaint_types)

    # Response time slider
    min_rt, max_rt = float(df["response_time_days"].min()), float(df["response_time_days"].max())
    rt_range = st.sidebar.slider(
        "Response time (days)",
        min_value=0.0,
        max_value=float(max_rt),
        value=(0.0, float(min(30.0, max_rt))),
        step=0.5,
    )

    # TODO (IN-CLASS): Add a checkbox toggle to cap outliers (e.g., at 99th percentile) -- Already done?
    cap_outliers = st.sidebar.checkbox("Cap extreme response times", value=False)

    return {
        "borough": borough,
        "channel": channel,
        "complaint": complaint_multiselect,
        "rt_range": rt_range,
        "cap_outliers": cap_outliers,
    }


def apply_filters(df: pd.DataFrame, selections: dict) -> pd.DataFrame:
    """Applying filter selections to the dataframe."""
    out = df.copy()

    if selections["borough"] != "All":
        out = out[out["borough"] == selections["borough"]]

    if selections["channel"] != "All":
        out = out[out["channel"] == selections["channel"]]

    if selections["complaint"]:
        out = out[out["complaint_type"].isin(selections["complaint"])]

    lo, hi = selections["rt_range"]
    out = out[(out["response_time_days"] >= lo) & (out["response_time_days"] <= hi)]

    # TODO (IN-CLASS): Implement outlier capping when cap_outliers is checked -- DONE
    # HINT: use out["response_time_days"].quantile(0.99)
    if selections["cap_outliers"]:
        perc99 = out["response_time_days"].quantile(0.99)
        out["response_time_days"] = out["response_time_days"].clip(upper=perc99)

    return out.reset_index(drop=True)
