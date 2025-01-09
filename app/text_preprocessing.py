from app.aws.bedrock_integration import analyze_text_with_bedrock
from langgraph.graph import END, START, StateGraph
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from typing import TypedDict
from dotenv import load_dotenv

class TaskState(TypedDict):
    query: str
    destination: str
    answer: str


def route_query(data):
    if len(data) < 100:
        return {"route": "prompt_1"}  # Повертаємо словник з ключем 'route'
    else:
        return {"route": "prompt_2"}

def prompt_1(data):
    return [{"event": f"Short-{i}", "sentiment_score": len(doc) % 10} for i, doc in enumerate(data)]

def prompt_2(data):
    return [{"event": f"Long-{i}", "sentiment_score": len(doc) % 10} for i, doc in enumerate(data)]

def load_data_from_sources(news_data, twitter_data):
    """Load data from news and Twitter datasets."""
    combined_data = news_data + twitter_data
    return combined_data

def preprocess_data(data):
    """Perform preprocessing like text cleaning and splitting."""
    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    # Ensure each item in data is a string
    split_data = [splitter.split_text(str(doc)) for doc in data]
    return [item for sublist in split_data for item in sublist]  # Flatten the list

def create_vector_store(data):
    """Create a FAISS vector store using Bedrock embeddings."""
    load_dotenv()

    if not data:
        raise ValueError("No data provided for vector store creation.")

    embeddings = [analyze_text_with_bedrock(f"Generate embeddings for: {doc}") for doc in data]
    vector_store = FAISS.from_embeddings(embeddings, data)
    return vector_store


def build_retrieval_chain(vector_store):
    """Build a retrieval-based chain using LangChain."""
    retriever = vector_store.as_retriever()
    chain = RetrievalQA.from_chain_type(llm=None, retriever=retriever)  # No LLM needed for Bedrock-only solution
    return chain


def analyze_sentiment_and_correlations_with_state_graph(data):
    """Perform sentiment analysis and correlation extraction using Bedrock and StateGraph."""
    correlations = []
    for item in data:
        prompt = f"Проаналізуй текст і визнач, які події можуть вплинути на криптовалютний ринок: {item}"
        analysis_result = analyze_text_with_bedrock(prompt)
        correlations.append({"event": item, "analysis": analysis_result})

    # Створення графа
    graph = StateGraph(TaskState)
    graph.add_node("route_query", route_query)
    graph.add_node("prompt_1", prompt_1)
    graph.add_node("prompt_2", prompt_2)

    graph.add_edge(START, "route_query")
    graph.add_conditional_edges("route_query", lambda state: state["route"])  # Використовуємо ключ 'route'
    graph.add_edge("prompt_1", END)
    graph.add_edge("prompt_2", END)

    app = graph.compile()

    # Запуск графа
    processed_correlations = []
    for event in app.stream({"query": correlations}, stream_mode="values"):
        processed_correlations.append(event)

    return processed_correlations