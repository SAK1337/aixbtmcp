"""FastAPI application entry point."""

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from mcp_aixbt import __version__
from mcp_aixbt.config import get_settings
from mcp_aixbt.middleware.logging import RequestLoggingMiddleware, configure_logging
from mcp_aixbt.routers import health, resources, tools


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Application lifespan context manager for startup/shutdown."""
    # Startup
    configure_logging()
    settings = get_settings()
    if settings.debug:
        print(f"Starting MCP AIXBT Server v{__version__} in debug mode")
    yield
    # Shutdown
    pass


app = FastAPI(
    title="MCP AIXBT Server",
    description="Model Context Protocol server for AIXBT market intelligence",
    version=__version__,
    lifespan=lifespan,
)

# Add middleware
app.add_middleware(RequestLoggingMiddleware)

# Register routers
app.include_router(health.router)
app.include_router(resources.router)
app.include_router(tools.router)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle uncaught exceptions."""
    return JSONResponse(
        status_code=500,
        content={
            "status": 500,
            "error": "Internal server error",
            "message": str(exc) if get_settings().debug else "An unexpected error occurred",
        },
    )


@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint."""
    return {
        "name": "MCP AIXBT Server",
        "version": __version__,
        "status": "running",
    }


def run() -> None:
    """Run the server using uvicorn."""
    import uvicorn

    settings = get_settings()
    uvicorn.run(
        "mcp_aixbt.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )


if __name__ == "__main__":
    run()
