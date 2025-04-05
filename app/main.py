from app.utils.exceptions import UnauthorizedPageException
from app.routers import api, login, reminders, root

from fastapi import FastAPI, Request
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException

app = FastAPI()
app.include_router(root.router)
app.include_router(api.router)
app.include_router(login.router)
app.include_router(reminders.router)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.exception_handler(UnauthorizedPageException)
async def unauthorized_exception_handler(request: Request, exc: UnauthorizedPageException):
  return RedirectResponse('/login?unauthorized=True', status_code=302)


@app.exception_handler(404)
async def page_not_found_exception_handler(request: Request, exc: HTTPException):
  if request.url.path.startswith('/api/'):
    return JSONResponse({'detail': exc.detail}, status_code=exc.status_code)
  else:
    return RedirectResponse('/not-found')


def custom_openapi():
  if app.openapi_schema:
    return app.openapi_schema

  description = \
    """Reminder8 is a web app for tracking reminders.
    """

  openapi_schema = get_openapi(
    title="Reminder8",
    version="1.0.0",
    description=description,
    routes=app.routes,
    tags=[
      {
        "name": "API",
        "description": "Backend API routes for managing reminder lists and items.",
      },
      {
        "name": "Pages",
        "description": "The main Reminder8 web pages.",
      },
      {
        "name": "Authentication",
        "description": "Routes for logging into and out of the app.",
      },
      {
        "name": "HTMX Partials",
        "description": "Routes that serve partial web page contents for HTMX-based requests.",
      },
    ]
  )

  app.openapi_schema = openapi_schema
  return app.openapi_schema


app.openapi = custom_openapi
