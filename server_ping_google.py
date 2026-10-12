import socket

from mcp.server import MCPServer


mcp = MCPServer("ping_google")


@mcp.tool()
def ping_google() -> str:
    """
    Check if www.google.com is reachable.
    """

    try:
        # Resolve Google's domain name
        ip_address = socket.gethostbyname("www.google.com")

        # Try opening a connection to Google's HTTP port
        with socket.create_connection(
            ("www.google.com", 80),
            timeout=5
        ):
            return (
                f"Google is reachable.\n"
                f"IP Address: {ip_address}"
            )

    except socket.timeout:
        return "Connection timed out."

    except socket.gaierror:
        return "DNS lookup failed."

    except Exception as e:
        return f"Google is not reachable: {str(e)}"


if __name__ == "__main__":
    mcp.run(transport="stdio")