from ninja import NinjaAPI

from api.routers.events import router as events_router

api = NinjaAPI(title="Kronobot Events API", urls_namespace="events_api")
api.add_router("/events", events_router)
