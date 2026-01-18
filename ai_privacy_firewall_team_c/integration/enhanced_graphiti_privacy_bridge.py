#!/usr/bin/env python3
"""
Enhanced Graphiti Privacy Bridge with Timezone Awareness
======================================================

This module bridges Team C's privacy ontology with Graphiti knowledge graph storage.
Uses Graphiti's higher-level abstraction for natural language to Cypher translation
with proper timestamp handling and timezone awareness for global team integration.

Key Features:
- Timezone-aware timestamp formatting for Graphiti LLM processing
- Business hours consideration for policy enforcement
- Natural language episode content for better LLM translation
- Proper ISO 8601 timestamp formatting with Z suffix

Author: Team C Privacy Firewall
Date: 2024-12-30
"""

import sys
import os
import json
from pathlib import Path
import uuid
from datetime import datetime, timezone, timedelta
import asyncio
from typing import Dict, List, Any, Optional

# Add parent directory to path
parent_dir = str(Path(__file__).parent.parent)
sys.path.append(parent_dir)

# Add Graphiti core path
graphiti_path = str(Path(__file__).parent.parent.parent / "graphiti_core")
sys.path.append(graphiti_path)

try:
    from graphiti_core import Graphiti
    from graphiti_core.nodes import EntityNode, EpisodicNode, EpisodeType
    from graphiti_core.edges import EntityEdge, EpisodicEdge
    from graphiti_core.utils.datetime_utils import utc_now
    GRAPHITI_AVAILABLE = True
    print("✅ Graphiti core imported successfully")
except ImportError as e:
    print(f"⚠️  Graphiti core not available: {e}")
    print("   Falling back to direct Neo4j for now...")
    GRAPHITI_AVAILABLE = False

# Always import Neo4j for fallback
try:
    from neo4j import AsyncGraphDatabase
    NEO4J_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Neo4j driver not available: {e}")
    NEO4J_AVAILABLE = False

# Import privacy ontology and timezone utilities
from ontology.privacy_ontology import AIPrivacyOntology
from integration.timezone_utils import TimezoneHandler
from integration.team_a_models import TeamAIntegrationClient, EnhancedContextualIntegrityTuple, TemporalContext
# Note: Removed Groq imports - now using OpenAI directly

# Load environment variables
try:
    from dotenv import load_dotenv
    # Explicitly load .env from current directory
    env_path = Path(__file__).parent.parent / '.env'
    load_dotenv(env_path)
    print(f"✅ Loaded environment from: {env_path}")
except ImportError:
    print("⚠️  python-dotenv not available, using environment variables directly")

