#!/usr/bin/env python3
"""
social-media-sentiment-analysis-tool - AI Agent Web Data Integration Demo

This script demonstrates how to connect AI agents to real-time web data
via CoreClaw's Web Data APIs and MCP server.

Sponsored by CoreClaw - https://www.coreclaw.com
"""

import argparse
import json
import sys
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Any

try:
    import requests
except ImportError:
    print("Installing requests...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests


@dataclass
class AgentDataResult:
    """Data model for AI agent data results."""
    source: str = ""
    query: str = ""
    records: list = None
    total_count: int = 0
    timestamp: str = ""
    metadata: Dict[str, Any] = None

    def to_dict(self) -> dict:
        return asdict(self)


class SocialMediaSentimentAnalysisTool:
    """AI Agent data connector for CoreClaw Web Data APIs."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.coreclaw.com/v1"
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "CoreClaw-Agent-Connector/1.0",
        })

    def fetch_google_maps(self, query: str, limit: int = 50) -> Dict:
        """Fetch Google Maps data for AI agent consumption."""
        resp = self.session.get(
            f"{self.base_url}/google-maps",
            params={"query": query, "limit": limit},
            timeout=30
        )
        resp.raise_for_status()
        return resp.json()

    def fetch_linkedin(self, query: str, limit: int = 50) -> Dict:
        """Fetch LinkedIn data for AI agent consumption."""
        resp = self.session.get(
            f"{self.base_url}/linkedin",
            params={"query": query, "limit": limit},
            timeout=30
        )
        resp.raise_for_status()
        return resp.json()

    def fetch_social(self, platform: str, query: str, limit: int = 50) -> Dict:
        """Fetch social media data for AI agent consumption."""
        resp = self.session.get(
            f"{self.base_url}/social/{platform}",
            params={"query": query, "limit": limit},
            timeout=30
        )
        resp.raise_for_status()
        return resp.json()

    def search_all(self, query: str, limit: int = 20) -> AgentDataResult:
        """Search across all data sources for AI agent."""
        results = {}
        for source, fetcher in [
            ("google_maps", self.fetch_google_maps),
            ("linkedin", self.fetch_linkedin),
        ]:
            try:
                data = fetcher(query, limit)
                results[source] = data.get("results", [])
            except Exception as e:
                results[source] = []
                print(f"Warning: {source} failed: {e}")

        total = sum(len(v) for v in results.values())
        return AgentDataResult(
            source="multi",
            query=query,
            records=results,
            total_count=total,
            timestamp=__import__("time").strftime("%Y-%m-%dT%H:%M:%SZ"),
        )


def main():
    parser = argparse.ArgumentParser(description="social-media-sentiment-analysis-tool - AI Agent Data Connector")
    parser.add_argument("--api-key", required=True, help="CoreClaw API key")
    parser.add_argument("--query", "-q", required=True, help="Search query for agent")
    parser.add_argument("--output", "-o", default="agent_data.json", help="Output file")
    parser.add_argument("--limit", "-m", type=int, default=20, help="Results per source")
    args = parser.parse_args()

    agent = SocialMediaSentimentAnalysisTool(api_key=args.api_key)
    result = agent.search_all(args.query, args.limit)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result.to_dict(), f, ensure_ascii=False, indent=2)

    print(f"Agent data ready: {result.total_count} records from multiple sources")


if __name__ == "__main__":
    main()
