from queue import Queue
from typing import Any, Optional
from threading import Thread
from uuid import UUID
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks.base import BaseCallbackHandler
from dotenv import load_dotenv
from langchain.schema.output import LLMResult
from langchain.schema.runnable import RunnableConfig

load_dotenv()


class StreamingHandler(BaseCallbackHandler):
    def __init__(self, queue: Queue):
        self.queue = queue

    def on_llm_new_token(self, token: str, **kwargs: Any) -> Any:
        self.queue.put(token)

    def on_llm_end(self, response: LLMResult, *, run_id: UUID, parent_run_id: UUID | None = None, **kwargs: Any) -> Any:
        self.queue.put(None)

    def on_llm_error(self, error: Exception, **kwargs: Any) -> Any:
        self.queue.put(None)


chat = ChatOpenAI(streaming=True)
prompt = ChatPromptTemplate.from_messages([
    ("human", "{content}")
])


class StreamableChain:
    def stream(self, input):
        queue = Queue()
        handler = StreamingHandler(queue)

        def task():
            self(input, callbacks=[handler])
        Thread(target=task).start()

        while True:
            token = queue.get()
            if token is None:
                break
            yield token


class StreamingChain(StreamableChain, LLMChain):
    pass


chain = StreamingChain(llm=chat, prompt=prompt)

for output in chain.stream(input={"content": "tell me a joke"}):
    print(output)
