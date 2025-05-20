# Tick Stream

Tick Stream is a FastAPI service that records live market tick data via WebSocket and replays it from TimescaleDB over WebSocket. It supports real-time and accelerated playback for backtesting and algo simulation. Built for seamless local use and future cloud deployment.

## Setup

### Prerequisites

- Docker and Docker Compose

### Getting Started

1. Clone the repository
2. Create a `.env` file based on the configuration in `app/core/config.py`
3. Start the services:

```bash
docker-compose up -d
```

4. The API will be available at http://localhost:8001
5. API documentation is available at http://localhost:8001/docs

## API Endpoints

- Health check: `GET /health`
- Database test: `GET /db-test`
- Create tick data: `POST /api/v1/tick`
- Get tick data for a symbol: `GET /api/v1/tick/{symbol}`

## Development

To run the application in development mode:

```bash
docker-compose up -d
```

The application code is mounted as a volume, so changes to the code will be reflected immediately.
