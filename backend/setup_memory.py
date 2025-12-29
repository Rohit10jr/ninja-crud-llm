# setup_memory.py
from langgraph.checkpoint.postgres import PostgresSaver
from psycopg import connect

DB_URI = "postgresql://user:password@localhost:5432/your_db"

def init_db():
    # Standard psycopg connection
    with connect(DB_URI) as conn:
        checkpointer = PostgresSaver(conn)
        # This creates the actual tables in your Postgres DB
        checkpointer.setup()
        print("LangGraph memory tables created successfully!")

if __name__ == "__main__":
    init_db()