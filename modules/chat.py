import argparse
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama
from langchain_community.chat_models import ChatOllama
from langchain.prompts import PromptTemplate
from langchain_community.llms import HuggingFaceHub
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.embeddings import OllamaEmbeddings
import weaviate
from langchain_weaviate.vectorstores import WeaviateVectorStore






if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser(description='vv_chat-1.0.0')
        parser.add_argument('--question', help='The question you want answered', required=True)

        args = parser.parse_args()


        model_name = "sentence-transformers/all-mpnet-base-v2"
        model_kwargs = {'device': 'cpu'}
        encode_kwargs = {'normalize_embeddings': True}

        embedder = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs=model_kwargs,
            encode_kwargs=encode_kwargs
        )

        weaviate_url = "http://127.0.0.1:8080"
        weaviate_client = weaviate.connect_to_local()

        db = WeaviateVectorStore(
            client=weaviate_client, index_name="car_info", text_key="text",embedding=embedder
        )

        retriever_w = db.as_retriever(
            search_type="mmr",
            search_kwargs={'k': 6, 'lambda_mult': 0.25}
        )


        template = """
        Please use the following context to answer the question provided. If you don't know the answer, simply state that you don't know. Do not attempt to fabricate an answer.

        As a representative of VV-Automobile, it is essential to be courteous and helpful in every response. Remember, VV-Automobile specializes in selling parts and accessories, not cars but you can help with prices of cars and stats.

        When asked about general repair, dont focus on a specific car make or model.

        Don't mention header rows like product_name

        Keep your response to a maximum of five sentences. Be as concise and clear as possible.

        {context}

        Question: {question}

        Helpful Answer:
        """
        prompt = PromptTemplate.from_template(template)

        llm = ChatOllama(model="llama3", temperature=0.2)
        qa_chain = RetrievalQA.from_chain_type(
            llm,
            retriever=retriever_w,
            return_source_documents=True,
            chain_type_kwargs={"prompt": prompt})


        response = qa_chain.invoke(args.question)

        print(f"result:{response['result']}")
    except Exception as e:
        print(f"error:{str(e)}")

    finally:
        weaviate_client.close()