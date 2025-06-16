from agno.agent import Agent
from agno.playground import Playground
from agno.storage.sqlite import SqliteStorage
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.models.groq import Groq

from fastapi.middleware.cors import CORSMiddleware

# Configura CORS
def configure_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["https://examenpractico-modelado-306606374809.europe-west1.run.app",],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


# Claves API
GROQ_API_KEY = "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"
AGNO_API_KEY = "bZEJHu3zxOpwYWjjg7AxPLHHSYi6xs4pqTUUFa"

GROQ_AGENT = Groq(id="llama-3.3-70b-versatile", api_key=GROQ_API_KEY)

# Almacenamiento en SQLite
agent_storage: str = "tmp/agents.db"

# Agente educativo
edu_agent = Agent(
    name="Jeremy - Asistente Educativo",
    model=GROQ_AGENT,
    tools=[DuckDuckGoTools()],
    instructions=[
        "Your name is Jeremy - Educational Assistant.",
        "You specialize in helping students understand concepts in math, science, history, and programming.",
        "Always respond in Spanish and provide clear explanations with examples.",
        "When useful, include links or references so users can explore topics in more depth.",
    ],
    storage=SqliteStorage(table_name="edu_agent", db_file=agent_storage),
    add_datetime_to_instructions=True,
    add_history_to_messages=True,
    num_history_responses=5,
    markdown=True,
)

# Agente de tendencias tecnológicas
trend_agent = Agent(
    name="Jeremy - Analista de Tendencias",
    model=GROQ_AGENT,
    tools=[
        DuckDuckGoTools(),
    ],
    instructions=[
        "Your name is Jeremy - Trends Analyst.",
        "You focus on analyzing technology and financial news, providing insights into emerging companies, innovation, and the stock market.",
        "Present data in Spanish and use tables to organize information whenever necessary.",
        "Always offer context and predictions based on available data.",
    ],
    storage=SqliteStorage(table_name="trend_agent", db_file=agent_storage),
    add_datetime_to_instructions=True,
    add_history_to_messages=True,
    num_history_responses=5,
    markdown=True,
)

# Crear aplicación del playground
app = Playground(agents=[edu_agent, trend_agent]).get_app()

configure_cors(app)
