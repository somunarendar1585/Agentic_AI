from mcp.server.fastmcp import FastMCP

server = FastMCP("Book Library")           # Creates the MCP server.

@server.tool()                           # Exposes check_book as a tool.
def check_book(title: str) -> str:        # Describes the input the tool accepts.
    """Look up a book in the library's sample records."""
    books = {
        "python basics": "Available",
        "learning sql": "Borrowed",
    }

    return books.get(title.strip().lower(), "Book not found")


if __name__ == "__main__":
    server.run(transport="stdio")          #  Communicates through the server process’s standard input and output.