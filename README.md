# FastMCP Credential Storage Demo

A comprehensive demonstration of secure credential storage in FastMCP using RedisStore with Fernet encryption, designed for multi-container deployments with modern uv tooling.

## 🎯 Overview

This project showcases how to implement secure credential management in FastMCP middleware by:

- **RedisStore**: Distributed storage for credentials across multiple server instances
- **Fernet Encryption**: Symmetric encryption to protect sensitive data at rest
- **Custom Middleware**: Automatic credential injection into tool calls
- **Multi-Container Support**: Docker Compose setup with load balancing
- **uv Integration**: Modern Python package management with multi-stage Docker builds
- **Package Organization**: Clean, modular structure with separate packages

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  FastMCP Server │    │  FastMCP Server │    │  FastMCP Server │
│       #1        │    │       #2        │    │       #3        │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                    ┌─────────────▼─────────────┐
                    │        Redis Store        │
                    │  (Encrypted Credentials)  │
                    └───────────────────────────┘
```

## 📁 Project Structure

```
fastmcp-test/
├── src/                       # Source code
│   ├── main.py               # FastMCP server with tools
│   ├── config.py             # Configuration management
│   ├── middleware.py         # Credential storage middleware
│   └── services.py           # Mock API services
├── scripts/                   # Utility scripts
│   ├── generate_keys.py      # Key generator
│   └── test_credential_flow.py  # Test suite
├── compose.yml               # Docker Compose configuration
├── Dockerfile                # Multi-stage uv build
├── pyproject.toml           # uv project configuration
├── uv.lock                  # uv lock file
├── .dockerignore           # Docker build exclusions
├── .env.example            # Environment template
└── README.md               # This file
```

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- uv (Python package manager)
- Python 3.13+
- Redis (if running locally)

### 1. Install uv

```bash
# macOS
brew install uv

# Linux/Windows
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Clone and Setup

```bash
git clone <repository-url>
cd fastmcp-test
```

### 3. Install Dependencies

```bash
uv sync
```

### 4. Generate Encryption Keys

```bash
# Using the script
python scripts/generate_keys.py
```

Copy the generated keys to your `.env` file:

```bash
cp .env.example .env
# Edit .env with your generated keys
```

### 5. Start with Docker Compose

```bash
# Start all services
docker compose up -d

# View logs
docker compose logs -f

# Stop services
docker compose down
```

### 6. Test the Setup

```bash
# Run credential flow tests
python scripts/test_credential_flow.py

# Test FastMCP CLI locally
fastmcp run src/fastmcp_demo/server/main.py
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `REDIS_HOST` | Redis server hostname | `localhost` |
| `REDIS_PORT` | Redis server port | `6379` |
| `REDIS_PASSWORD` | Redis authentication password | (none) |
| `STORAGE_ENCRYPTION_KEY` | Fernet encryption key | (required) |
| `JWT_SIGNING_KEY` | JWT signing key | (required) |
| `SERVER_NAME` | Server instance name | `fastmcp-credential-demo` |

### Security Notes

- **Never commit encryption keys to version control**
- **Use different keys for each server in production**
- **Store keys in a secure secret manager**
- **Rotate keys regularly**

## 🔌 Available Tools

### API Tools
- `api_get_user_data(user_id)` - Fetch user data from external API
- `api_fetch_metrics(metric_type)` - Get system metrics

### Database Tools  
- `db_query_users(limit)` - Query users from database
- `db_get_analytics(days)` - Get analytics data

### External Service Tools
- `service_fetch_weather(city)` - Get weather data
- `service_send_notification(message, recipient)` - Send notifications
- `service_process_payment(amount, currency)` - Process payments

### Admin Tools
- `admin_store_credentials(tool_name, credentials)` - Store tool credentials
- `admin_revoke_credentials(tool_name)` - Revoke tool credentials

## 🛡️ Security Features

### Encryption
- **Fernet symmetric encryption** for all stored credentials
- **32-byte encryption keys** for strong security
- **Automatic key validation** on startup

### Middleware Protection
- **Automatic credential injection** - No manual handling required
- **Response sanitization** - Credentials never leak in responses
- **Tool-based access control** - Credentials only injected when needed

### Distributed Security
- **Namespaced storage** - Isolation between server instances
- **Redis authentication** - Network-level security
- **TLS support** - Encrypted Redis connections

## 🐳 Docker Deployment

### Multi-Stage Build with uv

The project uses uv's multi-stage Docker build pattern for optimal image sizes and build performance:

```dockerfile
# Builder stage with uv
FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim AS builder
# ... dependency installation ...

