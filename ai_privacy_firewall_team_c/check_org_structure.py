#!/usr/bin/env python3

"""
Quick script to check the organizational structure and understand
why Team B's queries are failing.
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from privacy_firewall_integration.core.graphiti_client import GraphitiClient

async def check_organizational_structure():
    """Check what's actually in the Neo4j database"""
    
    client = GraphitiClient()
    
    try:
        # Check employees and their departments
        employee_query = """
        MATCH (e:Entity)-[r:RELATES_TO]->(d:Entity)
        WHERE e.name IN ['Jennifer Williams', "Michael O'Brien", 'Rachel Green', 'Priya Patel']
        AND (r.name = 'MEMBER_OF' OR r.fact CONTAINS 'member of' OR r.fact CONTAINS 'works in')
        RETURN e.name as employee, d.name as department, r.name as relationship, r.fact as fact
        ORDER BY employee
        """
        
        print("👥 Employee Department Relationships:")
        result = await client.driver.execute_query(employee_query)
        for record in result.records:
            print(f"  {record['employee']} -> {record['department']} ({record['relationship']}: {record['fact']})")
        
        if not result.records:
            print("  ❌ No department relationships found!")
            
            # Check what relationships these employees DO have
            all_rels_query = """
            MATCH (e:Entity)-[r:RELATES_TO]->(target:Entity)
            WHERE e.name IN ['Jennifer Williams', "Michael O'Brien", 'Rachel Green', 'Priya Patel']
            RETURN e.name as employee, target.name as target, r.name as rel_type, r.fact as fact
            ORDER BY employee
            """
            
            print("\n🔍 All relationships for these employees:")
            result = await client.driver.execute_query(all_rels_query)
            for record in result.records:
                print(f"  {record['employee']} -> {record['target']} ({record['rel_type']}: {record['fact']})")
        
        # Check if company_data exists
        company_data_query = """
        MATCH (n:Entity)
        WHERE n.name = 'company_data'
        RETURN n.name as name, n.id as id
        """
        
        print("\n🏢 Company Data Entity:")
        result = await client.driver.execute_query(company_data_query)
        if result.records:
            for record in result.records:
                print(f"  Found: {record['name']} (ID: {record['id']})")
        else:
            print("  ❌ No 'company_data' entity found!")
            
        # Check what entities DO exist
        all_entities_query = """
        MATCH (n:Entity)
        RETURN n.name as name, labels(n) as labels
        ORDER BY n.name
        LIMIT 20
        """
        
        print(f"\n📋 Sample entities in database:")
        result = await client.driver.execute_query(all_entities_query)
        for record in result.records:
            print(f"  {record['name']} ({record['labels']})")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(check_organizational_structure())