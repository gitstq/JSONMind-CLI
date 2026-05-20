#!/bin/bash
# JSONMind-CLI Installation Script
# 轻量级AI驱动JSON智能处理引擎安装脚本

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
INSTALL_DIR="/usr/local/bin"
REPO_URL="https://github.com/gitstq/JSONMind-CLI"
VERSION="1.0.0"

echo -e "${BLUE}🧠 JSONMind-CLI Installation Script${NC}"
echo -e "${BLUE}====================================${NC}\n"

# Check Python version
check_python() {
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
        REQUIRED_VERSION="3.8"
        
        if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" = "$REQUIRED_VERSION" ]; then
            echo -e "${GREEN}✓ Python $PYTHON_VERSION detected${NC}"
            return 0
        else
            echo -e "${RED}✗ Python 3.8+ required, found $PYTHON_VERSION${NC}"
            return 1
        fi
    else
        echo -e "${RED}✗ Python 3 not found${NC}"
        return 1
    fi
}

# Install from source
install_from_source() {
    echo -e "\n${YELLOW}📦 Installing JSONMind-CLI...${NC}\n"
    
    # Create temporary directory
    TEMP_DIR=$(mktemp -d)
    cd "$TEMP_DIR"
    
    # Download source
    echo -e "${BLUE}Downloading source...${NC}"
    curl -L -o jsonmind-cli.tar.gz "${REPO_URL}/archive/refs/tags/v${VERSION}.tar.gz" 2>/dev/null || {
        echo -e "${YELLOW}Could not download release, using git clone...${NC}"
        git clone --depth 1 "$REPO_URL" jsonmind-cli 2>/dev/null || {
            echo -e "${RED}Failed to download source${NC}"
            exit 1
        }
        cd jsonmind-cli
    }
    
    # Extract if downloaded as tar
    if [ -f jsonmind-cli.tar.gz ]; then
        tar -xzf jsonmind-cli.tar.gz
        cd JSONMind-CLI-*
    fi
    
    # Install
    echo -e "${BLUE}Installing...${NC}"
    
    # Create installation directory
    sudo mkdir -p "$INSTALL_DIR"
    
    # Copy main script
    sudo cp jsonmind.py "$INSTALL_DIR/jsonmind"
    sudo chmod +x "$INSTALL_DIR/jsonmind"
    
    # Create wrapper script for TUI
    cat > /tmp/jsonmind-tui << 'EOF'
#!/bin/bash
python3 -c "import sys; sys.path.insert(0, '/usr/local/bin'); exec(open('/usr/local/bin/jsonmind').read().replace('jsonmind.py', 'tui.py'))" "$@"
EOF
    sudo cp /tmp/jsonmind-tui "$INSTALL_DIR/jsonmind-tui"
    sudo chmod +x "$INSTALL_DIR/jsonmind-tui"
    
    # Cleanup
    cd /
    rm -rf "$TEMP_DIR"
    
    echo -e "\n${GREEN}✅ JSONMind-CLI installed successfully!${NC}\n"
}

# Install using pip
install_with_pip() {
    echo -e "\n${YELLOW}📦 Installing via pip...${NC}\n"
    pip3 install jsonmind-cli || {
        echo -e "${RED}pip installation failed, falling back to source...${NC}"
        install_from_source
        return
    }
    echo -e "\n${GREEN}✅ JSONMind-CLI installed via pip!${NC}\n"
}

# Main installation
main() {
    # Check Python
    if ! check_python; then
        echo -e "${RED}Please install Python 3.8 or higher${NC}"
        exit 1
    fi
    
    # Check if pip is available
    if command -v pip3 &> /dev/null; then
        read -p "Install via pip? (recommended) [Y/n]: " choice
        choice=${choice:-Y}
        if [[ $choice =~ ^[Yy]$ ]]; then
            install_with_pip
        else
            install_from_source
        fi
    else
        install_from_source
    fi
    
    # Verify installation
    echo -e "${BLUE}Verifying installation...${NC}"
    if command -v jsonmind &> /dev/null; then
        VERSION_INSTALLED=$(jsonmind --version 2>&1)
        echo -e "${GREEN}✓ Installed: $VERSION_INSTALLED${NC}"
    else
        echo -e "${YELLOW}⚠ jsonmind not found in PATH${NC}"
        echo -e "${YELLOW}  You may need to add $INSTALL_DIR to your PATH${NC}"
    fi
    
    echo -e "\n${GREEN}🎉 Installation complete!${NC}"
    echo -e "\n${BLUE}Quick Start:${NC}"
    echo -e "  jsonmind --help          Show help"
    echo -e "  jsonmind sample          Generate sample data"
    echo -e "  jsonmind-tui             Launch interactive mode"
    echo -e "\n${BLUE}Documentation:${NC} $REPO_URL"
    echo ""
}

# Run main
main "$@"
