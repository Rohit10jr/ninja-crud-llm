# AI CRUD Memory Backend

This project implements a simple CRUD (Create, Read, Update, Delete) API using Django Ninja, integrated with LLM (Large Language Model) tools for performing CRUD operations. It features a simple frontend with persistent memory connected to a PostgreSQL database.

## Features

- **CRUD API**: Built with Django Ninja for fast and easy API development
- **LLM Integration**: AI-powered tools to interact with the CRUD operations
- **Persistent Memory**: PostgreSQL database for data retention
- **Simple Frontend**: User interface to interact with the API and LLM tools

## Tech Stack

- **Backend**: Django, Django Ninja
- **Database**: PostgreSQL
- **AI/LLM**: Integration with language models for CRUD operations
- **Frontend**: Simple web interface (to be implemented)

## Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Configure PostgreSQL database in `core/settings.py`
4. Run migrations: `python manage.py migrate`
5. Start the server: `python manage.py runserver`

## API Endpoints

The API provides standard CRUD operations for the main model (to be defined).

## LLM Tools

LLM tools allow natural language interaction with the CRUD operations, enabling users to perform database operations through conversational AI.

## Frontend

A simple web interface that connects to the API and LLM tools, with memory persistence in PostgreSQL.

## Contributing

Please read the contributing guidelines before making changes.

## License

This project is licensed under the MIT License.