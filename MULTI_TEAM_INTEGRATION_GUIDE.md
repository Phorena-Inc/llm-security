================================================================================
MULTI-TEAM INTEGRATION SETUP GUIDE - COMPLETE WORKING VERSION
================================================================================
Last Updated: February 6, 2026
Status: ✅ TESTED AND WORKING (100% Success Rate)

This guide provides step-by-step commands to set up and run the multi-team
AI privacy integration system without errors.

================================================================================
PREREQUISITES
================================================================================

1. Python 3.10 or higher (3.12+ recommended)
2. Docker and Docker Compose (for Neo4j database)
3. Git (to clone/access the repository)

Required API Keys (add to .env file):
- OPENAI_API_KEY (required)
- GROQ_API_KEY (optional, for Groq LLM support)

================================================================================
STEP 1: NAVIGATE TO PROJECT ROOT
================================================================================

cd /home/nibin/Desktop/Internship/llm-security

================================================================================
STEP 2: CREATE AND ACTIVATE VIRTUAL ENVIRONMENT
================================================================================

# Remove old virtual environment if it exists
rm -rf .venv

# Create new virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

================================================================================
STEP 3: INSTALL ALL REQUIRED DEPENDENCIES
================================================================================

# Install core dependencies using pip
pip install --upgrade pip

# Install all required packages in one command
pip install \
    annotated-doc==0.0.4 \
    annotated-types==0.7.0 \
    anyio==4.12.1 \
    certifi \
    click>=8.0.0 \
    deal>=4.24.0 \
    diskcache>=5.6.3 \
    distro \
    fastapi>=0.104.0 \
    groq>=0.4.0 \
    h11>=0.16.0 \
    httpcore \
    httpx>=0.25.0 \
    idna \
    jiter \
    neo4j>=5.26.0 \
    numpy>=2.0.0 \
    openai>=1.91.0 \
    owlready2>=0.48 \
    pydantic>=2.11.5 \
    pydantic_core \
    python-dateutil>=2.8.0 \
    python-dotenv>=1.0.0 \
    pytz>=2023.3 \
    PyYAML>=6.0 \
    six \
    sniffio \
    starlette \
    tenacity>=9.0.0 \
    tqdm \
    typing-inspection \
    typing_extensions \
    uvicorn>=0.24.0 \
    pytest>=7.0.0 \
    pytest-asyncio>=0.21.0

================================================================================
STEP 4: CONFIGURE ENVIRONMENT VARIABLES
================================================================================

# Create .env file in Team C directory if it doesn't exist
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

# Make sure to replace 'your_openai_api_key_here' with your actual API key
# You can edit the file with:
# nano ai_privacy_firewall_team_c/.env

================================================================================
STEP 5: START NEO4J DATABASE (OPTIONAL - FOR FULL FUNCTIONALITY)
================================================================================

# Note: Tests can run without Neo4j using fallback mode, but for production:

# If you have docker and docker-compose:
cd privacy_firewall_integration
docker compose up -d
cd ..

# Verify Neo4j is running (optional):
# docker ps | grep neo4j

# To load organizational data into Neo4j (if database is running):
# cd privacy_firewall_integration
# python data/ingestion.py
# cd ..

================================================================================
STEP 6: RUN THE MULTI-TEAM INTEGRATION TEST
================================================================================

# Navigate to Team C directory
cd ai_privacy_firewall_team_c

# Make sure virtual environment is activated
source ../.venv/bin/activate

# Run the multi-team integration test
python3 multi_team_integration_test.py

================================================================================
EXPECTED OUTPUT
================================================================================

You should see output similar to:

✅ Graphiti core imported successfully
✅ Loaded environment from: .../ai_privacy_firewall_team_c/.env
🔧 Multi-Team Privacy Integration Test Suite

🚀 Multi-Team Integration Test
============================================================
Testing: Team A (Temporal) + Team B (Org Policies) + Team C (AI)

Test Results:
✅ Test 1: Medical Emergency Access - PASS
✅ Test 2: HR Employee Data Access - PASS
✅ Test 3: Sales Customer Data - PASS
✅ Test 4: Contractor Source Code Access - PASS
✅ Test 5: Finance Team Revenue Data - PASS
✅ Test 6: Cross-Department API Access - PASS

============================================================
🎯 MULTI-TEAM INTEGRATION TEST SUMMARY
============================================================
Total Tests: 6
✅ Passed: 6
❌ Failed: 0
Success Rate: 100.0%

Integration Status:
Team A (Temporal): 6/6 active
Team B (Org Policies): 6/6 active

✅ ALL TESTS PASSED - Multi-team integration working perfectly!

================================================================================
TROUBLESHOOTING
================================================================================

Problem: "No module named 'deal'" or similar import errors
Solution: Make sure all dependencies from STEP 3 are installed
          Run: pip list | grep -i deal
          If missing: pip install deal>=4.24.0

Problem: "cannot import name 'AsyncGroq' from 'groq'"
Solution: Install groq package: pip install groq>=0.4.0

Problem: "No module named 'numpy'"
Solution: Install numpy: pip install numpy>=2.0.0

Problem: "No module named 'diskcache'"
Solution: Install diskcache: pip install diskcache>=5.6.3

Problem: Neo4j connection errors
Solution: Tests will work with MOCK_FALLBACK mode without Neo4j
          For full functionality, ensure Neo4j is running on localhost:7687

