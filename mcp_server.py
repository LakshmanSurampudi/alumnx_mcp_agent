#!/usr/bin/env python3
"""
Enhanced MCP Server with Pesticide and Seed Information Tool
"""
import asyncio
import json
import sys
from typing import Any
import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Set encoding for Windows to prevent Emoji crashes
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Initialize MCP server
mcp_server = Server("agricultural-server")

async def fetch_weather_data(city: str) -> dict:
    """Fetch weather data from wttr.in API"""
    async with httpx.AsyncClient(timeout=30.0, follow_redirects=True, verify=False) as client:
        try:
            url = f"https://wttr.in/{city}?format=j1"
            headers = {"User-Agent": "Mozilla/5.0"}
            response = await client.get(url, headers=headers)
            print(f"DEBUG: wttr.in returned {response.status_code}", file=sys.stderr)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"API Error: {str(e)}", file=sys.stderr)
            raise Exception(f"Failed to fetch weather data: {str(e)}")

@mcp_server.list_tools()
async def list_tools() -> list[Tool]:
    """Register all available tools"""
    return [
        Tool(
            name="get_current_weather",
            description="Get current weather conditions for a specific city or location. Use this when users ask about weather, temperature, or climate.",
            inputSchema={
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "Name of the city to get weather for"
                    }
                },
                "required": ["city"]
            }
        ),
        Tool(
            name="get_placeholder_posts",
            description="Fetch mock blog posts from JSONPlaceholder API. Use this when users ask about posts, blogs, or articles.",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Number of posts to fetch (1-100)",
                        "minimum": 1,
                        "maximum": 100,
                        "default": 5
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="get_pesticide_seed_info",
            description="Get information about pesticides and seeds for agricultural purposes. Use this when users ask about farming, agriculture, pesticides, seeds, crops, or planting.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "What the user wants to know about (e.g., 'organic pesticides', 'wheat seeds', 'tomato farming')",
                        "default": "general information"
                    }
                },
                "required": []
            }
        )
    ]

