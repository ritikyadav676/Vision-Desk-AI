src/agent/workflow.py
__init__.py

workflow.py
 
 
from typing import TypedDict
 
from langgraph.graph import StateGraph, START, END

from langchain_openai import ChatOpenAI
 
from src.vision.detector import (

    detect_image,

    format_detections

)
 
from src.knowledge_base.database import (

    search_knowledge_base

)
 
 
class AgentState(TypedDict):
 
    image_path: str
 
    question: str
 
    visual_result: str
 
    document_context: str
 
    sources: list
 
    final_answer: str
 
 
def make_workflow(vector_db, model_path="best.pt"):
 
    # --------------------------------

    # NODE 1 - VISION

    # --------------------------------
 
    def vision_node(state):
 
        detections = detect_image(

            state["image_path"],

            model_path

        )
 
        visual_result = format_detections(

            detections

        )
 
        return {

            "visual_result": visual_result

        }
 
    # --------------------------------

    # NODE 2 - RAG

    # --------------------------------
 
    def rag_node(state):
 
        documents = search_knowledge_base(

            vector_db,

            state["question"],

            k=3

        )
 
        context = "\n\n".join(

            document.page_content

            for document in documents

        )
 
        sources = [

            document.metadata.get(

                "document_name",

                "Unknown"

            )

            for document in documents

        ]
 
        return {

            "document_context": context,

            "sources": sources

        }
 
    # --------------------------------

    # NODE 3 - LLM

    # --------------------------------
 
    def llm_node(state):
 
        prompt = f"""

You are VisionDesk AI,

a workplace safety assistant.
 
VISUAL DETECTION:

{state["visual_result"]}
 
SAFETY DOCUMENT INFORMATION:

{state["document_context"]}
 
USER QUESTION:

{state["question"]}
 
Instructions:
 
1. Use the visual detection information.

2. Use the safety document information.

3. Answer the user's question clearly.

4. Do not invent information.

5. Clearly distinguish visual observations

   from safety rules in the document.

6. If the document does not contain enough

   information, say so.

"""
 
        llm = ChatOpenAI(

            model="gpt-4o-mini",

            temperature=0

        )
 
        response = llm.invoke(prompt)
 
        return {

            "final_answer": response.content

        }
 
    # --------------------------------

    # CREATE LANGGRAPH

    # --------------------------------
 
    workflow = StateGraph(AgentState)
 
    workflow.add_node(

        "vision",

        vision_node

    )
 
    workflow.add_node(

        "rag",

        rag_node

    )
 
    workflow.add_node(

        "llm",

        llm_node

    )
 
    # Flow
 
    workflow.add_edge(

        START,

        "vision"

    )
 
    workflow.add_edge(

        "vision",

        "rag"

    )
 
    workflow.add_edge(

        "rag",

        "llm"

    )
 
    workflow.add_edge(

        "llm",

        END

    )
 
    return workflow.compile()
 
milestone3_practice.py
 
import os
 
from dotenv import load_dotenv
 
from src.knowledge_base.database import (

    build_knowledge_base,

    load_knowledge_base

)
 
from src.agent.workflow import make_workflow
 
 
load_dotenv()
 
 
PDF_PATH = "data/safety_manual.pdf"
 
INDEX_PATH = "faiss_index"
 
 
def main():
 
    # --------------------------------

    # CHECK API KEY

    # --------------------------------
 
    if not os.getenv("OPENAI_API_KEY"):
 
        print("OPENAI_API_KEY is missing.")
 
        print(

            "Create .env and add your API key."

        )
 
        return
 
    # --------------------------------

    # CHECK PDF

    # --------------------------------
 
    if not os.path.exists(PDF_PATH):
 
        print(

            "Safety manual not found:"

        )
 
        print(PDF_PATH)
 
        return
 
    # --------------------------------

    # CREATE / LOAD KNOWLEDGE BASE

    # --------------------------------
 
    if not os.path.exists(INDEX_PATH):
 
        print(

            "Creating knowledge base..."

        )
 
        vector_db = build_knowledge_base(

            PDF_PATH,

            INDEX_PATH

        )
 
    else:
 
        print(

            "Loading existing knowledge base..."

        )
 
        vector_db = load_knowledge_base(

            INDEX_PATH

        )
 
    # --------------------------------

    # CREATE WORKFLOW

    # --------------------------------
 
    workflow = make_workflow(

        vector_db

    )
 
    # --------------------------------

    # USER INPUT

    # --------------------------------
 
    image_path = input(

        "Enter image path: "

    ).strip()
 
    question = input(

        "Ask your safety question: "

    ).strip()
 
    # --------------------------------

    # CHECK IMAGE

    # --------------------------------
 
    if not os.path.exists(image_path):
 
        print(

            "Image not found."

        )
 
        return
 
    # --------------------------------

    # RUN WORKFLOW

    # --------------------------------
 
    result = workflow.invoke({
 
        "image_path": image_path,
 
        "question": question,
 
        "visual_result": "",
 
        "document_context": "",
 
        "sources": [],
 
        "final_answer": ""

    })
 
    # --------------------------------

    # DISPLAY RESULT

    # --------------------------------
 
    print()

    print("=" * 50)
 
    print("VISUAL DETECTION")
 
    print("=" * 50)
 
    print(

        result["visual_result"]

    )
 
    print()
 
    print("=" * 50)
 
    print("DOCUMENT SOURCES")
 
    print("=" * 50)
 
    for source in result["sources"]:
 
        print("-", source)
 
    print()
 
    print("=" * 50)
 
    print("FINAL ANSWER")
 
    print("=" * 50)
 
    print(

        result["final_answer"]

    )
 
 
if __name__ == "__main__":
 
    main()
 