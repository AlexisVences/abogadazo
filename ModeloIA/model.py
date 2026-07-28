import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.environ["OLLAMA_NUM_THREADS"] = "16"  # Usa 12 hilos para LLM
from langchain_ollama import OllamaLLM
from langchain.chains import RetrievalQA
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from typing import Dict, List

class AsistenteLegal:
    #Categorias posibles para clasificar
    CATEGORIAS = {
        "multas": "Consultas sobre multas de tránsito, sanciones económicas y recursos",
        "procedimientos": "Consultas sobre trámites, procesos administrativos o judiciales",
        "reglamentacion": "Consultas sobre normas, leyes y reglamentos de tránsito",
        "general": "Otras consultas sobre legislación de tránsito"
    }

    def __init__(self):
        """
        Inicializa el asistente legal con:
        - Modelo de embeddings para búsqueda semántica
        - Base de conocimientos vectorial
        - Modelo LLM para generación de respuestas
        - Cadena de QA configurada
        """
        self._inicializar_modelos()
        self._configurar_cadena_qa()
        self._configurar_clasificador()

    def _inicializar_modelos(self):
        """Configura los modelos necesarios"""
        try:
            # 1. Modelo de embeddings
            self.embeddings = OllamaEmbeddings(model="mxbai-embed-large",)
            
            # 2. Base vectorial con las leyes
            self.vectorstore = FAISS.load_local(
                "legal_embeddings",
                self.embeddings,
                allow_dangerous_deserialization=True
            )
            
            # 3. Modelo de lenguaje (versión corregida de tu modelo)
            self.llm = OllamaLLM(
                model="gemma2:2b",
                temperature=0.3,
                num_ctx=2048,
                timeout=300,
                f16_kv=False,        # Más estable en CPU
            )
            
        except Exception as e:
            raise RuntimeError(f"Error inicializando modelos: {str(e)}")
        
    def _configurar_cadena_qa(self):
        """Configura la cadena de pregunta-respuesta"""
        # Prompt idéntico al que tenías originalmente
        prompt_template = """
        Eres un experto en legislación de tránsito con amplia experiencia en leyes y normativas. 
        Responde únicamente usando la información proporcionada en el contexto, que contiene artículos legales relacionados con la consulta.
        No inventes información fuera del contexto.
        Brinda una respuesta clara, detallada y precisa, citando los artículos relevantes.
        Si la consulta requiere opinión, emítela basada en los artículos del contexto.
        Si te piden ayuda u orientacion, emite un juicio que le sea de ayuda basado en los articulos proporcionados.

        Contexto: {context}
        Pregunta: {question}
        Respuesta precisa citando artículos y explicando la fundamentación legal:
        """

        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )
        
        # Crear cadena de QA
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(search_kwargs={"k": 3}),
            chain_type_kwargs={"prompt": prompt},
            return_source_documents=True
        )

    def _configurar_clasificador(self):
        """Configura el prompt para clasificación de consultas"""
        categorias_str = "\n".join([f"- {k}: {v}" for k, v in self.CATEGORIAS.items()])

        clasificador_template = f"""Clasifica la siguiente consulta legal sobre tránsito en una de estas categorías:
        {categorias_str}

        Devuelve SOLO la palabra clave de la categoría (multas, procedimientos, reglamentacion o general).

        Prioriza las primeras 3 categorias, si la consulta no entra en ninguna de esas 3 devuelve General

        Consulta: {{consulta}}
        Categoría:"""
        
        self.clasificador_prompt = PromptTemplate(
            template=clasificador_template,
            input_variables=["consulta"]
        )

    def _clasificar_consulta(self, consulta: str) -> str:
        """Clasifica la consulta en una de las categorías definidas"""
        try:
            # Usamos el mismo LLM pero con temperatura más baja para clasificación
            clasificador_chain = self.clasificador_prompt | self.llm
            categoria = clasificador_chain.invoke({"consulta": consulta}).strip().lower()
            
            # Validamos que la categoría sea válida
            return categoria if categoria in self.CATEGORIAS else "general"
            
        except Exception as e:
            print(f"Error al clasificar consulta: {str(e)}")
            return "general"

    def consultar(self, pregunta: str) -> Dict:
        try:
            # Paso 1: Clasificar la consulta
            categoria = self._clasificar_consulta(pregunta)
            print(categoria)

            # Paso 2: Obtener respuesta legal
            resultado = self.qa_chain.invoke({"query": pregunta})
            
            return {
                "respuesta": resultado["result"],
                "categoria": categoria,
                "fuentes": [
                    {
                        "documento": doc.metadata["source"],
                        "pagina": doc.metadata.get("page", "N/A")
                    }
                    for doc in resultado["source_documents"]
                ]
            }
            
        except Exception as e:
            return {
                "respuesta": f"Error procesando la consulta: {str(e)}",
                "categoria": "general",
                "fuentes": []
            }