# Production stage
FROM python:3.14-slim-bookworm AS production
# ... copy only necessary artifacts ...
```

### Single Server
```bash
docker build -t fastmcp-credentials .
docker run -p 8000:8000 --env-file .env fastmcp-credentials
```

### Multi-Server Cluster
```bash
docker compose up -d
```

This creates:
- 1 Redis instance
- 3 FastMCP server instances
- 1 Nginx load balancer

### Scaling
```bash
# Add more server instances
docker compose up -d --scale fastmcp-server=5
```

## 🧪 Testing

### Run Test Suite
```bash
python scripts/test_credential_flow.py
```

### CLI Commands
```bash
# Run server locally with FastMCP CLI
fastmcp run src/main.py

# Run with HTTP transport
fastmcp run src/main.py --transport http --port 8000

# Inspect server without running
fastmcp inspect src/main.py

# Run with additional packages
fastmcp run src/main.py --with httpx --with numpy
```

### Test Coverage
- ✅ Credential storage and retrieval
- ✅ Cross-server credential sharing
- ✅ Encryption/decryption security
- ✅ Mock API integration
- ✅ Middleware functionality

## 📊 Monitoring

### Health Checks
- **Redis connectivity** - Automatic health monitoring
- **Encryption validation** - Key format verification
- **Service availability** - Container health checks

### Logging
- **Credential operations** - All storage/retrieval actions logged
- **Security events** - Failed access attempts tracked
- **Performance metrics** - Request timing and success rates

## 🔍 How It Works

### 1. Credential Storage Flow
```
Tool Call → Middleware Detection → Credential Retrieval → Decryption → Injection → Tool Execution
```

### 2. Encryption Process
```
Plain Credentials → Fernet Encryption → Redis Storage → Fernet Decryption → Plain Credentials
```

### 3. Multi-Server Sharing
```
Server 1 Store → Encrypted Redis → Server 2 Retrieve → Decrypted Usage
```

## 🚀 Production Considerations

### Security
- Use environment-specific encryption keys
- Implement proper secret management
- Enable Redis authentication and TLS
- Regular security audits

### Performance
- Redis connection pooling
- Credential caching strategies
- Load balancing configuration
- Monitoring and alerting

### Reliability
- Redis clustering for high availability
- Graceful degradation on Redis failures
- Backup and recovery procedures
- Disaster recovery planning

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔗 Related Resources

- [FastMCP Documentation](https://fastmcp.wiki)
- [uv Documentation](https://docs.astral.sh/uv/)
- [uv Docker Examples](https://github.com/astral-sh/uv-docker-example)
- [py-key-value-aio](https://github.com/strawgate/py-key-value)
- [Cryptography Fernet](https://cryptography.io/en/latest/fernet/)
- [Redis Documentation](https://redis.io/documentation)

## 🆘 Troubleshooting

### Common Issues

**uv Not Found**
```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or use brew
brew install uv
```

**Docker Build Issues**
```bash
# Clear Docker cache
docker builder prune

# Rebuild without cache
docker compose build --no-cache
```

**Redis Connection Failed**
```bash
# Check Redis is running
docker compose logs redis

# Test FastMCP CLI locally
fastmcp run src/fastmcp_demo/server/main.py --help
```

**Invalid Encryption Key**
```bash
# Generate new keys
python scripts/generate_keys.py

# Update .env file
vim .env
```

**Credential Not Found**
```bash
# Check middleware logs
docker compose logs fastmcp-server-1

# Verify Redis data
docker compose exec redis redis-cli --scan --pattern "*credentials*"
```

### Debug Mode
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
fastmcp run src/fastmcp_demo/server/main.py
```

---

**Built with ❤️ for secure FastMCP deployments using uv**