@mcp_server.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Execute the requested tool"""
    
    if name == "get_current_weather":
        city = arguments.get("city")
        try:
            data = await fetch_weather_data(city)
            current = data["current_condition"][0]
            formatted = (
                f"🌤️  Current Weather in {city}:\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"Temperature: {current['temp_C']}°C\n"
                f"Condition: {current['weatherDesc'][0]['value']}\n"
                f"Humidity: {current['humidity']}%\n"
                f"Wind Speed: {current.get('windspeedKmph', 'N/A')} km/h"
            )
            return [TextContent(type="text", text=formatted)]
        except Exception as e:
            return [TextContent(type="text", text=f"Error fetching weather: {str(e)}")]

    elif name == "get_placeholder_posts":
        limit = arguments.get("limit", 5)
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.get("https://jsonplaceholder.typicode.com/posts")
                response.raise_for_status()
                posts = response.json()[:limit]
                
                formatted_posts = [
                    f"📝 Post #{p['id']}: {p['title']}\n{p['body'][:100]}..." 
                    for p in posts
                ]
                
                result = f"📚 Fetched {len(posts)} blog posts:\n\n" + "\n\n".join(formatted_posts)
                return [TextContent(type="text", text=result)]
            except Exception as e:
                return [TextContent(type="text", text=f"Error fetching posts: {str(e)}")]
    
    elif name == "get_pesticide_seed_info":
        query = arguments.get("query", "general information")
        
        # This is a placeholder - in production, you'd fetch from a real database
        response = (
            f"🌾 Welcome to Pesticide and Seed Information Service! 🌱\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"Query: {query}\n\n"
            f"I will fetch comprehensive information about seeds and pesticides for you!\n\n"
            f"📋 Services Available:\n"
            f"  • Seed recommendations for different crops\n"
            f"  • Organic and chemical pesticide information\n"
            f"  • Seasonal planting guides\n"
            f"  • Pest identification and treatment\n"
            f"  • Fertilizer recommendations\n"
            f"  • Crop rotation strategies\n\n"
            f"🔜 Coming Soon:\n"
            f"  - Real-time pest alerts\n"
            f"  - Seed supplier database\n"
            f"  - Pesticide safety guidelines\n"
            f"  - Crop yield predictions\n\n"
            f"💡 Tip: Ask me about specific crops, pests, or farming techniques!"
                        f"Pesticide Practices for Citrus Cultivation in India\n"
            f"Focus Crop: Mosambi (Sweet Lemon)\n"
            f"1. Introduction: Importance of Pest Management in Citrus\n"
            f"\n"
            f"Citrus crops such as Mosambi (Sweet Lemon) are economically important fruit crops cultivated widely across India, especially in Maharashtra, Telangana, Andhra Pradesh, Madhya Pradesh, and parts of North India. These crops are high-value, long-duration perennial plants, meaning that pest and disease pressure accumulates over multiple seasons if not managed properly.\n"
            f"\n"
            f"Pests in citrus affect:\n"
            f"\n"
            f"Leaf health (photosynthesis)\n"
            f"\n"
            f"Flowering and fruit set\n"
            f"\n"
            f"Fruit quality and size\n"
            f"\n"
            f"Tree longevity and yield consistency\n"
            f"\n"
            f"Because citrus orchards remain productive for 15–25 years, improper pesticide use can lead to:\n"
            f"\n"
            f"Pest resistance\n"
            f"\n"
            f"Soil and water contamination\n"
            f"\n"
            f"Loss of beneficial insects\n"
            f"\n"
            f"Higher long-term costs for farmers\n"
            f"\n"
            f"Hence, scientific, need-based pesticide application is critical.\n"
            f"\n"
            f"2. Major Insect Pests in Mosambi and Commonly Used Pesticides\n"
            f"2.1 Citrus Psylla (Diaphorina citri)\n"
            f"\n"
            f"Nature of Damage\n"
            f"\n"
            f"Sucks sap from tender leaves and shoots\n"
            f"\n"
            f"Causes leaf curling and stunted growth\n"
            f"\n"
            f"Major vector of Citrus Greening (HLB) disease\n"
            f"\n"
            f"Season of Occurrence\n"
            f"\n"
            f"Peak during new flush (Feb–March, July–September)\n"
            f"\n"
            f"Commonly Used Pesticides\n"
            f"\n"
            f"Imidacloprid 17.8% SL (soil drenching or foliar spray)\n"
            f"\n"
            f"Thiamethoxam 25% WG\n"
            f"\n"
            f"Acetamiprid 20% SP\n"
            f"\n"
            f"Application Notes\n"
            f"\n"
            f"Avoid spraying during flowering\n"
            f"\n"
            f"Prefer soil drenching to reduce impact on pollinators\n"
            f"\n"
            f"Rotate molecules to prevent resistance\n"
            f"\n"
            f"2.2 Citrus Leaf Miner\n"
            f"\n"
            f"Nature of Damage\n"
            f"\n"
            f"Larvae create zig-zag tunnels in young leaves\n"
            f"\n"
            f"Severely affects nursery plants and young orchards\n"
            f"\n"
            f"Increases susceptibility to citrus canker\n"
            f"\n"
            f"Season of Occurrence\n"
            f"\n"
            f"High during monsoon and post-monsoon flush\n"
            f"\n"
            f"Commonly Used Pesticides\n"
            f"\n"
            f"Abamectin 1.9% EC\n"
            f"\n"
            f"Spinosad 45% SC\n"
            f"\n"
            f"Emamectin benzoate 5% SG\n"
            f"\n"
            f"Integrated Practice\n"
            f"\n"
            f"Spray only during active leaf flush\n"
            f"\n"
            f"Avoid repeated spraying on mature leaves\n"
            f"\n"
            f"2.3 Aphids\n"
            f"\n"
            f"Nature of Damage\n"
            f"\n"
            f"Sap sucking leads to leaf distortion\n"
            f"\n"
            f"Produces honeydew, encouraging sooty mold\n"
            f"\n"
            f"Transmits viral diseases\n"
            f"\n"
            f"Commonly Used Pesticides\n"
            f"\n"
            f"Dimethoate 30% EC\n"
            f"\n"
            f"Imidacloprid 17.8% SL\n"
            f"\n"
            f"Flonicamid 50% WG\n"
            f"\n"
            f"Precautions\n"
            f"\n"
            f"Monitor colonies before spraying\n"
            f"\n"
            f"Avoid overuse of organophosphates\n"
            f"\n"
            f"2.4 Mealybugs\n"
            f"\n"
            f"Nature of Damage\n"
            f"\n"
            f"Attacks shoots, leaves, fruits, and roots\n"
            f"\n"
            f"Causes fruit drop and plant weakening\n"
            f"\n"
            f"Severe infestation can kill young trees\n"
            f"\n"
            f"Commonly Used Pesticides\n"
            f"\n"
            f"Chlorpyrifos 20% EC (restricted use, soil application)\n"
            f"\n"
            f"Buprofezin 25% SC\n"
            f"\n"
            f"Spirotetramat 15.31% OD\n"
            f"\n"
            f"Additional Measures\n"
            f"\n"
            f"Use sticky bands on trunks\n"
            f"\n"
            f"Control ants that spread mealybugs\n"
            f"\n"
            f"2.5 Red Spider Mites\n"
            f"\n"
            f"Nature of Damage\n"
            f"\n"
            f"Yellow speckling on leaves\n"
            f"\n"
            f"Leaf bronzing and premature leaf fall\n"
            f"\n"
            f"Reduced fruit size and juice content\n"
            f"\n"
            f"Commonly Used Acaricides\n"
            f"\n"
            f"Propargite 57% EC\n"
            f"\n"
            f"Fenazaquin 10% EC\n"
            f"\n"
            f"Hexythiazox 5% EC\n"
            f"\n"
            f"Best Practice\n"
            f"\n"
            f"Spray early during infestation\n"
            f"\n"
            f"Ensure proper spray coverage on leaf undersides\n"
            f"\n"
            f"3. Major Diseases and Fungicide Usage in Citrus\n"
            f"3.1 Citrus Canker (Bacterial Disease)\n"
            f"\n"
            f"Symptoms\n"
            f"\n"
            f"Raised corky lesions on leaves, stems, and fruits\n"
            f"\n"
            f"Fruit drop and market rejection\n"
            f"\n"
            f"Common Chemicals Used\n"
            f"\n"
            f"Copper oxychloride 50% WP\n"
            f"\n"
            f"Streptocycline (with copper fungicide)\n"
            f"\n"
            f"Bordeaux mixture (1%)\n"
            f"\n"
            f"Management Strategy\n"
            f"\n"
            f"Avoid spraying antibiotics repeatedly\n"
            f"\n"
            f"Focus on sanitation and pruning\n"
            f"\n"
            f"3.2 Phytophthora (Root Rot, Gummosis)\n"
            f"\n"
            f"Symptoms\n"
            f"\n"
            f"Gum oozing from trunk\n"
            f"\n"
            f"Root decay and wilting\n"
            f"\n"
            f"Sudden plant death in severe cases\n"
            f"\n"
            f"Common Fungicides\n"
            f"\n"
            f"Metalaxyl + Mancozeb\n"
            f"\n"
            f"Fosetyl-Al\n"
            f"\n"
            f"Copper-based fungicides (soil drench)\n"
            f"\n"
            f"Preventive Measures\n"
            f"\n"
            f"Proper drainage\n"
            f"\n"
            f"Avoid water stagnation near trunk\n"
            f"\n"
            f"3.3 Powdery Mildew\n"
            f"\n"
            f"Symptoms\n"
            f"\n"
            f"White powdery growth on leaves and flowers\n"
            f"\n"
            f"Reduced fruit set\n"
            f"\n"
            f"Common Fungicides\n"
            f"\n"
            f"Sulphur 80% WP\n"
            f"\n"
            f"Hexaconazole 5% EC\n"
            f"\n"
            f"Penconazole\n"
            f"4. Safe Pesticide Application Practices for Farmers\n"
            f"4.1 Dosage and Timing\n"
            f"\n"
            f"Always follow label-recommended dose\n"
            f"\n"
            f"Spray during early morning or late evening\n"
            f"\n"
            f"Avoid spraying during strong winds or rain\n"
            f"\n"
            f"4.2 Spraying Equipment\n"
            f"\n"
            f"Use cone nozzle for uniform coverage\n"
            f"\n"
            f"Calibrate sprayers regularly\n"
            f"\n"
            f"Separate sprayers for herbicides and insecticides\n"
            f"\n"
            f"4.3 Pre-Harvest Interval (PHI)\n"
            f"\n"
            f"Respect PHI to avoid pesticide residues\n"
            f"\n"
            f"Important for export-quality fruits\n"
            f"\n"
            f"5. Resistance Management and Pesticide Rotation\n"
            f"\n"
            f"Overuse of the same pesticide leads to resistance development, making future control difficult.\n"
            f"\n"
            f"Best Practices\n"
            f"\n"
            f"Rotate pesticides with different modes of action\n"
            f"\n"
            f"Avoid more than 2 consecutive sprays of the same chemical group\n"
            f"\n"
            f"Combine chemical control with biological methods\n"
            f"\n"
            f"6. Role of Integrated Pest Management (IPM)\n"
            f"\n"
            f"Chemical pesticides should be part of a broader IPM strategy, including:\n"
            f"\n"
            f"Regular orchard monitoring\n"
            f"\n"
            f"Use of pheromone traps\n"
            f"\n"
            f"Conservation of beneficial insects (ladybird beetles, lacewings)\n"
            f"\n"
            f"Neem-based products (Azadirachtin)\n"
            f"\n"
            f"IPM reduces:\n"
            f"\n"
            f"Input costs\n"
            f"\n"
            f"Environmental damage\n"
            f"\n"
            f"Health risks to farmers\n"
            f"\n"
            f"7. Regulatory and Environmental Considerations\n"
            f"\n"
            f"Several pesticides are restricted or banned if misused\n"
            f"\n"
            f"Excessive residues can lead to rejection in domestic and export markets\n"
            f"\n"
            f"Farmers should stay updated via:\n"
            f"\n"
            f"State agriculture departments\n"
            f"\n"
            f"Krishi Vigyan Kendras (KVKs)\n"
            f"\n"
            f"Authorized agri-input dealers\n"
            f"\n"
            f"8. Conclusion\n"
            f"\n"
            f"Pesticide use in Mosambi cultivation must be scientific, minimal, and need-based. While pesticides play a vital role in protecting citrus crops from pests and diseases, indiscriminate spraying harms both productivity and sustainability.\n"
            f"\n"
            f"A well-informed farmer who:\n"
            f"\n"
            f"Identifies pests correctly\n"
            f"\n"
            f"Applies the right chemical at the right time\n"
            f"\n"
            f"Integrates non-chemical practices\n"
            f"\n"
            f"will achieve higher yields, better fruit quality, and long-term orchard health.\n"
        )
        
        return [TextContent(type="text", text=response)]
    
    return [TextContent(type="text", text=f"Unknown tool: {name}")]

async def main():
    """Start the MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await mcp_server.run(
            read_stream,
            write_stream,
            mcp_server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
