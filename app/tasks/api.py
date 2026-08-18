from ninja import NinjaAPI

from tasks.router import router as tasks_router

tasks_api = NinjaAPI(title="Kronobot Tasks API", urls_namespace="tasks_api")
tasks_api.add_router("", tasks_router)
