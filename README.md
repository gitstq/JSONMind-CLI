# 🧠 JSONMind-CLI

<div align="center">

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-black.svg)](https://github.com/psf/black)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-zero-orange.svg)](requirements.txt)

**AI-Powered Intelligent JSON Processing & Analysis Engine**

[English](#english) | [简体中文](#简体中文) | [繁體中文](#繁體中文)

</div>

---

## English

### 🎉 Project Introduction

**JSONMind-CLI** is an AI-powered intelligent JSON data processing and analysis engine designed for developers who work with JSON data daily. It transforms complex JSON operations into simple, intuitive commands.

**Core Value Propositions:**
- 🚀 **Zero Dependencies**: Pure Python implementation with no external dependencies
- 🧠 **AI-Powered**: Natural language query support for intuitive data exploration
- 🎯 **Developer-Friendly**: Replaces complex `jq` syntax with simple commands
- 📊 **Interactive TUI**: Beautiful terminal interface for data browsing
- 🔒 **Privacy-First**: Local processing, no data leaves your machine

**Problems Solved:**
1. Complex `jq` syntax with steep learning curve
2. Difficulty understanding large JSON structures
3. Tedious JSON transformation scripts
4. Lack of visual JSON exploration tools

### ✨ Core Features

| Feature | Description | Command |
|---------|-------------|---------|
| 🔍 **Smart Analysis** | Deep structure analysis with statistics | `jsonmind analyze data.json` |
| 🗣️ **Natural Language** | Query JSON using plain English | `jsonmind ask "find users over 25"` |
| 🔎 **Path Query** | Dot-notation path queries | `jsonmind query data.json users.0.name` |
| 🔀 **Smart Filter** | Filter arrays with conditions | `jsonmind filter data.json age gt 25` |
| 📉 **Flatten** | Flatten nested structures | `jsonmind flatten data.json` |
| 📤 **Export** | Convert to CSV, YAML, Tree view | `jsonmind tocsv data.json output.csv` |
| ✅ **Validate** | JSON validation with detailed errors | `jsonmind validate data.json` |
| 🖥️ **TUI Mode** | Interactive terminal interface | `jsonmind-tui` |

### 🚀 Quick Start

#### Installation

```bash
# Option 1: Direct install
curl -fsSL https://raw.githubusercontent.com/gitstq/JSONMind-CLI/main/install.sh | bash

# Option 2: Clone and install
git clone https://github.com/gitstq/JSONMind-CLI.git
cd JSONMind-CLI
python3 jsonmind.py --version
```

#### Requirements

- **Python**: 3.8 or higher
- **OS**: Linux, macOS, Windows (with Python)
- **Dependencies**: None (zero dependencies!)

#### Basic Usage

```bash
# Generate sample data
jsonmind sample

# Analyze JSON structure
jsonmind analyze data.json

# Query specific path
jsonmind query data.json users.0.name

# Filter data
jsonmind query data.json users | jsonmind filter - age gt 25

# Convert to CSV
jsonmind query data.json users | jsonmind tocsv - output.csv

# Interactive TUI mode
python3 tui.py
```

### 📖 Detailed Usage Guide

#### 1. Structure Analysis

```bash
jsonmind analyze data.json
```

Output:
```
📊 JSON Structure Analysis
==================================================
  Type: dict
  Max Depth: 4
  Total Keys: 35

Type Distribution:
  Objects: 8
  Arrays: 4
  Strings: 22
  Numbers: 10
```

#### 2. Path Queries

```bash
# Dot notation
jsonmind query data.json users.0.profile.location

# Array indexing
jsonmind query data.json users.1

# Pipe to filter
cat data.json | jsonmind query - users | jsonmind filter - active eq true
```

#### 3. Filtering

Supported operators: `eq`, `ne`, `gt`, `gte`, `lt`, `lte`, `contains`, `startswith`, `endswith`

```bash
# Filter by age
jsonmind filter users.json age gt 25

# Filter by string contains
jsonmind filter users.json name contains "Alice"

# Chain with query
jsonmind query data.json users | jsonmind filter - role eq admin
```

#### 4. Format Conversion

```bash
# Tree view
jsonmind format data.json --type tree

# YAML
jsonmind format data.json --type yaml

# Compact JSON
jsonmind format data.json --type compact
```

#### 5. Interactive TUI

Launch the interactive mode:

```bash
python3 tui.py
```

Features:
- 📂 Load JSON files
- 🔍 Browse data structure
- 🔎 Query with natural language
- 📤 Export to multiple formats
- 📊 Real-time analysis

### 💡 Design Philosophy

**Why JSONMind?**

1. **Simplicity Over Complexity**: We believe JSON manipulation should be accessible to everyone, not just `jq` experts.

2. **Zero Dependencies**: No pip install nightmares. Just Python and go.

3. **AI-Enhanced, Not AI-Required**: Core functionality works offline. AI features are optional enhancements.

4. **Terminal-Native**: Built for developers who live in the terminal.

### 📦 Packaging & Deployment

#### Build Executable

```bash
# Install pyinstaller
pip3 install pyinstaller

# Build standalone executable
pyinstaller --onefile jsonmind.py --name jsonmind

# Build TUI version
pyinstaller --onefile tui.py --name jsonmind-tui
```

#### Distribution

```bash
# Create distribution package
python3 setup.py sdist bdist_wheel

# Install from source
pip3 install .
```

### 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md).

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 简体中文

### 🎉 项目介绍

**JSONMind-CLI** 是一款AI驱动的智能JSON数据处理与分析引擎，专为日常需要处理JSON数据的开发者设计。它将复杂的JSON操作转化为简单直观的命令。

**核心价值主张：**
- 🚀 **零依赖**：纯Python实现，无需任何外部依赖
- 🧠 **AI驱动**：支持自然语言查询，直观探索数据
- 🎯 **开发者友好**：用简单命令替代复杂的`jq`语法
- 📊 **交互式TUI**：美观的终端界面浏览数据
- 🔒 **隐私优先**：本地处理，数据不会离开您的机器

**解决的问题：**
1. `jq`语法复杂，学习曲线陡峭
2. 难以理解大型JSON结构
3. JSON转换脚本编写繁琐
4. 缺乏可视化JSON探索工具

### ✨ 核心特性

| 特性 | 描述 | 命令 |
|------|------|------|
| 🔍 **智能分析** | 深度结构分析与统计 | `jsonmind analyze data.json` |
| 🗣️ **自然语言** | 用自然英语查询JSON | `jsonmind ask "find users over 25"` |
| 🔎 **路径查询** | 点符号路径查询 | `jsonmind query data.json users.0.name` |
| 🔀 **智能过滤** | 条件过滤数组 | `jsonmind filter data.json age gt 25` |
| 📉 **扁平化** | 扁平化嵌套结构 | `jsonmind flatten data.json` |
| 📤 **导出** | 转换为CSV、YAML、树形视图 | `jsonmind tocsv data.json output.csv` |
| ✅ **验证** | JSON验证与详细错误 | `jsonmind validate data.json` |
| 🖥️ **TUI模式** | 交互式终端界面 | `jsonmind-tui` |

### 🚀 快速开始

#### 安装

```bash
# 方式1：直接安装
curl -fsSL https://raw.githubusercontent.com/gitstq/JSONMind-CLI/main/install.sh | bash

# 方式2：克隆并安装
git clone https://github.com/gitstq/JSONMind-CLI.git
cd JSONMind-CLI
python3 jsonmind.py --version
```

#### 环境要求

- **Python**：3.8 或更高版本
- **操作系统**：Linux、macOS、Windows（需安装Python）
- **依赖项**：无（零依赖！）

#### 基本用法

```bash
# 生成示例数据
jsonmind sample

# 分析JSON结构
jsonmind analyze data.json

# 查询特定路径
jsonmind query data.json users.0.name

# 过滤数据
jsonmind query data.json users | jsonmind filter - age gt 25

# 转换为CSV
jsonmind query data.json users | jsonmind tocsv - output.csv

# 交互式TUI模式
python3 tui.py
```

### 📖 详细使用指南

#### 1. 结构分析

```bash
jsonmind analyze data.json
```

输出：
```
📊 JSON结构分析
==================================================
  类型: dict
  最大深度: 4
  总键数: 35

类型分布：
  对象: 8
  数组: 4
  字符串: 22
  数字: 10
```

#### 2. 路径查询

```bash
# 点符号表示法
jsonmind query data.json users.0.profile.location

# 数组索引
jsonmind query data.json users.1

# 管道到过滤器
cat data.json | jsonmind query - users | jsonmind filter - active eq true
```

#### 3. 过滤

支持的运算符：`eq`、`ne`、`gt`、`gte`、`lt`、`lte`、`contains`、`startswith`、`endswith`

```bash
# 按年龄过滤
jsonmind filter users.json age gt 25

# 按字符串包含过滤
jsonmind filter users.json name contains "Alice"

# 与查询链式调用
jsonmind query data.json users | jsonmind filter - role eq admin
```

#### 4. 格式转换

```bash
# 树形视图
jsonmind format data.json --type tree

# YAML
jsonmind format data.json --type yaml

# 紧凑JSON
jsonmind format data.json --type compact
```

#### 5. 交互式TUI

启动交互模式：

```bash
python3 tui.py
```

功能：
- 📂 加载JSON文件
- 🔍 浏览数据结构
- 🔎 使用自然语言查询
- 📤 导出为多种格式
- 📊 实时分析

### 💡 设计理念

**为什么选择JSONMind？**

1. **简洁优于复杂**：我们相信JSON操作应该对每个人都可访问，而不仅仅是`jq`专家。

2. **零依赖**：没有pip安装的噩梦。只需Python即可运行。

3. **AI增强，非AI必需**：核心功能离线工作。AI功能是可选增强。

4. **原生终端**：为生活在终端中的开发者构建。

### 📦 打包与部署

#### 构建可执行文件

```bash
# 安装pyinstaller
pip3 install pyinstaller

# 构建独立可执行文件
pyinstaller --onefile jsonmind.py --name jsonmind

# 构建TUI版本
pyinstaller --onefile tui.py --name jsonmind-tui
```

#### 分发

```bash
# 创建分发包
python3 setup.py sdist bdist_wheel

# 从源代码安装
pip3 install .
```

### 🤝 贡献指南

我们欢迎贡献！请参阅我们的[贡献指南](CONTRIBUTING.md)。

1. Fork 本仓库
2. 创建您的功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交您的更改 (`git commit -m 'feat: 添加惊人功能'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 打开 Pull Request

### 📄 开源协议

本项目采用 MIT 许可证 - 详情请参阅 [LICENSE](LICENSE) 文件。

---

## 繁體中文

### 🎉 專案介紹

**JSONMind-CLI** 是一款AI驅動的智能JSON資料處理與分析引擎，專為日常需要處理JSON資料的開發者設計。它將複雜的JSON操作轉化為簡單直觀的命令。

**核心價值主張：**
- 🚀 **零依賴**：純Python實現，無需任何外部依賴
- 🧠 **AI驅動**：支援自然語言查詢，直觀探索資料
- 🎯 **開發者友善**：用簡單命令替代複雜的`jq`語法
- 📊 **互動式TUI**：美觀的終端介面瀏覽資料
- 🔒 **隱私優先**：本地處理，資料不會離開您的機器

**解決的問題：**
1. `jq`語法複雜，學習曲線陡峭
2. 難以理解大型JSON結構
3. JSON轉換腳本編寫繁瑣
4. 缺乏可視化JSON探索工具

### ✨ 核心特性

| 特性 | 描述 | 命令 |
|------|------|------|
| 🔍 **智能分析** | 深度結構分析與統計 | `jsonmind analyze data.json` |
| 🗣️ **自然語言** | 用自然英語查詢JSON | `jsonmind ask "find users over 25"` |
| 🔎 **路徑查詢** | 點符號路徑查詢 | `jsonmind query data.json users.0.name` |
| 🔀 **智能過濾** | 條件過濾陣列 | `jsonmind filter data.json age gt 25` |
| 📉 **扁平化** | 扁平化嵌套結構 | `jsonmind flatten data.json` |
| 📤 **匯出** | 轉換為CSV、YAML、樹形視圖 | `jsonmind tocsv data.json output.csv` |
| ✅ **驗證** | JSON驗證與詳細錯誤 | `jsonmind validate data.json` |
| 🖥️ **TUI模式** | 互動式終端介面 | `jsonmind-tui` |

### 🚀 快速開始

#### 安裝

```bash
# 方式1：直接安裝
curl -fsSL https://raw.githubusercontent.com/gitstq/JSONMind-CLI/main/install.sh | bash

# 方式2：克隆並安裝
git clone https://github.com/gitstq/JSONMind-CLI.git
cd JSONMind-CLI
python3 jsonmind.py --version
```

#### 環境要求

- **Python**：3.8 或更高版本
- **作業系統**：Linux、macOS、Windows（需安裝Python）
- **依賴項**：無（零依賴！）

#### 基本用法

```bash
# 生成範例資料
jsonmind sample

# 分析JSON結構
jsonmind analyze data.json

# 查詢特定路徑
jsonmind query data.json users.0.name

# 過濾資料
jsonmind query data.json users | jsonmind filter - age gt 25

# 轉換為CSV
jsonmind query data.json users | jsonmind tocsv - output.csv

# 互動式TUI模式
python3 tui.py
```

### 📖 詳細使用指南

#### 1. 結構分析

```bash
jsonmind analyze data.json
```

輸出：
```
📊 JSON結構分析
==================================================
  類型: dict
  最大深度: 4
  總鍵數: 35

類型分布：
  物件: 8
  陣列: 4
  字串: 22
  數字: 10
```

#### 2. 路徑查詢

```bash
# 點符號表示法
jsonmind query data.json users.0.profile.location

# 陣列索引
jsonmind query data.json users.1

# 管道到過濾器
cat data.json | jsonmind query - users | jsonmind filter - active eq true
```

#### 3. 過濾

支援的運算子：`eq`、`ne`、`gt`、`gte`、`lt`、`lte`、`contains`、`startswith`、`endswith`

```bash
# 按年齡過濾
jsonmind filter users.json age gt 25

# 按字串包含過濾
jsonmind filter users.json name contains "Alice"

# 與查詢鏈式呼叫
jsonmind query data.json users | jsonmind filter - role eq admin
```

#### 4. 格式轉換

```bash
# 樹形視圖
jsonmind format data.json --type tree

# YAML
jsonmind format data.json --type yaml

# 緊湊JSON
jsonmind format data.json --type compact
```

#### 5. 互動式TUI

啟動互動模式：

```bash
python3 tui.py
```

功能：
- 📂 載入JSON檔案
- 🔍 瀏覽資料結構
- 🔎 使用自然語言查詢
- 📤 匯出為多種格式
- 📊 即時分析

### 💡 設計理念

**為什麼選擇JSONMind？**

1. **簡潔優於複雜**：我們相信JSON操作應該對每個人都可訪問，而不僅僅是`jq`專家。

2. **零依賴**：沒有pip安裝的噩夢。只需Python即可運行。

3. **AI增強，非AI必需**：核心功能離線工作。AI功能是可選增強。

4. **原生終端**：為生活在終端中的開發者構建。

### 📦 打包與部署

#### 構建可執行檔

```bash
# 安裝pyinstaller
pip3 install pyinstaller

# 構建獨立可執行檔
pyinstaller --onefile jsonmind.py --name jsonmind

# 構建TUI版本
pyinstaller --onefile tui.py --name jsonmind-tui
```

#### 分發

```bash
# 創建分發包
python3 setup.py sdist bdist_wheel

# 從原始碼安裝
pip3 install .
```

### 🤝 貢獻指南

我們歡迎貢獻！請參閱我們的[貢獻指南](CONTRIBUTING.md)。

1. Fork 本倉庫
2. 創建您的功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交您的更改 (`git commit -m 'feat: 添加驚人功能'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 打開 Pull Request

### 📄 開源協議

本專案採用 MIT 許可證 - 詳情請參閱 [LICENSE](LICENSE) 檔案。

---

<div align="center">

**Made with ❤️ by the JSONMind Team**

[⭐ Star us on GitHub](https://github.com/gitstq/JSONMind-CLI) | [🐛 Report Bug](https://github.com/gitstq/JSONMind-CLI/issues) | [💡 Request Feature](https://github.com/gitstq/JSONMind-CLI/issues)

</div>
