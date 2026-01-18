#!/usr/bin/env python3
"""
Team B Integration Module for Direct Python Integration
====================================================

This module provides direct Python integration with Team B's Privacy Firewall
organizational policies. It transforms Team C requests into Team B format,
evaluates organizational policies, and returns structured decisions.

Team B Features:
- 43 YAML organizational policies
- Neo4j organizational data (45 employees, 6 departments, 13 teams)
- Employee lookup and role validation
- Department-based access controls
- Policy evaluation with confidence scoring

Integration Pattern: Direct Python imports (no HTTP API calls)

Author: Team C Privacy Firewall  
Date: 2024-12-09
Integration: Multi-Team Direct Python
"""

import sys
import os
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional

# Add Team B integration path - multiple possible locations
possible_team_b_paths = [
    str(Path(__file__).parent.parent.parent / "privacy_firewall_integration"),  # ../privacy_firewall_integration
    "/Users/apple/Downloads/graphiti/graphiti/privacy_firewall_integration"      # absolute path
]

# Also add the graphiti root to PYTHONPATH for proper module resolution
graphiti_root = str(Path(__file__).parent.parent.parent)
sys.path.insert(0, graphiti_root)

for team_b_path in possible_team_b_paths:
    if Path(team_b_path).exists():
        sys.path.insert(0, team_b_path)
        print(f"✅ Added Team B path: {team_b_path}")
        break

