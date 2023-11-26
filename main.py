from langchain.document_loaders.csv_loader import CSVLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.memory import ConversationBufferMemory
from fastapi import FastAPI, HTTPException
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores import Qdrant
from langchain.llms import GooglePalm

class LanguageModelManager:
    def __init__(self, google_api_key):
        self.google_api_key = google_api_key

    def create_model(self):
        llm = GooglePalm(google_api_key=self.google_api_key)
        return llm

class ChainSetup:
    def __init__(self, file_path):
        self.file_path = file_path

    def setup_chain(self):
        loader = CSVLoader(file_path=self.file_path)
        data = loader.load()
        embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

        qdrant = Qdrant.from_documents(
            data,
            embeddings,
            location=":memory:",
            collection_name="vector_database",
        )

        llm_manager = LanguageModelManager(google_api_key="AIzaSyD6Vlv1bz3QokAbLQTIswbz_afVvEQwxUo")
        llm = llm_manager.create_model()
        memory = ConversationBufferMemory(memory_key="chat_history", input_key="question", output_key='answer')
        chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever=qdrant.as_retriever(), memory=memory)
        return chain

class ConversationalChat:
    def __init__(self):
        self.chain = ChainSetup(file_path=r"D:\chabhi\bigbasketdata.csv").setup_chain()
        self.chat_history = []

    def chat(self, query):
        self.chat_history.append(query)
        combined_input = {"question": query, "chat_history": self.chat_history}
        result = self.chain(combined_input)
        return result["answer"]

app = FastAPI()
conversational_chat = ConversationalChat()

@app.post('/ask')
async def ask_question(user_input: dict):
    try:
        output = conversational_chat.chat(user_input['user_input'])
        return {"response": output}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
