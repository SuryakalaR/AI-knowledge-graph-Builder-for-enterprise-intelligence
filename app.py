import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx
from graph_utils import fetch_student_data, fetch_graph_data
import pandas as pd

st.set_page_config(layout="wide")

# ------------------ THEME ------------------
st.markdown("""
<style>
.stApp {
    background-color: #1C3D36;
    color: #E9F5F2;
}
.metric-box {
    background: #2C6155;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    font-weight: bold;
    color: #E9F5F2;
}
</style>
""", unsafe_allow_html=True)

st.title("📊 Interactive College Analytics Dashboard")

# ------------------ LOAD DATA ------------------
df = fetch_student_data()

# ------------------ FILTERS ------------------
st.sidebar.header("🔎 Filters")

department = st.sidebar.selectbox(
    "Select Department",
    ["All"] + list(df["department"].unique())
)

min_cgpa = st.sidebar.slider(
    "Minimum CGPA",
    0.0,
    10.0,
    0.0
)

filtered = df.copy()

if department != "All":
    filtered = filtered[filtered["department"] == department]

filtered = filtered[filtered["cgpa"] >= min_cgpa]

G = fetch_graph_data(department)

# ------------------ KPI SECTION ------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f"<div class='metric-box'>Total Students<br>{len(filtered)}</div>",
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"<div class='metric-box'>Departments<br>{filtered['department'].nunique()}</div>",
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"<div class='metric-box'>Avg CGPA<br>{round(filtered['cgpa'].mean(),2)}</div>",
        unsafe_allow_html=True
    )

st.markdown("---")

# ------------------ BAR CHART ------------------
st.markdown("## 📊 Students Per Department")

fig_bar = px.bar(
    filtered,
    x="department",
    color="department",
    color_discrete_sequence=["#4FB09B"]
)

fig_bar.update_layout(
    plot_bgcolor="#1C3D36",
    paper_bgcolor="#1C3D36",
    font=dict(color="white", size=14),
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=False),
    legend=dict(
        font=dict(color="white")
    )
)

st.plotly_chart(fig_bar, use_container_width=True)

# ------------------ PIE CHART ------------------
st.markdown("## 🥧 Top Teachers Distribution")

teacher_count = (
    filtered.groupby("teacher")
    .size()
    .reset_index(name="count")
    .sort_values("count", ascending=False)
)

top_teachers = teacher_count.head(8)

fig_pie = px.pie(
    top_teachers,
    names="teacher",
    values="count",
    color_discrete_sequence=px.colors.sequential.Teal
)

fig_pie.update_traces(textfont=dict(color="white"))

fig_pie.update_layout(
    plot_bgcolor="#1C3D36",
    paper_bgcolor="#1C3D36",
    font=dict(color="white", size=14),
    legend=dict(font=dict(color="white"))
)

st.plotly_chart(fig_pie, use_container_width=True)

# ------------------ LINE CHART ------------------
st.markdown("## 📈 Average Marks by Department")

line_df = (
    filtered.groupby("department")["marks"]
    .mean()
    .reset_index()
)

fig_line = px.line(
    line_df,
    x="department",
    y="marks",
    markers=True,
    color_discrete_sequence=["#6ABBAA"]
)

fig_line.update_layout(
    plot_bgcolor="#1C3D36",
    paper_bgcolor="#1C3D36",
    font=dict(color="#E9F5F2", size=14),
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=False)
)

st.plotly_chart(fig_line, use_container_width=True)

# ------------------ NETWORK GRAPH ------------------
st.markdown("## 🔗 Node Relationship View")

if len(G.nodes()) > 0:

    pos = nx.spring_layout(G, k=1.2, iterations=100)

    edge_x = []
    edge_y = []

    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=1, color='#6ABBAA'),
        hoverinfo='none',
        mode='lines'
    )

    node_x = []
    node_y = []
    node_color = []
    node_size = []
    text = []

    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        text.append(node)

        if node in filtered["department"].unique():
            node_color.append("#6ABBAA")
            node_size.append(25)
        elif node in filtered["teacher"].unique():
            node_color.append("#4FB09B")
            node_size.append(18)
        else:
            node_color.append("#A9D1C5")
            node_size.append(10)

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode='markers+text',
        text=text,
        textposition="top center",
        marker=dict(
            size=node_size,
            color=node_color,
            line_width=1
        )
    )

    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20, l=5, r=5, t=40),
            plot_bgcolor="#1C3D36",
            paper_bgcolor="#1C3D36",
            font=dict(color="#E9F5F2")
        )
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("No graph data available.")
