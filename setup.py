#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JSONMind-CLI Setup Script
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding='utf-8') if readme_path.exists() else ""

setup(
    name="jsonmind-cli",
    version="1.0.0",
    author="JSONMind Team",
    author_email="hello@jsonmind.dev",
    description="🧠 AI-Powered Intelligent JSON Processing & Analysis Engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gitstq/JSONMind-CLI",
    py_modules=["jsonmind", "tui", "ai_module"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "jsonmind=jsonmind:main",
            "jsonmind-tui=tui:main",
        ],
    },
    keywords="json, cli, ai, data-processing, terminal, tui, query, filter, transform",
    project_urls={
        "Bug Reports": "https://github.com/gitstq/JSONMind-CLI/issues",
        "Source": "https://github.com/gitstq/JSONMind-CLI",
        "Documentation": "https://github.com/gitstq/JSONMind-CLI#readme",
    },
)
