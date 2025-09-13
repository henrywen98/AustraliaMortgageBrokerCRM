from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware

from app.core.config import settings
from app.api.routes import api_router
from app.db.base import init_db
from app.jobs.scheduler import start_scheduler


limiter = Limiter(key_func=get_remote_address, default_limits=[settings.RATE_LIMIT])


def create_app() -> FastAPI:
    app = FastAPI(title=settings.APP_NAME)
    app.state.limiter = limiter
    app.add_middleware(SlowAPIMiddleware)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix=settings.API_PREFIX)

    @app.get("/health")
    def health():
        return {"ok": True}

    @app.middleware("http")
    async def ip_blacklist_mw(request, call_next):
        if request.client and request.client.host in set(settings.IP_BLACKLIST):
            from fastapi.responses import JSONResponse
            return JSONResponse({"detail": "IP blocked"}, status_code=403)
        return await call_next(request)

    @app.on_event("startup")
    def _startup():
        try:
            init_db()
        except Exception:
            pass
        start_scheduler()

    return app


app = create_app()
