---
title: Weather MCP Server
emoji: 🌤️
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 8081
pinned: false
---

# Weather MCP Server

A real-time weather query MCP server built on the HelloAgents framework.

## Features

- 🌤️ Real-time weather queries
- 🌍 Built-in mapping for 13 major Chinese cities (Changsha included); any other city name is forwarded to wttr.in as-is, so most cities worldwide work via English names
- 🔄 Powered by the wttr.in API (no API key required)
- 🚀 Built on the HelloAgents framework
- 🐳 Ships with a Dockerfile, ready to deploy on Smithery

## Installation

```bash
pip install hello-agents requests
```

## Usage

### Run locally

```bash
python server.py
```

The server starts on `0.0.0.0:8081` over HTTP transport by default. Override with the `PORT` / `HOST` environment variables. The MCP endpoint is `http://<host>:<port>/mcp`.

### Use in Claude Desktop

Edit `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "weather": {
      "command": "python",
      "args": ["/path/to/server.py"]
    }
  }
}
```

### Use in HelloAgents

```python
from hello_agents import SimpleAgent, HelloAgentsLLM
from hello_agents.tools import MCPTool

agent = SimpleAgent(name="WeatherAssistant", llm=HelloAgentsLLM())
weather_tool = MCPTool(server_command=["python", "server.py"])
agent.add_tool(weather_tool)

response = agent.run("What's the weather in Beijing today?")
```

## API Tools

### get_weather

Get the current weather for a given city.

**Parameters:**
- `city` (string): City name (Chinese or English)

**Example:**
```json
{
  "city": "北京"
}
```

**Returns:**
```json
{
  "city": "北京",
  "temperature": 10.0,
  "feels_like": 9.0,
  "humidity": 94,
  "condition": "Light rain",
  "wind_speed": 1.7,
  "visibility": 10.0,
  "timestamp": "2026-06-05 13:25:03"
}
```

### list_supported_cities

List every Chinese city name the server has a built-in mapping for.

**Returns:**
```json
{
  "cities": ["北京", "上海", "广州", "深圳", "杭州", "成都", "重庆", "武汉", "西安", "南京", "天津", "苏州", "长沙"],
  "count": 13
}
```

### get_server_info

Return server metadata.

**Returns:**
```json
{
  "name": "Weather MCP Server",
  "version": "1.0.0",
  "tools": ["get_weather", "list_supported_cities", "get_server_info"]
}
```

## Supported cities

Beijing, Shanghai, Guangzhou, Shenzhen, Hangzhou, Chengdu, Chongqing, Wuhan, Xi'an, Nanjing, Tianjin, Suzhou, Changsha.

Any other city name is passed straight through to wttr.in, so most major cities worldwide work using their English name.

## Deploy on Smithery

The repo root already contains `smithery.yaml` and `Dockerfile`. Submit the repo URL on [Smithery](https://smithery.ai/) via "Publish Server":

```
https://github.com/CZ114/weather-mcp-server
```

## License

MIT License

## Author

ZheC