class TeamBIntegration:
    """Direct Python integration with Team B Privacy Firewall."""
    
    def __init__(self, neo4j_password="skyber123"):  # Use correct Team B password
        """Initialize Team B integration with fallback support."""
        print("🔗 Initializing Team B Privacy Firewall Integration")
        
        # Try to import Team B components with fallback
        self.team_b_available = self._init_team_b_components()
        self.neo4j_password = neo4j_password
        self._fresh_connection_created = False
        
        # Organizational data for mock fallback
        self._init_organizational_data()
        
        print(f"✅ Team B Integration: {'ACTIVE' if self.team_b_available else 'MOCK_FALLBACK'}")
    
    def _init_team_b_components(self) -> bool:
        """Initialize Team B components with graceful fallback."""
        try:
            # Try direct imports from Team B Privacy Firewall (correct paths)
            from privacy_firewall_integration.api import PrivacyFirewallAPI
            from privacy_firewall_integration.core.models import CompanyAttributes  # Use actual models
            
            # Ensure OpenAI API key is set for Team B initialization
            if not os.getenv("OPENAI_API_KEY"):
                print("⚠️  OPENAI_API_KEY required for Team B Privacy Firewall")
                raise ImportError("Missing OPENAI_API_KEY for Team B initialization")
            
            self.privacy_firewall_api = PrivacyFirewallAPI()
            self.CompanyAttributes = CompanyAttributes
            # Note: PolicyRequest/PolicyResponse may not exist, using dict format instead
            
            print("✅ Team B Direct Python integration successful")
            return True
            
        except ImportError as e:
            print(f"⚠️  Team B direct import failed: {e}")
            print("   Using mock fallback for Team B integration")
            return False
    
    def _init_organizational_data(self):
        """Initialize organizational data for Team B policy evaluation."""
        # Mock organizational structure for fallback
        self.organizational_data = {
            "departments": {
                "engineering": {"id": "eng", "head": "engineering_manager", "teams": ["backend", "frontend", "devops"]},
                "hr": {"id": "hr", "head": "hr_manager", "teams": ["recruitment", "benefits"]},
                "finance": {"id": "fin", "head": "finance_director", "teams": ["accounting", "payroll"]},
                "marketing": {"id": "mkt", "head": "marketing_director", "teams": ["digital", "content"]},
                "sales": {"id": "sales", "head": "sales_director", "teams": ["enterprise", "smb"]},
                "legal": {"id": "legal", "head": "legal_counsel", "teams": ["compliance"]}
            },
            "employees": {
                "medical_doctor": {"department": "medical", "role": "doctor", "clearance": "high"},
                "hr_specialist": {"department": "hr", "role": "specialist", "clearance": "medium"}, 
                "marketing_manager": {"department": "marketing", "role": "manager", "clearance": "medium"},
                "contractor": {"department": "external", "role": "contractor", "clearance": "low"},
                "financial_analyst": {"department": "finance", "role": "analyst", "clearance": "high"},
                "engineering_lead": {"department": "engineering", "role": "lead", "clearance": "high"}
            }
        }
    
    async def _refresh_team_b_connection(self):
        """Refresh Team B Neo4j connection to bypass rate limiting."""
        if not self.team_b_available:
            return
            
        try:
            print("🔄 Refreshing Team B Neo4j connection...")
            
            # Force recreate the Privacy Firewall API with fresh connections
            from privacy_firewall_integration.api import PrivacyFirewallAPI
            
            # Create a new instance to get fresh Neo4j connection pools
            self.privacy_firewall_api = PrivacyFirewallAPI()
            
            print("✅ Team B connection refreshed successfully")
            
        except Exception as e:
            print(f"⚠️  Failed to refresh Team B connection: {e}")
            # Don't fail completely, let the original call proceed
    
    async def make_team_b_decision(self, privacy_request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make Team B organizational policy decision.
        
        Args:
            privacy_request: Team C format request
            
        Returns:
            Team B decision with organizational policy evaluation
        """
        print("🏢 Team B: Evaluating organizational policies")
        
        try:
            if self.team_b_available:
                return await self._make_real_team_b_decision(privacy_request)
            else:
                return await self._make_mock_team_b_decision(privacy_request)
                
        except Exception as e:
            print(f"❌ Team B decision failed: {e}")
            return self._create_error_decision(str(e))
    
    async def _make_real_team_b_decision(self, privacy_request: Dict[str, Any]) -> Dict[str, Any]:
        """Make real Team B decision using direct Python integration."""
        
        # Refresh Neo4j connection if this is the first call to clear any rate limiting
        if not self._fresh_connection_created:
            await self._refresh_team_b_connection()
            self._fresh_connection_created = True
        
        # Transform Team C request to Team B format
        team_b_request = self._transform_request_to_team_b(privacy_request)
        
        print(f"📤 Team B Request: {team_b_request['requester']} -> {team_b_request['data_type']}")
        
        # Map Team C data types to Team B resource types
        resource_mapping = {
            "medical_data": "medical_records",
            "employee_data": "salary_info", 
            "customer_data": "financial_reports",
            "proprietary_data": "code_repository",
            "financial_data": "financial_reports",
            "system_credentials": "financial_reports"  # Financial API keys should be treated as financial access
        }
        
        resource_type = resource_mapping.get(team_b_request["data_type"], "department_docs")
        
        try:
            # Call Team B Privacy Firewall API
            policy_response = await self.privacy_firewall_api.check_access_permission(
                requester_id=team_b_request["requester"],
                target_id="company_data",  # Generic target for company resources
                resource_type=resource_type,
                timestamp=datetime.now(timezone.utc)
            )
        except Exception as e:
            if "AuthenticationRateLimit" in str(e):
                print("🔄 Neo4j rate limit detected, falling back to organizational mock policies...")
                # Fall back to mock organizational decision instead of retrying
                return self._make_mock_organizational_decision(
                    privacy_request['requester'], 
                    privacy_request['data_field'], 
                    privacy_request['purpose'], 
                    privacy_request.get('employee_info', {})
                )
            else:
                raise e
        
        # Transform Team B response back to Team C format  
        return self._transform_response_from_team_b(policy_response, privacy_request)
    
    async def _make_mock_team_b_decision(self, privacy_request: Dict[str, Any]) -> Dict[str, Any]:
        """Mock Team B decision for fallback scenarios."""
        
        print("🎭 Team B Mock: Simulating organizational policy evaluation")
        
        # Extract request details
        requester = privacy_request.get('requester', 'unknown')
        data_field = privacy_request.get('data_field', 'unknown') 
        purpose = privacy_request.get('purpose', 'unknown')
        
        # Get employee info
        employee_info = self.organizational_data["employees"].get(requester, {
            "department": "external",
            "role": "unknown", 
            "clearance": "none"
        })
        
        # Evaluate organizational policies (mock)
        decision = self._evaluate_organizational_policies(
            requester, data_field, purpose, employee_info
        )
        
        return {
            "allowed": decision["allowed"],
            "reason": decision["reason"],
            "confidence": decision["confidence"],
            "team_b_integration": True,
            "integration": "mock_fallback",
            "organizational_context": {
                "department": employee_info.get("department"),
                "role": employee_info.get("role"),
                "clearance": employee_info.get("clearance"),
                "policies_evaluated": decision.get("policies_evaluated", [])
            },
            "decision_id": f"team_b_mock_{uuid.uuid4()}",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    
    def _transform_request_to_team_b(self, privacy_request: Dict[str, Any]):
        """Transform Team C request format to Team B PolicyRequest format."""
        
        # Map Team C data fields to Team B data types
        data_type_mapping = {
            "patient_medical_records": "medical_data",
            "employee_salary_data": "employee_data", 
            "customer_email_addresses": "customer_data",
            "source_code": "proprietary_data",
            "customer_purchase_history": "financial_data",
            "api_keys": "system_credentials"
        }
        
        # Map Team C purposes to Team B access types
        purpose_mapping = {
            "emergency_treatment": "emergency_access",
            "compliance_audit": "audit_access", 
            "campaign_personalization": "marketing_access",
            "system_maintenance": "maintenance_access",
            "revenue_analysis": "analysis_access",
            "system_integration": "integration_access"
        }
        
        team_b_data_type = data_type_mapping.get(
            privacy_request.get("data_field"), 
            "general_data"
        )
        
        team_b_access_type = purpose_mapping.get(
            privacy_request.get("purpose"),
            "general_access" 
        )
        
        # Create Team B policy request (using dict format)
        team_b_request_dict = {
            "requester": privacy_request.get("requester", "unknown"),
            "data_type": team_b_data_type,
            "access_type": team_b_access_type,
            "context": privacy_request.get("context", ""),
            "emergency": privacy_request.get("emergency", False),
            "request_id": f"team_c_{uuid.uuid4()}",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        return team_b_request_dict if self.team_b_available else {
            "requester": privacy_request.get("requester", "unknown"),
            "data_type": team_b_data_type,
            "access_type": team_b_access_type,
            "context": privacy_request.get("context", ""),
            "emergency": privacy_request.get("emergency", False)
        }
    
    def _transform_response_from_team_b(self, policy_response, original_request: Dict[str, Any]) -> Dict[str, Any]:
        """Transform Team B API response back to Team C format."""
        
        return {
            "allowed": policy_response.get("allowed", False),
            "reason": policy_response.get("reason", "Team B organizational decision"),
            "confidence": policy_response.get("confidence", 0.8),
            "team_b_integration": True,
            "integration": "direct_python",
            "organizational_context": {
                "policies_matched": policy_response.get("policies_applied", []),
                "department": policy_response.get("requester_department"),
                "role": policy_response.get("requester_role"),
                "clearance_level": policy_response.get("access_level"),
                "relationship_found": policy_response.get("relationship_found", False)
            },
            "decision_id": f"team_b_real_{uuid.uuid4()}",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "team_b_response": policy_response  # Include raw response for debugging
        }
    
    def _make_mock_organizational_decision(self, requester: str, data_field: str, purpose: str, employee_info: Dict[str, Any]) -> Dict[str, Any]:
        """Make intelligent mock organizational policy decision when Neo4j is unavailable."""
        
        # Analyze requester role and purpose
        requester_role = employee_info.get('position', 'unknown').lower()
        requester_department = employee_info.get('department', 'unknown').lower()
        data_sensitivity = self._assess_data_sensitivity(data_field)
        purpose_category = self._categorize_purpose(purpose)
        
        # Decision logic based on organizational hierarchy principles
        allowed = False
        reason = "Access denied - organizational policies enforced via mock evaluation"
        confidence = 0.7
        
        # High-level executives - broader access
        if any(title in requester_role for title in ['ceo', 'cto', 'cfo', 'vp', 'director']):
            if data_sensitivity <= 2:  # Low to medium sensitivity
                allowed = True
                reason = "Approved - Executive level access"
                confidence = 0.9
        
        # HR department - access to employee data
        elif 'hr' in requester_department or 'human resources' in requester_department:
            if 'employee' in data_field.lower() and purpose_category in ['hr_operations', 'compliance']:
                allowed = True
                reason = "Approved - HR department accessing employee data for legitimate purposes"
                confidence = 0.85
        
        # Same department access for operational data
        elif purpose_category == 'operational':
            if data_sensitivity <= 1:  # Low sensitivity only
                allowed = True
                reason = "Approved - Same department operational access"
                confidence = 0.75
        
        # Manager access to team data
        elif 'manager' in requester_role or 'lead' in requester_role:
            if data_sensitivity <= 1 and purpose_category in ['operational', 'reporting']:
                allowed = True
                reason = "Approved - Manager access to team operational data"
                confidence = 0.8
        
        # Emergency purposes - limited access
        elif 'emergency' in purpose.lower() or 'urgent' in purpose.lower():
            if data_sensitivity <= 2:
                allowed = True
                reason = "Approved - Emergency access granted"
                confidence = 0.7
        
        return {
            "allowed": allowed,
            "reason": reason,
            "confidence": confidence,
            "policies_evaluated": ["mock_organizational_hierarchy", "mock_department_access", "mock_data_sensitivity"],
            "mock_decision": True,
            "fallback_reason": "Neo4j organizational data unavailable - using mock policies",
            "metadata": {
                "requester_role": requester_role,
                "requester_department": requester_department,
                "data_sensitivity": data_sensitivity,
                "purpose_category": purpose_category,
                "clearance_level": "mock_evaluation",
                "relationship_found": False
            },
            "decision_id": f"team_b_mock_{uuid.uuid4()}",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    
    def _assess_data_sensitivity(self, data_field: str) -> int:
        """Assess data sensitivity level (1=low, 2=medium, 3=high)."""
        data_field_lower = data_field.lower()
        
        # High sensitivity
        if any(term in data_field_lower for term in ['salary', 'ssn', 'medical', 'financial', 'confidential', 'classified']):
            return 3
        
        # Medium sensitivity  
        elif any(term in data_field_lower for term in ['employee', 'personal', 'contact', 'performance', 'internal']):
            return 2
        
        # Low sensitivity
        else:
            return 1
    
    def _categorize_purpose(self, purpose: str) -> str:
        """Categorize access purpose for policy evaluation."""
        purpose_lower = purpose.lower()
        
        if any(term in purpose_lower for term in ['hr', 'human resources', 'hiring', 'onboarding', 'termination']):
            return 'hr_operations'
        elif any(term in purpose_lower for term in ['audit', 'compliance', 'legal', 'investigation']):
            return 'compliance'
        elif any(term in purpose_lower for term in ['report', 'analysis', 'metrics', 'dashboard']):
            return 'reporting'
        elif any(term in purpose_lower for term in ['emergency', 'urgent', 'critical', 'incident']):
            return 'emergency'
        elif any(term in purpose_lower for term in ['daily', 'operational', 'workflow', 'process']):
            return 'operational'
        else:
            return 'other'
    
    def _evaluate_organizational_policies(self, requester: str, data_field: str, purpose: str, employee_info: Dict[str, Any]) -> Dict[str, Any]:
        """Mock organizational policy evaluation."""
        
        policies_evaluated = []
        allowed = False
        reason = "Access denied by organizational policy"
        confidence = 0.6
        
        # Policy 1: Medical Data Access
        if "medical" in data_field.lower():
            policies_evaluated.append("medical_data_policy")
            if employee_info.get("department") == "medical" or employee_info.get("role") == "doctor":
                allowed = True
                reason = "Medical professional authorized for medical data access"
                confidence = 0.9
            elif purpose == "emergency_treatment":
                allowed = True  
                reason = "Emergency override for medical data access"
                confidence = 0.8
        
        # Policy 2: Employee Data Access
        elif "employee" in data_field.lower():
            policies_evaluated.append("employee_data_policy")
            if employee_info.get("department") == "hr":
                allowed = True
                reason = "HR department authorized for employee data access"
                confidence = 0.85
            elif employee_info.get("role") in ["manager", "director"]:
                allowed = True
                reason = "Management role authorized for employee data access" 
                confidence = 0.75
        
        # Policy 3: Customer Data Access
        elif "customer" in data_field.lower():
            policies_evaluated.append("customer_data_policy")
            if employee_info.get("department") in ["marketing", "sales", "finance"]:
                allowed = True
                reason = f"{employee_info.get('department').title()} department authorized for customer data"
                confidence = 0.8
        
        # Policy 4: Source Code Access
        elif "source_code" in data_field.lower() or "code" in data_field.lower():
            policies_evaluated.append("source_code_policy") 
            if employee_info.get("department") == "engineering":
                allowed = True
                reason = "Engineering department authorized for source code access"
                confidence = 0.9
            elif employee_info.get("role") == "contractor":
                allowed = False
                reason = "Contractors restricted from source code access"
                confidence = 0.95
        
        # Policy 5: API Keys / Credentials
        elif "api" in data_field.lower() or "key" in data_field.lower():
            policies_evaluated.append("api_credentials_policy")
            if employee_info.get("clearance") == "high" and employee_info.get("department") in ["engineering", "devops"]:
                allowed = True
                reason = "High clearance engineering role authorized for API access"
                confidence = 0.85
        
        # Default Policy: General Access Control
        if not policies_evaluated:
            policies_evaluated.append("general_access_policy")
            if employee_info.get("clearance") in ["medium", "high"]:
                allowed = True
                reason = "General access granted based on clearance level"
                confidence = 0.6
        
        return {
            "allowed": allowed,
            "reason": reason, 
            "confidence": confidence,
            "policies_evaluated": policies_evaluated
        }
    
    def _create_error_decision(self, error_message: str) -> Dict[str, Any]:
        """Create error decision for Team B failures."""
        return {
            "allowed": False,
            "reason": f"Team B integration error: {error_message}",
            "confidence": 0.0,
            "team_b_integration": False,
            "integration": "error",
            "error": error_message,
            "decision_id": f"team_b_error_{uuid.uuid4()}",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    
    async def get_organizational_context(self, requester: str) -> Dict[str, Any]:
        """Get organizational context for a requester."""
        if self.team_b_available:
            try:
                # Call real Team B organizational API
                org_context = await self.privacy_firewall_api.get_employee_context(requester)
                return org_context
            except Exception as e:
                print(f"⚠️  Team B org context failed: {e}")
        
        # Fallback to mock data
        employee_info = self.organizational_data["employees"].get(requester, {})
        return {
            "employee_id": requester,
            "department": employee_info.get("department", "unknown"),
            "role": employee_info.get("role", "unknown"), 
            "clearance_level": employee_info.get("clearance", "none"),
            "integration": "mock_fallback"
        }

# Export the integration class
__all__ = ["TeamBIntegration"]