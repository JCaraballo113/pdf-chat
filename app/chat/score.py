import random
from app.chat.redis import client


def random_component_by_score(component_type: str, component_map: dict):
    # Make sure component_type is 'llm', 'retriever', or'memory'
    if component_type not in ["llm", "retriever", "memory"]:
        raise ValueError(
            f"component_type must be 'llm','retriever', or'memory', not {component_type}")

    # From redis, get the hash containing the sum total scores for the given component_type
    values = client.hgetall(f"{component_type}_score_values")
    counts = client.hgetall(f"{component_type}_score_count")

    names = component_map.keys()

    avg_scores = {}
    for name in names:
        score = int(values.get(name, 1))
        counts = int(counts.get(name, 1))
        avg = score / counts
        avg_scores[name] = max(avg, 0.1)

    # Do a weighted random selection
    sum_scores = sum(avg_scores.values())
    random_val = random.uniform(0, sum_scores)
    cumulative = 0

    for name, score in avg_scores.items():
        cumulative += score
        if random_val <= cumulative:
            return name


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
    aggregate = {"llm": {}, "retriever": {}, "memory": {}}
    for component_type in aggregate.keys():
        values = client.hgetall(f"{component_type}_score_values")
        counts = client.hgetall(f"{component_type}_score_count")

        names = values.keys()
        for name in names:
            score = int(values.get(name, 1))
            count = int(counts.get(name, 1))
            avg = score / count
            aggregate[component_type][name] = [avg]

    return aggregate
