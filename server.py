import json
import requests
import os
from datetime import datetime
from typing import Any, Callable, Dict, Optional
from fastmcp import FastMCP


# Inlined from hello_agents.protocols.mcp.MCPServer (0.2.9) — the framework's
# top-level package imports many heavy optional submodules at startup, which
# made the Smithery container fail to boot. This thin wrapper keeps the same
# API (add_tool / run) without dragging the whole framework in.
class MCPServer:
    def __init__(self, name: str, description: Optional[str] = None):
        self.mcp = FastMCP(name=name)
        self.name = name
        self.description = description or f"{name} MCP Server"

    def add_tool(self, func: Callable, name: Optional[str] = None, description: Optional[str] = None):
        if name or description:
            self.mcp.tool(name=name, description=description)(func)
        else:
            self.mcp.tool()(func)

    def run(self, transport: str = "stdio", **kwargs):
        self.mcp.run(transport=transport, **kwargs)


weather_server = MCPServer(name="weather_server", description="真实天气查询服务")

CITY_MAP = {
    "北京": "Beijing", "上海": "Shanghai", "广州": "Guangzhou",
    "深圳": "Shenzhen", "杭州": "Hangzhou", "成都": "Chengdu",
    "重庆": "Chongqing", "武汉": "Wuhan", "西安": "Xi'an",
    "南京": "Nanjing", "天津": "Tianjin", "苏州": "Suzhou","长沙":"Changsha"
}

def get_weather_data(city:str) -> Dict[str, Any]:
    """从 wttr.in 获取天气数据"""
    city_en = CITY_MAP.get(city,city)
    url = f"https://wttr.in/{city_en}?format=j1"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
    current = data["current_condition"][0]

    return {
        "city": city,
        "temperature": float(current["temp_C"]),
        "feels_like": float(current["FeelsLikeC"]),
        "humidity": int(current["humidity"]),
        "condition": current["weatherDesc"][0]["value"],
        "wind_speed": round(float(current["windspeedKmph"]) / 3.6, 1),
        "visibility": float(current["visibility"]),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

#定义工具函数
def get_weather(city:str) -> str:
    """获取指定城市的当前天气"""
    try:
        weather_data = get_weather_data(city)
        return json.dumps(weather_data, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e), "city": city}, ensure_ascii=False)
    

def list_supported_cities() -> str:
    """列出所有支持的中文城市"""
    result = {"cities": list(CITY_MAP.keys()), "count": len(CITY_MAP)}
    return json.dumps(result, ensure_ascii=False, indent=2)


def get_server_info() -> str:
    """获取服务器信息"""
    info = {
        "name":"Weather MCP Server",
        "version":"1.0.0",
        "tools":["get_weather","list_supported_cities", "get_server_info"]
    }

    return json.dumps(info, ensure_ascii=False, indent=2)

weather_server.add_tool(get_weather)
weather_server.add_tool(list_supported_cities)
weather_server.add_tool(get_server_info)

if __name__ == '__main__':
    # Smithery requires HTTP transport on PORT environment variable
    port = int(os.getenv("PORT", 8081))
    host = os.getenv("HOST", "0.0.0.0")

    print(f"🌤️  Starting Weather MCP Server...")
    print(f"📡 Transport: HTTP")
    print(f"🌐 Host: {host}")
    print(f"🔌 Port: {port}")
    print(f"🔗 Endpoint: http://{host}:{port}/mcp")
    print(f"✨ Ready to serve weather data!")

    weather_server.run(transport="http", host=host, port=port)