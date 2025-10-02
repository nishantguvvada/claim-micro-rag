import requests
import json

class RAGEval:

    TOP_K = 3

    def __init__(self, eval_set_path):
        self.eval_set_path = eval_set_path

    def load_eval_set(self):
        with open(self.eval_set_path, 'r', encoding='utf-8') as file:
            return [json.loads(line) for line in file]

    def evaluate(self):
        eval_set = self.load_eval_set()
        total_queries = len(eval_set)
        total_hits = 0
        total_correct = 0
        total_retrieved = 0

        for query in eval_set:
            q = query["q"]
            expected = query["ans_contains"].lower()
            # print("q: ", q)
            # print("ans_contains: ", expected)

            response = requests.post(
                "http://localhost:8000/ask",
                json={"query": f"{q}", "k": RAGEval.TOP_K}
            )

            result = response.json()

            answer = result.get("answer", "").lower()
            # print("answer: ", answer)
            citations = result.get("citations", [])
            # print("citations: ", citations)

            citation_text = " ".join(c["content"] for c in citations).lower()
            # print("citation_text: ", citation_text)

            # print("Match: ", expected in citation_text)

            if expected in answer or expected in citation_text:
                total_hits += 1

            total_retrieved += len(citations)
            total_correct += sum(1 for c in citations if expected in c["content"].lower())

        hit_rate = total_hits / total_queries
        precision_k = total_correct / total_retrieved if total_retrieved > 0 else 0

        print(f"n={total_queries} | hit_rate={hit_rate:.2f} | precision@{RAGEval.TOP_K}={precision_k:.2f}")

if __name__ == "__main__":
    eval = RAGEval(eval_set_path="./eval.jsonl")
    eval.evaluate()