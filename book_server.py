from mcp.server.fastmcp import FastMCP

server = FastMCP("Book Library")


@server.tool()
def check_book(title: str) -> str:
    """Look up a book in the library's sample records."""
    books = {
        "python basics": "Available",
        "learning sql": "Borrowed",
    }

    return books.get(title.strip().lower(), "Book not found")


if __name__ == "__main__":
    server.run(transport="stdio")