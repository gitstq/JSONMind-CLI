#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JSONMind AI Module: Natural Language Query Processing
AI自然语言查询处理模块

This module provides optional AI-powered features for JSONMind.
It requires external AI API access (OpenAI, Anthropic, etc.)
"""

import json
import re
from typing import Any, Dict, List, Optional
from urllib.request import Request, urlopen
from urllib.error import URLError


class AIQueryEngine:
    """AI-powered query engine for natural language JSON queries"""
    
    def __init__(self, api_key: Optional[str] = None, provider: str = "openai"):
        self.api_key = api_key
        self.provider = provider.lower()
        self.base_urls = {
            "openai": "https://api.openai.com/v1/chat/completions",
            "anthropic": "https://api.anthropic.com/v1/messages",
        }
    
    def _call_api(self, prompt: str, json_context: str) -> Optional[str]:
        """Call AI API with prompt"""
        if not self.api_key:
            return None
        
        try:
            if self.provider == "openai":
                return self._call_openai(prompt, json_context)
            elif self.provider == "anthropic":
                return self._call_anthropic(prompt, json_context)
        except Exception as e:
            print(f"AI API Error: {e}")
            return None
        
        return None
    
    def _call_openai(self, prompt: str, json_context: str) -> Optional[str]:
        """Call OpenAI API"""
        url = self.base_urls["openai"]
        
        system_prompt = """You are a JSON query assistant. Convert natural language queries into JSONPath-like expressions.
Given a JSON structure and a natural language query, return ONLY the query path.

Examples:
- "find users over 25" -> "users[?age > 25]"
- "get the first user's name" -> "users.0.name"
- "count all active users" -> "count(users[?active == true])"
- "find users in Beijing" -> "users[?profile.location == 'Beijing']"

Return ONLY the query expression, no explanation."""
        
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"JSON Structure:\n{json_context}\n\nQuery: {prompt}"}
            ],
            "temperature": 0.1,
            "max_tokens": 100
        }
        
        req = Request(
            url,
            data=json.dumps(data).encode('utf-8'),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            },
            method="POST"
        )
        
        with urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result['choices'][0]['message']['content'].strip()
    
    def _call_anthropic(self, prompt: str, json_context: str) -> Optional[str]:
        """Call Anthropic API"""
        url = self.base_urls["anthropic"]
        
        system_prompt = """You are a JSON query assistant. Convert natural language queries into JSONPath-like expressions.
Given a JSON structure and a natural language query, return ONLY the query path.

Examples:
- "find users over 25" -> "users[?age > 25]"
- "get the first user's name" -> "users.0.name"
- "count all active users" -> "count(users[?active == true])"
- "find users in Beijing" -> "users[?profile.location == 'Beijing']"

