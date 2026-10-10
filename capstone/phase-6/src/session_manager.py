from typing import List, Dict, Any

class SessionManager:
    """
    Manages user sessions with advanced context compaction and pruning
    to prevent context degradation and LLM instruction dilution.
    """
    def __init__(self, max_turns: int = 10, max_tokens_approx: int = 4000):
        self.sessions: Dict[str, List[Dict[str, Any]]] = {}
        self.max_turns = max_turns
        self.max_tokens_approx = max_tokens_approx

    def get_history(self, session_id: str) -> List[Dict[str, Any]]:
        return self.sessions.get(session_id, [])

    def add_message(self, session_id: str, role: str, content: str) -> None:
        if session_id not in self.sessions:
            self.sessions[session_id] = []

        self.sessions[session_id].append({"role": role, "content": content})
        self._prune_and_compact(session_id)

    def _prune_and_compact(self, session_id: str) -> None:
        """
        Prunes old conversation turns while maintaining recent context window stability.
        """
        history = self.sessions[session_id]

        # Keep system instructions or initial context if stored,
        # and strictly bound total turns to prevent context rot.
        max_messages = self.max_turns * 2
        if len(history) > max_messages:
            # Retain the most recent N turns
            self.sessions[session_id] = history[-max_messages:]

        # Optional: Implement heuristic token compaction for very long text messages
        for msg in self.sessions[session_id]:
            if len(msg["content"]) > 1500:
                # Truncate overly verbose user inputs or tool dumps to protect token budget
                msg["content"] = msg["content"][:1500] + "... [Content Truncated for Context Optimization]"

    def clear_session(self, session_id: str) -> None:
        if session_id in self.sessions:
            del self.sessions[session_id]