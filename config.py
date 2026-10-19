"""
Configuration module for the Neo4j Movies GraphRAG system.
Loads settings from environment variables or .env file.
"""

import os
from dotenv import load_dotenv

# Load .env file
load_dotenv(override=True)

# Neo4j Database Settings
DEFAULT_NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
DEFAULT_NEO4J_USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
DEFAULT_NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")
DEFAULT_NEO4J_DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")

# Gemini API Key (Loaded exclusively from .env)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# App Metadata
APP_TITLE = "NeoCinema GraphRAG"
APP_SUBTITLE = "Knowledge Graph Retrieval-Augmented Generation grounded on Neo4j Movies"
