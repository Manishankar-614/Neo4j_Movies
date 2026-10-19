"""
NeoCinema GraphRAG - Next-Generation Movie Knowledge Graph Intelligence
An interactive, cinematic Streamlit application grounded on the official Neo4j Movies dataset.
"""

import streamlit as st
import pandas as pd
from typing import List, Dict, Any

from config import (
    DEFAULT_NEO4J_URI,
    DEFAULT_NEO4J_USERNAME,
    DEFAULT_NEO4J_PASSWORD,
    DEFAULT_NEO4J_DATABASE,
    GEMINI_API_KEY,
    APP_TITLE,
    APP_SUBTITLE
)
from graph_db import GraphManager, Neo4jDatabase
from rag_engine import GraphRAGEngine
from graph_visualizer import build_graph_html, parse_graph_elements
from movies_data import LOCAL_MOVIES_DATA

# Set Streamlit Page Config
st.set_page_config(
    page_title="NeoCinema | GraphRAG Intelligence",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-End Cyber-Cinema CSS Design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    h1, h2, h3, h4, .cinematic-title {
        font-family: 'Outfit', sans-serif;
        letter-spacing: -0.02em;
    }

    /* Ambient Background Glow */
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgba(30, 27, 75, 0.4) 0%, rgba(15, 23, 42, 1) 90%);
    }

    /* Hero Banner */
    .hero-container {
        padding: 1.8rem 2.2rem;
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.8) 100%);
        border-radius: 18px;
        border: 1px solid rgba(148, 163, 184, 0.12);
        box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(12px);
        margin-bottom: 1.8rem;
    }

    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: linear-gradient(90deg, rgba(99, 102, 241, 0.2) 0%, rgba(168, 85, 247, 0.2) 100%);
        border: 1px solid rgba(168, 85, 247, 0.4);
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        color: #c084fc;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.6rem;
    }

    .hero-heading {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #ffffff 0%, #cbd5e1 40%, #a855f7 80%, #38bdf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.15;
        margin: 0.2rem 0 0.5rem 0;
    }

    .hero-description {
        font-size: 1.05rem;
        color: #94a3b8;
        max-width: 850px;
        line-height: 1.5;
        margin: 0;
    }

    /* Metric Cards */
    .metric-card {
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid rgba(71, 85, 105, 0.3);
        border-radius: 14px;
        padding: 1.1rem 1.4rem;
        backdrop-filter: blur(10px);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: rgba(168, 85, 247, 0.5);
    }
    .metric-val {
        font-size: 2rem;
        font-weight: 800;
        font-family: 'Outfit', sans-serif;
        background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-lbl {
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #94a3b8;
        font-weight: 600;
    }

    /* Execution Trace Pill */
    .trace-container {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(51, 65, 85, 0.6);
        border-radius: 10px;
        padding: 8px 12px;
        margin-top: 10px;
        align-items: center;
        font-size: 0.82rem;
        color: #94a3b8;
    }
    .trace-tag {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.78rem;
    }
    .tag-purple { background: rgba(168, 85, 247, 0.15); color: #d8b4fe; border: 1px solid rgba(168, 85, 247, 0.3); }
    .tag-cyan { background: rgba(56, 189, 248, 0.15); color: #7dd3fc; border: 1px solid rgba(56, 189, 248, 0.3); }
    .tag-emerald { background: rgba(16, 185, 129, 0.15); color: #6ee7b7; border: 1px solid rgba(16, 185, 129, 0.3); }

    /* Custom Code Styling */
    code, pre {
        font-family: 'JetBrains Mono', monospace !important;
    }
</style>
""", unsafe_allow_html=True)


# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "👋 **Welcome to NeoCinema GraphRAG Intelligence!**\n\n"
                "I am your movie graph assistant powered by the official **Neo4j Movies Dataset** and **Google Gemini**.\n"
                "I translate your questions into **Cypher graph queries**, retrieve connected subgraphs, and synthesize comprehensive, factual answers.\n\n"
                "Try picking a query from the categories below or type your own question!"
            ),
            "cypher": None,
            "records": None,
            "trace": None
        }
    ]

# ------------------------------------------------------------------------------
# SIDEBAR CONTROLS
# ------------------------------------------------------------------------------
st.sidebar.markdown("## ⚙️ Control Deck")

# LLM Status Indicator (Loaded automatically from .env)
st.sidebar.markdown("### 🧠 AI Engine Status")
if GEMINI_API_KEY:
    st.sidebar.markdown("""
    <div style="background: rgba(16, 185, 129, 0.12); border: 1px solid rgba(16, 185, 129, 0.35); border-radius: 8px; padding: 10px; font-size: 0.85rem; color: #6ee7b7;">
        🟢 <b>Google Gemini AI Active</b><br/>
        Model: <code>gemini-3.8-flash</code><br/>
        <span style="font-size: 0.75rem; color: #a7f3d0;">Key securely loaded from <code>.env</code> file.</span>
    </div>
    """, unsafe_allow_html=True)
else:
    st.sidebar.markdown("""
    <div style="background: rgba(245, 158, 11, 0.12); border: 1px solid rgba(245, 158, 11, 0.35); border-radius: 8px; padding: 10px; font-size: 0.85rem; color: #fde68a;">
        ⚡ <b>Offline Smart Synthesizer Active</b><br/>
        <span style="font-size: 0.75rem; color: #fef3c7;">No GEMINI_API_KEY found in <code>.env</code>. Running locally with built-in heuristic engine.</span>
    </div>
    """, unsafe_allow_html=True)

st.sidebar.markdown("---")

# Database Mode Selection
st.sidebar.markdown("### 🔌 Graph Database")
db_mode = st.sidebar.radio(
    "Knowledge Source:",
    ["Built-in Movies Graph (Instant / In-Memory)", "Live Neo4j Instance (Local / Aura / Docker)"],
    index=0
)

use_live_neo4j = (db_mode == "Live Neo4j Instance (Local / Aura / Docker)")

if use_live_neo4j:
    neo4j_uri = st.sidebar.text_input("Bolt / Aura URI", value=DEFAULT_NEO4J_URI, help="e.g., bolt://localhost:7687 or neo4j+s://xxx.databases.neo4j.io")
    neo4j_user = st.sidebar.text_input("Username", value=DEFAULT_NEO4J_USERNAME)
    neo4j_pwd = st.sidebar.text_input("Password", value=DEFAULT_NEO4J_PASSWORD, type="password")
    neo4j_db = st.sidebar.text_input("Database Name", value=DEFAULT_NEO4J_DATABASE)

    col_btn1, col_btn2 = st.sidebar.columns(2)
    with col_btn1:
        if st.button("⚡ Test DB", use_container_width=True):
            test_db = Neo4jDatabase(neo4j_uri, neo4j_user, neo4j_pwd, neo4j_db)
            success, msg = test_db.test_connection()
            if success:
                st.sidebar.success(msg)
            else:
                st.sidebar.error(msg)
    with col_btn2:
        if st.button("🌱 Seed DB", use_container_width=True):
            with st.spinner("Seeding official Neo4j Movies dataset..."):
                seed_db = Neo4jDatabase(neo4j_uri, neo4j_user, neo4j_pwd, neo4j_db)
                ok, seed_msg = seed_db.seed_movies()
                if ok:
                    st.sidebar.success(seed_msg)
                else:
                    st.sidebar.error(seed_msg)
else:
    neo4j_uri = ""
    neo4j_user = ""
    neo4j_pwd = ""
    neo4j_db = ""
    st.sidebar.markdown("""
    <div style="background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.3); border-radius: 8px; padding: 10px; font-size: 0.85rem; color: #7dd3fc;">
        ⚡ <b>Built-in Graph Engine</b><br/>
        Preloaded with 22 movies, 92 actors/directors, and 150 relationships. Zero setup required!
    </div>
    """, unsafe_allow_html=True)

st.sidebar.markdown("---")

# Schema Inspector
with st.sidebar.expander("📖 Movies Schema Inspector"):
    st.markdown("""
    **Nodes:**
    - `(:Movie {title, released, tagline})`
    - `(:Person {name, born})`

    **Relationships:**
    - `(:Person)-[:ACTED_IN {roles}]->(:Movie)`
    - `(:Person)-[:DIRECTED]->(:Movie)`
    - `(:Person)-[:PRODUCED]->(:Movie)`
    - `(:Person)-[:WROTE]->(:Movie)`
    - `(:Person)-[:REVIEWED {rating, summary}]->(:Movie)`
    """)

# Initialize Graph Manager & RAG Engine
graph_mgr = GraphManager(
    use_live_neo4j=use_live_neo4j,
    uri=neo4j_uri,
    user=neo4j_user,
    password=neo4j_pwd,
    database=neo4j_db
)
rag_engine = GraphRAGEngine(graph_mgr)
stats = graph_mgr.get_stats()

# ------------------------------------------------------------------------------
# MAIN PAGE HERO HEADER
# ------------------------------------------------------------------------------
st.markdown(f"""
<div class="hero-container">
    <div class="hero-badge">⚡ GraphRAG Intelligence</div>
    <div class="hero-heading">{APP_TITLE}</div>
    <p class="hero-description">{APP_SUBTITLE}. Grounded on graph traversal, Text-to-Cypher translation, and interactive multi-hop knowledge retrieval.</p>
</div>
""", unsafe_allow_html=True)

# Metric Badges Row
col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
with col_stat1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-lbl">Total Movies</div>
        <div class="metric-val">{stats.get('movies', 0)}</div>
    </div>
    """, unsafe_allow_html=True)

with col_stat2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-lbl">Actors & Directors</div>
        <div class="metric-val">{stats.get('people', 0)}</div>
    </div>
    """, unsafe_allow_html=True)

with col_stat3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-lbl">Graph Relationships</div>
        <div class="metric-val">{stats.get('relationships', 0)}</div>
    </div>
    """, unsafe_allow_html=True)

with col_stat4:
    engine_label = "Neo4j Live" if use_live_neo4j else "Built-in Graph"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-lbl">Graph Knowledge Mode</div>
        <div class="metric-val" style="font-size: 1.4rem; padding-top: 0.3rem;">{engine_label}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br/>", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# NAVIGATION TABS (Removed Free API Guide as requested)
# ------------------------------------------------------------------------------
tab_chat, tab_explorer, tab_cypher = st.tabs([
    "💬 NeoCinema Chat",
    "🕸️ Interactive Graph Explorer",
    "💻 Cypher Playground"
])

# ------------------------------------------------------------------------------
# TAB 1: NEOCINEMA CHAT
# ------------------------------------------------------------------------------
with tab_chat:
    st.markdown("#### 💡 Categorized Query Inspiration:")
    
    # Category Pills
    cat_tab1, cat_tab2, cat_tab3, cat_tab4 = st.tabs([
        "🎬 Movie Spotlights",
        "🎭 Filmography & Roles",
        "🎥 Directors & Crew",
        "🤝 Co-Star Chemistry"
    ])
    
    selected_prompt = None

    with cat_tab1:
        p_col1, p_col2 = st.columns(2)
        with p_col1:
            if st.button("🕶️ Tell me about The Matrix", use_container_width=True):
                selected_prompt = "Tell me about The Matrix"
        with p_col2:
            if st.button("🚀 What is Apollo 13 about and who directed it?", use_container_width=True):
                selected_prompt = "What is Apollo 13 about and who directed it?"

    with cat_tab2:
        p_col1, p_col2 = st.columns(2)
        with p_col1:
            if st.button("🎭 What movies did Keanu Reeves act in and what roles did he play?", use_container_width=True):
                selected_prompt = "What movies did Keanu Reeves act in and what roles did he play?"
        with p_col2:
            if st.button("✈️ Which movies star Tom Cruise?", use_container_width=True):
                selected_prompt = "Which movies star Tom Cruise?"

    with cat_tab3:
        p_col1, p_col2 = st.columns(2)
        with p_col1:
            if st.button("🎬 Who directed The Matrix and what other movies did they direct?", use_container_width=True):
                selected_prompt = "Who directed The Matrix and what other movies did they direct?"
        with p_col2:
            if st.button("🤠 Find movies directed by Clint Eastwood", use_container_width=True):
                selected_prompt = "Find movies directed by Clint Eastwood"

    with cat_tab4:
        p_col1, p_col2 = st.columns(2)
        with p_col1:
            if st.button("💌 Which movies do Tom Hanks and Meg Ryan star together in?", use_container_width=True):
                selected_prompt = "Which movies do Tom Hanks and Meg Ryan star together in?"
        with p_col2:
            if st.button("⭐ What movies have reviews and ratings in the knowledge graph?", use_container_width=True):
                selected_prompt = "What movies have reviews and ratings in the knowledge graph?"

    st.markdown("---")

    # Display Chat History
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

            # Render Execution Trace Pill if present
            if msg.get("trace"):
                tr = msg["trace"]
                st.markdown(f"""
                <div class="trace-container">
                    <span class="trace-tag tag-purple">🧠 {tr.get('synth_model', 'LLM')}</span>
                    <span class="trace-tag tag-cyan">⚡ Cypher: {tr.get('cypher_model', 'Generated')}</span>
                    <span class="trace-tag tag-emerald">⏱️ {tr.get('latency_ms', 0)}ms</span>
                    <span>Retrieved <b>{tr.get('records_count', 0)}</b> graph records</span>
                </div>
                """, unsafe_allow_html=True)

            # Display Cypher Query & Graph Details Accordion
            if msg.get("cypher"):
                with st.expander("🔍 Generated Cypher Query & Raw Graph Records", expanded=False):
                    st.code(msg["cypher"], language="cypher")
                    if msg.get("records"):
                        st.dataframe(pd.DataFrame(msg["records"]), use_container_width=True)

            # Display Force-Directed Visualizer
            if msg.get("records"):
                graph_elements = parse_graph_elements(msg["records"])
                if graph_elements["nodes"]:
                    with st.expander("🕸️ Interactive Force-Directed Subgraph", expanded=True):
                        graph_html = build_graph_html(graph_elements["nodes"], graph_elements["edges"], height=380)
                        st.components.v1.html(graph_html, height=400)

    # Function to execute query
    def execute_rag(prompt_text: str):
        st.session_state.messages.append({"role": "user", "content": prompt_text})
        with st.chat_message("user"):
            st.markdown(prompt_text)

        with st.chat_message("assistant"):
            with st.spinner("Analyzing question, generating Cypher, and traversing Neo4j knowledge..."):
                result = rag_engine.process_query(
                    user_query=prompt_text,
                    api_key=GEMINI_API_KEY
                )

            st.markdown(result["answer"])

            # Render Execution Trace
            tr = result.get("trace", {})
            st.markdown(f"""
            <div class="trace-container">
                <span class="trace-tag tag-purple">🧠 {tr.get('synth_model', 'LLM')}</span>
                <span class="trace-tag tag-cyan">⚡ Cypher: {tr.get('cypher_model', 'Generated')}</span>
                <span class="trace-tag tag-emerald">⏱️ {tr.get('latency_ms', 0)}ms</span>
                <span>Retrieved <b>{tr.get('records_count', 0)}</b> graph records</span>
            </div>
            """, unsafe_allow_html=True)

            with st.expander("🔍 Generated Cypher Query & Raw Graph Records", expanded=False):
                st.code(result["cypher"], language="cypher")
                if result.get("error"):
                    st.error(result["error"])
                if result.get("records"):
                    st.dataframe(pd.DataFrame(result["records"]), use_container_width=True)

            if result.get("records"):
                graph_elements = parse_graph_elements(result["records"])
                if graph_elements["nodes"]:
                    with st.expander("🕸️ Interactive Force-Directed Subgraph", expanded=True):
                        graph_html = build_graph_html(graph_elements["nodes"], graph_elements["edges"], height=380)
                        st.components.v1.html(graph_html, height=400)

        # Save to session history
        st.session_state.messages.append({
            "role": "assistant",
            "content": result["answer"],
            "cypher": result["cypher"],
            "records": result["records"],
            "trace": result.get("trace")
        })

    # Trigger from quick prompt
    if selected_prompt:
        execute_rag(selected_prompt)

    # Chat Input Box
    user_query = st.chat_input("Ask about movies, directors, co-actors, release years, or taglines...")
    if user_query:
        execute_rag(user_query)

    col_c1, col_c2 = st.columns([8, 2])
    with col_c2:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

# ------------------------------------------------------------------------------
# TAB 2: INTERACTIVE GRAPH EXPLORER
# ------------------------------------------------------------------------------
with tab_explorer:
    st.markdown("### 🕸️ Complete Movies Knowledge Graph Explorer")
    st.markdown("Explore the complete graph network. Drag nodes, zoom in/out, and hover over entities to inspect their connections and properties.")

    filter_col1, filter_col2 = st.columns([3, 1])
    with filter_col1:
        search_filter = st.text_input("Filter Graph by Entity (e.g. 'Matrix', 'Keanu', 'Hanks', 'Apollo')", value="")
    with filter_col2:
        max_nodes = st.slider("Node Limit", min_value=10, max_value=80, value=40)

    all_movies = LOCAL_MOVIES_DATA["movies"]
    all_people = LOCAL_MOVIES_DATA["people"]
    all_rels = LOCAL_MOVIES_DATA["relationships"]

    if search_filter:
        flt = search_filter.lower()
        active_rels = [
            r for r in all_rels
            if flt in r["from"].lower() or flt in r["to"].lower()
        ]
        if not active_rels:
            st.warning(f"No connections found matching '{search_filter}'. Showing default network.")
            active_rels = all_rels[:max_nodes]
    else:
        active_rels = all_rels[:max_nodes]

    records_for_vis = [
        {"source": r["from"], "target": r["to"], "type": r["type"], "details": r.get("props", {})}
        for r in active_rels
    ]
    full_graph_elements = parse_graph_elements(records_for_vis)
    full_html = build_graph_html(full_graph_elements["nodes"], full_graph_elements["edges"], height=550)
    st.components.v1.html(full_html, height=580)

# ------------------------------------------------------------------------------
# TAB 3: CYPHER PLAYGROUND
# ------------------------------------------------------------------------------
with tab_cypher:
    st.markdown("### 💻 Cypher Query Studio")
    st.markdown("Test raw Cypher queries directly against the active graph database or in-memory engine.")

    snippet_choice = st.selectbox(
        "Load Pre-built Cypher Template:",
        [
            "Select a template...",
            "1. Co-actors: Keanu Reeves and Carrie-Anne Moss",
            "2. Directorial Collaborations of Tom Hanks",
            "3. Top Rated Movie Reviews",
            "4. Actors who also Directed Movies",
            "5. Movies Released in the 1990s"
        ]
    )

    default_code = "MATCH (p:Person)-[r:ACTED_IN]->(m:Movie)\nRETURN p.name AS actor, m.title AS movie, r.roles AS roles\nLIMIT 15"
    if snippet_choice == "1. Co-actors: Keanu Reeves and Carrie-Anne Moss":
        default_code = "MATCH (p1:Person)-[:ACTED_IN]->(m:Movie)<-[:ACTED_IN]-(p2:Person)\nWHERE p1.name = 'Keanu Reeves' AND p2.name = 'Carrie-Anne Moss'\nRETURN p1.name AS actor1, p2.name AS actor2, m.title AS movie, m.released AS released"
    elif snippet_choice == "2. Directorial Collaborations of Tom Hanks":
        default_code = "MATCH (p:Person)-[:DIRECTED]->(m:Movie)<-[:ACTED_IN]-(a:Person)\nWHERE a.name = 'Tom Hanks'\nRETURN p.name AS director, m.title AS movie, m.released AS released"
    elif snippet_choice == "3. Top Rated Movie Reviews":
        default_code = "MATCH (p:Person)-[r:REVIEWED]->(m:Movie)\nRETURN p.name AS reviewer, m.title AS movie, r.rating AS rating, r.summary AS summary\nORDER BY r.rating DESC"
    elif snippet_choice == "4. Actors who also Directed Movies":
        default_code = "MATCH (p:Person)-[:ACTED_IN]->(m1:Movie)\nMATCH (p)-[:DIRECTED]->(m2:Movie)\nRETURN DISTINCT p.name AS actor_director, m1.title AS acted_movie, m2.title AS directed_movie"
    elif snippet_choice == "5. Movies Released in the 1990s":
        default_code = "MATCH (m:Movie)\nWHERE m.released >= 1990 AND m.released < 2000\nRETURN m.title AS movie, m.released AS released, m.tagline AS tagline\nORDER BY m.released DESC"

    user_cypher = st.text_area("Cypher Query", value=default_code, height=130)

    if st.button("🚀 Execute Cypher Query", use_container_width=True):
        records, err = graph_mgr.run_query(user_cypher)
        if err:
            st.error(err)
        elif not records:
            st.warning("Query executed successfully, but returned 0 records.")
        else:
            st.success(f"Returned {len(records)} record(s)!")
            c_res1, c_res2 = st.columns([1, 1])
            with c_res1:
                st.markdown("##### 📋 Result Table")
                st.dataframe(pd.DataFrame(records), use_container_width=True)
            with c_res2:
                st.markdown("##### 🕸️ Result Subgraph")
                elem = parse_graph_elements(records)
                if elem["nodes"]:
                    html_code = build_graph_html(elem["nodes"], elem["edges"], height=320)
                    st.components.v1.html(html_code, height=340)
