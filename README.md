# FastMCP Credential Storage Demo

A FastMCP server demonstrating secure credential storage with Redis and Fernet encryption.

## Purpose

Demonstrates secure credential management in FastMCP middleware using:
- Redis for distributed credential storage
- Fernet encryption for data protection
- HTTP transport for Docker deployment
- FastMCP CLI configuration

## Structure

```
fastmcp-test/
├── src/                    # Source code
│   ├── server.py          # FastMCP server with tools
│   ├── settings.py        # Configuration management
│   ├── middlewares.py     # Credential storage middleware
│   └── services/          # Mock API services
├── test_scripts/          # Test scripts
├── fastmcp.json          # FastMCP CLI configuration
├── docker-compose.yml     # Docker deployment
├── Dockerfile            # Multi-stage build
└── .env.example          # Environment template
```

## How to Run

### Local Development

1. **Setup environment**
```bash
cp .env.example .env
# Edit .env with your encryption keys
```

2. **Install dependencies**
```bash
uv sync
```

3. **Start server**
```bash
fastmcp run
```

### Docker Deployment

1. **Start services**
```bash
docker compose up -d
```

2. **Test with client**
```bash
python test_scripts/test_client_auth.py
```

## Available Tools

- `api_get_user_data(user_id)` - Fetch user data
- `db_query_users(limit)` - Query users from database

## Configuration

Key environment variables:
- `REDIS_HOST` - Redis server hostname
- `REDIS_PORT` - Redis server port  
- `ENCRYPTION_KEY` - Fernet encryption key

## Security Features

- Fernet encryption for stored credentials
- Automatic credential injection via middleware
- Namespaced Redis storage
- HTTP transport with health endpoints

## Testing

```bash
# Test client authentication
python test_scripts/test_client_auth.py

# Test health endpoint
curl http://localhost:8000/health