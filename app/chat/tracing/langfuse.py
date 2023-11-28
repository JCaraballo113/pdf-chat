import os
from langfuse.client import Langfuse

langfuse = Langfuse(
    os.environ.get("LANGFUSE_PUBLIC_KEY"),
    os.environ.get("LANGFUSE_SECRET_KEY"),
    os.environ.get("LANGFUSE_API_KEY"),
    host="https://prod-langfuse.fly.dev"
)
