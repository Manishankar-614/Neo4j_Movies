"""
Generates the official PDF report matching the uploaded evaluation format with embedded screenshots.
Student: Manishankar (1GA23AI025)
Subject: Advance NLP (AML23702) - Lab Exercise 3
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def create_pdf(filename="Lab_Exercise_3_Report.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=45,
        leftMargin=45,
        topMargin=45,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()

    header_style = ParagraphStyle(
        'HeaderStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        textColor=colors.HexColor('#444444'),
        spaceAfter=12
    )

    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=17,
        alignment=1,
        spaceAfter=5
    )

    subtitle_style = ParagraphStyle(
        'SubtitleStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=12,
        alignment=1,
        textColor=colors.HexColor('#222222'),
        spaceAfter=12
    )

    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=13.5,
        textColor=colors.HexColor('#000000'),
        spaceBefore=8,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#111111'),
        spaceAfter=5
    )

    bullet_style = ParagraphStyle(
        'BulletStyle',
        parent=body_style,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=3
    )

    caption_style = ParagraphStyle(
        'CaptionStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor('#333333'),
        spaceBefore=4,
        spaceAfter=10
    )

    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=9.5
    )

    table_header = ParagraphStyle(
        'TableHeader',
        parent=table_cell,
        fontName='Helvetica-Bold',
        textColor=colors.HexColor('#000000')
    )

    story = []

    def add_page_header():
        header_table = Table(
            [[
                Paragraph("Department of AIML", ParagraphStyle('L', parent=header_style, alignment=0)),
                Paragraph("Advance NLP (AML23702)", ParagraphStyle('R', parent=header_style, alignment=2))
            ]],
            colWidths=[260, 260]
        )
        header_table.setStyle(TableStyle([
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor('#888888'))
        ]))
        story.append(header_table)
        story.append(Spacer(1, 8))

    # --- PAGE 1 ---
    add_page_header()
    story.append(Paragraph("LAB EXERCISE: 3", ParagraphStyle('LabEx', fontName='Helvetica-Bold', fontSize=11, alignment=1, spaceAfter=3)))
    story.append(Paragraph("Graph Retrieval-Augmented Generation (RAG) — Natural-Language<br/>Question Answering over the Neo4j Movies Knowledge Graph", title_style))
    story.append(Paragraph("A modular Streamlit web application that links each question to movies and people in the Neo4j Movies graph, retrieves the relevant subgraph with parameterised Cypher queries, and grounds an LLM-generated answer in the retrieved facts.", subtitle_style))

    story.append(Paragraph("Aim / Objective", section_heading))
    story.append(Paragraph(
        "This project implements a complete Retrieval-Augmented Generation (RAG) system that uses the Neo4j Movies dataset as its knowledge source. Instead of letting a large language model (LLM) answer movie questions from its own parametric memory — where it can silently hallucinate cast lists, directors or release years — the system first retrieves the relevant facts from a graph database and then asks the LLM to answer only from those facts.",
        body_style
    ))
    story.append(Paragraph(
        "The pipeline is organised as reusable modules: a graph store (graph_db.py) that executes Cypher against Neo4j, a GraphRetriever that turns a free-text question into linked entities, intents and a ranked list of graph facts, and a generator (rag_engine.py) that builds a grounded prompt and calls Google Gemini (gemini-3.8-flash) via google.genai. The Streamlit front end (app.py) shows the answer next to the evidence it was built from: the retrieved facts, the drawn subgraph, the execution trace metrics, the exact prompt sent to the LLM, and the Cypher that was executed.",
        body_style
    ))
    story.append(Paragraph(
        "The system was evaluated on a hand-written set of 30 questions covering eleven answerable question types, three deliberately hard types and one out-of-graph question, so that both its strengths and its edge cases are reported.",
        body_style
    ))

    story.append(Paragraph("Expected Outcomes Addressed", section_heading))
    story.append(Paragraph("• <b>1. Use a graph database as the knowledge source.</b> The official Neo4j Movies script (movies.cypher) is loaded into Neo4j, giving 171 nodes and 253 relationships. All retrieval goes through named, parameterised Cypher templates — user text is never concatenated into a query.", bullet_style))
    story.append(Paragraph("• <b>2. Retrieve relevant movie information for a user query.</b> Movie titles and person names are linked to graph nodes (exact phrase, unique surname, or fuzzy match); keyword rules detect which relationship types are being asked about and any release-year constraint; the 1-hop neighbourhood of every linked node (plus a shared-movie path for two people) is fetched and ranked.", bullet_style))
    story.append(Paragraph("• <b>3. Build a grounded context for the LLM.</b> Retrieved facts are serialised as numbered (subject) -[RELATION]-> (object) [detail] triples and placed under a system prompt that forbids outside knowledge and prescribes a fixed refusal sentence when the answer is missing.", bullet_style))
    story.append(Paragraph("• <b>4. Generate natural-language answers with an LLM.</b> LLMGenerator posts the prompt to Google Gemini (gemini-3.8-flash) at low temperature. If offline, a deterministic template generator verbalises the same facts so the app always answers.", bullet_style))
    story.append(Paragraph("• <b>5. Present and evaluate the system.</b> A Streamlit UI exposes the answer with its evidence, and evaluation test suites score entity linking, context recall and answer accuracy across test questions.", bullet_style))

    story.append(PageBreak())

    # --- PAGE 2 ---
    add_page_header()
    story.append(Paragraph("Tools & Technologies Used", section_heading))
    tools_data = [
        [Paragraph("Category", table_header), Paragraph("Tool / Library", table_header), Paragraph("Purpose in this pipeline", table_header)],
        [Paragraph("Language / runtime", table_cell), Paragraph("Python 3", table_cell), Paragraph("Core implementation language for the whole system.", table_cell)],
        [Paragraph("Knowledge source", table_cell), Paragraph("Neo4j 5 (graph DB) + Movies dataset", table_cell), Paragraph("Stores Movie and Person nodes and their ACTED_IN / DIRECTED / WROTE / PRODUCED / REVIEWED / FOLLOWS relationships.", table_cell)],
        [Paragraph("Graph access", table_cell), Paragraph("neo4j Python driver, Cypher", table_cell), Paragraph("Parameterised Cypher templates for movie profiles, person profiles, shared-movie paths and year ranges.", table_cell)],
        [Paragraph("Entity linking", table_cell), Paragraph("Regex & RapidFuzz", table_cell), Paragraph("Fuzzy string matching of misspelt titles and names (ratio ≥ 88).", table_cell)],
        [Paragraph("Fallback retrieval", table_cell), Paragraph("Hybrid Entity Search", table_cell), Paragraph("Neighbourhood subgraph traversal when no exact entity is linked.", table_cell)],
        [Paragraph("Generation", table_cell), Paragraph("Google Gemini (gemini-3.8-flash) via google.genai", table_cell), Paragraph("Writes the final answer from the grounded prompt at low temperature.", table_cell)],
        [Paragraph("Web framework", table_cell), Paragraph("Streamlit", table_cell), Paragraph("Sidebar configuration, question input, answer card, tabs, CSV download.", table_cell)],
        [Paragraph("Graphs", table_cell), Paragraph("Vis.js Force Network", table_cell), Paragraph("Draws the retrieved subgraph as an interactive node–edge chart.", table_cell)],
        [Paragraph("Tabular data", table_cell), Paragraph("pandas", table_cell), Paragraph("Facts table, CSV export and evaluation results.", table_cell)],
    ]
    t1 = Table(tools_data, colWidths=[100, 150, 270])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e8eef8')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#bbbbbb')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t1)
    story.append(Spacer(1, 8))

    story.append(Paragraph("Dataset / Corpus Description", section_heading))
    story.append(Paragraph(
        "The knowledge source is the Neo4j Movies example graph — the dataset Neo4j ships for its :play movies tutorial and publishes as movies.cypher. It is a small, curated property graph rather than a text corpus, which makes it well suited to RAG: every fact is explicit, typed and individually retrievable.",
        body_style
    ))

    dataset_data = [
        [Paragraph("Element", table_header), Paragraph("Count", table_header), Paragraph("Properties / notes", table_header)],
        [Paragraph("Movie nodes", table_cell), Paragraph("38", table_cell), Paragraph("title, released (1975–2012), tagline", table_cell)],
        [Paragraph("Person nodes", table_cell), Paragraph("133", table_cell), Paragraph("name, born", table_cell)],
        [Paragraph("ACTED_IN", table_cell), Paragraph("172", table_cell), Paragraph("roles (list of character names)", table_cell)],
        [Paragraph("DIRECTED", table_cell), Paragraph("44", table_cell), Paragraph("—", table_cell)],
        [Paragraph("PRODUCED", table_cell), Paragraph("15", table_cell), Paragraph("—", table_cell)],
        [Paragraph("WROTE", table_cell), Paragraph("10", table_cell), Paragraph("—", table_cell)],
        [Paragraph("REVIEWED", table_cell), Paragraph("9", table_cell), Paragraph("summary, rating (0–100)", table_cell)],
        [Paragraph("FOLLOWS", table_cell), Paragraph("3", table_cell), Paragraph("Person → Person", table_cell)],
        [Paragraph("<b>Total</b>", table_header), Paragraph("<b>171 nodes / 253 rels</b>", table_header), Paragraph("<b>Verified after loading.</b>", table_header)],
    ]
    t2 = Table(dataset_data, colWidths=[100, 130, 290])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e8eef8')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#bbbbbb')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t2)

    story.append(PageBreak())

    # --- PAGE 3 ---
    add_page_header()
    story.append(Paragraph("System Architecture / Pipeline Design", section_heading))
    pipe_data = [
        [Paragraph("Stage", table_header), Paragraph("What happens", table_header)],
        [Paragraph("1. Input", table_cell), Paragraph("User enters query; sidebar selects graph back end and displays active Gemini 3.8 Flash AI status.", table_cell)],
        [Paragraph("2. Entity linking", table_cell), Paragraph("Matches graph's titles and names against normalized question, longest first (e.g. 'The Matrix Reloaded' before 'The Matrix').", table_cell)],
        [Paragraph("3. Intent & constraints", table_cell), Paragraph("Maps keywords to relationship types (directed → DIRECTED, roles → ACTED_IN) and parses year bounds.", table_cell)],
        [Paragraph("4. Graph retrieval", table_cell), Paragraph("For each linked movie, movie_profile; for each person, person_profile; for two people, shared_movies path.", table_cell)],
        [Paragraph("5. Fallback retrieval", table_cell), Paragraph("If nothing was linked, hybrid subgraph traversal returns the closest connected entities.", table_cell)],
        [Paragraph("6. Ranking & context", table_cell), Paragraph("Facts are scored, de-duplicated and cut to top triples.", table_cell)],
        [Paragraph("7. Prompt & generation", table_cell), Paragraph("build_prompt() adds system rules; Google Gemini (gemini-3.8-flash) answers strictly from context.", table_cell)],
        [Paragraph("8. Streamlit UI", table_cell), Paragraph("Answer card, execution metrics, interactive force-directed subgraph, and Cypher details.", table_cell)],
    ]
    t3 = Table(pipe_data, colWidths=[120, 400])
    t3.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e8eef8')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#bbbbbb')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t3)
    story.append(Spacer(1, 8))

    story.append(Paragraph("Backend Implementation", section_heading))
    story.append(Paragraph("<b>6.1 Approach / Algorithm</b>", ParagraphStyle('SubSub', parent=body_style, fontName='Helvetica-Bold')))
    story.append(Paragraph(
        "Retrieval is graph-native and entity-first. Because every answer in the Movies graph hangs off a named movie or person, the retriever's first job is to find those names in the question; the graph then supplies a precise, complete neighbourhood for each one in a single Cypher round-trip. This avoids chunking fragmentation on structured data, because the unit of retrieval is the node's whole 1-hop subgraph.",
        body_style
    ))
    story.append(Paragraph(
        "Generation is constrained, not creative: the system prompt restricts the model to the numbered facts, asks for concise factual sentences with release years, and fixes the refusal sentence. Temperature 0 keeps answers repeatable. Every component is configurable from environment variables (NEO4J_URI, GEMINI_API_KEY).",
        body_style
    ))

    story.append(PageBreak())

    # --- PAGE 4: FRONTEND SCREENSHOTS (FIGURE 7.3.1 & 7.3.2) ---
    add_page_header()
    story.append(Paragraph("Frontend / UI Implementation & Screenshots", section_heading))
    story.append(Paragraph("<b>7.1 Capabilities & Architecture</b>", ParagraphStyle('SubSub2', parent=body_style, fontName='Helvetica-Bold')))
    story.append(Paragraph(
        "The web interface is built with Streamlit and styled with a Cyber-Cinema aesthetic. It includes dynamic status badges, categorized query inspiration buttons, expandable Cypher inspections, and an embedded Vis.js force-directed graph canvas.",
        body_style
    ))
    story.append(Spacer(1, 4))

    img1_path = "c:/ANLP/Project3/screenshots/fig_7_3_1_input_screen.png"
    if os.path.exists(img1_path):
        story.append(Image(img1_path, width=500, height=195))
        story.append(Paragraph("<b>Figure 7.3.1.</b> The application's input screen: hero banner, metric cards, sidebar showing active Google Gemini 3.8 Flash connection loaded from .env, and categorized query inspiration tabs.", caption_style))

    img2_path = "c:/ANLP/Project3/screenshots/fig_7_3_2_answer_result.png"
    if os.path.exists(img2_path):
        story.append(Image(img2_path, width=500, height=195))
        story.append(Paragraph("<b>Figure 7.3.2.</b> Result for “Tell me about The Matrix”: conversational answer synthesized by Gemini 3.8 Flash, live execution trace tag (latency, model, records), release year, tagline, directors, and cast list.", caption_style))

    story.append(PageBreak())

    # --- PAGE 5: SCREENSHOTS CONTINUED (FIGURE 7.3.3 & 7.3.4) ---
    add_page_header()
    story.append(Paragraph("Frontend Screenshots (Continued)", section_heading))

    img3_path = "c:/ANLP/Project3/screenshots/fig_7_3_3_cypher_records.png"
    if os.path.exists(img3_path):
        story.append(Image(img3_path, width=500, height=195))
        story.append(Paragraph("<b>Figure 7.3.3.</b> Generated Cypher query inspection and raw knowledge graph records table: shows the exact Cypher query executed against the graph and the tabular records returned.", caption_style))

    img4_path = "c:/ANLP/Project3/screenshots/fig_7_3_4_subgraph_visualizer.png"
    if os.path.exists(img4_path):
        story.append(Image(img4_path, width=500, height=195))
        story.append(Paragraph("<b>Figure 7.3.4.</b> Interactive Force-Directed Subgraph: embedded Vis.js network rendering the retrieved movie node (Coral) connected to its actors (Blue) and directors with directional relationship edges.", caption_style))

    story.append(PageBreak())

    # --- PAGE 6: SAMPLE INPUT & OUTPUT ---
    add_page_header()
    story.append(Paragraph("Sample Input & Output", section_heading))
    sample_data = [
        [Paragraph("Input (question)", table_header), Paragraph("Pipeline stage", table_header), Paragraph("Output produced", table_header)],
        [
            Paragraph("“Tell me about The Matrix”", table_cell),
            Paragraph("Movie Spotlight & Cast Retrieval", table_cell),
            Paragraph("<b>The Matrix</b> (1999), Tagline: <i>“Welcome to the Real World”</i>. Directed by Lana Wachowski and Lilly Wachowski. Cast includes Keanu Reeves (as Neo), Carrie-Anne Moss (as Trinity), Laurence Fishburne (as Morpheus), Hugo Weaving (as Agent Smith).", table_cell)
        ],
        [
            Paragraph("“Who played Neo in The Matrix?”", table_cell),
            Paragraph("Linking → retrieval → generation", table_cell),
            Paragraph("Linked movie: The Matrix; intent ROLE; 5 facts. Answer: “In The Matrix (1999), the cast includes Keanu Reeves (as Neo).”", table_cell)
        ],
        [
            Paragraph("“When was Keanu Reeves born?”", table_cell),
            Paragraph("Fuzzy entity linking", table_cell),
            Paragraph("RapidFuzz links “keanu reeves” to Keanu Reeves; the BORN fact gives “Keanu Reeves was born in 1964.”", table_cell)
        ],
        [
            Paragraph("“Which movies did Tom Hanks act in after 2000?”", table_cell),
            Paragraph("Year-constrained retrieval", table_cell),
            Paragraph("“after 2000” → range 2001+; person_profile is filtered to 4 films. Answer: “Tom Hanks acted in The Polar Express (2004), The Da Vinci Code (2006), Charlie Wilson's War (2007) and Cloud Atlas (2012).”", table_cell)
        ],
        [
            Paragraph("“What rating did Jessica Thompson give Unforgiven?”", table_cell),
            Paragraph("Edge-property retrieval", table_cell),
            Paragraph("The REVIEWED edge's rating and summary are returned: “Unforgiven (1992) was reviewed by Jessica Thompson (rating 85: 'Dark, but compelling').”", table_cell)
        ],
        [
            Paragraph("“Who directed Titanic?”", table_cell),
            Paragraph("Out-of-graph refusal", table_cell),
            Paragraph("Nothing linked in movie graph, so context is empty and fixed refusal is returned: “I searched the Neo4j Movies Knowledge Graph, but could not find matching records.”", table_cell)
        ],
    ]
    t4 = Table(sample_data, colWidths=[120, 110, 290])
    t4.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e8eef8')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#bbbbbb')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t4)
    story.append(Spacer(1, 10))

    story.append(Paragraph("Results & Quantitative Evaluation", section_heading))
    results_conf = [
        [Paragraph("Setting", table_header), Paragraph("Value", table_header)],
        [Paragraph("Graph back end", table_cell), Paragraph("Neo4j AuraDB Cloud / Built-in High-Fidelity Movies Graph (171 nodes, 253 rels)", table_cell)],
        [Paragraph("Generator", table_cell), Paragraph("Google Gemini (gemini-3.8-flash) via google.genai / Semantic Synthesizer", table_cell)],
        [Paragraph("Context size / threshold", table_cell), Paragraph("max_facts = 25, Temperature = 0.0 - 0.2", table_cell)],
    ]
    t5 = Table(results_conf, colWidths=[160, 360])
    t5.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e8eef8')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#bbbbbb')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t5)
    story.append(Spacer(1, 6))

    agg_data = [
        [Paragraph("Metric", table_header), Paragraph("Value", table_header), Paragraph("Definition", table_header)],
        [Paragraph("Entity-linking accuracy", table_cell), Paragraph("100% (30/30)", table_cell), Paragraph("Linked movies + people exactly equal expected set.", table_cell)],
        [Paragraph("Context recall", table_cell), Paragraph("90% (27/30)", table_cell), Paragraph("Every gold answer string appears in retrieved context.", table_cell)],
        [Paragraph("Answer accuracy", table_cell), Paragraph("90% (27/30)", table_cell), Paragraph("Every gold string appears in final answer (or refusal).", table_cell)],
        [Paragraph("Mean facts per context", table_cell), Paragraph("8.6 (range 0–23)", table_cell), Paragraph("Triples sent to the generator.", table_cell)],
        [Paragraph("Retrieval latency", table_cell), Paragraph("1.33 ms mean", table_cell), Paragraph("Linking + retrieval + ranking on graph.", table_cell)],
    ]
    t6 = Table(agg_data, colWidths=[130, 90, 300])
    t6.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e8eef8')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#bbbbbb')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t6)

    story.append(PageBreak())

    # --- PAGE 7: CONCLUSION & EVALUATION SHEET ---
    add_page_header()
    story.append(Paragraph("Conclusion", section_heading))
    story.append(Paragraph(
        "The project delivers a working Graph RAG system over the Neo4j Movies dataset: questions are linked to graph entities, the relevant subgraph is retrieved with parameterised Cypher, and an LLM is asked to answer strictly from the retrieved, numbered facts, with every step visible in the Streamlit interface. On a 30-question test set, entity linking was correct for every question, context recall and answer accuracy were both 90%, and all entity-centred question types — including typos, surname-only names, year filters and two-person questions — were answered correctly, while an out-of-graph question was correctly refused.",
        body_style
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("Project Repository (GitHub Link)", section_heading))
    repo_data = [
        [Paragraph("Field", table_header), Paragraph("Value", table_header)],
        [Paragraph("GitHub Repository URL", table_cell), Paragraph("https://github.com/Manishankar-614/Neo4j_Movies.git", table_cell)],
        [Paragraph("Repository Visibility", table_cell), Paragraph("Public", table_cell)],
        [Paragraph("Branch / Commit Used for Submission", table_cell), Paragraph("main", table_cell)],
    ]
    t7 = Table(repo_data, colWidths=[180, 340])
    t7.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e8eef8')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#bbbbbb')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t7)
    story.append(Spacer(1, 10))

    story.append(Paragraph("ADVANCE NLP (AML23702) — Lab Exercise Evaluation Sheet", title_style))
    story.append(Spacer(1, 6))

    eval_meta = [
        [Paragraph("Field", table_header), Paragraph("Value", table_header)],
        [Paragraph("Student Name", table_cell), Paragraph("<b>Manishankar</b>", table_cell)],
        [Paragraph("USN", table_cell), Paragraph("<b>1GA23AI025</b>", table_cell)],
        [Paragraph("Lab Exercise No.", table_cell), Paragraph("3", table_cell)],
        [Paragraph("Experiment Title", table_cell), Paragraph("Graph Retrieval-Augmented Generation (RAG) — Natural-Language Question Answering over the Neo4j Movies Knowledge Graph", table_cell)],
    ]
    t8 = Table(eval_meta, colWidths=[150, 370])
    t8.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e8eef8')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#bbbbbb')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
    ]))
    story.append(t8)
    story.append(Spacer(1, 8))

    story.append(Paragraph("Marks Awarded", section_heading))
    marks_data = [
        [Paragraph("Sl. No.", table_header), Paragraph("Evaluation Criteria", table_header), Paragraph("Max Marks", table_header), Paragraph("Marks Obtained", table_header)],
        [Paragraph("1", table_cell), Paragraph("Problem Understanding & Scope", table_cell), Paragraph("5", table_cell), Paragraph("", table_cell)],
        [Paragraph("2", table_cell), Paragraph("Pipeline Design & Methodology", table_cell), Paragraph("10", table_cell), Paragraph("", table_cell)],
        [Paragraph("3", table_cell), Paragraph("Implementation Correctness", table_cell), Paragraph("10", table_cell), Paragraph("", table_cell)],
        [Paragraph("4", table_cell), Paragraph("Use of NLP Tools / Models", table_cell), Paragraph("5", table_cell), Paragraph("", table_cell)],
        [Paragraph("5", table_cell), Paragraph("Output Quality / Task Performance", table_cell), Paragraph("10", table_cell), Paragraph("", table_cell)],
        [Paragraph("6", table_cell), Paragraph("Analysis & Interpretation", table_cell), Paragraph("5", table_cell), Paragraph("", table_cell)],
        [Paragraph("7", table_cell), Paragraph("Documentation & Deliverables", table_cell), Paragraph("2.5", table_cell), Paragraph("", table_cell)],
        [Paragraph("8", table_cell), Paragraph("Presentation & Reproducibility", table_cell), Paragraph("2.5", table_cell), Paragraph("", table_cell)],
        [Paragraph("<b>Total</b>", table_header), Paragraph("<b>Total Marks</b>", table_header), Paragraph("<b>50</b>", table_header), Paragraph("", table_cell)],
    ]
    t9 = Table(marks_data, colWidths=[45, 275, 95, 105])
    t9.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e8eef8')),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#f0f4f8')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#bbbbbb')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (0,0), (0,-1), 'CENTER'),
        ('ALIGN', (2,0), (2,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t9)
    story.append(Spacer(1, 12))

    story.append(Paragraph("Overall Comments", section_heading))
    comments_box = Table([["\n\n"]], colWidths=[520])
    comments_box.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#888888')),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#fafafa'))
    ]))
    story.append(comments_box)
    story.append(Spacer(1, 16))

    sig_table = Table([
        [
            Paragraph("Date of Submission: ______________", ParagraphStyle('DS', parent=body_style)),
            Paragraph("Signature of Faculty: ______________", ParagraphStyle('SF', parent=body_style, alignment=2))
        ]
    ], colWidths=[260, 260])
    sig_table.setStyle(TableStyle([
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(sig_table)

    doc.build(story)
    print(f"Report with screenshots generated successfully: {filename}")

if __name__ == "__main__":
    create_pdf()
