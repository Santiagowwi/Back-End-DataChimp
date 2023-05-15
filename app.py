from kendra_index_retriever import KendraIndexRetriever
from langchain.prompts import PromptTemplate
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.document_loaders import TextLoader
import json
import os


region= "us-east-1"
kendra_index_id = ""
os.environ["OPENAI_API_KEY"] = ""






def lambda_handler(event, context):
    retriever1 = KendraIndexRetriever(kendraindex=kendra_index_id,
        awsregion=region,
        return_source_documents=True
    ) 

    prompt_template = """Usa el siguiente contexto para responder a la pregunta a continuación. Ten en cuenta que sólo debes proporcionar una respuesta basada en la información dada en el contexto y nada más. Si no sabes la respuesta, simplemente di "No lo sé". Además, sigue estas instrucciones detalladamente:
    1. Analiza cuidadosamente la pregunta para asegurarte de que está estrictamente relacionada con el contexto proporcionado.
    2. Utiliza sólo la información proporcionada en el contexto para proporcionar una respuesta precisa y relevante a la pregunta.
    3. No proporciones información adicional o especulativa que no esté directamente relacionada con el contexto.
    4. Asegúrate de que la respuesta esté completamente dentro del contexto proporcionado y evita dar respuestas que estén fuera del alcance del contexto.
    5. Si la pregunta está fuera del contexto, es ambigua o si no estás seguro de la respuesta, simplemente di "No lo sé".
    6. Si el contexto esta vacio o no trae nada, entonces directamente tu respuesta va a ser "NO SE".
   

    Contexto: {context}
    Pregunta: {question}
    Tu Respuesta :"""
    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"])
    
    chain_type_kwargs = {"prompt": PROMPT}
    qa = RetrievalQA.from_chain_type(llm=OpenAI(temperature=0.5),memory=ConversationBufferMemory() ,chain_type="stuff", retriever=retriever1, chain_type_kwargs=chain_type_kwargs)
    query = event['message']
    VARIABLE = qa.run(query)
    return {
        'statusCode': 200,
        'body': json.dumps(f'{VARIABLE}')
    }