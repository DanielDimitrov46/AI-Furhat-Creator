# AI-Furhat-Creator

Backend API for creating and managing conversational AI characters with Furhat robot integration.

## Features

- Create AI characters with custom prompts, languages, and voice/face configurations
- Manage conversation sessions with active/ended states
- Real-time conversation turns with AI-generated responses
- Furhat robot integration (facial expressions, head movements, actions)
- Conversation history tracking

## API Endpoints

### Characters
- **POST /characters** - Create a new AI character with name, prompt, language, voice/face settings
- **GET /characters** - List all available characters
- **GET /characters/{character_id}** - Retrieve specific character details

### Sessions
- **POST /characters/{character_id}/sessions** - Start a new conversation session with a character (optional user_id)
- **POST /sessions/{session_id}/end** - End an active conversation session

### Conversation
- **POST /sessions/{session_id}/user-turn** - Send user text input and receive character response with text, facial expressions, head movements, and actions

## Tech Stack

- FastAPI
- SQLAlchemy + PostgreSQL
- Pydantic for data validation
- Docker Compose for containerization