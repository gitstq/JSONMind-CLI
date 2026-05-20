#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JSONMind TUI: Interactive Terminal User Interface
轻量级交互式终端界面模块
"""

import json
import sys
import os
from typing import Any, Dict, List, Optional
from jsonmind import JSONMind, Colors


class TUI:
    """Terminal User Interface for JSONMind"""
    
    def __init__(self):
        self.jm = JSONMind()
        self.c = Colors()
        self.data: Optional[Any] = None
        self.current_path = ""
        self.history: List[str] = []
    
    def clear_screen(self) -> None:
        """Clear terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self, title: str) -> None:
        """Print header with title"""
        width = 60
        print(f"\n{self.c.BG_BLUE}{self.c.WHITE}{self.c.BOLD}", end="")
        print(f" {title} ".center(width), end="")
        print(f"{self.c.RESET}\n")
    
    def print_menu(self, options: List[tuple]) -> None:
        """Print menu options"""
        for i, (key, desc) in enumerate(options, 1):
            print(f"  {self.c.CYAN}[{i}]{self.c.RESET} {desc}")
        print(f"  {self.c.CYAN}[0]{self.c.RESET} Exit")
    
    def get_input(self, prompt: str = "") -> str:
        """Get user input"""
        if prompt:
            print(f"{self.c.YELLOW}{prompt}{self.c.RESET}", end=" ")
        try:
            return input().strip()
        except (EOFError, KeyboardInterrupt):
            return ""
    
    def load_file(self) -> bool:
        """Load JSON file interactively"""
        self.print_header("📂 Load JSON File")
        
        filepath = self.get_input("Enter JSON file path (or '-' for stdin):")
        if not filepath:
            return False
        
        try:
            self.data = self.jm.load_json(filepath)
            self.current_path = filepath
            print(f"\n{self.c.GREEN}✅ Successfully loaded: {filepath}{self.c.RESET}")
            stats = self.jm.analyze_structure(self.data)
            print(f"  Type: {stats['type']}")
            print(f"  Total Keys: {stats['total_keys']}")
            print(f"  Max Depth: {stats['max_depth']}")
            self.get_input("\nPress Enter to continue...")
            return True
        except Exception as e:
            print(f"\n{self.c.RED}❌ Error: {e}{self.c.RESET}")
            self.get_input("Press Enter to continue...")
            return False
    
    def browse_data(self) -> None:
        """Interactive data browser"""
        if self.data is None:
            print(f"{self.c.RED}No data loaded!{self.c.RESET}")
            return
        
        current = self.data
        path_stack: List[tuple] = []
        
        while True:
            self.clear_screen()
            self.print_header(f"🔍 Data Browser - {self.current_path or 'root'}")
            
            # Display current data
            if isinstance(current, dict):
                print(f"{self.c.BOLD}Object with {len(current)} keys:{self.c.RESET}\n")
                for i, (k, v) in enumerate(current.items(), 1):
                    value_preview = self._preview_value(v)
                    print(f"  {self.c.CYAN}[{i}]{self.c.RESET} {self.c.BOLD}{k}{self.c.RESET}: {value_preview}")
                print(f"\n  {self.c.YELLOW}[b]{self.c.RESET} Back")
                print(f"  {self.c.YELLOW}[q]{self.c.RESET} Quit browser")
                
                choice = self.get_input("\nSelect option:")
                
                if choice.lower() == 'q':
                    break
                elif choice.lower() == 'b':
                    if path_stack:
                        current = path_stack.pop()[1]
                    continue
                
                try:
                    idx = int(choice) - 1
                    keys = list(current.keys())
                    if 0 <= idx < len(keys):
                        key = keys[idx]
                        value = current[key]
                        if isinstance(value, (dict, list)):
                            path_stack.append((key, current))
                            current = value
                        else:
                            print(f"\n{self.c.GREEN}Value:{self.c.RESET}")
                            print(f"  {json.dumps(value, ensure_ascii=False, indent=2)}")
                            self.get_input("\nPress Enter to continue...")
                except (ValueError, IndexError):
                    pass
            
            elif isinstance(current, list):
                print(f"{self.c.BOLD}Array with {len(current)} items:{self.c.RESET}\n")
                for i, item in enumerate(current[:50]):  # Show first 50
                    preview = self._preview_value(item, max_len=40)
                    print(f"  {self.c.CYAN}[{i}]{self.c.RESET} {preview}")
                if len(current) > 50:
                    print(f"  ... and {len(current) - 50} more items")
                
                print(f"\n  {self.c.YELLOW}[b]{self.c.RESET} Back")
                print(f"  {self.c.YELLOW}[q]{self.c.RESET} Quit browser")
                
                choice = self.get_input("\nSelect option:")
                
                if choice.lower() == 'q':
                    break
                elif choice.lower() == 'b':
                    if path_stack:
                        current = path_stack.pop()[1]
                    continue
                
                try:
                    idx = int(choice)
                    if 0 <= idx < len(current):
                        item = current[idx]
                        if isinstance(item, (dict, list)):
                            path_stack.append((f"[{idx}]", current))
                            current = item
                        else:
                            print(f"\n{self.c.GREEN}Value:{self.c.RESET}")
                            print(f"  {json.dumps(item, ensure_ascii=False, indent=2)}")
                            self.get_input("\nPress Enter to continue...")
                except (ValueError, IndexError):
                    pass
            else:
                print(f"{self.c.GREEN}Value:{self.c.RESET}")
                print(f"  {json.dumps(current, ensure_ascii=False, indent=2)}")
                self.get_input("\nPress Enter to continue...")
                if path_stack:
                    current = path_stack.pop()[1]
                else:
                    break
    
    def _preview_value(self, value: Any, max_len: int = 30) -> str:
        """Generate preview string for value"""
        if isinstance(value, dict):
            return f"{self.c.MAGENTA}Object{{{len(value)}}}{self.c.RESET}"
        elif isinstance(value, list):
            return f"{self.c.BLUE}Array[{len(value)}]{self.c.RESET}"
        elif isinstance(value, str):
            if len(value) > max_len:
                return f'"{value[:max_len]}..."'
            return f'"{value}"'
        elif isinstance(value, bool):
            return f"{self.c.YELLOW}{value}{self.c.RESET}"
        elif isinstance(value, (int, float)):
            return f"{self.c.CYAN}{value}{self.c.RESET}"
        elif value is None:
            return f"{self.c.DIM}null{self.c.RESET}"
        return str(value)
    
    def query_interface(self) -> None:
        """Interactive query interface"""
        if self.data is None:
            print(f"{self.c.RED}No data loaded!{self.c.RESET}")
            return
        
        while True:
            self.clear_screen()
            self.print_header("🔍 Query Interface")
            
            print(f"{self.c.DIM}Available paths (examples):{self.c.RESET}")
            print("  • users.0.name")
            print("  • metadata.version")
            print("  • users[0]")
            print("")
            
            query = self.get_input("Enter query path (or 'q' to quit):")
            
            if query.lower() == 'q':
                break
            
            if not query:
                continue
            
            try:
                result = self.jm.query(self.data, query)
                print(f"\n{self.c.GREEN}Result:{self.c.RESET}")
                print(json.dumps(result, ensure_ascii=False, indent=2))
            except Exception as e:
                print(f"\n{self.c.RED}Error: {e}{self.c.RESET}")
            
            self.get_input("\nPress Enter to continue...")
    
    def filter_interface(self) -> None:
        """Interactive filter interface"""
        if self.data is None:
            print(f"{self.c.RED}No data loaded!{self.c.RESET}")
            return
        
        if not isinstance(self.data, list):
            print(f"{self.c.RED}Filter only works on arrays!{self.c.RESET}")
            self.get_input("Press Enter to continue...")
            return
        
        while True:
            self.clear_screen()
            self.print_header("🔎 Filter Interface")
            
            print(f"{self.c.DIM}Available operators:{self.c.RESET}")
            print("  eq, ne, gt, gte, lt, lte, contains, startswith, endswith")
            print("")
            
            key = self.get_input("Enter key to filter (or 'q' to quit):")
            if key.lower() == 'q':
                break
            if not key:
                continue
            
            operator = self.get_input("Enter operator:")
            if not operator:
                continue
            
            value = self.get_input("Enter value:")
            
            try:
                result = self.jm.filter_by_condition(self.data, key, operator, value)
                print(f"\n{self.c.GREEN}Found {len(result)} matching items:{self.c.RESET}")
                print(json.dumps(result, ensure_ascii=False, indent=2))
            except Exception as e:
                print(f"\n{self.c.RED}Error: {e}{self.c.RESET}")
            
            self.get_input("\nPress Enter to continue...")
    
    def export_interface(self) -> None:
        """Interactive export interface"""
        if self.data is None:
            print(f"{self.c.RED}No data loaded!{self.c.RESET}")
            return
        
        self.clear_screen()
        self.print_header("📤 Export Data")
        
        print("Export formats:")
        print(f"  {self.c.CYAN}[1]{self.c.RESET} JSON (formatted)")
        print(f"  {self.c.CYAN}[2]{self.c.RESET} JSON (compact)")
        print(f"  {self.c.CYAN}[3]{self.c.RESET} YAML")
        print(f"  {self.c.CYAN}[4]{self.c.RESET} CSV (arrays only)")
        print(f"  {self.c.CYAN}[0]{self.c.RESET} Cancel")
        
        choice = self.get_input("\nSelect format:")
        
        if choice == '0':
            return
        
        filepath = self.get_input("Enter output file path:")
        if not filepath:
            return
        
        try:
            if choice == '1':
                self.jm.save_json(self.data, filepath)
            elif choice == '2':
                self.jm.save_json(self.data, filepath, compact=True)
            elif choice == '3':
                yaml_content = self.jm._to_yaml(self.data)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(yaml_content)
            elif choice == '4':
                self.jm.to_csv(self.data, filepath)
            
            print(f"\n{self.c.GREEN}✅ Exported to: {filepath}{self.c.RESET}")
        except Exception as e:
            print(f"\n{self.c.RED}❌ Error: {e}{self.c.RESET}")
        
        self.get_input("\nPress Enter to continue...")
    
    def run(self) -> None:
        """Run TUI main loop"""
        while True:
            self.clear_screen()
            self.print_header("🧠 JSONMind-CLI Interactive Mode")
            
            if self.data is not None:
                stats = self.jm.analyze_structure(self.data)
                print(f"{self.c.GREEN}📄 Loaded:{self.c.RESET} {self.current_path or 'stdin'}")
                print(f"   Type: {stats['type']} | Keys: {stats['total_keys']} | Depth: {stats['max_depth']}")
                print("")
            
            options = [
                ("1", "📂 Load JSON File"),
                ("2", "🔍 Browse Data"),
                ("3", "🔎 Query Data"),
                ("4", "🔎 Filter Data"),
                ("5", "📊 Analyze Structure"),
                ("6", "📤 Export Data"),
            ]
            
            if self.data is None:
                options = [options[0]]  # Only show load option
            
            self.print_menu(options)
            
            choice = self.get_input("\nSelect option:")
            
            if choice == '0':
                print(f"\n{self.c.GREEN}Goodbye! 👋{self.c.RESET}\n")
                break
            elif choice == '1':
                self.load_file()
            elif choice == '2' and self.data is not None:
                self.browse_data()
            elif choice == '3' and self.data is not None:
                self.query_interface()
            elif choice == '4' and self.data is not None:
                self.filter_interface()
            elif choice == '5' and self.data is not None:
                self.clear_screen()
                self.print_header("📊 Structure Analysis")
                stats = self.jm.analyze_structure(self.data)
                self.jm.print_analysis(stats)
                self.get_input("\nPress Enter to continue...")
            elif choice == '6' and self.data is not None:
                self.export_interface()


def main():
    """TUI entry point"""
    tui = TUI()
    try:
        tui.run()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.GREEN}Goodbye! 👋{Colors.RESET}\n")
        sys.exit(0)


if __name__ == '__main__':
    main()
