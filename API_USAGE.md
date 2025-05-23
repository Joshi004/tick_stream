# Tick Stream API Usage Guide

## API Endpoints

All API endpoints are prefixed with `/api/v1`.

### Streaming Ticks

To subscribe to real-time ticks for a specific instrument, use:

```
POST /api/v1/stream-ticks/subscribe/{instrument_code}
```

or 

```
GET /api/v1/stream-ticks/subscribe/{instrument_code}
```

Where `{instrument_code}` is the Kite instrument token (an integer value).

#### Example

To subscribe to instrument with code 4514561:

```
curl -X POST http://localhost:8001/api/v1/stream-ticks/subscribe/4514561
```

or 

```
curl http://localhost:8001/api/v1/stream-ticks/subscribe/4514561
```

#### Response

A successful response will look like:

```json
{
  "status": "success",
  "message": "Started streaming ticks for instrument 4514561",
  "instrument_code": "4514561"
}
```

### Notes

- The API requires Kite API credentials to be set in environment variables
- The WebSocket connection is maintained for the life of the application
- All received ticks are logged to the console