class EnhancedGraphitiPrivacyBridge:
    """
    Enhanced privacy bridge with timezone awareness and proper timestamp handling.
    
    Uses Graphiti's higher-level abstraction with LLM-powered natural language
    to Cypher translation, ensuring proper temporal data for policy enforcement.
    """
    
    def __init__(self, neo4j_uri="bolt://localhost:7687", 
                 neo4j_user="neo4j", neo4j_password="12345678", 
                 openai_api_key=None, team_a_endpoint="http://localhost:8000"):
        self.neo4j_uri = neo4j_uri
        self.neo4j_user = neo4j_user
        self.neo4j_password = neo4j_password
        self.ontology = AIPrivacyOntology()
        self.openai_client = None
        self.team_a_client = TeamAIntegrationClient(team_a_endpoint)
        
        # Initialize OpenAI LLM client if API key available
        self._init_openai_client(openai_api_key)
        
        if GRAPHITI_AVAILABLE:
            self._init_graphiti()
        else:
            self._init_neo4j_fallback()
    
    def _init_openai_client(self, openai_api_key=None):
        """Initialize OpenAI LLM client for privacy decisions."""
        try:
            # Get API key from parameter or environment
            api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
            
            if api_key:
                # Set environment variable for Graphiti to use
                os.environ["OPENAI_API_KEY"] = api_key
                
                # Set model from environment or default
                model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
                os.environ["OPENAI_MODEL"] = model
                
                print(f"✅ OpenAI API configured with {model}")
                print(f"   Key: {api_key[:20]}...")
                print("   Using OpenAI for privacy decision intelligence")
                self.openai_enabled = True
            else:
                print("⚠️  OPENAI_API_KEY not found, using fallback decision logic")
                self.openai_enabled = False
        except Exception as e:
            print(f"⚠️  OpenAI initialization failed: {e}")
            print("   Using fallback decision logic")
            self.openai_enabled = False
    
    def _init_graphiti(self):
        """Initialize Graphiti with OpenAI."""
        try:
            # Check if we have the OpenAI API key
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                print("⚠️  No OPENAI_API_KEY found, falling back to Neo4j")
                self._init_neo4j_fallback()
                return
            
            # Get Neo4j password from environment
            neo4j_password = os.getenv('NEO4J_PASSWORD', self.neo4j_password)
            
            # Initialize Graphiti with OpenAI (no custom client needed)
            self.graphiti = Graphiti(
                uri=self.neo4j_uri,
                user=self.neo4j_user,
                password=neo4j_password
            )
            self.use_graphiti = True
            
            model = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
            print(f"✅ Graphiti initialized with OpenAI at {self.neo4j_uri}")
            print(f"   Using OpenAI {model} for LLM reasoning")
            print(f"   Neo4j password: {neo4j_password}")
            
            # Also initialize Neo4j driver for fallback scenarios
            if NEO4J_AVAILABLE:
                self.driver = AsyncGraphDatabase.driver(
                    self.neo4j_uri,
                    auth=(self.neo4j_user, neo4j_password)
                )
                print(f"✅ Neo4j fallback driver initialized")
            
        except Exception as e:
            print(f"❌ Graphiti initialization failed: {e}")
            print("   Falling back to direct Neo4j")
            self._init_neo4j_fallback()
            print(f"   Model: llama-3.3-70b-versatile")
            print(f"   API Key: {api_key[:20]}...")
        except Exception as e:
            print(f"⚠️  Graphiti initialization failed: {e}")
            print("   Falling back to Neo4j...")
            self._init_neo4j_fallback()
    
    def _init_neo4j_fallback(self):
        """Initialize Neo4j fallback for development."""
        if not NEO4J_AVAILABLE:
            raise ImportError("Neo4j driver not available and Graphiti initialization failed")
            
        self.driver = AsyncGraphDatabase.driver(
            self.neo4j_uri,
            auth=(self.neo4j_user, self.neo4j_password)
        )
        self.use_graphiti = False
        print(f"✅ Neo4j fallback initialized at {self.neo4j_uri}")
    
    async def create_privacy_decision_episode(self, privacy_request: dict):
        """
        Create privacy decision record with timezone-aware timestamps.
        
        Current: Team A integration only
        Future: Will add Team B integration and combine decisions before storage
        """
        
        print(f"🔍 DEBUG: openai_enabled = {self.openai_enabled}")
        print(f"🔍 DEBUG: privacy_request = {privacy_request}")
        
        try:
            # Get Team A decision (no storage yet)
            print("🔍 DEBUG: Calling Team A integrated decision")
            decision = await self.make_team_a_integrated_decision(privacy_request)
            print(f"✅ Team A integration decision: {'ALLOW' if decision['allowed'] else 'DENY'}")
            print(f"🔍 DEBUG: Team A decision = {decision}")
            
            # TODO: Add Team B integration here later
            # TODO: Combine Team A + Team B decisions
            
            # For now, use Team A decision as final decision
            # Later: This will be the combined decision from Team A + Team B
            final_decision = decision
            
        except Exception as e:
            print(f"⚠️  Team A integration failed: {e}, falling back to LLM")
            final_decision = await self.make_enhanced_privacy_decision(privacy_request)
        
        # NOW store the final decision (currently just Team A, later will be combined)
        return await self.store_decision_episode(final_decision, privacy_request)
    
    async def store_decision_episode(self, decision: dict, privacy_request: dict):
        """Store the final privacy decision episode (separated from decision logic)."""
        print("💾 Storing final privacy decision episode...")
        
        # Use existing storage logic but as separate method
        current_time = datetime.now(timezone.utc)
        formatted_timestamp = TimezoneHandler.format_for_graphiti(current_time)
        requester_location = privacy_request.get('location', 'UTC')
        
        # Prepare Team A integration info if present
        team_a_info = ""
        if decision.get('team_a_integration', False):
            team_a_info = f"""
Team A Temporal Framework Integration:
Decision ID: {decision.get('decision_id', 'N/A')}
Policy Matched: {decision.get('policy_matched', 'N/A')}
Emergency Override: {decision.get('emergency_override', False)}
Urgency Level: {decision.get('urgency_level', 'N/A')}
Time Window Valid: {decision.get('time_window_valid', 'N/A')}
Audit Required: {decision.get('audit_required', False)}"""

        episode_content = f"""PrivacyBot ({formatted_timestamp}): Privacy decision processed for data access request.

Requester ({formatted_timestamp}): {privacy_request['requester']} requested access to {privacy_request['data_field']} for {privacy_request['purpose']}

PrivacyBot ({formatted_timestamp}): Decision: {'ALLOWED' if decision.get('allowed', False) else 'DENIED'}
Reason: {decision.get('reason', 'No reason provided')}
Confidence: {decision.get('confidence', 0.0)}
Context: {privacy_request.get('context', 'General request')}
Emergency Override: {'Active' if privacy_request.get('emergency', False) else 'None'}{team_a_info}

BusinessContext ({formatted_timestamp}): {TimezoneHandler.get_business_context(requester_location, current_time)}"""
        
        try:
            # Add episode to Graphiti
            result = await self.graphiti.add_episode(
                name=f"Privacy Decision: {privacy_request['data_field']} at {formatted_timestamp}",
                episode_body=episode_content,
                source_description="Team C Privacy Firewall Decision",
                reference_time=current_time,
                source=EpisodeType.message if GRAPHITI_AVAILABLE else "message",
                group_id="team_c_privacy"
            )
            
            print(f"✅ Created Graphiti privacy decision episode: {result.episode_uuid if hasattr(result, 'episode_uuid') else 'generated'}")
            print(f"   Decision: {'ALLOWED' if decision['allowed'] else 'DENIED'}")
            print(f"   Timestamp: {formatted_timestamp}")
            
            return decision
            
        except Exception as e:
            print(f"⚠️  Graphiti episode creation failed: {e}")
            print("   Falling back to Neo4j...")
            return await self._create_episode_neo4j_fallback(privacy_request, decision)
    
    async def get_team_a_decision(self, privacy_request: dict):
        """Get Team A decision without storing it."""
        try:
            # Primary: Team A temporal framework integration
            print("🔍 DEBUG: Calling Team A integrated decision")
            decision = await self.make_team_a_integrated_decision(privacy_request)
            print(f"🔍 DEBUG: Team A decision = {decision}")
            return decision
        except Exception as e:
            print(f"⚠️  Team A integration failed: {e}, falling back to LLM")
            
            if self.openai_enabled:
                try:
                    print("🔍 DEBUG: Calling make_enhanced_privacy_decision")
                    decision = await self.make_enhanced_privacy_decision(privacy_request)
                    print(f"🔍 DEBUG: LLM decision = {decision}")
                    return decision
                except Exception as e:
                    print(f"⚠️  LLM decision failed: {e}, falling back to rule-based")
                    import traceback
                    traceback.print_exc()
                    return self.ontology.make_privacy_decision(
                        requester=privacy_request["requester"],
                        data_field=privacy_request["data_field"], 
                        purpose=privacy_request["purpose"],
                        context=privacy_request.get("context"),
                        emergency=privacy_request.get("emergency", False)
                    )
            else:
                # Fallback to rule-based decision
                return self.ontology.make_privacy_decision(
                    requester=privacy_request["requester"],
                    data_field=privacy_request["data_field"], 
                    purpose=privacy_request["purpose"],
                    context=privacy_request.get("context"),
                    emergency=privacy_request.get("emergency", False)
                )
    
    async def get_team_b_decision(self, privacy_request: dict):
        """Get Team B (Semantic Handoff) decision - TODO: Not implemented yet."""
        print("🔍 Team B integration: Not yet implemented, using placeholder")
        
        # TODO: Replace with actual Team B integration
        # For now, return a placeholder decision
        return {
            "allowed": True,  # Placeholder - Team B would evaluate semantic context
            "reason": "Team B semantic analysis pending implementation",
            "confidence": 0.7,
            "team_b_integration": True,
            "semantic_context": "placeholder"
        }
    
    async def make_final_team_c_decision(self, team_a_decision: dict, team_b_decision: dict, privacy_request: dict):
        """Combine Team A and Team B decisions into final Team C decision."""
        print("🧠 Team C: Combining Team A and Team B decisions")
        
        # Simple combination logic (can be enhanced later)
        team_a_allowed = team_a_decision.get('allowed', False)
        team_b_allowed = team_b_decision.get('allowed', False)
        
        # Both teams must allow for final approval
        final_allowed = team_a_allowed and team_b_allowed
        
        # Combine confidence scores
        team_a_confidence = team_a_decision.get('confidence', 0.0)
        team_b_confidence = team_b_decision.get('confidence', 0.0)
        final_confidence = (team_a_confidence + team_b_confidence) / 2
        
        # Generate combined reason
        if final_allowed:
            final_reason = f"Approved by both Team A ({team_a_decision.get('reason', '')}) and Team B ({team_b_decision.get('reason', '')})"
        else:
            denied_by = []
            if not team_a_allowed:
                denied_by.append(f"Team A: {team_a_decision.get('reason', '')}")
            if not team_b_allowed:
                denied_by.append(f"Team B: {team_b_decision.get('reason', '')}")
            final_reason = f"Denied by {'; '.join(denied_by)}"
        
        return {
            "allowed": final_allowed,
            "reason": final_reason,
            "confidence": final_confidence,
            "team_a_decision": team_a_decision,
            "team_b_decision": team_b_decision,
            "method": "team_c_combined",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    async def make_multi_team_decision_only(self, privacy_request: dict):
        """
        Make multi-team integrated decision (Team A + Team B + Team C) without storage.
        This is the main method for testing multi-team integration.
        """
        print("🚀 Making Multi-Team Integrated Decision (Team A + Team B + Team C)")
        
        # Step 1: Get Team A decision (temporal framework)
        print("⏰ Consulting Team A (Temporal Framework)...")
        team_a_decision = await self.make_team_a_integrated_decision(privacy_request)
        
        # Step 2: Get Team B decision (organizational policies)
        print("🏢 Consulting Team B (Organizational Policies)...")
        team_b_decision = await self._make_team_b_decision(privacy_request)
        
        # Step 3: Team C combines both decisions with intelligent override logic
        print("🧠 Team C: Applying decision combination logic...")
        
        # Enhanced decision combination with emergency and organizational overrides
        team_a_allowed = team_a_decision.get('allowed', False)
        team_b_allowed = team_b_decision.get('allowed', False)
        emergency_override = privacy_request.get('emergency', False)
        
        # Check for organizational override (HR, Finance, Medical professionals)
        requester = privacy_request.get('requester', '').lower()
        organizational_override = any(role in requester for role in ['hr', 'finance', 'doctor', 'medical', 'cfo', 'executive'])
        
        # Decision combination logic with overrides
        if team_a_allowed and team_b_allowed:
            # Both teams allow - consensus approval
            final_decision = "ALLOW"
            method = "consensus_allow"
            confidence = (team_a_decision.get('confidence', 0.8) + team_b_decision.get('confidence', 0.8)) / 2 + 0.1
            reasoning = f"Consensus approval from both Team A (temporal) and Team B (organizational)"
            
        elif emergency_override and not team_b_allowed:
            # Emergency override case - Team A allows, Team B denies, but emergency
            final_decision = "ALLOW"
            method = "emergency_override" 
            confidence = 0.9
            reasoning = f"Emergency situation overrides Team B restrictions"
            
        elif organizational_override and not team_a_allowed:
            # Organizational override - Team B allows, Team A denies, but high-level access
            final_decision = "ALLOW"
            method = "organizational_override"
            confidence = 0.85
            reasoning = f"Organizational authority overrides Team A temporal restrictions"
            
        else:
            # Security priority - if either team denies without valid override
            final_decision = "DENY"
            method = "security_priority"
            confidence = max(team_a_decision.get('confidence', 0.8), team_b_decision.get('confidence', 0.8))
            reasoning = f"Security priority: Access denied by {'Team A' if not team_a_allowed else 'Team B'}"

        print(f"🎯 Final Decision: {final_decision} (Method: {method})")
        print(f"💪 Confidence: {confidence:.1%}")
        print(f"📝 Reasoning: {reasoning}")
        
        return {
            "decision": final_decision,
            "allowed": final_decision == "ALLOW",
            "method": method,
            "reason": reasoning,  # Changed from "reasoning" to "reason"
            "confidence": confidence,
            "emergency_override_used": emergency_override and final_decision == "ALLOW" and method == "emergency_override",
            "organizational_override_used": organizational_override and final_decision == "ALLOW" and method == "organizational_override",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "multi_team_integration": True,
            "multi_team_decision": {  # Added this structure for test compatibility
                "team_a_result": team_a_decision,
                "team_b_result": team_b_decision
            }
        }

    async def _make_team_b_decision(self, privacy_request: dict):
        """Make Team B organizational policy decision using direct Python integration."""
        print("🏢 Team B: Making organizational policy decision...")
        
        try:
            # Import Team B integration
            from .team_b_integration import TeamBIntegration
            
            # Create Team B instance
            team_b = TeamBIntegration()
            
            # Make decision using Team B's organizational policies
            decision = await team_b.make_team_b_decision(privacy_request)
            
            print(f"🏢 Team B Decision: {'ALLOW' if decision.get('allowed', False) else 'DENY'}")
            return decision
            
        except Exception as e:
            print(f"❌ Team B integration error: {e}")
            print("   Using fallback organizational logic...")
            
            # Fallback organizational logic
            requester = privacy_request.get('requester', '').lower()
            data_field = privacy_request.get('data_field', '').lower()
            
            # Simple organizational rules
            if 'hr' in requester and ('employee' in data_field or 'salary' in data_field):
                return {"allowed": True, "reason": "HR access to employee data", "confidence": 0.8}
            elif 'finance' in requester and ('revenue' in data_field or 'financial' in data_field):
                return {"allowed": True, "reason": "Finance team access to financial data", "confidence": 0.8}
            elif 'contractor' in requester:
                return {"allowed": False, "reason": "Contractor access restricted", "confidence": 0.9}
            else:
                return {"allowed": True, "reason": "Standard organizational access", "confidence": 0.7}

    async def _create_episode_with_graphiti(self, privacy_request: dict, decision: dict):
        """
        Create privacy decision episode using Graphiti's high-level abstraction.
        
        Uses natural language content with proper timestamp formatting for LLM-powered Cypher translation.
        Includes timezone awareness for global team integration.
        """
        try:
            episode_id = str(uuid.uuid4())
            
            # Get timezone-aware timestamp using Graphiti's datetime utilities
            current_time = utc_now() if GRAPHITI_AVAILABLE else TimezoneHandler.get_current_utc()
            requester_location = privacy_request.get('requester_location', 'utc')
            
            # Create properly formatted episode content following conversation pattern
            # This follows the shoe_conversation examples you provided
            formatted_timestamp = TimezoneHandler.format_for_graphiti(current_time, requester_location)
            
            # Enhanced episode content with Team A integration metadata
            team_a_info = ""
            if decision.get('team_a_integration', False):
                team_a_info = f"""

TeamAIntegration ({formatted_timestamp}): Enhanced temporal policy evaluation completed
Decision ID: {decision.get('decision_id', 'N/A')}
Policy Matched: {decision.get('policy_matched', 'N/A')}
Risk Level: {decision.get('risk_level', 'unknown')}
Expires At: {decision.get('expires_at', 'N/A')}
Next Review: {decision.get('next_review', 'N/A')}
Temporal Factors: {decision.get('temporal_factors', {})}"""

            episode_content = f"""PrivacyBot ({formatted_timestamp}): Privacy decision processed for data access request.

Requester ({formatted_timestamp}): {privacy_request['requester']} requested access to {privacy_request['data_field']} for {privacy_request['purpose']}

PrivacyBot ({formatted_timestamp}): Decision: {'ALLOWED' if decision.get('allowed', False) else 'DENIED'}
Reason: {decision.get('reason', 'No reason provided')}
Confidence: {decision.get('confidence', 0.0)}
Context: {privacy_request.get('context', 'General request')}
Emergency Override: {'Active' if privacy_request.get('emergency', False) else 'None'}{team_a_info}

BusinessContext ({formatted_timestamp}): {TimezoneHandler.get_business_context(requester_location, current_time)}"""
            
            # Add episode to Graphiti using correct API (let Graphiti generate UUID)
            result = await self.graphiti.add_episode(
                name=f"Privacy Decision: {privacy_request['data_field']} at {formatted_timestamp}",
                episode_body=episode_content,
                source_description="Team C Privacy Firewall Decision",
                reference_time=current_time,
                source=EpisodeType.message if GRAPHITI_AVAILABLE else "message",
                group_id="team_c_privacy"
            )
            
            print(f"✅ Created Graphiti privacy decision episode: {result.episode_uuid if hasattr(result, 'episode_uuid') else 'generated'}")
            print(f"   Decision: {'ALLOWED' if decision['allowed'] else 'DENIED'}")
            print(f"   LLM-powered reasoning stored in Graphiti knowledge graph")
            print(f"   Timestamp: {formatted_timestamp}")
            print(f"   Using LLM + Graphiti integration (no fallback needed)")
            
            return decision
            
        except Exception as e:
            print(f"⚠️  Graphiti episode creation failed: {e}")
            print("   Falling back to Neo4j...")
            return await self._create_episode_neo4j_fallback(privacy_request, decision)
    
    async def _create_data_entity_with_graphiti(self, data_field: str, classification: dict, timestamp: datetime):
        """
        Create data entity using Graphiti's EntityNode abstraction.
        
        Uses timezone-aware descriptive content for LLM understanding and proper temporal tracking.
        """
        try:
            entity_id = str(uuid.uuid4())
            
            # Create descriptive entity content with timestamp following conversation pattern
            formatted_timestamp = TimezoneHandler.format_for_graphiti(timestamp)
            
            entity_summary = f"""DataClassifier ({formatted_timestamp}): Classified data field '{data_field}'

Classification Results ({formatted_timestamp}):
- Data Type: {classification.get('data_type', 'Unknown')}
- Sensitivity Level: {classification.get('sensitivity_level', 'Unknown')} 
- PII Status: {'Contains PII' if classification.get('is_pii', False) else 'No PII detected'}
- Confidence: {classification.get('confidence', 0.0)}
- Reasoning: {classification.get('reasoning', 'Automated classification')}

SystemNote ({formatted_timestamp}): This data asset has been processed by Team C's Privacy Ontology for access control and policy enforcement."""
            
            # Create EntityNode with timezone-aware descriptive content
            data_entity = EntityNode(
                name=f"{data_field}",
                summary=entity_summary,
                labels=["DataField", "ClassifiedAsset", "TimezoneAware", classification.get('data_type', 'Unknown')],
                uuid=entity_id,
                group_id="team_c_privacy",
                created_at=timestamp
            )
            
            # Add entity to Graphiti
            await self.graphiti.add_entity_nodes([data_entity])
            
            print(f"✅ Created Graphiti data entity: {data_field}")
            
        except Exception as e:
            print(f"⚠️  Graphiti data entity creation failed: {e}")
    
    async def _create_episode_neo4j_fallback(self, privacy_request: dict, decision: dict):
        """Fallback method using direct Neo4j access with timezone awareness."""
        current_time = TimezoneHandler.get_current_utc()
        formatted_timestamp = TimezoneHandler.format_for_graphiti(current_time)
        
        async with self.driver.session() as session:
            result = await session.run("""
                CREATE (e:PrivacyDecisionEpisode {
                    uuid: $uuid,
                    name: $name,
                    requester: $requester,
                    data_field: $data_field,
                    purpose: $purpose,
                    context: $context,
                    decision: $decision,
                    reason: $reason,
                    confidence: $confidence,
                    emergency: $emergency,
                    timestamp: $timestamp,
                    iso_timestamp: $iso_timestamp,
                    created_at: datetime($created_at),
                    team: 'C',
                    team_a_integration: $team_a_integration,
                    decision_id: $decision_id,
                    policy_matched: $policy_matched,
                    risk_level: $risk_level,
                    expires_at: $expires_at,
                    next_review: $next_review
                })
                RETURN e.uuid as episode_id
            """, 
                uuid=str(uuid.uuid4()),
                name=f"Privacy Decision: {privacy_request['data_field']}",
                requester=privacy_request["requester"],
                data_field=privacy_request["data_field"],
                purpose=privacy_request["purpose"],
                context=privacy_request.get("context", ""),
                decision="ALLOWED" if decision["allowed"] else "DENIED",
                reason=decision["reason"],
                confidence=decision["confidence"],
                emergency=privacy_request.get("emergency", False),
                timestamp=formatted_timestamp,
                iso_timestamp=current_time.isoformat(),
                created_at=current_time.isoformat(),
                team_a_integration=decision.get("team_a_integration", False),
                decision_id=decision.get("decision_id"),
                policy_matched=decision.get("policy_matched"),
                risk_level=decision.get("risk_level", "unknown"),
                expires_at=decision.get("expires_at"),
                next_review=decision.get("next_review")
            )
            
            print(f"✅ Created Neo4j privacy decision (fallback)")
            print(f"   Decision: {'ALLOWED' if decision['allowed'] else 'DENIED'}")
            print(f"   Timestamp: {formatted_timestamp}")
            
            return decision
    
    async def classify_data_field(self, data_field: str, context: str = None):
        """
        Classify data field using Groq LLM intelligence or fallback logic.
        
        Args:
            data_field: The data field to classify
            context: Additional context about the data
            
        Returns:
            Classification result with data type and sensitivity
        """
        if self.openai_enabled:
            try:
                # Use OpenAI for intelligent classification via Graphiti
                # Note: For now using fallback since we don't have direct OpenAI client
                print("⚠️  Direct OpenAI classification not implemented yet")
                print("   Using fallback classification logic")
            except Exception as e:
                print(f"⚠️  OpenAI classification failed: {e}")
                print("   Using fallback classification logic")
        
        # Fallback to ontology-based classification with timezone tracking
        current_time = TimezoneHandler.get_current_utc()
        classification = self.ontology.classify_data_field(data_field, context)
        
        # Note: Entity relationships will be created when episode is added
        return classification
    
    async def make_team_a_integrated_decision(self, privacy_request: dict):
        """
        Make privacy decision using Team A's temporal policy engine integration.
        
        Creates proper Team A format and processes their enhanced response.
        """
        print("🔗 Making privacy decision via Team A temporal integration")
        
        try:
            # Create Team A compatible tuple
            tuple_data = self.team_a_client.create_temporal_tuple(
                privacy_request, 
                emergency=privacy_request.get("emergency", False)
            )
            
            # Format request for Team A
            team_a_request = self.team_a_client.format_request_for_team_a(tuple_data)
            
            print(f"📤 Sending to Team A: request_id={team_a_request['request_id']}")
            print(f"   Emergency Auth: {team_a_request.get('emergency_authorization_id', 'None')}")
            
            # TODO: Replace with actual HTTP call to Team A's endpoint
            # For now, simulate Team A's response format based on their exact examples
            simulated_team_a_response = {
                # Team A REQUIRED: Echo back the original request_id
                "request_id": team_a_request["request_id"],
                "decision": "ALLOW" if self._should_allow_request(privacy_request) else "DENY",
                "decision_id": f"decision_{uuid.uuid4()}",
                "evaluation_timestamp": datetime.now(timezone.utc).isoformat(),
                "confidence": 0.8 if privacy_request.get("emergency", False) else 0.6,
                "reasoning": self._get_decision_reason(privacy_request),  # Team A uses "reasoning" not "reasons"
                "policy_rule_matched": "team_c_integration_policy", 
                "emergency_override": tuple_data.temporal_context.emergency_override,
                # Team A REQUIRED: urgency_level in response
                "urgency_level": tuple_data.temporal_context.urgency_level,
                "time_window_valid": True,
                "audit_required": tuple_data.audit_required
            }
            
            # Parse Team A's response into Team C format
            decision = self.team_a_client.parse_team_a_response(simulated_team_a_response)
            
            print(f"📥 Received Team A decision: {'ALLOW' if decision['allowed'] else 'DENY'}")
            
            return decision
            
        except Exception as e:
            print(f"❌ Team A integration failed: {e}")
            print("   Falling back to local OpenAI decision")
            return await self.make_enhanced_privacy_decision(privacy_request)
    
    def _should_allow_request(self, privacy_request: dict) -> bool:
        """Team A temporal framework simulation logic."""
        requester = privacy_request.get("requester", "").lower()
        data_field = privacy_request.get("data_field", "").lower()
        purpose = privacy_request.get("purpose", "").lower()
        
        # Always allow emergency requests (Team A's emergency override)
        if privacy_request.get("emergency", False):
            return True
        
        # Medical staff accessing medical data
        if "medical" in data_field and any(role in requester for role in ["doctor", "medical", "physician"]):
            return True
        
        # HR access to employee data (normal business hours)
        if ("employee" in data_field or "salary" in data_field) and "hr" in requester:
            return True
            
        # Finance team accessing financial data (normal business context)
        if ("revenue" in data_field or "financial" in data_field or "purchase" in data_field) and "finance" in requester:
            return True
            
        # Sales accessing customer data for legitimate business purposes
        if ("customer" in data_field or "outreach" in purpose) and "sales" in requester:
            return True
            
        # Deny contractors accessing sensitive code/internal data
        if "contractor" in requester and ("source" in data_field or "code" in data_field or "api" in data_field):
            return False
            
        # Engineering accessing APIs should be restricted cross-department
        if "engineering" in requester and "financial" in data_field:
            return False
            
        # Default allow for most legitimate business access (Team A focuses on temporal context)
        # Team A would typically check time-based policies, business hours, etc.
        return True
    
    def _get_decision_reason(self, privacy_request: dict) -> str:
        """Get detailed reason for Team A temporal decision."""
        requester = privacy_request.get("requester", "").lower()
        data_field = privacy_request.get("data_field", "").lower()
        
        if self._should_allow_request(privacy_request):
            if privacy_request.get("emergency", False):
                return "Emergency temporal override: Critical access granted"
            elif "medical" in data_field and "doctor" in requester:
                return "Medical professional temporal access: Healthcare data approved"
            elif "hr" in requester and ("employee" in data_field or "salary" in data_field):
                return "HR temporal access: Employee data within business hours"
            elif "finance" in requester and ("revenue" in data_field or "financial" in data_field):
                return "Finance temporal access: Financial data within authorized timeframe"
            elif "sales" in requester and "customer" in data_field:
                return "Sales temporal access: Customer data for business outreach"
            else:
                return "Temporal framework: Standard business access approved"
        else:
            if "contractor" in requester:
                return "Temporal restriction: Contractor access outside permitted timeframe"
            elif "engineering" in requester and "financial" in data_field:
                return "Temporal boundary: Cross-department access restricted"
            else:
                return "Temporal policy: Access denied outside authorized time window"

    async def make_enhanced_privacy_decision(self, privacy_request: dict):
        """
        Make privacy decision using REAL OpenAI LLM intelligence.
        
        Uses actual OpenAI API calls instead of hardcoded rules.
        """
        print("🧠 Making REAL LLM-powered privacy decision via OpenAI API")
        
        try:
            # Import OpenAI for direct API calls
            from openai import AsyncOpenAI
            
            # Get API key from environment
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise Exception("No OpenAI API key found")
            
            # Create OpenAI client
            client = AsyncOpenAI(api_key=api_key)
            
            # Prepare the prompt for OpenAI
            prompt = f"""You are an AI Privacy Expert making access control decisions. Analyze this request and respond with a JSON decision.

REQUEST DETAILS:
- Requester: {privacy_request.get('requester', 'unknown')}
- Data Field: {privacy_request.get('data_field', 'unknown')}
- Purpose: {privacy_request.get('purpose', 'unknown')}
- Context: {privacy_request.get('context', 'unknown')}
- Emergency: {privacy_request.get('emergency', False)}

DECISION CRITERIA:
- Medical data should only be accessible to medical professionals or in emergencies
- Financial data should only be accessible to authorized financial personnel or auditors
- Personal data should have appropriate access controls
- Emergency situations may override normal restrictions
- Contractors/temporary staff should have limited access

Respond with a JSON object containing:
{{
  "allowed": true/false,
  "reasoning": "detailed explanation of the decision",
  "confidence": 0.0-1.0,
  "data_sensitivity": "low/medium/high/critical"
}}"""

            print("📡 Making OpenAI API call for privacy decision...")
            
            # Make real OpenAI API call
            response = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert AI privacy decision system."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.1,  # Low temperature for consistent decisions
                max_tokens=500
            )
            
            # Parse the LLM response
            llm_response = response.choices[0].message.content
            print(f"📡 OpenAI Response: {llm_response}")
            
            import json
            decision_data = json.loads(llm_response)
            
            # Get data classification 
            classification = await self.classify_data_field(
                privacy_request["data_field"], 
                privacy_request.get("context")
            )
            
            print(f"🧠 REAL LLM Decision: {'ALLOW' if decision_data['allowed'] else 'DENY'}")
            print(f"🧠 REAL LLM Reasoning: {decision_data['reasoning']}")
            print(f"🧠 REAL LLM Confidence: {decision_data['confidence']}")
            
            return {
                "allowed": decision_data["allowed"],
                "reason": decision_data["reasoning"],
                "confidence": decision_data["confidence"],
                "data_classification": classification,
                "emergency_used": privacy_request.get("emergency", False),
                "integration_ready": True,
                "llm_powered": True,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "openai_response": llm_response  # Include raw OpenAI response for verification
            }
            
        except Exception as e:
            print(f"❌ REAL OpenAI LLM call failed: {e}")
            print("   Falling back to ontology-based decision")
            # Fallback to ontology-based decision
            decision = self.ontology.make_privacy_decision(
                requester=privacy_request["requester"],
                data_field=privacy_request["data_field"],
                purpose=privacy_request["purpose"],
                context=privacy_request.get("context"),
                emergency=privacy_request.get("emergency", False)
            )
            return decision
    
    async def close(self):
        """Close connections properly."""
        # Close OpenAI resources if needed
        if self.openai_enabled:
            try:
                # OpenAI client doesn't require explicit closing
                print("✅ OpenAI resources cleaned up")
            except Exception as e:
                print(f"⚠️  Error closing Groq client: {e}")
        
        # Then close database connections
        if self.use_graphiti:
            try:
                await self.graphiti.close()
                print("✅ Graphiti connection closed")
            except Exception as e:
                print(f"⚠️  Error closing Graphiti: {e}")
        else:
            try:
                await self.driver.close()
                print("✅ Neo4j connection closed")
            except Exception as e:
                print(f"⚠️  Error closing Neo4j: {e}")

# Create instance for backward compatibility
GraphitiPrivacyBridge = EnhancedGraphitiPrivacyBridge