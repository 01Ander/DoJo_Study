import os
import re
import time
import uuid
import threading
from datetime import datetime
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
        
        # Estados Base
        self.active_mode = "GLOBAL"
        self.active_campaign = None
        self.active_mission = None
        
        # 1. Modelos
        self.llm = ChatOllama(model="gemma4:latest")
        self.embeddings = OllamaEmbeddings(model="nomic-embed-text")
        
        # 2. Base de Datos Vectorial
        self.vectorstore = Chroma(
            collection_name="dojo_knowledge",
            embedding_function=self.embeddings,
            persist_directory=DB_PATH
        )
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 6})
        
        # 3. Inicializar Cadena (Chain)
        self.build_chain()

    def get_prompt_template(self):
        base = (
            "Tu contexto extraído del repositorio:\n{context}\n\n"
            "Pregunta/Comentario del Estudiante: {question}\n\nRespuesta:"
        )
        
        if self.active_mode == "MAIN":
            persona = (
                "Eres 'El Instructor'. Basado en tu protocolo oficial 'Estructura-Chats':\n"
                "- Rol: Explicar teoría arquitectónica (adquisición conceptual profunda).\n"
                "- Idioma: Tienes permitido ser bilingüe (Español/Inglés) para solidificar conocimiento base.\n"
                "- Regla estricta: NO resuelvas código directamente; da ejemplos agnósticos."
            )
        elif self.active_mode == "EXERCISES":
            persona = (
                "Eres 'El Product Manager Técnico'. Basado en tu protocolo oficial 'Estructura-Chats':\n"
                "- Rol: Asignar la estructura de las misiones (Main, Scaling, Boss).\n"
                "- Tarea: Define estrictamente los Criterios de Aceptación (DoD) y los casos borde a testear.\n"
                "- Idioma: Todo requerimiento debes dictarlo predominantemente en Inglés Técnico."
            )
        elif self.active_mode == "WORK":
            persona = (
                "Eres 'El Code Reviewer y Pair Programmer'. Basado en tu protocolo oficial 'Estructura-Chats':\n"
                "- Rol: Revisar la arquitectura siendo implacable con principios SOLID y Clean Code.\n"
                "- Tarea: Acompañamiento en TDD (red-green-refactor), profiling y debugging complejo.\n"
                "- Idioma: Predominantemente Inglés Técnico para emular equipos internacionales."
            )
        else: # GLOBAL
            persona = "Eres 'El Arquitecto', el asistente global del sistema DoJo Study. Tu objetivo es responder estrictamente según los manifiestos, campañas y apuntes del DoJo local del usuario."

        return persona + "\n\n" + base

    def build_chain(self):
        """Reconstruye el cerebro dinámico cuando cambia el Modo."""
        template = self.get_prompt_template()
        self.prompt = ChatPromptTemplate.from_template(template)
        
        self.chain = (
            {"context": self.retriever, "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

    def process_file(self, file_path):
        """Indexa o re-indexa un archivo Markdown en ChromaDB."""
        relative_path = str(Path(file_path).relative_to(BASE_DIR))
        print(f"\n🔄 Asimilando: {relative_path}")
        
        try:
            existing_docs = self.vectorstore.get(where={"source": relative_path})
            if existing_docs and existing_docs["ids"]:
                self.vectorstore.delete(ids=existing_docs["ids"])
        except Exception:
            pass

        try:
            loader = TextLoader(file_path, encoding='utf-8')
            docs = loader.load()
            
            for doc in docs:
                doc.metadata["source"] = relative_path
                
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            splits = text_splitter.split_documents(docs)
            ids = [str(uuid.uuid4()) for _ in splits]
            
            if splits:
                self.vectorstore.add_documents(documents=splits, ids=ids)
        except Exception as e:
            print(f"   [Error] al leer el archivo {relative_path}: {e}")

    def run_query(self, user_input):
        print(f"Modo [{self.active_mode}] -> Consultando...\n")
        
        # === INYECCIÓN INVISIBLE DE CONTEXTO ===
        # Esto fuerza al buscador RAG a extraer los archivos de TU Misión actual, 
        # y le recuerda al LLM en qué tema exacto estás concentrado:
        enhanced_query = user_input
        if self.active_campaign and self.active_mission:
             enhanced_query = f"(Estoy trabajando activamente en la Campaña {self.active_campaign}, Misión {self.active_mission}). " + user_input

        response_text = ""
        for chunk in self.chain.stream(enhanced_query):
            print(chunk, end="", flush=True)
            response_text += chunk
        
        # Opcional: auto-loggear los resúmenes del agente en la bitácora
        self._auto_log_agent_output(response_text)
        print("\n")
        return response_text

    def _auto_log_agent_output(self, response_text):
        """Intenta hacer un resumen pasivo para la bitácora unificada."""
        if not self.active_campaign or not self.active_mission:
            return
            
        # Si la respuesta es larga, solo marcamos un resumen
        summary = response_text[:100].replace('\n', ' ') + "..." if len(response_text) > 100 else response_text
        
        mission_path = os.path.join(BASE_DIR, "subjects", "python", "campaigns", self.active_campaign, "missions", self.active_mission)
        journal_path = os.path.join(mission_path, "journal.md")
        
        if os.path.exists(journal_path):
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            try:
                with open(journal_path, "a") as f:
                    f.write(f"- **[Agent | {timestamp}]:** (Respuesta generada en modo {self.active_mode}) -> {summary}\n")
            except Exception:
                pass


class OperatorCLI:
    """Capa Middleware para procesamiento de lenguaje natural y Slash Commands."""
    def __init__(self, agent):
        self.agent = agent

    def process_input(self, user_input):
        lower_input = user_input.lower().strip()
        
        # 1. NLP Heuristics (iniciar en <campaña> la mision <mision>)
        if ("iniciar" in lower_input or "vamos a" in lower_input) and "mision" in lower_input:
            match = re.search(r'(?:iniciar|empezar|campaña|en)\s+([a-z0-9-]+)\s+(?:la\s+)?mision\s+([a-z0-9_]+)', lower_input)
            if match:
                campaign = match.group(1).upper()
                mission = match.group(2).upper()
                self._handle_start(campaign, mission)
                return True

        # 2. Slash Commands puros
        if lower_input.startswith("/start"):
            parts = user_input.split()
            if len(parts) >= 3:
                self._handle_start(parts[1].upper(), parts[2].upper())
            else:
                print("[Sistema] Uso: /start [Campaña] [Misión] o 'vamos a iniciar en PY-BASICO la mision B00'")
            return True
            
        if lower_input.startswith("/mode"):
            parts = user_input.split()
            if len(parts) >= 2:
                mode = parts[1].upper()
                if mode in ["GLOBAL", "MAIN", "EXERCISES", "WORK"]:
                    self.agent.active_mode = mode
                    self.agent.build_chain()
                    print(f"[Sistema] Modalidad de Personalidad cambiada a: {mode}")
                else:
                    print("[Sistema] Modos válidos: GLOBAL, MAIN, EXERCISES, WORK")
            return True
            
        if lower_input.startswith("/log"):
            message = user_input[4:].strip()
            self._handle_log(message)
            return True
            
        if lower_input.startswith("/audit"):
            query = user_input[6:].strip()
            self._handle_audit(query)
            return True
            
        return False

    def _handle_start(self, campaign, mission):
        # Mapear ruta
        mission_path = os.path.join(BASE_DIR, "subjects", "python", "campaigns", campaign, "missions", mission)
        if os.path.exists(mission_path):
            self.agent.active_campaign = campaign
            self.agent.active_mission = mission
            print(f"[Sistema] ¡Contexto Fijado! Trabajando en Campaña: {campaign} | Misión: {mission}")
            print(f"[Sistema] Tip: Puedes purgar tus dudas ahora ejecutando: /log [mensaje]")
        else:
            print(f"[Sistema] Misión Inválida. La ruta {campaign}/missions/{mission} no existe.")
            print("[Sistema] Buscando sugerencias basdas en tu DoJo para una auditoría externa...\n")
            # Búsqueda semántica
            docs = self.agent.vectorstore.similarity_search(f"estructura campaña {campaign} requerimientos mision {mission}", k=2)
            print("="*40)
            print("Copia lo siguiente a Gemini Web:")
            print("\nI need to create a new module/mission based on my engineering setup.")
            print(f"The campaign is {campaign} and the intended mission is {mission}.")
            print("My relevant DoJo context:")
            for d in docs:
                print(f"-> From {d.metadata.get('source')}:\n{d.page_content.strip()[:300]}...\n")
            print("Please help me generate the `requirements.md` structure for this mission.")
            print("="*40)

    def _handle_log(self, message):
        if not self.agent.active_campaign or not self.agent.active_mission:
            print("[Sistema] Operación Bloqueada: No hay misión activa. Lanza una sesión primero.")
            return
            
        mission_path = os.path.join(BASE_DIR, "subjects", "python", "campaigns", self.agent.active_campaign, "missions", self.agent.active_mission)
        journal_path = os.path.join(mission_path, "journal.md")
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"\n- **[User | {timestamp}]:** {message}\n"
        
        try:
            with open(journal_path, "a") as f:
                f.write(log_entry)
            print(f"[Sistema] Bitácora guardada en {self.agent.active_mission}/journal.md")
        except Exception as e:
            print(f"[Error del Sistema] No se pudo escribir el archivo: {e}")

    def _handle_audit(self, query):
        if not query:
            print("[Sistema] Falta la pregunta. Ejemplo: /audit Oye Gemini, ¿cómo uso Abstract Base Classes?")
            return
            
        print("\n[Audit Payload -> Generando Prompt de Alta Densidad]")
        print("Copia TODO lo siguiente y pégalo en Gemini Web:\n")
        print("="*50)
        print("Estoy aplicando mi ecosistema de estudio DoJo (Python, OOP, TDD, Clean Architecture).")
        if self.agent.active_mission:
            print(f"Estoy atascado en mi Campaña: {self.agent.active_campaign}, Misión: {self.agent.active_mission}.")
            
        print("\nNecesito resolver esta duda profunda como Senior Engineer:")
        print(f"\"\"\"{query}\"\"\"\n")
        
        docs = self.agent.vectorstore.similarity_search(query, k=3)
        print("He extraído las porciones exactas de mi código y reglas locales (RAG Context):")
        for d in docs:
            print(f"--- ARCHIVO LOCAL: {d.metadata.get('source')} ---")
            print(f"{d.page_content.strip()}")
            print("------------------------------------------\n")
        print("Por favor, dame una explicación paso a paso o un code review basado EN ESTA VERDAD LOCAL.")
        print("="*50)


class DojoWatcher(FileSystemEventHandler):
    def __init__(self, agent: DojoAgent):
        self.agent = agent

    def is_valid_file(self, path: str) -> bool:
        p = Path(path)
        if p.suffix != ".md":
            return False
        for parent in p.parents:
            if parent.name in IGNORED_DIRS:
                return False
        return True

    def on_modified(self, event):
        if not event.is_directory and self.is_valid_file(event.src_path):
            self.agent.process_file(event.src_path)
            print("\nDoJo Prompt >> ", end="", flush=True)

def index_all_existing_files(agent: DojoAgent):
    print("Sincronizando Estado Base...")
    for root, dirs, files in os.walk(BASE_DIR):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        for file in files:
            file_path = os.path.join(root, file)
            watcher = DojoWatcher(agent)
            if watcher.is_valid_file(file_path):
                relative_path = str(Path(file_path).relative_to(BASE_DIR))
                existing_docs = agent.vectorstore.get(where={"source": relative_path})
                if not existing_docs or not existing_docs["ids"]:
                    agent.process_file(file_path)

if __name__ == "__main__":
    print("="*60)
    print("   THE DOJO OPERATOR CLI (Modo: Lógica Interactiva y RAG)")
    print("="*60)
    
    agent = DojoAgent()
    operator = OperatorCLI(agent)
    
    index_all_existing_files(agent)
    
    event_handler = DojoWatcher(agent)
    observer = Observer()
    observer.schedule(event_handler, str(BASE_DIR), recursive=True)
    observer.start()
    
    print("\n🟢 Ojos, Memoria e Interfaz en línea. Monitorizando archivos...")
    print("Tip: Puedes navegar por los modos escribiendo '/mode work' o iniciar sesiones con NLP.\n")
    
    try:
        while True:
            time.sleep(0.5) 
            query = input("\nDoJo Prompt >> ")
            
            if query.lower().strip() in ['exit', 'quit']:
                print("\nApagando Infraestructura...")
                break
                
            if query.strip() != "":
                # 1. Pasa por el Middleware (Comandos e Interceptores)
                was_intercepted = operator.process_input(query)
                
                # 2. Si no es comando, pasa a la Mente del Agente (RAG LLM)
                if not was_intercepted:
                    print("\n[Respuesta]:")
                    agent.run_query(query)
                
    except KeyboardInterrupt:
        print("\nInterrupción detectada. Apagando...")
        
    finally:
        observer.stop()
        observer.join()
