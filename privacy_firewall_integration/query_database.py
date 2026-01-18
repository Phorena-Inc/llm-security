"""
Neo4j Database Query Script

This script queries the Neo4j database to understand the current state
and fix the organizational relationship issues.
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from core.graphiti_client import GraphitiClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def query_database_entities():
    """Query database to see what entities exist"""
    
    client = GraphitiClient()
    
    try:
        # Query all entities
        query = """
        MATCH (n:Entity)
        RETURN n.name as name, n.id as id, labels(n) as labels
        LIMIT 50
        """
        
        result = await client.driver.execute_query(query)
        
        logger.info("📊 Entities in Neo4j Database:")
        logger.info("=" * 50)
        
        entities = []
        for record in result.records:
            name = record.get('name', 'Unknown')
            entity_id = record.get('id', 'Unknown')
            labels = record.get('labels', [])
            entities.append({"name": name, "id": entity_id, "labels": labels})
            logger.info(f"  {name} (ID: {entity_id}) - Labels: {labels}")
        
        logger.info(f"📈 Total entities found: {len(entities)}")
        
        # Query relationships
        logger.info("\n🔗 Relationships in Database:")
        logger.info("=" * 50)
        
        rel_query = """
        MATCH (a:Entity)-[r:RELATES_TO]->(b:Entity)
        RETURN a.name as from_name, r.name as rel_type, r.fact as fact, b.name as to_name
        LIMIT 20
        """
        
        rel_result = await client.driver.execute_query(rel_query)
        
        relationships = []
        for record in rel_result.records:
            from_name = record.get('from_name', 'Unknown')
            rel_type = record.get('rel_type', 'Unknown')
            fact = record.get('fact', 'Unknown')
            to_name = record.get('to_name', 'Unknown')
            relationships.append({
                "from": from_name,
                "type": rel_type,
                "fact": fact,
                "to": to_name
            })
            logger.info(f"  {from_name} --[{rel_type}: {fact}]--> {to_name}")
        
        logger.info(f"🔗 Total relationships found: {len(relationships)}")
        
        # Look specifically for users that match test cases
        test_users = ['marketing_manager', 'financial_analyst', 'engineering_lead', 'hr_specialist', 'medical_doctor', 'contractor']
        
        logger.info(f"\n🔍 Checking for test users:")
        logger.info("=" * 50)
        
        for user in test_users:
            user_query = """
            MATCH (n:Entity)
            WHERE n.id = $user_id OR n.name CONTAINS $user_name
            RETURN n.name as name, n.id as id, labels(n) as labels
            """
            
            user_result = await client.driver.execute_query(
                user_query, 
                user_id=user, 
                user_name=user.replace('_', ' ').title()
            )
            
            if user_result.records:
                for record in user_result.records:
                    name = record.get('name', 'Unknown')
                    entity_id = record.get('id', 'Unknown')
                    labels = record.get('labels', [])
                    logger.info(f"  ✅ Found: {user} -> {name} (ID: {entity_id}) - Labels: {labels}")
            else:
                logger.info(f"  ❌ Missing: {user}")
        
        return {"entities": entities, "relationships": relationships}
        
    except Exception as e:
        logger.error(f"❌ Database query failed: {e}")
        return None


async def main():
    """Main execution function"""
    try:
        logger.info("🚀 Querying Neo4j database state...")
        result = await query_database_entities()
        
        if result:
            logger.info("✅ Database query completed successfully")
            return 0
        else:
            logger.error("❌ Database query failed")
            return 1
            
    except Exception as e:
        logger.error(f"❌ Execution failed: {e}")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)