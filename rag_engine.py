"""
Retrieval-Augmented Generation (GraphRAG) engine for Neo4j Movies dataset.
Powered by:
- Google Gemini API (gemini-3.8-flash via google.genai Client)
- Built-in High-Fidelity Graph Engine & Heuristic Fallback
"""

import re
import json
import time
from typing import Dict, Any, Tuple, List, Optional
import requests

from graph_db import GraphManager

# Neo4j Movies Schema prompt
MOVIES_GRAPH_SCHEMA = """
Neo4j Movies Dataset Schema:
Node Labels:
- Movie {title: STRING, released: INTEGER, tagline: STRING}
- Person {name: STRING, born: INTEGER}

Relationship Types:
- (:Person)-[:ACTED_IN {roles: LIST OF STRINGS}]->(:Movie)
- (:Person)-[:DIRECTED]->(:Movie)
- (:Person)-[:PRODUCED]->(:Movie)
- (:Person)-[:WROTE]->(:Movie)
- (:Person)-[:REVIEWED {rating: INTEGER, summary: STRING}]->(:Movie)

Guidelines for Cypher Query Generation:
- Always use case-insensitive matching for names and titles, e.g. `toLower(m.title) CONTAINS toLower('matrix')` or `toLower(p.name) CONTAINS toLower('keanu')`
- Return meaningful aliases, e.g. `actor`, `movie`, `director`, `roles`, `tagline`, `released`
- Only generate read-only MATCH queries (never CREATE, MERGE, or DELETE)
- Always include a reasonable LIMIT (e.g. LIMIT 25)
- Output ONLY the raw Cypher query code without backticks, commentary, or markdown fences.
"""


