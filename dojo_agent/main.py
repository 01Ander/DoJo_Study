import os
import time
import uuid
import threading
from pathlib import Path

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# --- CONFIGURACIÓN ---
BASE_DIR = Path(__file__).parent.parent.absolute()
DB_PATH = os.path.join(BASE_DIR, "dojo_agent", "chroma_db")
IGNORED_DIRS = {".git", ".obsidian", "dojo_agent", "__pycache__", "archive"}

class DojoAgent:
    def __init__(self):
        print("🧠 Inicializando el DoJo Agent y la Base Vectorial Local...")
        # 1. Modelos
        self.llm = ChatOllama(model="gemma4:latest")
        self.embeddings = OllamaEmbeddings(model="nomic-embed-text")
        
        # 2. Base de Datos Vectorial
        self.vectorstore = Chroma(
            collection_name="dojo_knowledge",
            embedding_function=self.embeddings,
            persist_directory=DB_PATH
        )
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 4})
        
        # 3. Chain RAG (Read-Only)
        template = """Eres 'El Arquitecto', el asistente del sistema DoJo Study. 
Tu objetivo es responder a las preguntas usando ESTRICTAMENTE el contexto proporcionado, que pertenece a las notas del sistema DoJo del usuario.
Si la respuesta no está en el contexto, di simplemente: 'No encuentro información sobre esto en el DoJo.'

Contexto extraído del DoJo:
{context}

Pregunta del usuario: {question}

Respuesta:"""
        self.prompt = ChatPromptTemplate.from_template(template)
        
        self.chain = (
            {"context": self.retriever, "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

    def process_file(self, file_path):
        """Indexa o re-indexa un archivo Markdown específico en ChromaDB."""
        relative_path = str(Path(file_path).relative_to(BASE_DIR))
        print(f"\n🔄 Procesando y asimilando: {relative_path}")
        
        # 1. Eliminar vectores antiguos de este archivo si existen
        try:
            # Recuperar documentos con este 'source'
            existing_docs = self.vectorstore.get(where={"source": relative_path})
            if existing_docs and existing_docs["ids"]:
                self.vectorstore.delete(ids=existing_docs["ids"])
                print(f"   [!] Vectores previos eliminados para actualización delta.")
        except Exception as e:
            print(f"   [Error] No se pudo buscar/eliminar vectores antiguos: {e}")

        # 2. Cargar y fragmentar el nuevo contenido
        try:
            loader = TextLoader(file_path, encoding='utf-8')
            docs = loader.load()
            
            # Asegurar que el metadata tenga el source local relativo para facilidad
            for doc in docs:
                doc.metadata["source"] = relative_path
                
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            splits = text_splitter.split_documents(docs)
            
            # Generar IDs únicos para trazabilidad (opcional pero buena práctica)
            ids = [str(uuid.uuid4()) for _ in splits]
            
            # 3. Insertar nuevos vectores
            if splits:
                self.vectorstore.add_documents(documents=splits, ids=ids)
                print(f"   [+] {len(splits)} chunks asimilados en la base de datos.")
            else:
                print(f"   [-] Archivo vacío o sin texto útil. No se añadieron chunks.")
                
        except Exception as e:
            print(f"   [Error] al leer el archivo {relative_path}: {e}")

    def run_query(self, user_input):
        print(f"Consultando la memoria del DoJo para: '{user_input}'...\n")
        
        # Usar stream en lugar de invoke para ver las palabras aparecer en tiempo real
        response_text = ""
        for chunk in self.chain.stream(user_input):
            print(chunk, end="", flush=True)
            response_text += chunk
        print("\n")
        return response_text

class DojoWatcher(FileSystemEventHandler):
    def __init__(self, agent: DojoAgent):
        self.agent = agent

    def is_valid_file(self, path: str) -> bool:
        """Verifica que el archivo sea .md y no pertenezca a un directorio ignorado."""
        p = Path(path)
        if p.suffix != ".md":
            return False
        # Revisar si alguna de las carpetas padre está ignorada
        for parent in p.parents:
            if parent.name in IGNORED_DIRS:
                return False
        return True

    def on_modified(self, event):
        if not event.is_directory and self.is_valid_file(event.src_path):
            self.agent.process_file(event.src_path)
            # Re-dibujar el prompt para no romper la CLI
            print("\nDoJo Prompt >> ", end="", flush=True)

def index_all_existing_files(agent: DojoAgent):
    """Realiza un barrido inicial la primera vez para indexar lo existente."""
    print("Iniciando barrido y sincronización inicial...")
    for root, dirs, files in os.walk(BASE_DIR):
        # Modificamos dirs in_place para saltar directorios ignorados
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        
        for file in files:
            file_path = os.path.join(root, file)
            watcher = DojoWatcher(agent)
            if watcher.is_valid_file(file_path):
                # Solo procesar si el vector asociado a este 'source' no existe aún
                relative_path = str(Path(file_path).relative_to(BASE_DIR))
                existing_docs = agent.vectorstore.get(where={"source": relative_path})
                if not existing_docs or not existing_docs["ids"]:
                    agent.process_file(file_path)

if __name__ == "__main__":
    print("="*50)
    print("   THE DOJO AGENT (MVD - Read Only Mode)")
    print("="*50)
    
    agent = DojoAgent()
    
    # Rastrear archivos que existan antes de encender el vigía
    index_all_existing_files(agent)
    
    # Configurar y lanzar el vigía
    event_handler = DojoWatcher(agent)
    observer = Observer()
    observer.schedule(event_handler, str(BASE_DIR), recursive=True)
    
    # Iniciamos watcher en un hilo separado
    observer.start()
    
    print("\n🟢 Ojos y Memoria en línea. Monitorizando archivos...")
    print("Escribe 'exit' o 'quit' para salir.\n")
    
    try:
        while True:
            # Pequeño delay para que los prints iniciales fluyan antes del input
            time.sleep(0.5) 
            query = input("\nDoJo Prompt >> ")
            
            if query.lower().strip() in ['exit', 'quit']:
                print("\nApagando Sistemas...")
                break
                
            if query.strip() != "":
                print("\n[Respuesta]:")
                agent.run_query(query)
                
    except KeyboardInterrupt:
        print("\nInterrupción detectada. Apagando...")
        
    finally:
        observer.stop()
        observer.join()