Problem: OpenAI API errors
Solution: Check your OPENAI_API_KEY in ai_privacy_firewall_team_c/.env
          Make sure you have credits in your OpenAI account

================================================================================
QUICK START (ALL COMMANDS IN SEQUENCE)
================================================================================

# Copy and paste these commands for a complete fresh setup:

cd /home/nibin/Desktop/Internship/llm-security
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install annotated-doc annotated-types anyio certifi click deal diskcache distro fastapi groq h11 httpcore httpx idna jiter neo4j numpy openai owlready2 pydantic pydantic_core python-dateutil python-dotenv pytz PyYAML six sniffio starlette tenacity tqdm typing-inspection typing_extensions uvicorn pytest pytest-asyncio
cd ai_privacy_firewall_team_c
python3 multi_team_integration_test.py

================================================================================
ALTERNATIVE: USING UV PACKAGE MANAGER
================================================================================

If you prefer using the 'uv' package manager:

# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Sync all dependencies
cd /home/nibin/Desktop/Internship/llm-security
uv sync

# Run the test
cd ai_privacy_firewall_team_c
uv run python multi_team_integration_test.py

================================================================================
TEAM FOLDER STRUCTURE
================================================================================

Team A (Temporal Framework):
  - ai_temporal_framework/ (production-ready)
  - temporal-framework-feature-temporal-context/ (feature development)

Team B (Organizational Policies):
  - privacy_firewall_integration/

Team C (AI Decision Orchestrator):
  - ai_privacy_firewall_team_c/

Main Project Root:
  - pyproject.toml (workspace configuration)
  - .venv/ (virtual environment)

================================================================================
DEPENDENCIES BY TEAM
================================================================================

Team A (Temporal Framework):
  - pytest>=7.0
  - PyYAML>=6.0
  - python-dateutil>=2.8.0
  - neo4j>=5.0.0

Team B (Organizational Policies):
  - graphiti-core>=0.3.0
  - neo4j>=5.0.0
  - python-dotenv>=1.0.0
  - deal>=4.24.0
  - PyYAML>=6.0
  - python-dateutil>=2.8.0
  - pytz>=2023.3
  - asyncio>=3.4.3
  - pytest>=7.0.0
  - pytest-asyncio>=0.21.0
  - pydantic>=2.0.0
  - fastapi>=0.104.0
  - uvicorn[standard]>=0.24.0
  - httpx>=0.25.0
  - openai>=1.0.0
  - groq>=0.4.0

Team C (AI Privacy Orchestrator):
  - diskcache>=5.6.3
  - fastapi>=0.118.0
  - httpx>=0.28.1
  - neo4j>=6.0.2
  - numpy>=2.3.3
  - openai>=2.0.1
  - owlready2>=0.48
  - pydantic>=2.11.9
  - python-dotenv>=1.1.1
  - pytz>=2025.2
  - pyyaml>=6.0.3
  - requests>=2.32.5
  - tenacity>=9.1.2
  - uvicorn>=0.37.0

================================================================================
INTEGRATION ARCHITECTURE
================================================================================

Request Flow:
  User Request
      ↓
  Team C (Coordinator)
      ↓
  ┌─────────────┴─────────────┐
  ↓                           ↓
Team A                     Team B
(Temporal)              (Organizational)
  ↓                           ↓
  └─────────────┬─────────────┘
                ↓
      Team C Decision Logic
                ↓
        Final ALLOW/DENY

Decision Combination Methods:
1. consensus_allow - Both teams ALLOW
2. emergency_override - Emergency situation overrides restrictions
3. organizational_override - Role-based access overrides temporal restrictions
4. security_priority - Either team DENY results in final DENY

================================================================================
TESTING DETAILS
================================================================================

Test Scenarios:
1. Medical Emergency Access - Tests emergency override logic
2. HR Employee Data Access - Tests organizational override
3. Sales Customer Data - Tests consensus allow
4. Contractor Source Code Access - Tests security boundary denial
5. Finance Team Revenue Data - Tests role-based consensus
6. Cross-Department API Access - Tests cross-boundary restrictions

Expected Performance:
- Success Rate: 100%
- Average Response Time: ~200-900ms
- Average Confidence: 80-82%

================================================================================
ADDITIONAL COMMANDS
================================================================================

# Check installed packages
pip list

# Verify specific package
pip show deal

# Update all packages
pip install --upgrade pip setuptools wheel

# Export current environment
pip freeze > requirements-frozen.txt

# Deactivate virtual environment
deactivate

# Remove virtual environment
rm -rf .venv

================================================================================
SUPPORT & DOCUMENTATION
================================================================================

Related Files:
- MULTI_TEAM_INTEGRATION_GUIDE.md (detailed architecture)
- MULTI_TEAM_INTEGRATION_DISCUSSION.md (technical discussion)
- API_SETUP_GUIDE.md (API configuration)
- README.md (project overview)

Integration Test File:
- ai_privacy_firewall_team_c/multi_team_integration_test.py

Configuration Files:
- pyproject.toml (main project config)
- ai_privacy_firewall_team_c/pyproject.toml (Team C config)
- ai_privacy_firewall_team_c/.env (environment variables)

================================================================================
END OF SETUP GUIDE
================================================================================

Last Test Date: February 6, 2026
Status: ✅ VERIFIED WORKING
Success Rate: 100% (6/6 tests passed)
