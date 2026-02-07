#!/bin/bash

################################################################################
# Multi-Team Integration Quick Setup Script
# Automated installation for new users
# Date: February 6, 2026
################################################################################

set -e  # Exit on error

echo "================================================================================"
echo "Multi-Team AI Privacy Integration System - Quick Setup"
echo "================================================================================"
echo ""

# Check Python version
echo "✓ Checking Python version..."
python3 --version

# Navigate to project root
PROJECT_ROOT="/home/nibin/Desktop/Internship/llm-security"
cd "$PROJECT_ROOT"
echo "✓ Working directory: $PROJECT_ROOT"
echo ""

# Remove old virtual environment
echo "→ Cleaning old virtual environment..."
rm -rf .venv
echo "✓ Old environment removed"
echo ""

# Create new virtual environment
echo "→ Creating new virtual environment..."
python3 -m venv .venv
echo "✓ Virtual environment created"
echo ""

# Activate virtual environment
echo "→ Activating virtual environment..."
source .venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Install uv if not available
echo "→ Installing uv (fast Python package installer)..."
if ! command -v uv &> /dev/null; then
    curl -LsSf https://astral.sh/uv/install.sh | sh > /dev/null 2>&1
    # Add uv to PATH for current session
    export PATH="$HOME/.local/bin:$PATH"
    if [ -f "$HOME/.cargo/env" ]; then
        source $HOME/.cargo/env
    fi
    echo "✓ uv installed successfully"
else
    echo "✓ uv already available"
fi
echo ""

# Install all dependencies using uv
echo "→ Installing all required dependencies using uv..."
echo "   This may take a few minutes..."
uv pip install -r requirements-complete.txt > /dev/null 2>&1
echo "✓ All dependencies installed successfully"
echo ""

# Verify critical packages
echo "→ Verifying critical packages..."
python3 -c "import deal; import numpy; import neo4j; import openai; import groq; print('✓ All critical packages verified')"
echo ""

# Check for .env file
echo "→ Checking environment configuration..."
if [ ! -f "ai_privacy_firewall_team_c/.env" ]; then
    echo "⚠  Warning: .env file not found"
    echo "   Creating template .env file..."
    cat > ai_privacy_firewall_team_c/.env << 'EOF'
# OpenAI Configuration (REQUIRED)
OPENAI_API_KEY=your_openai_api_key_here

# Groq Configuration (OPTIONAL)
GROQ_API_KEY=your_groq_api_key_here

# Neo4j Configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=skyber123

# LLM Model Selection
LLM_PROVIDER=openai
OPENAI_MODEL=gpt-4o-mini
GROQ_MODEL=llama-3.3-70b-versatile

# Environment
ENVIRONMENT=production
EOF
    echo "✓ Template .env file created"
    echo ""
    echo "⚠  IMPORTANT: Edit ai_privacy_firewall_team_c/.env and add your OPENAI_API_KEY"
    echo "   Command: nano ai_privacy_firewall_team_c/.env"
else
    echo "✓ Environment file exists"
fi
echo ""

# Initialize organizational data
echo "→ Initializing organizational data..."
cd privacy_firewall_integration
if python3 data/ingestion.py > /dev/null 2>&1; then
    echo "✓ Organizational data loaded successfully"
else
    echo "⚠  Warning: Could not load organizational data (Neo4j may not be running)"
    echo "   To load data manually: cd privacy_firewall_integration && python3 data/ingestion.py"
fi
cd "$PROJECT_ROOT"
echo ""

# Summary
echo "================================================================================"
echo "✅ SETUP COMPLETE!"
echo "================================================================================"
echo ""
echo "To run the multi-team integration test:"
echo ""
echo "  cd ai_privacy_firewall_team_c"
echo "  source ../.venv/bin/activate"
echo "  python3 multi_team_integration_test.py"
echo "cd .."
echo ""
echo "Expected result: 6/6 tests passed (100% success rate)"
echo ""
echo "If organizational data loading failed during setup, run manually:"
echo "  cd privacy_firewall_integration"
echo "  python3 data/ingestion.py"
echo ""
echo "For detailed instructions, see: MULTI_TEAM_INTEGRATION_GUIDE.md"
echo "================================================================================"
