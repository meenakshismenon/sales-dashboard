import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Sales Performance Dashboard",
    page_icon="📊",
    layout="wide",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    .block-container { padding-top: 1.5rem; padding-bottom: 1.5rem; }
    .metric-card {
        background: white;
        border-radius: 10px;
        padding: 1rem 1.25rem;
        border: 1px solid #e9ecef;
    }
    div[data-testid="metric-container"] {
        background: white;
        border: 1px solid #e9ecef;
        border-radius: 10px;
        padding: 1rem 1.25rem;
    }
    div[data-testid="metric-container"] label {
        font-size: 12px !important;
        color: #6c757d !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    div[data-testid="metric-container"] div[data-testid="metric-value"] {
        font-size: 1.6rem !important;
        font-weight: 600;
    }
    .section-header {
        font-size: 13px;
        font-weight: 600;
        color: #6c757d;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
    }
    .badge-hi  { background:#EAF3DE; color:#27500A; padding:2px 8px; border-radius:20px; font-size:12px; font-weight:600; }
    .badge-md  { background:#FAEEDA; color:#633806; padding:2px 8px; border-radius:20px; font-size:12px; font-weight:600; }
    .badge-lo  { background:#FCEBEB; color:#791F1F; padding:2px 8px; border-radius:20px; font-size:12px; font-weight:600; }
    h1, h2, h3 { font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# ── Data 
MONTHS     = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
ACTUAL     = [310,355,390,420,460,510,490,530,570,620,580,590]
TARGET     = [340,360,380,400,440,480,500,520,550,580,560,580]

df_monthly = pd.DataFrame({"Month": MONTHS, "Actual ($K)": ACTUAL, "Target ($K)": TARGET})

df_products = pd.DataFrame({
    "Product":  ["ProBook X500","AirPods Max 3","Sofa Luxe Pro","UltraRun Shoes","SmartWatch S9"],
    "Revenue":  ["$812K","$634K","$511K","$429K","$388K"],
    "Growth":   ["+24%","+18%","+7%","+4%","-2%"],
    "Badge":    ["hi","hi","md","md","lo"],
})

df_region = pd.DataFrame({
    "Region":  ["North America","Europe","Asia Pacific","Latin America","Middle East"],
    "Revenue": [1820,1250,960,530,260],
})

df_category = pd.DataFrame({
    "Category": ["Electronics","Apparel","Home","Other"],
    "Share":    [38,24,20,18],
})

COLORS = ["#185FA5","#1D9E75","#D85A30","#BA7517","#888780"]

# ── Sidebar filter ────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("📊 Sales Dashboard")
    st.markdown("**FY 2024**")
    st.divider()

    period = st.radio("Time period", ["All Year","H1 (Jan–Jun)","H2 (Jul–Dec)"])
    st.divider()

    st.markdown("**Quick filters**")
    show_target = st.checkbox("Show target line", value=True)
    selected_regions = st.multiselect(
        "Regions",
        df_region["Region"].tolist(),
        default=df_region["Region"].tolist(),
    )

# ── Period slicing ────────────────────────────────────────────────────────────
if period == "H1 (Jan–Jun)":
    df_plot = df_monthly.iloc[:6]
    kpi = {"rev":"$2.24M","rev_d":15.2,"units":"17,890","units_d":9.8,"aov":"$125.2","aov_d":5.1,"ret":"3.4%","ret_d":-0.2}
elif period == "H2 (Jul–Dec)":
    df_plot = df_monthly.iloc[6:]
    kpi = {"rev":"$2.58M","rev_d":21.1,"units":"20,520","units_d":14.3,"aov":"$125.8","aov_d":5.9,"ret":"3.0%","ret_d":-0.6}
else:
    df_plot = df_monthly
    kpi = {"rev":"$4.82M","rev_d":18.4,"units":"38,410","units_d":12.1,"aov":"$125.5","aov_d":5.6,"ret":"3.2%","ret_d":-0.4}

df_region_filtered = df_region[df_region["Region"].isin(selected_regions)]

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("## Sales Performance Dashboard")
st.markdown(f"**FY 2024 · All regions · {period}**")
st.divider()

# ── KPI row ───────────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Revenue",     kpi["rev"],   f"▲ {kpi['rev_d']}% vs LY")
k2.metric("Units Sold",        kpi["units"], f"▲ {kpi['units_d']}% vs LY")
k3.metric("Avg Order Value",   kpi["aov"],   f"▲ {kpi['aov_d']}% vs LY")
k4.metric("Return Rate",       kpi["ret"],   f"▼ {abs(kpi['ret_d'])}pp vs LY", delta_color="inverse")

st.markdown("<br>", unsafe_allow_html=True)

# ── Row 1: Revenue chart + Donut ──────────────────────────────────────────────
col_left, col_right = st.columns([2, 1], gap="medium")

with col_left:
    st.markdown('<p class="section-header">Monthly Revenue vs Target</p>', unsafe_allow_html=True)
    fig_line = go.Figure()
    fig_line.add_trace(go.Bar(
        x=df_plot["Month"], y=df_plot["Actual ($K)"],
        name="Actual", marker_color="#185FA5",
        marker_cornerradius=4,
    ))
    if show_target:
        fig_line.add_trace(go.Scatter(
            x=df_plot["Month"], y=df_plot["Target ($K)"],
            name="Target", mode="lines",
            line=dict(color="#D85A30", width=2, dash="dot"),
        ))
    fig_line.update_layout(
        height=280, margin=dict(t=10, b=10, l=0, r=10),
        plot_bgcolor="white", paper_bgcolor="white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        yaxis=dict(tickprefix="$", ticksuffix="K", gridcolor="#f0f0f0"),
        xaxis=dict(showgrid=False),
        bargap=0.35,
    )
    st.plotly_chart(fig_line, use_container_width=True)

with col_right:
    st.markdown('<p class="section-header">Revenue by Category</p>', unsafe_allow_html=True)
    fig_donut = go.Figure(go.Pie(
        labels=df_category["Category"],
        values=df_category["Share"],
        hole=0.65,
        marker=dict(colors=COLORS[:4], line=dict(color="white", width=2)),
        textinfo="percent",
        hovertemplate="%{label}: %{value}%<extra></extra>",
    ))
    fig_donut.update_layout(
        height=280, margin=dict(t=10, b=10, l=10, r=10),
        paper_bgcolor="white",
        showlegend=True,
        legend=dict(orientation="v", x=1.0, y=0.5, font=dict(size=11)),
    )
    st.plotly_chart(fig_donut, use_container_width=True)

# ── Row 2: Products table + Region bars ──────────────────────────────────────
col_a, col_b = st.columns(2, gap="medium")

with col_a:
    st.markdown('<p class="section-header">Top Products</p>', unsafe_allow_html=True)

    badge_map = {"hi":"badge-hi","md":"badge-md","lo":"badge-lo"}

    header = "<table style='width:100%;border-collapse:collapse;font-size:13px;'>"
    header += "<thead><tr style='background:#f8f9fa;'>"
    for col in ["#","Product","Revenue","Growth"]:
        header += f"<th style='padding:8px 12px;text-align:left;font-size:12px;color:#6c757d;font-weight:600;border-bottom:1px solid #e9ecef;'>{col}</th>"
    header += "</tr></thead><tbody>"

    rows = ""
    for i, row in df_products.iterrows():
        badge_class = badge_map[row["Badge"]]
        rows += f"""
        <tr style='border-bottom:1px solid #f0f0f0;'>
          <td style='padding:9px 12px;color:#adb5bd;'>{i+1}</td>
          <td style='padding:9px 12px;font-weight:500;'>{row["Product"]}</td>
          <td style='padding:9px 12px;'>{row["Revenue"]}</td>
          <td style='padding:9px 12px;'><span class='{badge_class}'>{row["Growth"]}</span></td>
        </tr>"""

    st.markdown(header + rows + "</tbody></table>", unsafe_allow_html=True)

with col_b:
    st.markdown('<p class="section-header">Revenue by Region</p>', unsafe_allow_html=True)
    fig_bar = go.Figure(go.Bar(
        x=df_region_filtered["Revenue"],
        y=df_region_filtered["Region"],
        orientation="h",
        marker=dict(color=COLORS[:len(df_region_filtered)], cornerradius=4),
        text=[f"${v:,}K" for v in df_region_filtered["Revenue"]],
        textposition="outside",
        hovertemplate="%{y}: $%{x:,}K<extra></extra>",
    ))
    fig_bar.update_layout(
        height=280,
        margin=dict(t=10, b=10, l=0, r=60),
        plot_bgcolor="white", paper_bgcolor="white",
        xaxis=dict(showgrid=True, gridcolor="#f0f0f0", tickprefix="$", ticksuffix="K", showticklabels=False),
        yaxis=dict(showgrid=False),
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.divider()
st.caption("Sales Dashboard · FY 2024 · Data is illustrative · Built with Streamlit + Plotly")
