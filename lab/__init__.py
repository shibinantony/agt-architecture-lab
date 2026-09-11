"""Original, offline teaching lab inspired by Agent Governance Toolkit concepts.

This package does not import, implement, or claim compatibility with Microsoft's
Agent Governance Toolkit policy format. All inventory and prices are synthetic.
"""

from .runtime import AuditError, GovernanceRuntime, PolicyError

__all__ = ["AuditError", "GovernanceRuntime", "PolicyError"]