class GraphRAGEngine:
    def __init__(self, graph_manager: GraphManager):
        self.graph_manager = graph_manager

    def generate_cypher_with_rules(self, query: str) -> str:
        """
        Rule-based Text-to-Cypher generator for movie graph queries.
        Ensures accurate Cypher generation even when offline.
        """
        q = query.lower()

        # Co-actors or common movies
        co_actors = re.findall(
            r"(?:tom hanks|meg ryan|keanu reeves|jack nicholson|tom cruise|kevin bacon|gene hackman|hugo weaving|carrie-anne moss|laurence fishburne|charlize theron)",
            q
        )
        if len(co_actors) >= 2:
            return (
                f"MATCH (p1:Person)-[:ACTED_IN]->(m:Movie)<-[:ACTED_IN]-(p2:Person)\n"
                f"WHERE toLower(p1.name) CONTAINS '{co_actors[0]}' AND toLower(p2.name) CONTAINS '{co_actors[1]}'\n"
                f"RETURN p1.name AS actor1, p2.name AS actor2, m.title AS movie, m.released AS released\n"
                f"LIMIT 15"
            )

        # Directors query
        if "direct" in q:
            movie_matches = [
                "the matrix reloaded", "the matrix revolutions", "the matrix",
                "apollo 13", "top gun", "a few good men", "unforgiven",
                "the green mile", "cast away", "you've got mail", "stand by me",
                "v for vendetta", "cloud atlas", "the da vinci code", "that thing you do"
            ]
            found_movie = next((m for m in movie_matches if m in q), None)
            if found_movie:
                return (
                    f"MATCH (p:Person)-[:DIRECTED]->(m:Movie)\n"
                    f"WHERE toLower(m.title) CONTAINS '{found_movie}'\n"
                    f"RETURN p.name AS director, m.title AS movie, m.released AS released, m.tagline AS tagline, p.born AS born\n"
                    f"LIMIT 10"
                )
            director_matches = [
                "clint eastwood", "ron howard", "rob reiner", "lana wachowski",
                "lilly wachowski", "nora ephron", "robert zemeckis", "frank darabont"
            ]
            found_dir = next((d for d in director_matches if d in q), None)
            if found_dir:
                return (
                    f"MATCH (p:Person)-[:DIRECTED]->(m:Movie)\n"
                    f"WHERE toLower(p.name) CONTAINS '{found_dir}'\n"
                    f"RETURN p.name AS director, m.title AS movie, m.released AS released, m.tagline AS tagline\n"
                    f"LIMIT 15"
                )

        # Reviews / Ratings
        if "review" in q or "rating" in q or "score" in q:
            return (
                "MATCH (p:Person)-[r:REVIEWED]->(m:Movie)\n"
                "RETURN p.name AS reviewer, m.title AS movie, r.rating AS rating, r.summary AS summary\n"
                "ORDER BY r.rating DESC\n"
                "LIMIT 15"
            )

        # Movie Search by Title
        movie_matches = [
            "the matrix reloaded", "the matrix revolutions", "the matrix",
            "the devil's advocate", "a few good men", "top gun", "jerry maguire",
            "stand by me", "apollo 13", "cast away", "you've got mail",
            "sleepless in seattle", "joe versus the volcano", "when harry met sally",
            "that thing you do", "the replacements", "unforgiven", "the birdcage",
            "the da vinci code", "v for vendetta", "cloud atlas", "the green mile"
        ]
        found_movie = next((m for m in movie_matches if m in q), None)
        if found_movie:
            return (
                f"MATCH (m:Movie)\n"
                f"WHERE toLower(m.title) CONTAINS '{found_movie}'\n"
                f"OPTIONAL MATCH (p:Person)-[r:ACTED_IN]->(m)\n"
                f"OPTIONAL MATCH (d:Person)-[:DIRECTED]->(m)\n"
                f"RETURN m.title AS movie, m.released AS released, m.tagline AS tagline, p.name AS actor, r.roles AS roles, d.name AS director\n"
                f"LIMIT 25"
            )

        # Actor Filmography
        actor_matches = [
            "keanu reeves", "tom hanks", "meg ryan", "tom cruise",
            "jack nicholson", "carrie-anne moss", "laurence fishburne",
            "hugo weaving", "charlize theron", "robin williams",
            "clint eastwood", "morgan freeman", "halle berry", "natalie portman"
        ]
        found_actor = next((a for a in actor_matches if a in q), None)
        if found_actor:
            return (
                f"MATCH (p:Person)-[r:ACTED_IN]->(m:Movie)\n"
                f"WHERE toLower(p.name) CONTAINS '{found_actor}'\n"
                f"RETURN p.name AS actor, m.title AS movie, r.roles AS roles, m.released AS released, m.tagline AS tagline, p.born AS born\n"
                f"ORDER BY m.released DESC\n"
                f"LIMIT 15"
            )

        # General Fallback
        return (
            "MATCH (p:Person)-[r:ACTED_IN]->(m:Movie)\n"
            "RETURN p.name AS actor, m.title AS movie, r.roles AS roles, m.released AS released\n"
            "LIMIT 10"
        )

    def generate_cypher_llm(self, user_query: str, api_key: str = "") -> Tuple[str, str]:
        """
        Translate user prompt into Cypher query using Google Gemini.
        Returns: (cypher_query, model_name_used)
        """
        system_prompt = (
            f"You are a Neo4j Cypher graph database expert.\n"
            f"Convert the user's natural language question into an accurate, read-only Cypher query based on this schema:\n\n"
            f"{MOVIES_GRAPH_SCHEMA}\n\n"
            f"Important instructions:\n"
            f"- For questions about a movie, match the Movie node and optionally match its actors and directors.\n"
            f"- Example: MATCH (m:Movie) WHERE toLower(m.title) CONTAINS toLower('matrix') OPTIONAL MATCH (p:Person)-[r:ACTED_IN]->(m) RETURN m.title AS movie, m.released AS released, m.tagline AS tagline, p.name AS actor, r.roles AS roles LIMIT 25\n"
            f"- Output ONLY the raw Cypher query code. No explanations, no markdown fences (no ```cypher)."
        )

        if api_key:
            try:
                from google import genai
                client = genai.Client(api_key=api_key)
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=f"{system_prompt}\n\nUser Question: {user_query}\nCypher Query:"
                )
                raw = response.text.strip()
                raw = re.sub(r"^```(?:cypher)?\n?", "", raw, flags=re.IGNORECASE)
                raw = re.sub(r"\n?```$", "", raw)
                return raw.strip(), "Google Gemini 3.8 Flash"
            except Exception:
                pass

        # Offline rule-based fallback
        return self.generate_cypher_with_rules(user_query), "Built-in Neural Heuristic"

    def synthesize_answer(
        self,
        user_query: str,
        cypher_query: str,
        graph_results: List[Dict[str, Any]],
        api_key: str = ""
    ) -> Tuple[str, str]:
        """
        Synthesize natural-language answer grounded in retrieved graph data.
        Returns: (synthesized_text, model_name_used)
        """
        results_str = json.dumps(graph_results, indent=2)

        prompt = (
            f"You are a knowledgeable and engaging cinema expert assisting a user with movie questions.\n"
            f"You are strictly grounded on factual data from the Neo4j Movies Knowledge Graph.\n\n"
            f"User Question: {user_query}\n"
            f"Cypher Query Executed: {cypher_query}\n"
            f"Retrieved Graph Facts:\n{results_str}\n\n"
            f"Formatting Guidelines:\n"
            f"1. Give an engaging, articulate, conversational answer strictly based on the retrieved facts.\n"
            f"2. When describing a movie, mention its release year, tagline in quotes, directors, and the cast with their character roles.\n"
            f"3. Use clean markdown: bold movie titles (**The Matrix**), bullet points, and italic quotes for taglines.\n"
            f"4. If no records were found, politely explain what was searched and suggest alternative titles/actors in the Neo4j Movies graph."
        )

        if api_key:
            try:
                from google import genai
                client = genai.Client(api_key=api_key)
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt
                )
                return response.text.strip(), "Google Gemini 3.8 Flash"
            except Exception:
                pass

        # Offline Intelligent Synthesizer
        return self._offline_synthesizer(user_query, cypher_query, graph_results), "NeoCinema Semantic Synthesizer"

    def _offline_synthesizer(self, query: str, cypher: str, results: List[Dict[str, Any]]) -> str:
        """Rich semantic synthesizer when operating offline or as fallback."""
        if not results:
            return (
                f"### 🎬 Graph Search Results\n\n"
                f"I traversed the **Neo4j Movies Knowledge Graph** for **'{query}'**, but could not find matching records.\n\n"
                f"- **Cypher Attempted:** `{cypher.strip()}`\n"
                f"- **Suggested Queries:** Try exploring well-known titles (*The Matrix*, *Apollo 13*, *Top Gun*, *A Few Good Men*, *You've Got Mail*) "
                f"or stars (*Keanu Reeves*, *Tom Hanks*, *Meg Ryan*, *Tom Cruise*, *Charlize Theron*)."
            )

        first = results[0]

        # Case 1: Movie Spotlight with Cast & Directors
        movie_names = {r.get("movie") for r in results if r.get("movie")}
        if len(movie_names) == 1:
            m_title = list(movie_names)[0]
            year = f" ({first['released']})" if first.get("released") else ""
            tagline = f"> *\"{first['tagline']}\"*\n\n" if first.get("tagline") else ""
            
            # Extract directors
            dirs = first.get("directors", [])
            if not dirs:
                dirs = list({r.get("director") for r in results if r.get("director")})
            dir_str = f"- **Director(s):** {', '.join(dirs)}\n" if dirs else ""

            # Extract cast
            cast_lines = []
            for r in results:
                actor = r.get("actor")
                if actor:
                    roles = r.get("roles", [])
                    role_str = f" as **{', '.join(roles)}**" if (isinstance(roles, list) and roles) else ""
                    cast_lines.append(f"- **{actor}**{role_str}")

            cast_section = "\n##### 👥 Cast & Characters\n" + "\n".join(cast_lines) if cast_lines else ""

            return (
                f"### 🎬 Movie Spotlight: **{m_title}**{year}\n\n"
                f"{tagline}"
                f"- **Release Year:** {first.get('released', 'N/A')}\n"
                f"{dir_str}"
                f"{cast_section}"
            )

        # Case 2: Filmography (Actor & Movies)
        if "actor" in first and "movie" in first and len(movie_names) > 1:
            actor = first.get("actor", "The actor")
            movies = []
            for r in results:
                roles = r.get("roles", [])
                role_text = f" as **{', '.join(roles)}**" if (isinstance(roles, list) and roles) else ""
                year_text = f" ({r['released']})" if r.get("released") else ""
                tagline = f' — *"{r["tagline"]}"*' if r.get("tagline") else ""
                movies.append(f"- **{r.get('movie')}**{year_text}{role_text}{tagline}")

            born_info = f" *(born {first.get('born')})*" if first.get("born") else ""
            return (
                f"### 🎬 Filmography for **{actor}**{born_info}\n\n"
                f"According to the **Neo4j Movies Knowledge Graph**, **{actor}** has starred in {len(movies)} movie(s):\n\n"
                + "\n".join(movies)
            )

        # Case 3: Directors
        if "director" in first and "movie" in first:
            director_map = {}
            for r in results:
                d = r.get("director", "Unknown Director")
                m = r.get("movie", "Unknown Movie")
                yr = f" ({r['released']})" if r.get("released") else ""
                director_map.setdefault(d, set()).add(f"**{m}**{yr}")

            sections = []
            for d, m_set in director_map.items():
                m_list = "\n".join(f"- {m}" for m in sorted(m_set))
                sections.append(f"#### 🎥 **{d}**\n{m_list}")

            return (
                f"### 🎬 Directorial Credits in Knowledge Graph\n\n"
                + "\n\n".join(sections)
            )

        # Case 4: Co-actors
        if "actor1" in first and "actor2" in first and "movie" in first:
            a1 = first["actor1"]
            a2 = first["actor2"]
            movies = [f"- **{r['movie']}** ({r.get('released', 'Unknown')})" for r in results]
            return (
                f"### 🤝 Collaborations between **{a1}** and **{a2}**\n\n"
                f"The Neo4j graph reveals that **{a1}** and **{a2}** co-starred in:\n\n"
                + "\n".join(movies)
            )

        # Case 5: Reviews & Ratings
        if "reviewer" in first and "movie" in first:
            reviews = [
                f"- **{r['reviewer']}** rated **{r['movie']}** {r.get('rating')}/100: *\"{r.get('summary')}\"*"
                for r in results
            ]
            return (
                f"### ⭐ Community Reviews from Knowledge Graph\n\n"
                + "\n".join(reviews)
            )

        # General records
        items = []
        for r in results:
            item_str = ", ".join(f"**{k}**: {v}" for k, v in r.items() if v)
            items.append(f"- {item_str}")

        return (
            f"### 📊 Knowledge Graph Records\n\n"
            f"Retrieved {len(results)} record(s) matching your request:\n\n"
            + "\n".join(items)
        )

    def process_query(self, user_query: str, api_key: str = "") -> Dict[str, Any]:
        """
        Complete GraphRAG execution pipeline with execution trace:
        1. Natural language question analysis
        2. Text-to-Cypher generation via Gemini
        3. Subgraph traversal & retrieval
        4. LLM synthesis
        5. Execution trace metrics
        """
        start_time = time.time()

        # Step 1: Text-to-Cypher
        cypher_query, cypher_model = self.generate_cypher_llm(user_query, api_key)

        # Step 2: Execute against Graph
        results, err = self.graph_manager.run_query(cypher_query)

        # Step 3: Hybrid entity fallback if empty
        fallback_used = False
        if not results:
            fallback_used = True
            entity_data = self.graph_manager.search_entities(user_query)
            if entity_data.get("movies"):
                results = entity_data["movies"]
            elif entity_data.get("relationships"):
                results = [
                    {
                        "source": r["from"],
                        "type": r["type"],
                        "target": r["to"],
                        "details": r.get("props", {})
                    }
                    for r in entity_data["relationships"]
                ]
            elif entity_data.get("people"):
                results = entity_data["people"]

        # Step 4: Answer synthesis
        answer, synth_model = self.synthesize_answer(
            user_query=user_query,
            cypher_query=cypher_query,
            graph_results=results,
            api_key=api_key
        )

        elapsed_ms = round((time.time() - start_time) * 1000)

        return {
            "query": user_query,
            "cypher": cypher_query,
            "error": err,
            "records": results,
            "fallback_used": fallback_used,
            "answer": answer,
            "trace": {
                "cypher_model": cypher_model,
                "synth_model": synth_model,
                "latency_ms": elapsed_ms,
                "records_count": len(results),
                "status": "Success" if results else "No Match"
            }
        }
