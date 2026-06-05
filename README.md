# Weather MCP Server

Real-time weather query MCP server built on the [HelloAgents](https://github.com/datawhalechina/hello-agents) framework. Backed by [wttr.in](https://wttr.in), no API key required.

## Tools

| Tool | Description |
|---|---|
| `get_weather(city)` | Current weather for the given city (temperature, humidity, condition, wind, visibility). Accepts Chinese city names (北京/上海/...) and English. |
| `list_supported_cities()` | List all Chinese-name → English-name mappings the server knows about. |
| `get_server_info()` | Server name, version, and exposed tools. |

Output is JSON for every tool.

## Supported cities (Chinese aliases)

北京, 上海, 广州, 深圳, 杭州, 成都, 重庆, 武汉, 西安, 南京, 天津, 苏州, 长沙.
Any other string is forwarded to wttr.in as-is, so most major cities worldwide still work in English.

## Run locally

```bash
pip install hello-agents requests
python server.py
```

The server starts via `hello_agents.protocols.MCPServer.run()` and is ready to be wired into an MCP-aware client.

## Smithery deployment

This repo ships with a [`smithery.yaml`](smithery.yaml) describing the server, its tools, and metadata. Smithery container build expects a `Dockerfile` at the repo root — add one (any `python:3.11-slim` image installing `hello-agents` and `requests`, then running `python server.py`) before publishing if you target the container runtime.

## Example response

```json
{
  "city": "北京",
  "temperature": 22.0,
  "feels_like": 21.0,
  "humidity": 45,
  "condition": "Sunny",
  "wind_speed": 2.8,
  "visibility": 10.0,
  "timestamp": "2026-06-05 14:30:00"
}
```

## License

MIT
