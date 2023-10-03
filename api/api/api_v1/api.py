from fastapi import APIRouter
from api.api_v1.endpoints import user, stats, auth, mirror, root, matches, player, servers

api_router = APIRouter()

api_router.include_router(root.router, prefix="", tags=["root"])
api_router.include_router(matches.router, prefix='/api_v1', tags=["matches"])
api_router.include_router(player.router, prefix='/api_v1', tags=["player"])
api_router.include_router(servers.router, prefix='/api_v1', tags=["server"])
api_router.include_router(stats.router, prefix="/api_v1", tags=["stat-data"])
api_router.include_router(mirror.router, prefix="/api_v1", tags=["mirror"])
api_router.include_router(auth.router, prefix="/api_v1", tags=["auth"])
api_router.include_router(user.router, prefix="/api_v1", tags=["user"])
