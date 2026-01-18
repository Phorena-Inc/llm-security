"""
Audit Logging System for Privacy Firewall

Logs all access control decisions for compliance and security auditing.
Supports both JSON file logging (simple) and Neo4j logging (advanced).
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from enum import Enum

logger = logging.getLogger(__name__)


class AuditDecision(str, Enum):
    """Access control decision types"""
    ALLOW = "ALLOW"
    DENY = "DENY"
    ERROR = "ERROR"


class AuditLogEntry:
    """Single audit log entry"""
    
    def __init__(
        self,
        timestamp: datetime,
        employee_email: str,
        resource_id: str,
        decision: AuditDecision,
        reason: str,
        policy_matched: Optional[str] = None,
        resource_classification: Optional[str] = None,
        employee_clearance: Optional[str] = None,
        additional_context: Optional[Dict] = None
    ):
        self.timestamp = timestamp
        self.employee_email = employee_email
        self.resource_id = resource_id
        self.decision = decision
        self.reason = reason
        self.policy_matched = policy_matched
        self.resource_classification = resource_classification
        self.employee_clearance = employee_clearance
        self.additional_context = additional_context or {}
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            "timestamp": self.timestamp.isoformat(),
            "employee_email": self.employee_email,
            "resource_id": self.resource_id,
            "decision": self.decision.value,
            "reason": self.reason,
            "policy_matched": self.policy_matched,
            "resource_classification": self.resource_classification,
            "employee_clearance": self.employee_clearance,
            "additional_context": self.additional_context
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'AuditLogEntry':
        """Create from dictionary"""
        return cls(
            timestamp=datetime.fromisoformat(data["timestamp"]),
            employee_email=data["employee_email"],
            resource_id=data["resource_id"],
            decision=AuditDecision(data["decision"]),
            reason=data["reason"],
            policy_matched=data.get("policy_matched"),
            resource_classification=data.get("resource_classification"),
            employee_clearance=data.get("employee_clearance"),
            additional_context=data.get("additional_context", {})
        )


class AuditLogger:
    """
    Audit logger for access control decisions
    
    Supports two backends:
    - JSON file logging (simple, default)
    - Neo4j logging (advanced, optional)
    """
    
    def __init__(self, log_dir: Path = None, use_neo4j: bool = False):
        """
        Initialize audit logger
        
        Args:
            log_dir: Directory for log files (default: logs/)
            use_neo4j: Whether to also log to Neo4j
        """
        self.log_dir = log_dir or Path(__file__).parent
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        self.use_neo4j = use_neo4j
        self.neo4j_client = None
        
        # JSON log file - one per day
        self.current_log_file = None
        self._update_log_file()
        
        logger.info(f"AuditLogger initialized (log_dir={self.log_dir}, use_neo4j={use_neo4j})")
    
    def _update_log_file(self):
        """Update log file path based on current date"""
        today = datetime.now().strftime("%Y-%m-%d")
        self.current_log_file = self.log_dir / f"audit_{today}.jsonl"
    
    def log_access(
        self,
        employee_email: str,
        resource_id: str,
        decision: AuditDecision,
        reason: str,
        policy_matched: Optional[str] = None,
        resource_classification: Optional[str] = None,
        employee_clearance: Optional[str] = None,
        **additional_context
    ):
        """
        Log an access control decision
        
        Args:
            employee_email: Email of employee requesting access
            resource_id: ID of resource being accessed
            decision: ALLOW, DENY, or ERROR
            reason: Human-readable reason for decision
            policy_matched: Name of policy that matched (if any)
            resource_classification: Classification level of resource
            employee_clearance: Clearance level of employee
            **additional_context: Additional context to log
        """
        entry = AuditLogEntry(
            timestamp=datetime.now(),
            employee_email=employee_email,
            resource_id=resource_id,
            decision=decision,
            reason=reason,
            policy_matched=policy_matched,
            resource_classification=resource_classification,
            employee_clearance=employee_clearance,
            additional_context=additional_context
        )
        
        # Log to JSON file
        self._log_to_file(entry)
        
        # Log to Neo4j if enabled
        if self.use_neo4j and self.neo4j_client:
            self._log_to_neo4j(entry)
        
        # Also log to application logger for monitoring
        log_level = logging.INFO if decision == AuditDecision.ALLOW else logging.WARNING
        logger.log(
            log_level,
            f"Access {decision.value}: {employee_email} → {resource_id} | {reason}",
            extra={
                "employee_email": employee_email,
                "resource_id": resource_id,
                "decision": decision.value,
                "policy": policy_matched
            }
        )
    
    def _log_to_file(self, entry: AuditLogEntry):
        """Log entry to JSON Lines file"""
        try:
            # Check if we need to rotate to new day's file
            self._update_log_file()
            
            # Append to JSONL file (one JSON object per line)
            with open(self.current_log_file, 'a') as f:
                f.write(json.dumps(entry.to_dict()) + '\n')
        
        except Exception as e:
            logger.error(f"Failed to write audit log to file: {e}", exc_info=True)
    
    def _log_to_neo4j(self, entry: AuditLogEntry):
        """Log entry to Neo4j (optional advanced feature)"""
        # TODO: Implement Neo4j audit logging
        # CREATE (a:AuditLog {
        #   timestamp: datetime(),
        #   employee_email: $email,
        #   resource_id: $resource_id,
        #   decision: $decision,
        #   ...
        # })
        pass
    
    def get_audit_trail(
        self,
        employee_email: Optional[str] = None,
        resource_id: Optional[str] = None,
        decision: Optional[AuditDecision] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100
    ) -> List[AuditLogEntry]:
        """
        Query audit trail with filters
        
        Args:
            employee_email: Filter by employee email
            resource_id: Filter by resource ID
            decision: Filter by decision type
            start_date: Filter entries after this date
            end_date: Filter entries before this date
            limit: Maximum number of entries to return
        
        Returns:
            List of matching audit log entries
        """
        entries = []
        
        # Determine which log files to read
        log_files = self._get_log_files_in_range(start_date, end_date)
        
        for log_file in log_files:
            try:
                with open(log_file, 'r') as f:
                    for line in f:
                        if not line.strip():
                            continue
                        
                        try:
                            data = json.loads(line)
                            entry = AuditLogEntry.from_dict(data)
                            
                            # Apply filters
                            if employee_email and entry.employee_email != employee_email:
                                continue
                            if resource_id and entry.resource_id != resource_id:
                                continue
                            if decision and entry.decision != decision:
                                continue
                            
                            # Convert datetime filters to comparable format
                            entry_date = entry.timestamp.date() if isinstance(entry.timestamp, datetime) else entry.timestamp
                            
                            if start_date:
                                filter_start = start_date if not isinstance(start_date, datetime) else start_date.date()
                                if entry_date < filter_start:
                                    continue
                            
                            if end_date:
                                filter_end = end_date if not isinstance(end_date, datetime) else end_date.date()
                                if entry_date > filter_end:
                                    continue
                            
                            entries.append(entry)
                            
                            # Check limit
                            if len(entries) >= limit:
                                return entries
                        
                        except json.JSONDecodeError as e:
                            logger.warning(f"Failed to parse audit log line: {e}")
                            continue
            
            except FileNotFoundError:
                continue
            except Exception as e:
                logger.error(f"Error reading audit log file {log_file}: {e}")
                continue
        
        return entries
    
    def _get_log_files_in_range(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Path]:
        """Get log files within date range"""
        log_files = sorted(self.log_dir.glob("audit_*.jsonl"), reverse=True)
        
        if not start_date and not end_date:
            return log_files
        
        filtered = []
        for log_file in log_files:
            # Extract date from filename: audit_YYYY-MM-DD.jsonl
            try:
                date_str = log_file.stem.replace("audit_", "")
                file_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                
                # Convert datetime objects to date if needed
                start = start_date if not isinstance(start_date, datetime) else start_date.date()
                end = end_date if not isinstance(end_date, datetime) else end_date.date()
                
                if start and file_date < start:
                    continue
                if end and file_date > end:
                    continue
                
                filtered.append(log_file)
            
            except ValueError:
                # Skip files that don't match expected format
                continue
        
        return filtered
    
    def get_stats(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict:
        """
        Get audit statistics
        
        Returns:
            Dictionary with statistics:
            - total_accesses: Total access attempts
            - allowed: Number of allowed accesses
            - denied: Number of denied accesses
            - errors: Number of errors
            - by_employee: Access counts by employee
            - by_resource: Access counts by resource
            - by_policy: Access counts by policy
        """
        entries = self.get_audit_trail(
            start_date=start_date,
            end_date=end_date,
            limit=10000  # Get more for stats
        )
        
        stats = {
            "total_accesses": len(entries),
            "allowed": 0,
            "denied": 0,
            "errors": 0,
            "by_employee": {},
            "by_resource": {},
            "by_policy": {}
        }
        
        for entry in entries:
            # Count by decision
            if entry.decision == AuditDecision.ALLOW:
                stats["allowed"] += 1
            elif entry.decision == AuditDecision.DENY:
                stats["denied"] += 1
            elif entry.decision == AuditDecision.ERROR:
                stats["errors"] += 1
            
            # Count by employee
            stats["by_employee"][entry.employee_email] = \
                stats["by_employee"].get(entry.employee_email, 0) + 1
            
            # Count by resource
            stats["by_resource"][entry.resource_id] = \
                stats["by_resource"].get(entry.resource_id, 0) + 1
            
            # Count by policy
            if entry.policy_matched:
                stats["by_policy"][entry.policy_matched] = \
                    stats["by_policy"].get(entry.policy_matched, 0) + 1
        
        return stats


# Global audit logger instance
_audit_logger: Optional[AuditLogger] = None


def get_audit_logger() -> AuditLogger:
    """Get or create global audit logger instance"""
    global _audit_logger
    if _audit_logger is None:
        log_dir = Path(__file__).parent
        _audit_logger = AuditLogger(log_dir=log_dir)
    return _audit_logger
