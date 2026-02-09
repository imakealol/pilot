#!/usr/bin/env python3
"""
Go Squad Framework - Process Logger

Audit trail for all agent invocations. Every action is logged.

Usage:
    from process_log import ProcessLog

    # Initialize
    log = ProcessLog(project='remanence')

    # Log an agent action
    log.record(
        agent_role='continuity_editor',
        action_type='validate',
        target='chapter_28',
        input_summary='Check timeline consistency',
        output_summary='Found 2 issues',
        status='partial',
    )

    # Query logs
    log.query(agent_role='continuity_editor')
    log.query(date='2025-01-14')
    log.violations()  # Get lane violations
"""

import yaml
import uuid
import json
from pathlib import Path
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, asdict, field
from datetime import datetime, date

# Project roots
PROJECTS = {
    'remanence': Path('/workspaces/pilot/REMANENCE'),
    'resonance': Path('/workspaces/pilot/RESONANCE'),
}


@dataclass
class LogEntry:
    """Single process log entry."""
    timestamp: str
    agent_role: str
    agent_id: str
    action_type: str  # query | recommend | edit | validate | create
    target: str
    input_summary: str
    output_summary: str
    status: str  # success | partial | failed | blocked

    # Optional fields
    lane_scope: Optional[str] = None
    escalation: Optional[str] = None
    tokens_used: Optional[int] = None
    duration_ms: Optional[int] = None
    parent_id: Optional[str] = None
    metadata: Dict = field(default_factory=dict)


@dataclass
class LaneViolation:
    """Record of a lane violation attempt."""
    timestamp: str
    agent_role: str
    attempted_action: str
    violated_constraint: str
    blocked: bool
    override_by: Optional[str] = None
    override_reason: Optional[str] = None


