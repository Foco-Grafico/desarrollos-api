from fastapi import FastAPI, APIRouter

class App():
    def __init__(
        self,
        routers: list[APIRouter] = []
    ) -> None:
        self.app = FastAPI()

        for router in routers:
            self._add_router(router)
        pass

    def _add_router(self, router: APIRouter) -> None:
        self.app.include_router(router)

    def get_app(self) -> FastAPI:
        return self.app