"""A2A protocol implementation for agent-to-agent communication.

This module implements a lightweight in-process A2A message broker. It is used
for the Coder -> QA review request and QA -> Coder fix instruction pathway.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field


class A2AMessage(BaseModel):
    """Serializable A2A message exchanged between two agents."""

    sender: str
    receiver: str
    intent: str
    payload: dict[str, Any] = Field(default_factory=dict)
    correlation_id: str = Field(default_factory=lambda: str(uuid4()))


class AgentCapability(BaseModel):
    """Capabilities advertised by an agent at startup."""

    agent_name: str
    supported_intents: list[str]


class A2ABroker:
    """In-memory A2A message broker with intent validation."""

    def __init__(self) -> None:
        """Initialize capability registry and message queues."""
        self.capabilities: dict[str, AgentCapability] = {}
        self.queues: dict[str, list[A2AMessage]] = defaultdict(list)
        self.message_log: list[A2AMessage] = []

    def register_agent(self, capability: AgentCapability) -> None:
        """Register an agent and its supported message intents."""
        self.capabilities[capability.agent_name] = capability

    def send(self, message: A2AMessage) -> A2AMessage:
        """Validate and enqueue a message for the receiver."""
        self._validate_receiver(message.receiver)
        self._validate_intent(message.receiver, message.intent)
        self.queues[message.receiver].append(message)
        self.message_log.append(message)
        return message

    def receive(self, agent_name: str) -> list[A2AMessage]:
        """Return and clear all pending messages for an agent."""
        self._validate_receiver(agent_name)
        messages = list(self.queues[agent_name])
        self.queues[agent_name].clear()
        return messages

    def reply(
        self,
        original: A2AMessage,
        sender: str,
        intent: str,
        payload: dict[str, Any],
    ) -> A2AMessage:
        """Send a correlated response to an existing A2A message."""
        response = A2AMessage(
            sender=sender,
            receiver=original.sender,
            intent=intent,
            payload=payload,
            correlation_id=original.correlation_id,
        )
        return self.send(response)

    def _validate_receiver(self, receiver: str) -> None:
        """Ensure the receiver is registered with the broker."""
        if receiver not in self.capabilities:
            raise ValueError(f"Unknown A2A receiver: {receiver}")

    def _validate_intent(self, receiver: str, intent: str) -> None:
        """Ensure the receiver supports the requested intent."""
        supported = self.capabilities[receiver].supported_intents
        if intent not in supported:
            raise ValueError(
                f"Receiver '{receiver}' does not support intent '{intent}'. "
                f"Supported intents: {supported}"
            )


def build_default_broker() -> A2ABroker:
    """Create the default broker used by the final pipeline."""
    broker = A2ABroker()
    broker.register_agent(
        AgentCapability(
            agent_name="coder",
            supported_intents=["fix_instruction"],
        )
    )
    broker.register_agent(
        AgentCapability(
            agent_name="qa",
            supported_intents=["review_request"],
        )
    )
    return broker