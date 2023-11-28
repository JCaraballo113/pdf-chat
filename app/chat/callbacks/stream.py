from queue import Queue
from typing import Any, Dict, List, Optional
from uuid import UUID
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema.messages import BaseMessage


class StreamingHandler(BaseCallbackHandler):
    def __init__(self, queue: Queue):
        self.queue = queue
        self.streaming_run_ids = set()

    def on_chat_model_start(self, serialized: Dict[str, Any], messages: List[List[BaseMessage]], *, run_id: UUID, parent_run_id: UUID | None = None, tags: List[str] | None = None, metadata: Dict[str, Any] | None = None, **kwargs: Any) -> Any:
        if serialized["kwargs"]["streaming"]:
            self.streaming_run_ids.add(run_id)

    def on_llm_new_token(self, token: str, **kwargs: Any) -> Any:
        self.queue.put(token)

    def on_llm_end(self, run_id, **kwargs: Any) -> Any:
        if run_id in self.streaming_run_ids:
            self.queue.put(None)
            self.streaming_run_ids.remove(run_id)

    def on_llm_error(self, error: Exception, **kwargs: Any) -> Any:
        self.queue.put(None)
