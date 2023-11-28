from app.chat.redis import client


def score_conversation(
    conversation_id: str, score: float, llm: str, retriever: str, memory: str
) -> None:
    score = min(max(score, 0), 1)

    client.hincrby("llm_score_values", llm, score)
    client.hincrby("llm_score_count", llm, 1)
    client.hincrby("retriever_score_values", retriever, score)
    client.hincrby("retriever_score_count", retriever, 1)
    client.hincrby("memory_score_values", memory, score)
    client.hincrby("memory_score_count", memory, 1)


def get_scores():
    """
    Retrieves and organizes scores from the langfuse client for different component types and names.
    The scores are categorized and aggregated in a nested dictionary format where the outer key represents
    the component type and the inner key represents the component name, with each score listed in an array.

    The function accesses the langfuse client's score endpoint to obtain scores.
    If the score name cannot be parsed into JSON, it is skipped.

    :return: A dictionary organized by component type and name, containing arrays of scores.

    Example:

        {
            'llm': {
                'chatopenai-3.5-turbo': [score1, score2],
                'chatopenai-4': [score3, score4]
            },
            'retriever': { 'pinecone_store': [score5, score6] },
            'memory': { 'persist_memory': [score7, score8] }
        }
    """

    pass
