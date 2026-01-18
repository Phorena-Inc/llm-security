#!/usr/bin/env python3
"""
Test Team B Privacy Firewall API with real organizational data
"""

import sys
import os
from datetime import datetime
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.privacy_api import PrivacyFirewallAPI

def test_privacy_firewall():
    """Test the privacy firewall with real organizational scenarios"""
    
    print("🔐 Testing Team B Privacy Firewall API")
    print("=" * 60)
    
    try:
        # Initialize the API
        api = PrivacyFirewallAPI()
        
        # Test 1: Database connectivity and stats
        print("📊 Test 1: Database Connectivity")
        stats = api.get_database_stats()
        print(f"   ✅ Connected! Nodes: {stats.get('nodes', 'Unknown')}, Relationships: {stats.get('relationships', 'Unknown')}")
        
        # Test 2: Employee access scenarios
        print("\n👤 Test 2: Employee Access Control")
        
        # Test CEO access (should have broad access)
        access = api.check_employee_access(
            requester_id="sarah.chen@techflow.com",
            target_employee_id="priya.patel@techflow.com",
            access_type="view_profile"
        )
        print(f"   CEO → Engineer access: {'✅ GRANTED' if access['allowed'] else '❌ DENIED'}")
        print(f"   Reason: {access['reason']}")
        
        # Test peer access within same team
        access = api.check_employee_access(
            requester_id="carlos.martinez@techflow.com", 
            target_employee_id="emily.zhang@techflow.com",
            access_type="view_contact"
        )
        print(f"   Peer → Peer access: {'✅ GRANTED' if access['allowed'] else '❌ DENIED'}")
        print(f"   Reason: {access['reason']}")
        
        # Test cross-department access
        access = api.check_employee_access(
            requester_id="michael.obrien@techflow.com",  # Sales
            target_employee_id="alex.turner@techflow.com",  # Security
            access_type="view_salary"
        )
        print(f"   Cross-dept → Sensitive: {'✅ GRANTED' if access['allowed'] else '❌ DENIED'}")
        print(f"   Reason: {access['reason']}")
        
        # Test 3: Department-level access
        print("\n📂 Test 3: Department Access Control")
        
        access = api.check_department_access(
            requester_id="jennifer.williams@techflow.com",  # Operations exec
            department="Engineering",
            access_type="view_metrics"
        )
        print(f"   Executive → Department: {'✅ GRANTED' if access['allowed'] else '❌ DENIED'}")
        print(f"   Reason: {access['reason']}")
        
        # Test 4: Project access scenarios
        print("\n🎯 Test 4: Project Access Control")
        
        access = api.check_project_access(
            requester_id="priya.patel@techflow.com",  # Backend manager
            project_id="project_phoenix",
            access_type="read"
        )
        print(f"   Manager → Cross-functional project: {'✅ GRANTED' if access['allowed'] else '❌ DENIED'}")
        print(f"   Reason: {access['reason']}")
        
        # Test 5: Policy enforcement scenarios
        print("\n📋 Test 5: Policy Enforcement")
        
        # Time-based access (should work during business hours)
        current_time = datetime.now()
        print(f"   Current time: {current_time.strftime('%H:%M')} on {current_time.strftime('%A')}")
        
        access = api.check_time_based_access(
            requester_id="marcus.johnson@techflow.com",
            resource="financial_reports",
            current_time=current_time
        )
        print(f"   Time-based access: {'✅ GRANTED' if access['allowed'] else '❌ DENIED'}")
        print(f"   Reason: {access['reason']}")
        
        # Test 6: Sensitive data classification
        print("\n🔒 Test 6: Data Classification")
        
        classification = api.classify_data_sensitivity("employee_salary_information")
        print(f"   Salary data classification: {classification['level']} ({classification['description']})")
        
        classification = api.classify_data_sensitivity("employee_public_profile")
        print(f"   Profile data classification: {classification['level']} ({classification['description']})")
        
        # Test 7: Audit logging
        print("\n📝 Test 7: Audit Logging")
        
        audit_id = api.log_access_attempt(
            requester_id="test.user@techflow.com",
            resource="employee_database", 
            action="query",
            result="granted",
            reason="Manager accessing direct reports"
        )
        print(f"   ✅ Audit logged with ID: {audit_id}")
        
        print("\n" + "=" * 60)
        print("✅ Privacy Firewall API Tests Complete!")
        print("🔐 System is ready for Team C integration")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_privacy_firewall()
    sys.exit(0 if success else 1)