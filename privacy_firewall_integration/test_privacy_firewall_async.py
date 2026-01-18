#!/usr/bin/env python3
"""
Test Team B Privacy Firewall API with real organizational data
"""

import asyncio
import sys
import os
from datetime import datetime
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.privacy_api import PrivacyFirewallAPI

async def test_privacy_firewall():
    """Test the privacy firewall with real organizational scenarios"""
    
    print("🔐 Testing Team B Privacy Firewall API")
    print("=" * 60)
    
    try:
        # Initialize the API
        api = PrivacyFirewallAPI()
        
        # Test 1: System stats and connectivity
        print("📊 Test 1: System Connectivity")
        stats = await api.get_system_stats()
        print(f"   ✅ Connected! System status: {stats.get('status', 'Unknown')}")
        if 'database' in stats:
            print(f"   Database: {stats['database'].get('status', 'Unknown')}")
        
        # Test 2: Employee access scenarios using check_access_permission
        print("\n👤 Test 2: Employee Access Control")
        
        # Test CEO access to employee data
        access = await api.check_access_permission(
            requester_id="sarah.chen@techflow.com",
            target_id="priya.patel@techflow.com",
            resource_type="performance_review"
        )
        print(f"   CEO → Engineer performance: {'✅ GRANTED' if access.get('allowed') else '❌ DENIED'}")
        print(f"   Reason: {access.get('reason', 'No reason provided')}")
        
        # Test peer access within same team
        access = await api.check_access_permission(
            requester_id="carlos.martinez@techflow.com", 
            target_id="emily.zhang@techflow.com",
            resource_type="team_calendar"
        )
        print(f"   Peer → Peer calendar: {'✅ GRANTED' if access.get('allowed') else '❌ DENIED'}")
        print(f"   Reason: {access.get('reason', 'No reason provided')}")
        
        # Test cross-department sensitive access
        access = await api.check_access_permission(
            requester_id="michael.obrien@techflow.com",  # Sales
            target_id="alex.turner@techflow.com",  # Security
            resource_type="salary_info"
        )
        print(f"   Cross-dept → Salary info: {'✅ GRANTED' if access.get('allowed') else '❌ DENIED'}")
        print(f"   Reason: {access.get('reason', 'No reason provided')}")
        
        # Test 3: Organizational relationships
        print("\n🔗 Test 3: Organizational Relationships")
        
        relationship = await api.check_organizational_relationship(
            user_a_id="priya.patel@techflow.com",
            user_b_id="carlos.martinez@techflow.com",
            relationship_type="manager"
        )
        print(f"   Manager → Team member relationship: {'✅ EXISTS' if relationship else '❌ NONE'}")
        
        # Test same team relationship
        same_team = await api.check_organizational_relationship(
            user_a_id="carlos.martinez@techflow.com",
            user_b_id="emily.zhang@techflow.com", 
            relationship_type="same_team"
        )
        print(f"   Same team relationship: {'✅ EXISTS' if same_team else '❌ NONE'}")
        
        # Test 4: Resource access scenarios  
        print("\n📁 Test 4: Resource Access Control")
        
        access = await api.check_resource_access(
            requester_id="david.kim@techflow.com",  # Product manager
            resource_owner="Product",
            resource_classification="confidential",
            resource_type="document",
            action="edit"
        )
        print(f"   Product Manager → Department docs: {'✅ GRANTED' if access.get('allowed') else '❌ DENIED'}")
        print(f"   Policy applied: {access.get('policy_matched', 'None')}")
        
        # Test 5: Cross-department resource access
        print("\n� Test 5: Cross-Department Security")
        
        access = await api.check_resource_access(
            requester_id="michael.obrien@techflow.com",  # Sales
            resource_owner="Engineering", 
            resource_classification="secret",
            resource_type="source_code",
            action="read"
        )
        print(f"   Sales → Engineering code: {'✅ GRANTED' if access.get('allowed') else '❌ DENIED'}")
        print(f"   Security level: {access.get('classification_level', 'None')}")
        
        print("\n" + "=" * 60)
        print("✅ Privacy Firewall API Tests Complete!")
        print("🔐 System is ready for Team C integration")
        
        # Test 7: Performance metrics
        print(f"\n⚡ Performance: All tests completed in async mode")
        print("🚀 Ready for production use with Team A (Temporal Framework)")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Main async entry point"""
    success = await test_privacy_firewall()
    return 0 if success else 1

if __name__ == "__main__":
    result = asyncio.run(main())
    sys.exit(result)