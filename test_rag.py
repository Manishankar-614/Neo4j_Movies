"""
Test script to validate the Neo4j Movies GraphRAG system end-to-end.
"""

from config import GEMINI_API_KEY
from graph_db import GraphManager
from rag_engine import GraphRAGEngine
from graph_visualizer import parse_graph_elements, build_graph_html

def test_pipeline():
    print("1. Initializing GraphManager (In-Memory Fallback)...")
    graph_mgr = GraphManager(use_live_neo4j=False)
    stats = graph_mgr.get_stats()
    print(f"   Stats: {stats}")
    assert stats["movies"] > 0, "No movies found in graph!"
    assert stats["people"] > 0, "No people found in graph!"
    assert stats["relationships"] > 0, "No relationships found in graph!"

    rag = GraphRAGEngine(graph_mgr)

    queries = [
        "Tell me about The Matrix",
        "What movies did Keanu Reeves act in and what roles did he play?",
        "Who directed The Matrix and what other movies did they direct?",
        "Which movies do Tom Hanks and Meg Ryan star together in?",
        "What is the tagline of Apollo 13?",
        "Top Gun"
    ]

    for q in queries:
        print(f"\n--- Testing Query: '{q}' ---")
        result = rag.process_query(q, api_key=GEMINI_API_KEY)
        print(f"Model: {result['trace']['synth_model']}")
        print(f"Generated Cypher:\n{result['cypher']}")
        print(f"Records Found: {len(result['records'])}")
        assert len(result['records']) > 0, f"Expected records for '{q}', got 0"
        
        safe_answer = result['answer'][:180].encode('ascii', 'replace').decode('ascii')
        print(f"Answer Preview:\n{safe_answer}...")

        # Test graph visualization elements
        elements = parse_graph_elements(result["records"])
        assert len(elements["nodes"]) > 0, "Expected graph nodes for visualizer"
        html = build_graph_html(elements["nodes"], elements["edges"])
        assert "vis.Network" in html, "Vis.js network script missing from HTML"
        print(f"Graph Visualizer: {len(elements['nodes'])} nodes, {len(elements['edges'])} edges")

    print("\nAll GraphRAG tests passed successfully!")

if __name__ == "__main__":
    test_pipeline()
