"""
Interactive Graph Visualizer for Neo4j Movies RAG using Vis.js Force-Directed Graph.
Generates an interactive, responsive HTML component embedded into Streamlit.
"""

import json
from typing import List, Dict, Any


def build_graph_html(nodes: List[Dict[str, Any]], edges: List[Dict[str, Any]], height: int = 450) -> str:
    """
    Builds a standalone interactive Vis.js Network graph HTML page.
    """
    nodes_json = json.dumps(nodes)
    edges_json = json.dumps(edges)

    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
      <style>
        body, html {{
          margin: 0;
          padding: 0;
          width: 100%;
          height: 100%;
          overflow: hidden;
          background: #0e1117;
          font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }}
        #network {{
          width: 100%;
          height: {height}px;
          border: 1px solid #262730;
          border-radius: 10px;
          background: radial-gradient(circle, #1a1c24 0%, #0e1117 100%);
        }}
        .legend {{
          position: absolute;
          top: 12px;
          right: 12px;
          background: rgba(14, 17, 23, 0.85);
          backdrop-filter: blur(8px);
          padding: 8px 14px;
          border-radius: 8px;
          border: 1px solid #333846;
          color: #e0e0e0;
          font-size: 11px;
          z-index: 10;
          display: flex;
          gap: 12px;
          align-items: center;
        }}
        .legend-item {{
          display: flex;
          align-items: center;
          gap: 6px;
        }}
        .legend-dot {{
          width: 10px;
          height: 10px;
          border-radius: 50%;
        }}
      </style>
    </head>
    <body>
      <div class="legend">
        <div class="legend-item">
          <div class="legend-dot" style="background: #FF6B6B;"></div>
          <span>Movie</span>
        </div>
        <div class="legend-item">
          <div class="legend-dot" style="background: #4D96FF;"></div>
          <span>Person (Actor/Director)</span>
        </div>
        <div class="legend-item">
          <div class="legend-dot" style="background: #6BCB77;"></div>
          <span>Relationship</span>
        </div>
      </div>
      <div id="network"></div>

      <script type="text/javascript">
        const rawNodes = {nodes_json};
        const rawEdges = {edges_json};

        const container = document.getElementById('network');
        const data = {{
          nodes: new vis.DataSet(rawNodes),
          edges: new vis.DataSet(rawEdges)
        }};

        const options = {{
          nodes: {{
            shape: 'dot',
            size: 20,
            font: {{
              size: 13,
              color: '#ffffff',
              face: 'sans-serif',
              strokeWidth: 2,
              strokeColor: '#000000'
            }},
            borderWidth: 2,
            shadow: {{
              enabled: true,
              color: 'rgba(0,0,0,0.5)',
              size: 8,
              x: 2,
              y: 2
            }}
          }},
          edges: {{
            width: 2,
            font: {{
              size: 11,
              color: '#a0aec0',
              strokeWidth: 2,
              strokeColor: '#0e1117',
              align: 'middle'
            }},
            color: {{
              color: '#4a5568',
              highlight: '#63b3ed',
              hover: '#90cdf4'
            }},
            arrows: {{
              to: {{ enabled: true, scaleFactor: 0.6 }}
            }},
            smooth: {{
              type: 'cubicBezier',
              forceDirection: 'none',
              roundness: 0.2
            }}
          }},
          physics: {{
            stabilization: {{ iterations: 120 }},
            barnesHut: {{
              gravitationalConstant: -2200,
              centralGravity: 0.3,
              springLength: 95,
              springConstant: 0.04,
              damping: 0.09
            }}
          }},
          interaction: {{
            hover: true,
            tooltipDelay: 100,
            zoomView: true,
            dragView: true
          }}
        }};

        const network = new vis.Network(container, data, options);
      </script>
    </body>
    </html>
    """
    return html_template


def parse_graph_elements(records: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """
    Transforms arbitrary Cypher query or entity results into Vis.js nodes and edges.
    """
    nodes_dict = {}
    edges_list = []

    def add_node(node_id: str, label: str, node_type: str, details: Dict[str, Any] = None):
        if node_id in nodes_dict:
            return
        details = details or {}
        if node_type == "Movie":
            color = {"background": "#FF6B6B", "border": "#FF4D4D"}
            tooltip = f"<b>🎬 {label}</b><br/>Released: {details.get('released', 'Unknown')}<br/>Tagline: {details.get('tagline', 'N/A')}"
            size = 24
        else:
            color = {"background": "#4D96FF", "border": "#2B7BFF"}
            tooltip = f"<b>👤 {label}</b><br/>Born: {details.get('born', 'Unknown')}"
            size = 20

        nodes_dict[node_id] = {
            "id": node_id,
            "label": label,
            "color": color,
            "title": tooltip,
            "size": size
        }

    for item in records:
        # Check standard record shapes
        if "movie" in item and "actor1" in item and "actor2" in item:
            m_title = str(item["movie"])
            a1 = str(item["actor1"])
            a2 = str(item["actor2"])
            add_node(m_title, m_title, "Movie", {"released": item.get("released")})
            add_node(a1, a1, "Person")
            add_node(a2, a2, "Person")
            edges_list.append({"from": a1, "to": m_title, "label": "ACTED_IN", "color": {"color": "#6BCB77"}})
            edges_list.append({"from": a2, "to": m_title, "label": "ACTED_IN", "color": {"color": "#6BCB77"}})

        elif "movie" in item and "reviewer" in item:
            m_title = str(item["movie"])
            rev = str(item["reviewer"])
            add_node(m_title, m_title, "Movie")
            add_node(rev, rev, "Person")
            rating = item.get("rating", "")
            edges_list.append({
                "from": rev,
                "to": m_title,
                "label": f"REVIEWED ({rating}/100)" if rating else "REVIEWED",
                "color": {"color": "#FF69B4"}
            })

        elif "movie" in item and "actor" in item:
            m_title = str(item["movie"])
            p_name = str(item["actor"])
            add_node(m_title, m_title, "Movie", {"released": item.get("released"), "tagline": item.get("tagline")})
            add_node(p_name, p_name, "Person", {"born": item.get("born")})
            roles = item.get("roles", [])
            role_label = f"['{roles[0]}']" if (isinstance(roles, list) and roles) else "ACTED_IN"
            edges_list.append({
                "from": p_name,
                "to": m_title,
                "label": f"ACTED_IN\n{role_label}",
                "color": {"color": "#6BCB77"}
            })

        elif "movie" in item and "director" in item:
            m_title = str(item["movie"])
            p_name = str(item["director"])
            add_node(m_title, m_title, "Movie", {"released": item.get("released"), "tagline": item.get("tagline")})
            add_node(p_name, p_name, "Person", {"born": item.get("born")})
            edges_list.append({
                "from": p_name,
                "to": m_title,
                "label": "DIRECTED",
                "color": {"color": "#9D4EDD"}
            })

        elif "movie" in item and "tagline" in item:
            m_title = str(item["movie"])
            add_node(m_title, m_title, "Movie", item)
            directors = item.get("directors", [])
            if isinstance(directors, list):
                for d in directors:
                    if d:
                        add_node(str(d), str(d), "Person")
                        edges_list.append({
                            "from": str(d),
                            "to": m_title,
                            "label": "DIRECTED",
                            "color": {"color": "#9D4EDD"}
                        })

        elif "source" in item and "target" in item:
            s_name = str(item["source"])
            t_name = str(item["target"])
            rel_type = str(item.get("type", "RELATED_TO"))
            add_node(s_name, s_name, "Person")
            add_node(t_name, t_name, "Movie")
            edges_list.append({
                "from": s_name,
                "to": t_name,
                "label": rel_type,
                "color": {"color": "#FFD93D"}
            })

        elif "title" in item and "released" in item:
            m_title = str(item["title"])
            add_node(m_title, m_title, "Movie", item)

        elif "name" in item and "born" in item:
            p_name = str(item["name"])
            add_node(p_name, p_name, "Person", item)

    return {
        "nodes": list(nodes_dict.values()),
        "edges": edges_list
    }