class ProcessLog:
    """
    Process logging system for Go Squad Framework.

    Maintains audit trail of all agent actions.
    Enforces lane boundaries.
    Tracks violations.
    """

    def __init__(self, project: str = 'remanence'):
        if project not in PROJECTS:
            raise ValueError(f"Unknown project: {project}")

        self.project = project
        self.root = PROJECTS[project]
        self.log_dir = self.root / 'logs'
        self.log_dir.mkdir(exist_ok=True)

        # Daily log file
        today = date.today().isoformat()
        self.log_file = self.log_dir / f'process_log_{today}.yaml'
        self.violation_file = self.log_dir / f'violations_{today}.yaml'

        # Lane definitions (from SCHEMAS.yaml)
        self.lane_rules = self._load_lane_rules()

    def _load_lane_rules(self) -> Dict:
        """Load lane rules from SCHEMAS.yaml."""
        schemas_path = Path(__file__).parent / 'SCHEMAS.yaml'
        if schemas_path.exists():
            with open(schemas_path, 'r', encoding='utf-8') as f:
                schemas = yaml.safe_load(f)
                roles = schemas.get('agent_roles', {}).get('production_crew', [])
                return {r['id']: r for r in roles}
        return {}

    def record(self,
               agent_role: str,
               action_type: str,
               target: str,
               input_summary: str,
               output_summary: str,
               status: str,
               **kwargs) -> str:
        """
        Record an agent action.

        Returns the log entry ID.
        """
        entry = LogEntry(
            timestamp=datetime.now().isoformat(),
            agent_role=agent_role,
            agent_id=kwargs.get('agent_id', str(uuid.uuid4())[:8]),
            action_type=action_type,
            target=target,
            input_summary=input_summary,
            output_summary=output_summary,
            status=status,
            lane_scope=kwargs.get('lane_scope'),
            escalation=kwargs.get('escalation'),
            tokens_used=kwargs.get('tokens_used'),
            duration_ms=kwargs.get('duration_ms'),
            parent_id=kwargs.get('parent_id'),
            metadata=kwargs.get('metadata', {}),
        )

        # Append to log file
        self._append_entry(entry)

        return entry.agent_id

    def _append_entry(self, entry: LogEntry):
        """Append entry to daily log file."""
        # Load existing entries
        entries = []
        if self.log_file.exists():
            with open(self.log_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f) or {}
                entries = data.get('entries', [])

        entries.append(asdict(entry))

        # Write back
        with open(self.log_file, 'w', encoding='utf-8') as f:
            yaml.dump({
                'project': self.project,
                'date': date.today().isoformat(),
                'entries': entries,
            }, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    def check_lane(self, agent_role: str, action_type: str, target_type: str) -> Dict:
        """
        Check if an action is within the agent's lane.

        Returns:
            {
                'allowed': bool,
                'reason': str,
                'can_read': bool,
                'can_write': bool,
            }
        """
        if agent_role not in self.lane_rules:
            return {
                'allowed': True,
                'reason': 'Unknown role - no restrictions',
                'can_read': True,
                'can_write': True,
            }

        rules = self.lane_rules[agent_role]
        can_read = target_type in rules.get('can_read', [])
        can_write = target_type in rules.get('can_write', [])
        cannot_write = target_type in rules.get('cannot_write', [])

        if action_type in ('query', 'read'):
            allowed = can_read
            reason = f"Lane allows reading {target_type}" if allowed else f"Lane forbids reading {target_type}"
        elif action_type in ('edit', 'write', 'create'):
            allowed = can_write and not cannot_write
            if cannot_write:
                reason = f"Lane explicitly forbids writing {target_type}"
            elif not can_write:
                reason = f"Lane does not allow writing {target_type}"
            else:
                reason = f"Lane allows writing {target_type}"
        else:
            allowed = True
            reason = f"Action type '{action_type}' not restricted"

        return {
            'allowed': allowed,
            'reason': reason,
            'can_read': can_read,
            'can_write': can_write and not cannot_write,
        }

    def record_violation(self,
                         agent_role: str,
                         attempted_action: str,
                         violated_constraint: str,
                         blocked: bool = True,
                         override_by: Optional[str] = None,
                         override_reason: Optional[str] = None):
        """Record a lane violation."""
        violation = LaneViolation(
            timestamp=datetime.now().isoformat(),
            agent_role=agent_role,
            attempted_action=attempted_action,
            violated_constraint=violated_constraint,
            blocked=blocked,
            override_by=override_by,
            override_reason=override_reason,
        )

        # Load existing violations
        violations = []
        if self.violation_file.exists():
            with open(self.violation_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f) or {}
                violations = data.get('violations', [])

        violations.append(asdict(violation))

        # Write back
        with open(self.violation_file, 'w', encoding='utf-8') as f:
            yaml.dump({
                'project': self.project,
                'date': date.today().isoformat(),
                'violations': violations,
            }, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    def query(self,
              agent_role: Optional[str] = None,
              action_type: Optional[str] = None,
              status: Optional[str] = None,
              date_str: Optional[str] = None,
              limit: int = 50) -> List[Dict]:
        """Query the process log."""
        # Determine which file(s) to read
        if date_str:
            log_file = self.log_dir / f'process_log_{date_str}.yaml'
            files = [log_file] if log_file.exists() else []
        else:
            files = sorted(self.log_dir.glob('process_log_*.yaml'), reverse=True)

        results = []
        for f in files:
            with open(f, 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file) or {}
                entries = data.get('entries', [])

                for entry in entries:
                    if agent_role and entry.get('agent_role') != agent_role:
                        continue
                    if action_type and entry.get('action_type') != action_type:
                        continue
                    if status and entry.get('status') != status:
                        continue

                    results.append(entry)

                    if len(results) >= limit:
                        return results

        return results

    def violations(self, date_str: Optional[str] = None) -> List[Dict]:
        """Get lane violations."""
        if date_str:
            violation_file = self.log_dir / f'violations_{date_str}.yaml'
        else:
            violation_file = self.violation_file

        if not violation_file.exists():
            return []

        with open(violation_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f) or {}
            return data.get('violations', [])

    def summary(self, date_str: Optional[str] = None) -> Dict:
        """Get summary statistics for the log."""
        entries = self.query(date_str=date_str, limit=10000)

        if not entries:
            return {'total': 0}

        by_role = {}
        by_action = {}
        by_status = {}

        for e in entries:
            role = e.get('agent_role', 'unknown')
            action = e.get('action_type', 'unknown')
            status = e.get('status', 'unknown')

            by_role[role] = by_role.get(role, 0) + 1
            by_action[action] = by_action.get(action, 0) + 1
            by_status[status] = by_status.get(status, 0) + 1

        violations = self.violations(date_str=date_str)

        return {
            'total': len(entries),
            'by_role': by_role,
            'by_action': by_action,
            'by_status': by_status,
            'violations': len(violations),
        }


# =============================================================================
# DECORATOR FOR AUTOMATIC LOGGING
# =============================================================================

def logged_action(agent_role: str, lane_scope: Optional[str] = None):
    """
    Decorator to automatically log agent actions.

    Usage:
        @logged_action('continuity_editor', lane_scope='fact_checking')
        def check_timeline(chapter_content):
            # ... do work ...
            return result
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            log = ProcessLog()
            agent_id = str(uuid.uuid4())[:8]
            start_time = datetime.now()

            # Extract target from args/kwargs if possible
            target = kwargs.get('target', str(args[0]) if args else 'unknown')
            input_summary = kwargs.get('input_summary', f"Called {func.__name__}")

            try:
                result = func(*args, **kwargs)
                status = 'success'
                output_summary = str(result)[:200] if result else 'No output'
            except Exception as e:
                status = 'failed'
                output_summary = f"Error: {str(e)}"
                result = None

            duration = int((datetime.now() - start_time).total_seconds() * 1000)

            log.record(
                agent_role=agent_role,
                agent_id=agent_id,
                action_type='execute',
                target=target,
                input_summary=input_summary,
                output_summary=output_summary,
                status=status,
                lane_scope=lane_scope,
                duration_ms=duration,
            )

            return result
        return wrapper
    return decorator


# =============================================================================
# CLI INTERFACE
# =============================================================================

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Go Squad Process Log")
    parser.add_argument('--project', '-p', default='remanence',
                        choices=['remanence', 'resonance'])

    subparsers = parser.add_subparsers(dest='command')

    # Query command
    query_parser = subparsers.add_parser('query', help='Query process log')
    query_parser.add_argument('--role', '-r', help='Filter by agent role')
    query_parser.add_argument('--action', '-a', help='Filter by action type')
    query_parser.add_argument('--status', '-s', help='Filter by status')
    query_parser.add_argument('--date', '-d', help='Filter by date (YYYY-MM-DD)')
    query_parser.add_argument('--limit', '-l', type=int, default=20)

    # Summary command
    subparsers.add_parser('summary', help='Get log summary')

    # Violations command
    subparsers.add_parser('violations', help='List lane violations')

    # Check lane command
    check_parser = subparsers.add_parser('check', help='Check lane permissions')
    check_parser.add_argument('role', help='Agent role')
    check_parser.add_argument('action', help='Action type')
    check_parser.add_argument('target', help='Target type')

    args = parser.parse_args()

    log = ProcessLog(project=args.project)

    if args.command == 'query':
        entries = log.query(
            agent_role=args.role,
            action_type=args.action,
            status=args.status,
            date_str=args.date,
            limit=args.limit,
        )
        print(f"\nFound {len(entries)} entries:\n")
        for e in entries:
            print(f"[{e['timestamp']}] {e['agent_role']}: {e['action_type']} on {e['target']}")
            print(f"  Status: {e['status']}")
            print(f"  Output: {e['output_summary'][:100]}")
            print()

    elif args.command == 'summary':
        summary = log.summary()
        print(f"\nProcess Log Summary:")
        print(f"Total entries: {summary['total']}")
        print(f"Violations: {summary.get('violations', 0)}")
        print(f"\nBy Role:")
        for role, count in summary.get('by_role', {}).items():
            print(f"  {role}: {count}")
        print(f"\nBy Status:")
        for status, count in summary.get('by_status', {}).items():
            print(f"  {status}: {count}")

    elif args.command == 'violations':
        violations = log.violations()
        print(f"\nFound {len(violations)} violations:\n")
        for v in violations:
            print(f"[{v['timestamp']}] {v['agent_role']}")
            print(f"  Attempted: {v['attempted_action']}")
            print(f"  Violated: {v['violated_constraint']}")
            print(f"  Blocked: {v['blocked']}")
            print()

    elif args.command == 'check':
        result = log.check_lane(args.role, args.action, args.target)
        print(f"\nLane Check: {args.role} -> {args.action} on {args.target}")
        print(f"Allowed: {result['allowed']}")
        print(f"Reason: {result['reason']}")

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
