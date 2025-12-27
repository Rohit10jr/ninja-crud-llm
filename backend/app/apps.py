from django.apps import AppConfig


class AppConfig(AppConfig):
    name = 'app'




# import os
# from django.apps import AppConfig
# from langgraph.checkpoint.postgres import PostgresSaver
# from psycopg import connect


# class AiAppConfig(AppConfig):
#     name = 'ai_app'

#     def ready(self):
#         # Only run this if we are starting the main server (not worker/migrations)
#         if os.environ.get('RUN_MAIN') == 'true':
#             # DB_URI = "postgresql://user:password@localhost:5432/your_db"
#             DB_URI = "postgresql://postgres:1234@localhost:5432/ninja_llm_crud?sslmode=disable"

#             with connect(DB_URI) as conn:
#                 checkpointer = PostgresSaver(conn)
#                 checkpointer.setup()