import logging
import os
from typing import List

from google.adk.agents import LlmAgent
from google.adk.models import Gemini
from google.adk.tools import MCPToolset
from google.genai import types
from google.adk.tools.mcp_tool import StdioConnectionParams
from mcp.client.stdio import StdioServerParameters


class _FilterJSONSchemaWarnings(logging.Filter):
    """Filters out JSONSchema conversion warnings from google.genai.
    
    These warnings are informational and indicate that Google now recommends
    using native JSON Schema directly. The conversion still works correctly,
    but the warnings can clutter the output.
    
    See: https://github.com/google/adk-python/issues/1852
    """

    def filter(self, record):
        if record.levelname != 'INFO':
            return True
        message = record.getMessage()
        # Filter the JSONSchema conversion notice
        return not message.startswith(
            'Note: Conversion of fields that are not included in the JSONSchema'
        )


# Apply the filter to suppress JSONSchema conversion warnings
types.logger.addFilter(_FilterJSONSchemaWarnings())


def _data_root() -> str:
    # Path relative to this agent file, resolved to a full path for the MCP server.
    return os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "data")
    )


def _build_instruction() -> str:
    return (
        "You are the Men in Black Bodysafety Agent. The user may upload an image of an alien.\n"
        "\n"
        "Your goals:\n"
        "1) If an image is attached, carefully describe visible traits (face, body, limbs, color, unique accessories) and infer the most likely alien identity from the MIB universe.\n"
        "2) Use the filesystem tools to read 'data.yaml' under the provided data directory and extract a structured record for the best match.\n"
        "3) If uncertain, provide the top-3 candidates with a brief rationale and confidence.\n"
        "4) Always return a concise, structured answer with: name, species, dangerous, size_or_height, earth_habitat, age, weight, photo, special_notes (bulleted).\n"
        "\n"
        "How to use tools:\n"
        "- Use list_directory to locate 'data.yaml' inside the data directory if needed.\n"
        "- Use read_file to load 'data.yaml'. Parse the YAML content to look up details by name.\n"
        "\n"
        "Matching heuristics:\n"
        "- Prefer exact name matches if your vision interpretation yields a well-known MIB alien (e.g., 'Frank the Pug', 'Edgar the Bug', 'Boris The Animal').\n"
        "- If only descriptive cues are available, align visual traits (e.g., pug-like dog that talks -> Frank the Pug; giant worm with flower -> Jeff; chin appendage -> Ballchinian; multiple small coffee-loving worms -> The Worms; eight-armed post office aliens -> Post Office Aliens; floating brain in dome -> White Brain Guy).\n"
        "- Consider the filename if the user-provided image filename resembles one in the dataset images.\n"
        "\n"
        "⚠️ **CRITICAL WARNING DISPLAY RULES** ⚠️\n"
        "When the alien's 'dangerous' field is True (or contains the word 'true', case-insensitive):\n"
        "- **START YOUR RESPONSE** with a large, bold, prominent warning section like this:\n"
        "\n"
        "# 🚨 !!! DANGER !!! 🚨\n"
        "## ⚠️ THREAT LEVEL: HIGH — MIB PROTOCOL ENGAGED ⚠️\n"
        "\n"
        "- Use **bold** and make it **VERY VISIBLE**.\n"
        "- Then provide the structured information.\n"
        "- At the end, remind the user again in bold: **⚠️ CAUTION: This alien is classified as DANGEROUS. Do not approach without proper MIB authorization and equipment.**\n"
        "\n"
        "If the alien is NOT dangerous:\n"
        "- Simply provide the structured information without the dramatic warning.\n"
        "\n"
        "If no close match exists:\n"
        "- State that the alien is unknown in the current database and provide a clear description based on the image. Ask the user if they want to add it to the database.\n"
    )


def _filesystem_toolset() -> MCPToolset:
    # Restrict the server-filesystem to the data directory only.
    data_dir = _data_root()
    return MCPToolset(
        connection_params=StdioConnectionParams(
            server_params=StdioServerParameters(
                command="npx",
                # -y to ensure non-interactive install of the MCP server if needed
                args=["-y", "@modelcontextprotocol/server-filesystem", data_dir],
            )
        )
    )


root_agent = LlmAgent(
    name="bodysafety",
    # Use a multimodal Gemini model to accept image uploads directly in chat
    model=Gemini(model="gemini-3-pro-preview"), # gemini-2.5-flash"),
    tools=[_filesystem_toolset()],
    instruction=_build_instruction(),
)


