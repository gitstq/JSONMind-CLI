#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JSONMind-CLI: AI-Powered Intelligent JSON Data Processing & Analysis Engine
轻量级AI驱动JSON智能处理与分析引擎

Author: JSONMind Team
License: MIT
Version: 1.0.0
"""

import json
import sys
import os
import re
import argparse
import csv
import io
from typing import Any, Dict, List, Optional, Union, Iterator
from pathlib import Path
from collections import Counter

__version__ = "1.0.0"
__author__ = "JSONMind Team"


class Colors:
    """Terminal color codes"""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BG_BLUE = '\033[44m'


class JSONMind:
    """Core JSON processing engine"""
    
    def __init__(self, use_color: bool = True):
        self.use_color = use_color and sys.stdout.isatty()
        self.c = Colors() if self.use_color else type('NoColor', (), {
            k: '' for k in Colors.__dict__ if not k.startswith('_')
        })()
    
    def colorize(self, text: str, color: str) -> str:
        """Apply color to text"""
        if not self.use_color:
            return text
        return f"{getattr(self.c, color, '')}{text}{self.c.RESET}"
    
    def load_json(self, source: Union[str, Path]) -> Any:
        """Load JSON from file or string"""
        source_str = str(source).strip()
        
        # Try to load as file path first
        if os.path.isfile(source_str):
            with open(source_str, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # Try to parse as JSON string
        try:
            return json.loads(source_str)
        except json.JSONDecodeError:
            pass
        
        # Try to read from stdin if source is '-'
        if source_str == '-':
            return json.load(sys.stdin)
        
        raise ValueError(f"Cannot load JSON from: {source}")
    
    def save_json(self, data: Any, output: Optional[str] = None, 
                  indent: int = 2, compact: bool = False) -> str:
        """Save JSON to file or return as string"""
        if compact:
            json_str = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
        else:
            json_str = json.dumps(data, ensure_ascii=False, indent=indent)
        
        if output:
            with open(output, 'w', encoding='utf-8') as f:
                f.write(json_str)
            return f"Saved to {output}"
        return json_str
    
    def analyze_structure(self, data: Any, max_depth: int = 10) -> Dict[str, Any]:
        """Analyze JSON structure and return statistics"""
        stats = {
            'type': type(data).__name__,
            'total_keys': 0,
            'max_depth': 0,
            'types_found': set(),
            'array_count': 0,
            'object_count': 0,
            'string_count': 0,
            'number_count': 0,
            'boolean_count': 0,
            'null_count': 0,
            'sample_keys': [],
        }
        
        def traverse(obj: Any, depth: int = 0, path: str = '') -> None:
            if depth > max_depth:
                return
            
            stats['max_depth'] = max(stats['max_depth'], depth)
            obj_type = type(obj).__name__
            stats['types_found'].add(obj_type)
            
            if isinstance(obj, dict):
                stats['object_count'] += 1
                for key, value in obj.items():
                    stats['total_keys'] += 1
                    if len(stats['sample_keys']) < 20:
                        stats['sample_keys'].append(f"{path}.{key}" if path else key)
                    traverse(value, depth + 1, f"{path}.{key}" if path else key)
            elif isinstance(obj, list):
                stats['array_count'] += 1
                for i, item in enumerate(obj[:100]):  # Limit to first 100 items
                    traverse(item, depth + 1, f"{path}[{i}]")
            elif isinstance(obj, str):
                stats['string_count'] += 1
            elif isinstance(obj, (int, float)):
                stats['number_count'] += 1
            elif isinstance(obj, bool):
                stats['boolean_count'] += 1
            elif obj is None:
                stats['null_count'] += 1
        
        traverse(data)
        stats['types_found'] = list(stats['types_found'])
        return stats
    
    def query(self, data: Any, query_str: str) -> Any:
        """Query JSON using simple path syntax"""
        # Handle array indexing
        if isinstance(data, list) and query_str.isdigit():
            idx = int(query_str)
            return data[idx] if 0 <= idx < len(data) else None
        
        # Handle dot notation path
        if '.' in query_str:
            parts = query_str.split('.')
            result = data
            for part in parts:
                if isinstance(result, dict):
                    result = result.get(part)
                elif isinstance(result, list) and part.isdigit():
                    idx = int(part)
                    result = result[idx] if 0 <= idx < len(result) else None
                else:
                    return None
            return result
        
        # Simple key lookup
        if isinstance(data, dict):
            return data.get(query_str)
        
        return None
    
    def filter_by_condition(self, data: Any, key: str, operator: str, value: str) -> List[Any]:
        """Filter array of objects by condition"""
        if not isinstance(data, list):
            return []
        
        results = []
        for item in data:
            if not isinstance(item, dict):
                continue
            
            item_value = item.get(key)
            
            # Try to convert value to number for comparison
            try:
                if '.' in value:
                    compare_value = float(value)
                else:
                    compare_value = int(value)
                if isinstance(item_value, str):
                    item_value = float(item_value) if '.' in item_value else int(item_value)
            except (ValueError, TypeError):
                compare_value = value
            
            match = False
            if operator == 'eq' or operator == '==':
                match = item_value == compare_value
            elif operator == 'ne' or operator == '!=':
                match = item_value != compare_value
            elif operator == 'gt' or operator == '>':
                match = item_value > compare_value if isinstance(item_value, (int, float)) else False
            elif operator == 'gte' or operator == '>=':
                match = item_value >= compare_value if isinstance(item_value, (int, float)) else False
            elif operator == 'lt' or operator == '<':
                match = item_value < compare_value if isinstance(item_value, (int, float)) else False
            elif operator == 'lte' or operator == '<=':
                match = item_value <= compare_value if isinstance(item_value, (int, float)) else False
            elif operator == 'contains':
                match = compare_value in str(item_value) if item_value is not None else False
            elif operator == 'startswith':
                match = str(item_value).startswith(str(compare_value)) if item_value is not None else False
            elif operator == 'endswith':
                match = str(item_value).endswith(str(compare_value)) if item_value is not None else False
            
            if match:
                results.append(item)
        
        return results
    
    def to_csv(self, data: Any, output: Optional[str] = None) -> str:
        """Convert JSON array to CSV"""
        if not isinstance(data, list) or len(data) == 0:
            raise ValueError("Data must be a non-empty array")
        
        # Get all unique keys from all objects
        keys = set()
        for item in data:
            if isinstance(item, dict):
                keys.update(item.keys())
        keys = sorted(keys)
        
        output_buffer = io.StringIO()
        writer = csv.DictWriter(output_buffer, fieldnames=keys)
        writer.writeheader()
        
        for item in data:
            if isinstance(item, dict):
                # Convert nested objects to JSON strings
                row = {}
                for k, v in item.items():
                    if isinstance(v, (dict, list)):
                        row[k] = json.dumps(v, ensure_ascii=False)
                    else:
                        row[k] = v
                writer.writerow(row)
        
        csv_str = output_buffer.getvalue()
        
        if output:
            with open(output, 'w', encoding='utf-8', newline='') as f:
                f.write(csv_str)
            return f"Saved to {output}"
        return csv_str
    
    def flatten(self, data: Any, separator: str = '.', prefix: str = '') -> Dict[str, Any]:
        """Flatten nested JSON structure"""
        result = {}
        
        if isinstance(data, dict):
            for key, value in data.items():
                new_key = f"{prefix}{separator}{key}" if prefix else key
                if isinstance(value, (dict, list)):
                    result.update(self.flatten(value, separator, new_key))
                else:
                    result[new_key] = value
        elif isinstance(data, list):
            for i, item in enumerate(data):
                new_key = f"{prefix}[{i}]" if prefix else f"[{i}]"
                if isinstance(item, (dict, list)):
                    result.update(self.flatten(item, separator, new_key))
                else:
                    result[new_key] = item
        else:
            result[prefix] = data
        
        return result
    
    def find_duplicates(self, data: Any, key: Optional[str] = None) -> Dict[Any, List[int]]:
        """Find duplicate values in array"""
        if not isinstance(data, list):
            return {}
        
        value_indices: Dict[Any, List[int]] = {}
        
        for i, item in enumerate(data):
            if key and isinstance(item, dict):
                value = item.get(key)
            else:
                value = json.dumps(item, sort_keys=True) if isinstance(item, (dict, list)) else item
            
            if value not in value_indices:
                value_indices[value] = []
            value_indices[value].append(i)
        
        # Return only duplicates
        return {k: v for k, v in value_indices.items() if len(v) > 1}
    
    def validate_schema(self, data: Any, schema_type: str = "basic") -> List[str]:
        """Validate JSON against basic schema rules"""
        errors = []
        
        if schema_type == "basic":
            # Check for common issues
            def check(obj: Any, path: str = "root") -> None:
                if isinstance(obj, dict):
                    for k, v in obj.items():
                        if not k:
                            errors.append(f"Empty key at {path}")
                        if isinstance(v, float):
                            if v != v:  # NaN check
                                errors.append(f"NaN value at {path}.{k}")
                            elif v == float('inf') or v == float('-inf'):
                                errors.append(f"Infinity value at {path}.{k}")
                        check(v, f"{path}.{k}")
                elif isinstance(obj, list):
                    for i, v in enumerate(obj):
                        check(v, f"{path}[{i}]")
            
            check(data)
        
        return errors
    
    def format_output(self, data: Any, format_type: str = "json") -> str:
        """Format output in various formats"""
        if format_type == "json":
            return json.dumps(data, ensure_ascii=False, indent=2)
        elif format_type == "compact":
            return json.dumps(data, ensure_ascii=False, separators=(',', ':'))
        elif format_type == "yaml":
            return self._to_yaml(data)
        elif format_type == "tree":
            return self._to_tree(data)
        else:
            return str(data)
    
    def _to_yaml(self, data: Any, indent: int = 0) -> str:
        """Simple YAML conversion"""
        lines = []
        prefix = "  " * indent
        
        if isinstance(data, dict):
            for k, v in data.items():
                if isinstance(v, (dict, list)):
                    lines.append(f"{prefix}{k}:")
                    lines.append(self._to_yaml(v, indent + 1))
                else:
                    if isinstance(v, str) and (':' in v or v.startswith('-')):
                        lines.append(f"{prefix}{k}: \"{v}\"")
                    else:
                        lines.append(f"{prefix}{k}: {v}")
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, (dict, list)):
                    lines.append(f"{prefix}-")
                    lines.append(self._to_yaml(item, indent + 1))
                else:
                    lines.append(f"{prefix}- {item}")
        else:
            lines.append(f"{prefix}{data}")
        
        return "\n".join(lines)
    
    def _to_tree(self, data: Any, prefix: str = "", is_last: bool = True) -> str:
        """Convert to tree view"""
        lines = []
        connector = "└── " if is_last else "├── "
        
        if isinstance(data, dict):
            items = list(data.items())
            for i, (k, v) in enumerate(items):
                is_last_item = i == len(items) - 1
                lines.append(f"{prefix}{connector}{k}")
                new_prefix = prefix + ("    " if is_last else "│   ")
                lines.append(self._to_tree(v, new_prefix, is_last_item))
        elif isinstance(data, list):
            for i, item in enumerate(data[:20]):  # Limit to first 20
                is_last_item = i == min(len(data), 20) - 1
                lines.append(f"{prefix}{connector}[{i}]")
                new_prefix = prefix + ("    " if is_last else "│   ")
                lines.append(self._to_tree(item, new_prefix, is_last_item))
            if len(data) > 20:
                lines.append(f"{prefix}{connector}... ({len(data) - 20} more items)")
        else:
            value_str = str(data)
            if len(value_str) > 50:
                value_str = value_str[:50] + "..."
            lines.append(f"{prefix}{connector}{value_str}")
        
        return "\n".join(lines)
    
    def print_analysis(self, stats: Dict[str, Any]) -> None:
        """Print formatted analysis results"""
        print(f"\n{self.colorize('📊 JSON Structure Analysis', 'BOLD')}")
        print("=" * 50)
        print(f"  {self.colorize('Type:', 'CYAN')} {stats['type']}")
        print(f"  {self.colorize('Max Depth:', 'CYAN')} {stats['max_depth']}")
        print(f"  {self.colorize('Total Keys:', 'CYAN')} {stats['total_keys']}")
        print(f"\n{self.colorize('Type Distribution:', 'YELLOW')}")
        print(f"  Objects: {stats['object_count']}")
        print(f"  Arrays: {stats['array_count']}")
        print(f"  Strings: {stats['string_count']}")
        print(f"  Numbers: {stats['number_count']}")
        print(f"  Booleans: {stats['boolean_count']}")
        print(f"  Nulls: {stats['null_count']}")
        
        if stats['sample_keys']:
            print(f"\n{self.colorize('Sample Keys:', 'GREEN')}")
            for key in stats['sample_keys'][:10]:
                print(f"  • {key}")


def create_sample_data() -> Dict[str, Any]:
    """Create sample JSON data for testing"""
    return {
        "users": [
            {
                "id": 1,
                "name": "Alice Chen",
                "email": "alice@example.com",
                "age": 28,
                "role": "admin",
                "active": True,
                "tags": ["developer", "backend"],
                "profile": {
                    "location": "Beijing",
                    "department": "Engineering"
                }
            },
            {
                "id": 2,
                "name": "Bob Wang",
                "email": "bob@example.com",
                "age": 32,
                "role": "user",
                "active": True,
                "tags": ["designer"],
                "profile": {
                    "location": "Shanghai",
                    "department": "Design"
                }
            },
            {
                "id": 3,
                "name": "Carol Liu",
                "email": "carol@example.com",
                "age": 25,
                "role": "user",
                "active": False,
                "tags": ["developer", "frontend"],
                "profile": {
                    "location": "Shenzhen",
                    "department": "Engineering"
                }
            }
        ],
        "metadata": {
            "version": "1.0.0",
            "total": 3,
            "generated_at": "2025-05-20T10:00:00Z"
        }
    }


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        prog='jsonmind',
        description='🧠 JSONMind-CLI: AI-Powered Intelligent JSON Processing Engine',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  jsonmind analyze data.json              Analyze JSON structure
  jsonmind query data.json users.0.name   Query specific path
  jsonmind filter data.json age gt 25     Filter by condition
  jsonmind flatten data.json              Flatten nested structure
  jsonmind tocsv data.json output.csv     Convert to CSV
  jsonmind validate data.json             Validate JSON
  jsonmind sample                         Generate sample data
        """
    )
    
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    parser.add_argument('--no-color', action='store_true', help='Disable colored output')
    parser.add_argument('-o', '--output', help='Output file path')
    parser.add_argument('-c', '--compact', action='store_true', help='Compact JSON output')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze JSON structure')
    analyze_parser.add_argument('source', help='JSON file path or "-" for stdin')
    
    # Query command
    query_parser = subparsers.add_parser('query', help='Query JSON by path')
    query_parser.add_argument('source', help='JSON file path or "-" for stdin')
    query_parser.add_argument('path', help='Query path (e.g., users.0.name)')
    
    # Filter command
    filter_parser = subparsers.add_parser('filter', help='Filter array by condition')
    filter_parser.add_argument('source', help='JSON file path or "-" for stdin')
    filter_parser.add_argument('key', help='Key to filter on')
    filter_parser.add_argument('operator', help='Operator (eq, ne, gt, lt, gte, lte, contains)')
    filter_parser.add_argument('value', nargs='+', help='Value to compare (use quotes for values with spaces)')
    
    # Flatten command
    flatten_parser = subparsers.add_parser('flatten', help='Flatten nested JSON')
    flatten_parser.add_argument('source', help='JSON file path or "-" for stdin')
    flatten_parser.add_argument('-s', '--separator', default='.', help='Key separator')
    
    # ToCSV command
    csv_parser = subparsers.add_parser('tocsv', help='Convert JSON to CSV')
    csv_parser.add_argument('source', help='JSON file path or "-" for stdin')
    csv_parser.add_argument('output', nargs='?', help='Output CSV file')
    
    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate JSON')
    validate_parser.add_argument('source', help='JSON file path or "-" for stdin')
    
    # Format command
    format_parser = subparsers.add_parser('format', help='Format JSON output')
    format_parser.add_argument('source', help='JSON file path or "-" for stdin')
    format_parser.add_argument('-t', '--type', default='json', 
                               choices=['json', 'compact', 'yaml', 'tree'],
                               help='Output format')
    
    # Sample command
    sample_parser = subparsers.add_parser('sample', help='Generate sample JSON data')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(0)
    
    # Initialize JSONMind
    jm = JSONMind(use_color=not args.no_color)
    
    try:
        if args.command == 'sample':
            data = create_sample_data()
            print(jm.save_json(data, args.output, compact=args.compact))
            return
        
        # Load JSON data
        data = jm.load_json(args.source)
        
        if args.command == 'analyze':
            stats = jm.analyze_structure(data)
            jm.print_analysis(stats)
        
        elif args.command == 'query':
            result = jm.query(data, args.path)
            print(jm.save_json(result, args.output, compact=args.compact))
        
        elif args.command == 'filter':
            # Join value parts if it's a list (nargs='+')
            value = ' '.join(args.value) if isinstance(args.value, list) else args.value
            result = jm.filter_by_condition(data, args.key, args.operator, value)
            print(jm.save_json(result, args.output, compact=args.compact))
        
        elif args.command == 'flatten':
            result = jm.flatten(data, args.separator)
            print(jm.save_json(result, args.output, compact=args.compact))
        
        elif args.command == 'tocsv':
            result = jm.to_csv(data, args.output)
            print(result)
        
        elif args.command == 'validate':
            errors = jm.validate_schema(data)
            if errors:
                print(jm.colorize("❌ Validation Errors:", "RED"))
                for error in errors:
                    print(f"  • {error}")
                sys.exit(1)
            else:
                print(jm.colorize("✅ JSON is valid!", "GREEN"))
        
        elif args.command == 'format':
            formatted = jm.format_output(data, args.type)
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(formatted)
                print(f"Saved to {args.output}")
            else:
                print(formatted)
    
    except FileNotFoundError:
        print(f"{jm.colorize('Error:', 'RED')} File not found: {args.source}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"{jm.colorize('Error:', 'RED')} Invalid JSON: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"{jm.colorize('Error:', 'RED')} {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