Return ONLY the query expression, no explanation."""
        
        data = {
            "model": "claude-3-haiku-20240307",
            "max_tokens": 100,
            "system": system_prompt,
            "messages": [
                {"role": "user", "content": f"JSON Structure:\n{json_context}\n\nQuery: {prompt}"}
            ]
        }
        
        req = Request(
            url,
            data=json.dumps(data).encode('utf-8'),
            headers={
                "Content-Type": "application/json",
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01"
            },
            method="POST"
        )
        
        with urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result['content'][0]['text'].strip()
    
    def natural_language_query(self, data: Any, query: str) -> Dict[str, Any]:
        """Process natural language query against JSON data"""
        # Generate context about JSON structure
        context = self._generate_context(data)
        
        # Try to parse query without AI first (rule-based)
        result = self._rule_based_query(data, query)
        if result is not None:
            return {
                "success": True,
                "method": "rule-based",
                "result": result
            }
        
        # Fall back to AI if API key is available
        if self.api_key:
            ai_result = self._call_api(query, context)
            if ai_result:
                # Parse AI result and execute
                result = self._execute_query_path(data, ai_result)
                return {
                    "success": True,
                    "method": "ai-assisted",
                    "query_path": ai_result,
                    "result": result
                }
        
        return {
            "success": False,
            "error": "Could not understand query. Try using specific syntax like 'users.0.name' or 'filter users where age > 25'"
        }
    
    def _generate_context(self, data: Any, max_depth: int = 3) -> str:
        """Generate JSON structure context for AI"""
        def describe(obj: Any, depth: int = 0) -> str:
            if depth > max_depth:
                return "..."
            
            if isinstance(obj, dict):
                items = []
                for k, v in list(obj.items())[:10]:  # Limit to 10 keys
                    items.append(f'"{k}": {describe(v, depth + 1)}')
                return "{" + ", ".join(items) + "}"
            elif isinstance(obj, list):
                if len(obj) > 0:
                    return f"[{describe(obj[0], depth + 1)}, ... ({len(obj)} items)]"
                return "[]"
            elif isinstance(obj, str):
                return '"string"'
            elif isinstance(obj, bool):
                return "boolean"
            elif isinstance(obj, (int, float)):
                return "number"
            else:
                return "null"
        
        return describe(data)
    
    def _rule_based_query(self, data: Any, query: str) -> Optional[Any]:
        """Parse natural language query using rules"""
        query_lower = query.lower().strip()
        
        # Pattern: "find X where Y op Z"
        # Example: "find users where age > 25"
        filter_pattern = r'find\s+(\w+)\s+where\s+(\w+)\s*(>|>=|<|<=|==|!=|contains)\s*(.+)'
        match = re.match(filter_pattern, query_lower)
        if match:
            collection, key, op, value = match.groups()
            value = value.strip().strip('"\'')
            
            # Map operator
            op_map = {
                '>': 'gt', '>=': 'gte', '<': 'lt', '<=': 'lte',
                '==': 'eq', '!=': 'ne'
            }
            operator = op_map.get(op, op)
            
            # Get collection
            if isinstance(data, dict) and collection in data:
                collection_data = data[collection]
            else:
                collection_data = data
            
            if isinstance(collection_data, list):
                from jsonmind import JSONMind
                jm = JSONMind()
                return jm.filter_by_condition(collection_data, key, operator, value)
        
        # Pattern: "get X of Y" or "X of Y"
        # Example: "name of first user" or "get first user's email"
        get_pattern = r'(?:get\s+)?(\w+)\s+of\s+(\w+)\s+(\w+)'
        match = re.match(get_pattern, query_lower)
        if match:
            field, position, collection = match.groups()
            
            # Get collection
            if isinstance(data, dict) and collection in data:
                collection_data = data[collection]
            else:
                collection_data = data
            
            if isinstance(collection_data, list):
                idx = 0 if position in ['first', '1st'] else -1 if position in ['last'] else 0
                if 0 <= idx < len(collection_data):
                    item = collection_data[idx]
                    if isinstance(item, dict) and field in item:
                        return item[field]
        
        # Pattern: "count X"
        count_pattern = r'count\s+(\w+)'
        match = re.match(count_pattern, query_lower)
        if match:
            target = match.group(1)
            if isinstance(data, dict) and target in data:
                target_data = data[target]
                if isinstance(target_data, list):
                    return len(target_data)
            elif isinstance(data, list):
                return len(data)
        
        # Pattern: "all X" or "list X"
        all_pattern = r'(?:all|list)\s+(\w+)'
        match = re.match(all_pattern, query_lower)
        if match:
            target = match.group(1)
            if isinstance(data, dict) and target in data:
                return data[target]
        
        return None
    
    def _execute_query_path(self, data: Any, path: str) -> Any:
        """Execute a query path against data"""
        from jsonmind import JSONMind
        jm = JSONMind()
        return jm.query(data, path)
    
    def generate_summary(self, data: Any) -> str:
        """Generate natural language summary of JSON data"""
        stats = self._analyze_stats(data)
        
        summary_parts = []
        
        if stats['type'] == 'dict':
            summary_parts.append(f"This JSON contains a root object with {stats['total_keys']} keys.")
        elif stats['type'] == 'list':
            summary_parts.append(f"This JSON contains an array with {stats['total_items']} items.")
        
        if stats['array_count'] > 0:
            summary_parts.append(f"It includes {stats['array_count']} array(s).")
        
        if stats['object_count'] > 0:
            summary_parts.append(f"It includes {stats['object_count']} nested object(s).")
        
        if stats['sample_keys']:
            keys_str = ', '.join(stats['sample_keys'][:5])
            summary_parts.append(f"Some notable keys: {keys_str}.")
        
        return ' '.join(summary_parts)
    
    def _analyze_stats(self, data: Any) -> Dict[str, Any]:
        """Analyze JSON structure for summary"""
        stats = {
            'type': type(data).__name__,
            'total_keys': 0,
            'total_items': 0,
            'array_count': 0,
            'object_count': 0,
            'sample_keys': [],
        }
        
        if isinstance(data, list):
            stats['total_items'] = len(data)
        
        def traverse(obj: Any) -> None:
            if isinstance(obj, dict):
                stats['object_count'] += 1
                for key, value in obj.items():
                    stats['total_keys'] += 1
                    if len(stats['sample_keys']) < 20:
                        stats['sample_keys'].append(key)
                    traverse(value)
            elif isinstance(obj, list):
                stats['array_count'] += 1
                for item in obj:
                    traverse(item)
        
        traverse(data)
        return stats


def main():
    """Test AI module"""
    # Test rule-based queries
    test_data = {
        "users": [
            {"name": "Alice", "age": 28, "city": "Beijing"},
            {"name": "Bob", "age": 32, "city": "Shanghai"},
            {"name": "Carol", "age": 25, "city": "Beijing"},
        ]
    }
    
    engine = AIQueryEngine()
    
    test_queries = [
        "find users where age > 25",
        "count users",
        "all users",
        "name of first user",
    ]
    
    print("Testing AI Query Engine (Rule-Based)")
    print("=" * 50)
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        result = engine.natural_language_query(test_data, query)
        print(f"Result: {json.dumps(result, indent=2)}")


if __name__ == '__main__':
    main()
