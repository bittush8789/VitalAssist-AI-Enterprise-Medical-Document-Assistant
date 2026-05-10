import streamlit as st
import pandas as pd
import plotly.express as px
from dashboard.data_tracker import get_stats, load_history
from collections import Counter

def render_analytics():
    st.markdown('<h1 class="main-title">Healthcare Insights</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Live analytics from your processed medical documents</p>', unsafe_allow_html=True)

    stats = get_stats()
    history = stats["history"]

    # Top Metrics
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
        <div class="glass-card" style="text-align:center; padding:1.5rem;">
            <div class="metric-label">Total Reports</div>
            <div class="metric-value">{stats['total_reports']}</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="glass-card" style="text-align:center; padding:1.5rem;">
            <div class="metric-label">Unique Diagnoses</div>
            <div class="metric-value">{len(set(stats['all_diagnoses']))}</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class="glass-card" style="text-align:center; padding:1.5rem;">
            <div class="metric-label">Medications Found</div>
            <div class="metric-value">{len(set(stats['all_medications']))}</div>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown(f"""
        <div class="glass-card" style="text-align:center; padding:1.5rem;">
            <div class="metric-label">This Month</div>
            <div class="metric-value">{list(stats['monthly'].values())[-1] if stats['monthly'] else 0}</div>
        </div>
        """, unsafe_allow_html=True)

    if stats["total_reports"] == 0:
        st.info("📭 No documents processed yet. Upload a medical document in **Document Processing** to see real analytics here.")
        return

    CHART_FONT = dict(family="Outfit, sans-serif", size=14, color="#1E293B")
    CHART_LAYOUT = dict(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=CHART_FONT,
        legend=dict(font=dict(color="#1E293B", size=12)),
        margin=dict(l=20, r=20, t=40, b=20)
    )

    # Charts Row
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="color:#1E293B;">🩺 Top Diagnoses Detected</h3>', unsafe_allow_html=True)
        if stats["all_diagnoses"]:
            diag_counts = Counter(stats["all_diagnoses"]).most_common(10)
            df_diag = pd.DataFrame(diag_counts, columns=["Diagnosis", "Count"])
            fig = px.pie(df_diag, values="Count", names="Diagnosis", hole=0.4,
                         color_discrete_sequence=["#3B82F6", "#60A5FA", "#93C5FD", "#BFDBFE", "#1E40AF",
                                                  "#2563EB", "#1D4ED8", "#DBEAFE", "#EFF6FF", "#1E3A8A"])
            fig.update_layout(**CHART_LAYOUT)
            fig.update_traces(textfont_color="#1E293B", textfont_size=13)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.caption("No diagnosis data yet.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="color:#1E293B;">💊 Top Medications</h3>', unsafe_allow_html=True)
        if stats["all_medications"]:
            med_counts = Counter(stats["all_medications"]).most_common(10)
            df_med = pd.DataFrame(med_counts, columns=["Medication", "Count"])
            fig_med = px.bar(df_med, x="Medication", y="Count",
                             color_discrete_sequence=["#3B82F6"])
            fig_med.update_layout(**CHART_LAYOUT)
            fig_med.update_layout(xaxis=dict(tickfont=dict(color="#1E293B", size=12)),
                                  yaxis=dict(tickfont=dict(color="#1E293B", size=12)))
            st.plotly_chart(fig_med, use_container_width=True)
        else:
            st.caption("No medication data yet.")
        st.markdown('</div>', unsafe_allow_html=True)

    # Monthly Trend
    if stats["monthly"]:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="color:#1E293B;">📈 Monthly Document Volume</h3>', unsafe_allow_html=True)
        df_monthly = pd.DataFrame(list(stats["monthly"].items()), columns=["Month", "Reports"])
        fig_trend = px.area(df_monthly, x="Month", y="Reports", markers=True)
        fig_trend.update_traces(fillcolor="rgba(59, 130, 246, 0.2)", line_color="#3B82F6")
        fig_trend.update_layout(**CHART_LAYOUT)
        fig_trend.update_layout(xaxis=dict(tickfont=dict(color="#1E293B", size=12)),
                                yaxis=dict(tickfont=dict(color="#1E293B", size=12)))
        st.plotly_chart(fig_trend, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Recent Processing History Table
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color:#1E293B;">📋 Recent Processing History</h3>', unsafe_allow_html=True)
    table_data = []
    for rec in history[-10:][::-1]:
        diag_list = rec.get("diagnosis", {}).get("diagnosis", []) if isinstance(rec.get("diagnosis"), dict) else []
        table_data.append({
            "Time": rec.get("timestamp", "N/A"),
            "File": rec.get("filename", "N/A"),
            "Diagnoses Found": ", ".join(diag_list[:3]) if diag_list else "None",
            "Status": "✅ Completed"
        })
    if table_data:
        st.dataframe(pd.DataFrame(table_data), use_container_width=True, hide_index=True)
    else:
        st.caption("No records yet.")
    st.markdown('</div>', unsafe_allow_html=True)
