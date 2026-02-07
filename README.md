# LLM Security

> **Multi-Team AI Privacy Integration System**

[![Lint](https://github.com/Phorena-Inc/llm-security/actions/workflows/lint.yml/badge.svg?style=flat)](https://github.com/Phorena-Inc/llm-security/actions/workflows/lint.yml)
[![Unit Tests](https://github.com/Phorena-Inc/llm-security/actions/workflows/unit_tests.yml/badge.svg)](https://github.com/Phorena-Inc/llm-security/actions/workflows/unit_tests.yml)
[![GitHub Repo stars](https://img.shields.io/github/stars/Phorena-Inc/llm-security)](https://github.com/Phorena-Inc/llm-security)

A comprehensive multi-team AI privacy firewall system that enables collaborative decision-making for enterprise privacy and access control. This system integrates temporal framework analysis, organizational policy enforcement, and AI-powered decision engines to make intelligent privacy decisions in real-time.

## 🚀 Quick Start

### Prerequisites

1. **Python 3.10+** (3.12+ recommended)
2. **Neo4j Database** (running locally or via Docker)
3. **API Keys** (OpenAI required, Groq optional)

### Installation

```bash
# Clone the repository
git clone https://github.com/Phorena-Inc/llm-security.git
cd llm-security

# Run quick setup (recommended)
./quick-setup.sh

# Or manual installation:
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-complete.txt
```

### Environment Setup

```bash
# Required environment variables (create .env files)
# ai_privacy_firewall_team_c/.env:
OPENAI_API_KEY=your_openai_api_key_here
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=skyber123

# Optional
GROQ_API_KEY=your_groq_api_key_here
LLM_PROVIDER=openai
OPENAI_MODEL=gpt-4o-mini
```

### Start Neo4j

**Option 1: Docker (Recommended)**
```bash
docker run -d \
  --name neo4j \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/skyber123 \
  neo4j:latest
```

**Option 2: Neo4j Desktop**
- Download and install [Neo4j Desktop](https://neo4j.com/download/)
- Create a new database with password `skyber123`
- Start the database

### Run Multi-Team Integration Test

```bash
cd ai_privacy_firewall_team_c
source ../.venv/bin/activate
python3 multi_team_integration_test.py
```

**Expected Result**: 6/6 tests passed (100% success rate)

## 🏢 System Architecture

This system implements a **collaborative AI privacy firewall** with three specialized teams:

### **🕐 Team A: Temporal Framework**
- **Location**: `ai_temporal_framework/`
- **Purpose**: Time-aware privacy decisions based on urgency, emergency situations, and temporal context
- **Key Features**: Emergency detection, time-based policies, urgency classification

### **🏢 Team B: Organizational Policies** 
- **Location**: `privacy_firewall_integration/`
- **Purpose**: Role-based access control using organizational structure and company policies
- **Key Features**: Employee role validation, department permissions, policy enforcement

### **🧠 Team C: AI Decision Engine**
- **Location**: `ai_privacy_firewall_team_c/`
- **Purpose**: Combines Team A + Team B decisions using intelligent logic and AI classification
- **Key Features**: Multi-team integration, final decision making, conflict resolution

## 📋 Real-World Example

> *"Can Dr. Sarah Johnson (Emergency Room) access patient medical records at 2 AM during a cardiac emergency?"*

- **Team A (Temporal)**: ✅ ALLOW (Emergency + High Urgency)
- **Team B (Organizational)**: ✅ ALLOW (Doctor role + Medical data access policy)
- **Team C (AI Decision)**: ✅ **FINAL DECISION: ALLOW** (Emergency Override)

## 📚 Policy Examples

The system includes various policy examples demonstrating sophisticated access control:

### 1. Time-of-Day Policy
**Simple time-based access control** - Restricts non-critical queries to working hours while allowing critical queries anytime.

```bash
cd time_of_day_policy
python time_of_day_policy_example.py
```

**Features:**
- Time-based access restrictions
- Query type classification (critical, non-critical, admin, research, weekend)
- Configurable working hours
- JSON-based configuration

### 2. Mission Phase Policy
**Complex role-based access control** with phase-specific restrictions for mission operations.

```bash
cd mission_phase_policy
python mission_phase_policy_example.py
```

**Features:**
- Role-based access control (RBAC)
- Mission phase-specific policies
- Commander override permissions
- Emergency protocol access

### 3. Prompt Sensitivity Policy
**Content filtering and redaction system** that automatically detects and redacts sensitive information.

```bash
cd prompt_sensitivity_policy
python prompt_sensitivity_example.py
```

**Features:**
- Firewall detection of sensitive terms
- Phase-specific content redaction
- Dynamic redaction based on mission phase
- Emergency override for safety

### 4. Before/After Event Policy
**Time-based blocking system** that restricts access to content based on scheduled events.

```bash
cd before_after_event_policy
python before_after_event_example.py
```

**Features:**
- Scheduled event blocking based on timestamps
- Before/after event access control
- Multiple concurrent scheduled events
- Timezone-aware timestamp comparisons

### 5. Multi-Factor Contradiction Policy
**Complex access control system** that handles multiple conflicting rules and contradiction resolution.

```bash
cd multi_factor_contradiction_policy
python multi_factor_contradiction_example.py
```

**Features:**
- Multiple conflicting rules and restrictions
- Contradiction resolution based on priority hierarchy
- User clearance levels and permissions
- Commander override and emergency access

### 6. Timezone-Aware Policy
**Sophisticated timezone-aware access control** that handles user identification and location-based timezone detection.

```bash
cd timezone_aware_policy
python timezone_aware_example.py
```

**Features:**
- User identification with email and name
- Location-based timezone detection
- Dynamic policy application based on user's local time
- Comprehensive location-to-timezone mapping

## 🛠️ Basic Usage

### Multi-Team Integration Example

```python
import asyncio
from ai_privacy_firewall_team_c.core.decision_engine import MultiTeamDecisionEngine

async def main():
    # Initialize the multi-team decision engine
    engine = MultiTeamDecisionEngine()
    
    # Example privacy decision request
    request = {
        "user": "Dr. Sarah Johnson",
        "role": "Emergency Room Doctor",
        "data_type": "patient_medical_records",
        "query": "Access patient cardiac emergency data",
        "timestamp": "2026-02-07T02:00:00Z",
        "context": "cardiac_emergency"
    }
    
    # Get decision from all teams
    decision = await engine.make_decision(request)
    
    print(f"Final Decision: {decision['final_decision']}")
    print(f"Team A (Temporal): {decision['team_a_decision']}")
    print(f"Team B (Organizational): {decision['team_b_decision']}")
    print(f"Team C (AI): {decision['team_c_decision']}")
    
    await engine.close()

# Run the example
asyncio.run(main())
```

### Individual Team Usage

```python
# Team A - Temporal Framework
from ai_temporal_framework.core.temporal_analyzer import TemporalAnalyzer
temporal = TemporalAnalyzer()
decision = temporal.analyze_temporal_context(request)

# Team B - Organizational Policies
from privacy_firewall_integration.core import OrganizationalPolicyEngine
org_engine = OrganizationalPolicyEngine()
decision = await org_engine.evaluate_policy(request)

# Team C - AI Decision Engine
from ai_privacy_firewall_team_c.core.ai_classifier import AIClassifier
ai_classifier = AIClassifier()
decision = await ai_classifier.classify_decision(request)
```

## 🔧 Configuration

The system uses JSON configuration files and environment variables:

### Team Configuration Files
- `ai_temporal_framework/config/temporal_config.json` - Time-based policies
- `privacy_firewall_integration/config/org_policies.json` - Organizational rules
- `ai_privacy_firewall_team_c/config/decision_config.json` - AI decision parameters

### Environment Files
- `ai_privacy_firewall_team_c/.env` - Main configuration with API keys
- Team-specific `.env.example` files in each folder

Example configuration structure:
```json
{
  "temporal_policies": {
    "emergency_override": true,
    "working_hours": "09:00-17:00",
    "critical_access": "always"
  },
  "organizational_policies": {
    "role_hierarchy": ["admin", "doctor", "nurse", "staff"],
    "data_access_matrix": {
      "doctor": ["patient_records", "medical_data"],
      "nurse": ["patient_basic_info"]
    }
  }
}
```

## 🏗️ Architecture

The LLM Security system uses a multi-layer architecture:

### Core Components
- **Multi-Team Integration Engine**: Coordinates decisions across all teams
- **Temporal Analysis Engine**: Time-aware policy evaluation
- **Organizational Policy Engine**: Role-based access control
- **AI Classification Engine**: Intelligent decision synthesis
- **Knowledge Graph**: Neo4j-powered data relationships
- **Audit System**: Complete decision tracking and logging

### Data Flow
1. **Request Input** → Privacy decision request from user/system
2. **Team A Analysis** → Temporal context and urgency evaluation
3. **Team B Analysis** → Organizational policy and role validation
4. **Team C Synthesis** → AI-powered final decision making
5. **Decision Output** → Allow/Deny with detailed reasoning
6. **Audit Logging** → Complete decision trail for compliance

### Integration Patterns
- **Synchronous**: Real-time decisions for critical requests
- **Asynchronous**: Batch processing for policy updates
- **Event-driven**: Reactive policies based on system events

## 📖 Documentation

- **Setup Guide**: [MULTI_TEAM_INTEGRATION_GUIDE.md](MULTI_TEAM_INTEGRATION_GUIDE.md) - Complete setup instructions
- **API Reference**: See individual team folders for detailed API documentation
- **Examples**: Check the `examples/` directory for usage examples
- **Testing**: Run `python3 multi_team_integration_test.py` for integration tests

## 🧪 Testing

### Integration Tests
```bash
cd ai_privacy_firewall_team_c
python3 multi_team_integration_test.py
```

### Individual Team Tests
```bash
# Team A Tests
cd ai_temporal_framework && python -m pytest tests/

# Team B Tests  
cd privacy_firewall_integration && python -m pytest tests/

# Team C Tests
cd ai_privacy_firewall_team_c && python -m pytest tests/
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/Phorena-Inc/llm-security/issues)
- **Documentation**: [Setup Guide](MULTI_TEAM_INTEGRATION_GUIDE.md)
- **Email**: Contact the development team at Phorena Inc.

## 🎯 Use Cases

### Enterprise Privacy Management
- Healthcare: Patient data access control
- Financial: Customer information protection  
- Government: Classified information security
- Corporate: Sensitive business data protection

### Multi-Team Environments
- Large organizations with complex role hierarchies
- Time-sensitive operations requiring emergency overrides
- Regulated industries needing audit trails
- Global companies with timezone-aware policies

---

**Built by Phorena Inc. - Advanced AI Privacy Solutions**

