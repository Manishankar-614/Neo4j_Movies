"""
Database connector and Graph Engine for Neo4j Movies RAG.
Provides both live Neo4j driver connection and an in-memory fallback graph engine.
"""

import re
from typing import List, Dict, Any, Tuple, Optional
from neo4j import GraphDatabase, Driver
from movies_data import OFFICIAL_MOVIES_CYPHER, LOCAL_MOVIES_DATA


class Neo4jDatabase:
    """Manages connection and Cypher execution with a real Neo4j instance."""

    def __init__(self, uri: str, user: str, password: str, database: str = "neo4j"):
        self.uri = uri
        self.user = user
        self.password = password
        self.database = database
        self._driver: Optional[Driver] = None

    def connect(self) -> Driver:
        """Create or return existing Neo4j driver."""
        if self._driver is None:
            self._driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
        return self._driver

    def test_connection(self) -> Tuple[bool, str]:
        """Verify if Neo4j is reachable and authentication succeeds."""
        try:
            driver = self.connect()
            driver.verify_connectivity()
            with driver.session(database=self.database) as session:
                result = session.run("RETURN 1 AS test")
                record = result.single()
                if record and record["test"] == 1:
                    return True, "Successfully connected to Neo4j!"
            return False, "Connected but test query returned no result."
        except Exception as e:
            return False, f"Neo4j connection error: {str(e)}"

    def run_query(self, query: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Execute a Cypher query and return results as clean Python dictionaries."""
        driver = self.connect()
        records_list = []
        with driver.session(database=self.database) as session:
            result = session.run(query, params or {})
            for record in result:
                row = {}
                for key in record.keys():
                    val = record[key]
                    # Convert Neo4j Node/Relationship to dict if necessary
                    if hasattr(val, "_properties"):
                        props = dict(val._properties)
                        if hasattr(val, "labels"):
                            props["_labels"] = list(val.labels)
                        elif hasattr(val, "type"):
                            props["_type"] = val.type
                        row[key] = props
                    else:
                        row[key] = val
                records_list.append(row)
        return records_list

    def seed_movies(self) -> Tuple[bool, str]:
        """Seed the official Neo4j Movies dataset into the active database."""
        try:
            driver = self.connect()
            with driver.session(database=self.database) as session:
                # Clear existing Movies & Person nodes first to avoid duplicates
                session.run("MATCH (n:Movie) DETACH DELETE n")
                session.run("MATCH (n:Person) DETACH DELETE n")

                # The script has multiple statements or a large block; execute via transaction
                # Split CREATE statements if needed or execute block
                statements = [s.strip() for s in OFFICIAL_MOVIES_CYPHER.split(";\n") if s.strip()]
                if not statements:
                    statements = [OFFICIAL_MOVIES_CYPHER]

                for stmt in statements:
                    if stmt:
                        session.run(stmt)

                # Count created nodes
                res = session.run(
                    "MATCH (m:Movie) WITH count(m) AS movies "
                    "MATCH (p:Person) WITH movies, count(p) AS people "
                    "MATCH ()-[r]->() RETURN movies, people, count(r) AS rels"
                ).single()

                if res:
                    return True, (
                        f"Database seeded successfully! Created {res['movies']} movies, "
                        f"{res['people']} people, and {res['rels']} relationships."
                    )
                return True, "Movies dataset created successfully."
        except Exception as e:
            return False, f"Failed to seed Neo4j database: {str(e)}"

    def get_stats(self) -> Dict[str, Any]:
        """Get summary statistics of the graph."""
        try:
            driver = self.connect()
            with driver.session(database=self.database) as session:
                movies_cnt = session.run("MATCH (m:Movie) RETURN count(m) AS cnt").single()["cnt"]
                people_cnt = session.run("MATCH (p:Person) RETURN count(p) AS cnt").single()["cnt"]
                rel_cnt = session.run("MATCH ()-[r]->() RETURN count(r) AS cnt").single()["cnt"]
                return {
                    "movies": movies_cnt,
                    "people": people_cnt,
                    "relationships": rel_cnt,
                    "connected": True
                }
        except Exception:
            return {"movies": 0, "people": 0, "relationships": 0, "connected": False}

    def close(self):
        """Close driver connection."""
        if self._driver:
            self._driver.close()
            self._driver = None


class LocalGraphEngine:
    """
    High-fidelity built-in In-Memory Knowledge Graph.
    Contains the full Neo4j Movies dataset and handles graph queries,
    entity lookups, multi-hop traversals, and simple Cypher parsing.
    """

    def __init__(self):
        self.movies = {m["title"].lower(): m for m in LOCAL_MOVIES_DATA["movies"]}
        self.people = {p["name"].lower(): p for p in LOCAL_MOVIES_DATA["people"]}
        self.relationships = LOCAL_MOVIES_DATA["relationships"]

    def get_stats(self) -> Dict[str, Any]:
        return {
            "movies": len(self.movies),
            "people": len(self.people),
            "relationships": len(self.relationships),
            "connected": True,
            "mode": "In-Memory Graph"
        }

    def search_entities(self, query_text: str) -> Dict[str, Any]:
        """
        Find matching movies and persons mentioned or related to the user prompt.
        """
        query_lower = query_text.lower()
        matched_movies = []
        matched_people = []

        for m_key, m_val in self.movies.items():
            if m_key in query_lower or any(word in query_lower for word in m_key.split() if len(word) > 3):
                matched_movies.append(m_val)

        for p_key, p_val in self.people.items():
            if p_key in query_lower or any(word in query_lower for word in p_key.split() if len(word) > 3):
                matched_people.append(p_val)

        # Retrieve connected subgraphs
        connected_rels = []
        movie_titles = {m["title"] for m in matched_movies}
        people_names = {p["name"] for p in matched_people}

        for rel in self.relationships:
            if rel["from"] in people_names or rel["to"] in movie_titles:
                connected_rels.append(rel)
                # Expand one hop
                if rel["to"] not in movie_titles:
                    m = self.get_movie(rel["to"])
                    if m and m not in matched_movies:
                        matched_movies.append(m)
                if rel["from"] not in people_names:
                    p = self.get_person(rel["from"])
                    if p and p not in matched_people:
                        matched_people.append(p)

        return {
            "movies": matched_movies,
            "people": matched_people,
            "relationships": connected_rels
        }

    def get_movie(self, title: str) -> Optional[Dict[str, Any]]:
        return self.movies.get(title.lower())

    def get_person(self, name: str) -> Optional[Dict[str, Any]]:
        return self.people.get(name.lower())

    def find_movie_in_text(self, text: str) -> Optional[Dict[str, Any]]:
        text_lower = text.lower()
        sorted_movies = sorted(self.movies.values(), key=lambda m: len(m["title"]), reverse=True)
        for m in sorted_movies:
            if m["title"].lower() in text_lower:
                return m
        return None

    def find_person_in_text(self, text: str) -> Optional[Dict[str, Any]]:
        text_lower = text.lower()
        sorted_people = sorted(self.people.values(), key=lambda p: len(p["name"]), reverse=True)
        for p in sorted_people:
            if p["name"].lower() in text_lower:
                return p
        return None

    def run_query(self, cypher: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        cypher_lower = cypher.lower()
        quoted = re.findall(r"['\"]([^'\"]+)['\"]", cypher)

        # 1. Co-actor query: p1 and p2 acting in same movie
        if ("p1" in cypher_lower and "p2" in cypher_lower and "acted_in" in cypher_lower) or len(quoted) >= 2:
            people_found = []
            for q in quoted:
                p = self.find_person_in_text(q)
                if p and p["name"] not in [x["name"] for x in people_found]:
                    people_found.append(p)
            if len(people_found) >= 2:
                a1 = people_found[0]["name"]
                a2 = people_found[1]["name"]
                m_a1 = {r["to"] for r in self.relationships if r["type"] == "ACTED_IN" and r["from"] == a1}
                m_a2 = {r["to"] for r in self.relationships if r["type"] == "ACTED_IN" and r["from"] == a2}
                common = m_a1.intersection(m_a2)
                results = []
                for title in common:
                    m_obj = self.movies.get(title.lower())
                    results.append({
                        "actor1": a1,
                        "actor2": a2,
                        "movie": title,
                        "released": m_obj["released"] if m_obj else None
                    })
                if results:
                    return results

        # 2. Check for target person in query
        target_person = None
        for q in quoted:
            p = self.find_person_in_text(q)
            if p:
                target_person = p
                break

        # 3. Check for target movie in query
        target_movie = None
        for q in quoted:
            m = self.find_movie_in_text(q)
            if m:
                target_movie = m
                break

        # If not in quotes, search the whole cypher string
        if not target_movie:
            target_movie = self.find_movie_in_text(cypher)
        if not target_person:
            target_person = self.find_person_in_text(cypher)

        # Case A: Movie was searched (e.g. "The Matrix", "Top Gun", "Apollo 13")
        if target_movie:
            m_title = target_movie["title"]
            movie_actors = []
            for r in self.relationships:
                if r["type"] == "ACTED_IN" and r["to"].lower() == m_title.lower():
                    p_obj = self.people.get(r["from"].lower(), {})
                    roles = r["props"].get("roles", [])
                    movie_actors.append({
                        "actor": r["from"],
                        "movie": m_title,
                        "roles": roles,
                        "released": target_movie["released"],
                        "tagline": target_movie["tagline"],
                        "born": p_obj.get("born")
                    })
            directors = [
                r["from"] for r in self.relationships
                if r["type"] == "DIRECTED" and r["to"].lower() == m_title.lower()
            ]
            reviews = [
                {"reviewer": r["from"], "rating": r["props"].get("rating"), "summary": r["props"].get("summary")}
                for r in self.relationships
                if r["type"] == "REVIEWED" and r["to"].lower() == m_title.lower()
            ]

            if "directed" in cypher_lower and not ("acted_in" in cypher_lower or "actor" in cypher_lower):
                return [
                    {
                        "director": d,
                        "movie": m_title,
                        "released": target_movie["released"],
                        "tagline": target_movie["tagline"]
                    }
                    for d in directors
                ] or [{"movie": m_title, "director": "Unknown", "released": target_movie["released"]}]

            if movie_actors:
                for ma in movie_actors:
                    ma["directors"] = directors
                    ma["reviews"] = reviews
                return movie_actors

            return [{
                "movie": m_title,
                "released": target_movie["released"],
                "tagline": target_movie["tagline"],
                "directors": directors
            }]

        # Case B: Person was searched (e.g. "Keanu Reeves", "Tom Hanks")
        if target_person:
            p_name = target_person["name"]
            person_movies = []
            for r in self.relationships:
                if r["type"] == "ACTED_IN" and r["from"].lower() == p_name.lower():
                    m_obj = self.movies.get(r["to"].lower(), {})
                    person_movies.append({
                        "actor": p_name,
                        "movie": r["to"],
                        "roles": r["props"].get("roles", []),
                        "released": m_obj.get("released"),
                        "tagline": m_obj.get("tagline"),
                        "born": target_person.get("born")
                    })
            if person_movies and ("acted_in" in cypher_lower or "director" not in cypher_lower):
                return sorted(person_movies, key=lambda x: x.get("released") or 0, reverse=True)

            directed_movies = []
            for r in self.relationships:
                if r["type"] == "DIRECTED" and r["from"].lower() == p_name.lower():
                    m_obj = self.movies.get(r["to"].lower(), {})
                    directed_movies.append({
                        "director": p_name,
                        "movie": r["to"],
                        "released": m_obj.get("released"),
                        "tagline": m_obj.get("tagline"),
                        "born": target_person.get("born")
                    })
            if directed_movies:
                return directed_movies

        # Case C: Reviews query
        if "reviewed" in cypher_lower:
            results = []
            for r in self.relationships:
                if r["type"] == "REVIEWED":
                    results.append({
                        "reviewer": r["from"],
                        "movie": r["to"],
                        "rating": r["props"].get("rating"),
                        "summary": r["props"].get("summary")
                    })
            return sorted(results, key=lambda x: x.get("rating") or 0, reverse=True)

        # Default fallback: Top 5 sample movies with their directors
        sample = []
        for m in list(self.movies.values())[:5]:
            dirs = [r["from"] for r in self.relationships if r["type"] == "DIRECTED" and r["to"].lower() == m["title"].lower()]
            sample.append({
                "movie": m["title"],
                "released": m["released"],
                "tagline": m["tagline"],
                "directors": dirs
            })
        return sample


class GraphManager:
    """
    Unified manager that delegates queries to either real Neo4j or In-Memory Graph.
    """

    def __init__(self, use_live_neo4j: bool = False, uri: str = "", user: str = "", password: str = "", database: str = "neo4j"):
        self.use_live_neo4j = use_live_neo4j
        self.neo4j_db = Neo4jDatabase(uri, user, password, database) if (use_live_neo4j and uri) else None
        self.local_graph = LocalGraphEngine()

    def is_live(self) -> bool:
        return bool(self.use_live_neo4j and self.neo4j_db)

    def test_connection(self) -> Tuple[bool, str]:
        if self.is_live():
            return self.neo4j_db.test_connection()
        return True, "Using Built-in High-Fidelity Movies Graph (In-Memory Engine)."

    def run_query(self, cypher: str, params: Optional[Dict[str, Any]] = None) -> Tuple[List[Dict[str, Any]], Optional[str]]:
        """
        Execute Cypher query. Returns (records, error_message).
        """
        if self.is_live():
            try:
                records = self.neo4j_db.run_query(cypher, params)
                return records, None
            except Exception as e:
                # If live query fails, return error
                return [], f"Cypher Execution Error: {str(e)}"
        else:
            try:
                records = self.local_graph.run_query(cypher, params)
                return records, None
            except Exception as e:
                return [], f"Local Graph Engine Error: {str(e)}"

    def search_entities(self, query_text: str) -> Dict[str, Any]:
        """Hybrid search across graph nodes and relationships."""
        if self.is_live():
            # Run Cypher entity search in Neo4j
            try:
                query = """
                MATCH (n)
                WHERE (n:Movie AND toLower(n.title) CONTAINS toLower($text))
                   OR (n:Person AND toLower(n.name) CONTAINS toLower($text))
                OPTIONAL MATCH (n)-[r]-(m)
                RETURN n, r, m LIMIT 25
                """
                results = self.neo4j_db.run_query(query, {"text": query_text})
                movies = []
                people = []
                rels = []
                for row in results:
                    n = row.get("n", {})
                    if "_labels" in n:
                        if "Movie" in n["_labels"] and n not in movies:
                            movies.append(n)
                        elif "Person" in n["_labels"] and n not in people:
                            people.append(n)
                    m = row.get("m", {})
                    if "_labels" in m:
                        if "Movie" in m["_labels"] and m not in movies:
                            movies.append(m)
                        elif "Person" in m["_labels"] and m not in people:
                            people.append(m)
                    r = row.get("r")
                    if r:
                        rels.append(r)
                return {"movies": movies, "people": people, "relationships": rels}
            except Exception:
                pass
        return self.local_graph.search_entities(query_text)

    def get_stats(self) -> Dict[str, Any]:
        if self.is_live():
            stats = self.neo4j_db.get_stats()
            stats["mode"] = "Live Neo4j Database"
            return stats
        return self.local_graph.get_stats()
