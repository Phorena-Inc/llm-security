#!/usr/bin/env python3
"""
Multi-Team Integration Test: Team A + Team B + Team C
===================================================

Comprehensive test of the fully integrated privacy decision system combining:
- Team A: Temporal Framework (6-tuple contextual integrity)
- Team B: Privacy Firewall (organizational policies)  
- Team C: AI Privacy Decisions (semantic classification)

Tests both real integrations and fallback scenarios.

Author: Team C Privacy Firewall
Date: 2024-12-09
Integration: Multi-Team Direct Python
"""

import asyncio
import sys
import os
from pathlib import Path
from datetime import datetime

# Add Team C integration path
team_c_path = str(Path(__file__).parent)
sys.path.insert(0, team_c_path)

# Add graphiti parent path for Team B integration
graphiti_root = str(Path(__file__).parent.parent)
sys.path.insert(0, graphiti_root)

from integration.enhanced_graphiti_privacy_bridge import EnhancedGraphitiPrivacyBridge

class MultiTeamIntegrationTest:
    """Comprehensive test suite for Team A + Team B + Team C integration."""
    
    def __init__(self):
        """Initialize the multi-team test environment."""
        print("🚀 Multi-Team Integration Test")
        print("=" * 60)
        print("Testing: Team A (Temporal) + Team B (Org Policies) + Team C (AI)")
        print()
        
        # Initialize Team C bridge with multi-team integration
        self.bridge = EnhancedGraphitiPrivacyBridge(
            neo4j_password=os.getenv('NEO4J_PASSWORD', 'skyber123'),
            openai_api_key=os.getenv('OPENAI_API_KEY'),
            team_a_endpoint="http://localhost:8000"
        )
        
        # Test scenarios using real employees from Team B's organizational database
        self.test_scenarios = [
            {
                "name": "Medical Emergency Access",
                "description": "Doctor accessing patient medical data in emergency",
                "request": {
                    "requester": "medical_doctor",  # External - should use emergency override
                    "data_field": "patient_medical_records",
                    "purpose": "emergency_treatment",
                    "context": "ICU patient requires immediate medical intervention",
                    "emergency": True,
                    "location": "America/New_York"
                },
                "expected": "ALLOW"
            },
            {
                "name": "HR Employee Data Access", 
                "description": "HR specialist accessing employee salary data",
                "request": {
                    "requester": "Jennifer Williams",  # Real HR employee (emp-003)
                    "data_field": "employee_salary_data",
                    "purpose": "compliance_audit", 
                    "context": "Annual salary review and compliance audit",
                    "emergency": False,
                    "location": "America/Los_Angeles"
                },
                "expected": "ALLOW"  # HR should access employee data
            },
            {
                "name": "Sales Customer Data",
                "description": "Sales manager accessing customer data for outreach",
                "request": {
                    "requester": "Michael O'Brien",  # Real Enterprise Sales manager (emp-022)
                    "data_field": "customer_email_addresses", 
                    "purpose": "campaign_personalization",
                    "context": "Approved marketing campaign for Q4 product launch",
                    "emergency": False,
                    "location": "Europe/London"
                },
                "expected": "ALLOW"  # Sales should access customer data
            },
            {
                "name": "Contractor Source Code Access",
                "description": "External contractor trying to access source code",
                "request": {
                    "requester": "contractor",  # External - should be denied
                    "data_field": "source_code",
                    "purpose": "system_maintenance", 
                    "context": "External contractor for temporary project",
                    "emergency": False,
                    "location": "Asia/Singapore"
                },
                "expected": "DENY"  # Contractors should be restricted
            },
            {
                "name": "Finance Team Revenue Data",
                "description": "Finance team member accessing customer purchase data",
                "request": {
                    "requester": "Rachel Green",  # Real Finance team member (emp-023)
                    "data_field": "customer_purchase_history",
                    "purpose": "revenue_analysis",
                    "context": "Quarterly financial reporting and revenue analysis", 
                    "emergency": False,
                    "location": "America/Chicago"
                },
                "expected": "ALLOW"  # Finance team should access financial data
            },
            {
                "name": "Cross-Department API Access",
                "description": "Engineering lead accessing financial APIs",
                "request": {
                    "requester": "Priya Patel",  # Real Backend Engineering lead (emp-007)
                    "data_field": "api_keys",
                    "purpose": "system_integration",
                    "context": "Setting up payment processing integration",
                    "emergency": False,
                    "location": "America/Denver"
                },
                "expected": "DENY"  # Cross-department access should be restricted
            }
        ]
    
    async def run_comprehensive_test(self):
        """Run all test scenarios and analyze results."""
        print("🧪 Running Multi-Team Integration Test Scenarios")
        print("=" * 60)
        
        results = []
        
        for i, scenario in enumerate(self.test_scenarios, 1):
            print(f"\n📋 Test {i}: {scenario['name']}")
            print(f"   Description: {scenario['description']}")
            print(f"   Expected: {scenario['expected']}")
            print()
            
            try:
                # Run the multi-team integrated decision (WITHOUT storage)
                start_time = datetime.now()
                decision = await self.bridge.make_multi_team_decision_only(scenario['request'])
                end_time = datetime.now()
                
                # Analyze results
                result = self._analyze_decision_result(scenario, decision, start_time, end_time)
                results.append(result)
                
                # Print result
                self._print_scenario_result(result)
                
            except Exception as e:
                print(f"❌ Test {i} FAILED: {e}")
                import traceback
                traceback.print_exc()
                results.append({
                    "scenario": scenario['name'],
                    "status": "ERROR",
                    "error": str(e)
                })
        
        # Print comprehensive summary
        self._print_test_summary(results)
        
        return results
    
    def _analyze_decision_result(self, scenario, decision, start_time, end_time):
        """Analyze the decision result against expected outcome."""
        
        # Extract key information
        allowed = decision.get('allowed', False)
        reason = decision.get('reason', 'No reason')
        confidence = decision.get('confidence', 0.0)
        
        # Multi-team analysis
        multi_team = decision.get('multi_team_decision', {})
        team_a_result = multi_team.get('team_a_result', {})
        team_b_result = multi_team.get('team_b_result', {})
        
        # Performance metrics
        response_time_ms = (end_time - start_time).total_seconds() * 1000
        
        # Determine test result
        actual_decision = "ALLOW" if allowed else "DENY"
        expected = scenario['expected']
        
        if expected == "CONDITIONAL":
            status = "PASS"  # Conditional means either outcome is acceptable
        else:
            status = "PASS" if actual_decision == expected else "FAIL"
        
        return {
            "scenario": scenario['name'],
            "status": status,
            "expected": expected,
            "actual": actual_decision,
            "decision": decision,
            "analysis": {
                "allowed": allowed,
                "reason": reason,
                "confidence": confidence,
                "response_time_ms": response_time_ms,
                "team_integration": {
                    "team_a": {
                        "active": team_a_result.get('team_a_integration', False),
                        "decision": "ALLOW" if team_a_result.get('allowed') else "DENY", 
                        "reason": team_a_result.get('reason', 'Unknown'),
                        "confidence": team_a_result.get('confidence', 0.0)
                    },
                    "team_b": {
                        "active": bool(team_b_result.get('allowed') is not None),
                        "decision": "ALLOW" if team_b_result.get('allowed') else "DENY", 
                        "reason": team_b_result.get('reason', 'Unknown'),
                        "confidence": team_b_result.get('confidence', 0.0)
                    }
                }
            }
        }
    
    def _print_scenario_result(self, result):
        """Print detailed result for a single scenario."""
        status_icon = "✅" if result['status'] == "PASS" else "❌" if result['status'] == "FAIL" else "⚠️"
        
        print(f"{status_icon} {result['status']}: {result['scenario']}")
        print(f"   Expected: {result['expected']} | Actual: {result['actual']}")
        print(f"   Decision: {'ALLOWED' if result['analysis']['allowed'] else 'DENIED'}")
        print(f"   Confidence: {result['analysis']['confidence']:.2f}")
        print(f"   Response Time: {result['analysis']['response_time_ms']:.1f}ms")
        print(f"   Reason: {result['analysis']['reason'][:100]}...")
        
        # Team integration status
        team_a = result['analysis']['team_integration']['team_a']
        team_b = result['analysis']['team_integration']['team_b']
        
        print(f"   Team A: {'✅' if team_a['active'] else '❌'} {team_a['decision']} ({team_a['confidence']:.2f})")
        print(f"   Team B: {'✅' if team_b['active'] else '❌'} {team_b['decision']} ({team_b['confidence']:.2f})")
        print()
    
    def _print_test_summary(self, results):
        """Print comprehensive test summary."""
        print("\n" + "=" * 60)
        print("🎯 MULTI-TEAM INTEGRATION TEST SUMMARY")
        print("=" * 60)
        
        # Count results
        total_tests = len(results)
        passed = sum(1 for r in results if r['status'] == 'PASS')
        failed = sum(1 for r in results if r['status'] == 'FAIL')
        errors = sum(1 for r in results if r['status'] == 'ERROR')
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"⚠️  Errors: {errors}")
        print(f"Success Rate: {(passed/total_tests)*100:.1f}%")
        
        # Performance analysis
        valid_results = [r for r in results if 'analysis' in r]
        if valid_results:
            avg_response_time = sum(r['analysis']['response_time_ms'] for r in valid_results) / len(valid_results)
            avg_confidence = sum(r['analysis']['confidence'] for r in valid_results) / len(valid_results)
            
            print(f"\nPerformance Metrics:")
            print(f"Average Response Time: {avg_response_time:.1f}ms")
            print(f"Average Confidence: {avg_confidence:.2f}")
        
        # Integration status
        team_a_active = sum(1 for r in valid_results if r['analysis']['team_integration']['team_a']['active'])
        team_b_active = sum(1 for r in valid_results if r['analysis']['team_integration']['team_b']['active'])
        
        print(f"\nIntegration Status:")
        print(f"Team A (Temporal): {team_a_active}/{total_tests} active")
        print(f"Team B (Org Policies): {team_b_active}/{total_tests} active")
        
        # Overall assessment
        print(f"\n🚀 INTEGRATION STATUS:")
        if passed == total_tests:
            print("✅ ALL TESTS PASSED - Multi-team integration working perfectly!")
        elif passed >= total_tests * 0.8:
            print("🟡 MOSTLY WORKING - Minor issues detected")
        else:
            print("🔴 INTEGRATION ISSUES - Significant problems detected")
        
        print("\n" + "=" * 60)

async def main():
    """Main test execution."""
    print("🔧 Multi-Team Privacy Integration Test Suite")
    print("Testing Team A + Team B + Team C combined decision making")
    print()
    
    # Initialize and run tests
    test_suite = MultiTeamIntegrationTest()
    results = await test_suite.run_comprehensive_test()
    
    # Return success/failure for CI/CD
    success_count = sum(1 for r in results if r['status'] == 'PASS')
    return 0 if success_count == len(results) else 1

if __name__ == "__main__":
    result = asyncio.run(main())
    sys.exit(result)