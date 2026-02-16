import pandas as pd
import streamlit as st

from src.charts import plot_response_hist, plot_borough_bar


def header_metrics(df: pd.DataFrame) -> None:
    """Rendering header metrics. Placeholder values are intentional."""
    c1, c2, c3 = st.columns(3)

    # TODO (IN-CLASS): Replace these placeholders with real metrics from df
    # Suggestions:
    # - Total complaints (len(df))
    # - Median response time
    # - % from Web vs Phone vs App (pick one)
    with c1:
        st.metric("Total complaints", (len(df)))
    with c2:
        st.metric("Median response (days)",round(df["response_time_days"].median(),1))
    with c3:
        st.metric("Most common complaint", df["complaint_type"].mode()[0])


def body_layout_tabs(df: pd.DataFrame) -> None:
    """Tabs layout with 3 default tabs."""
    t1, t2, t3 = st.tabs(["Distribution", "By Borough", "Table"])

    with t1:
        st.subheader("Response Time Distribution")
        plot_response_hist(df)

        # TODO (IN-CLASS): Add a short interpretation sentence under the chart -- done
        st.caption("Most complaints are resolved within 2 weeks")

    with t2:
        st.subheader("Median Response Time by Borough")
        plot_borough_bar(df)

        # TODO (IN-CLASS): Add a second view here (e.g., count by borough) -- Done
        st.subheader("Complaints by Borough")
        borough_counts = df["borough"].value_counts()
        st.bar_chart(borough_counts)

    with t3:
        st.subheader("Filtered Rows")
        st.dataframe(df, use_container_width=True, height=480)

        # TODO (OPTIONAL): Add st.download_button to export filtered rows -- Done

    st.download_button(label="Download Filtered Data", data= df.to_csv(index= False), file_name="filtered_complaints", mime="text/csv")
