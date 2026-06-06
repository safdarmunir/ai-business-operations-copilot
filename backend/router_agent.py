from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END


class RouterState(TypedDict):
    question: str
    filename: Optional[str]
    route: Optional[str]
    result: Optional[dict]


class RouterAgent:
    def __init__(self, rag_pipeline, analytics_agent, upload_dir):
        self.rag_pipeline = rag_pipeline
        self.analytics_agent = analytics_agent
        self.upload_dir = upload_dir
        self.graph = self.build_graph()

    def classify_question(self, state: RouterState):
        question = state["question"].lower()
        filename = state.get("filename")

        if filename:
            filename_lower = filename.lower()

            # If selected file is document, force document route
            if filename_lower.endswith((".pdf", ".docx", ".txt")):
                route = "document_qa"

            # If selected file is data file, route analytics/forecast
            elif filename_lower.endswith((".csv", ".xlsx")):
                if any(word in question for word in ["forecast", "predict", "future"]):
                    route = "forecast"
                else:
                    route = "analytics"

            else:
                route = "document_qa"

        else:
            if any(word in question for word in ["forecast", "predict", "future"]):
                route = "forecast"

            elif any(word in question for word in ["revenue", "sales", "product", "customer", "region", "trend"]):
                route = "analytics"

            else:
                route = "document_qa"

        return {
            **state,
            "route": route
        }
    def document_node(self, state: RouterState):
        result = self.rag_pipeline.answer_question(
    question=state["question"],
    filename=state.get("filename")
)
        return {
            **state,
            "result": {
                "route": "document_qa",
                "answer": result["answer"],
                "sources": result["sources"]
            }
        }

    def analytics_node(self, state: RouterState):
        filename = state.get("filename")

        if not filename:
            return {
                **state,
                "result": {
                    "route": "analytics",
                    "error": "Filename is required for analytics questions."
                }
            }

        file_path = self.upload_dir / filename

        result = self.analytics_agent.analyze(
            file_path=str(file_path),
            question=state["question"]
        )

        return {
            **state,
            "result": {
                "route": "analytics",
                **result
            }
        }

    def forecast_node(self, state: RouterState):
        filename = state.get("filename")

        if not filename:
            return {
                **state,
                "result": {
                    "route": "forecast",
                    "error": "Filename is required for forecasting questions."
                }
            }

        file_path = self.upload_dir / filename

        result = self.analytics_agent.analyze(
            file_path=str(file_path),
            question=state["question"]
        )

        return {
            **state,
            "result": {
                "route": "forecast",
                **result
            }
        }

    def route_decision(self, state: RouterState):
        return state["route"]

    def build_graph(self):
        graph = StateGraph(RouterState)

        graph.add_node("classifier", self.classify_question)
        graph.add_node("document_qa", self.document_node)
        graph.add_node("analytics", self.analytics_node)
        graph.add_node("forecast", self.forecast_node)

        graph.set_entry_point("classifier")

        graph.add_conditional_edges(
            "classifier",
            self.route_decision,
            {
                "document_qa": "document_qa",
                "analytics": "analytics",
                "forecast": "forecast"
            }
        )

        graph.add_edge("document_qa", END)
        graph.add_edge("analytics", END)
        graph.add_edge("forecast", END)

        return graph.compile()

    def run(self, question, filename=None):
        state = {
            "question": question,
            "filename": filename,
            "route": None,
            "result": None
        }

        output = self.graph.invoke(state)

        return output["result"]