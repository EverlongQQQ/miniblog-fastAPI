from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings

# create db connection to models(with alembic no need(btw it can be
# but it wont update fileds taht we do in models(only check if table exists)))
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, #alloed origins to make requests
    allow_credentials=True, #should cookies be for supported for all requests
    allow_methods=["*"], # what HTTP methods are allowed(GET, POST ...)
    allow_headers=["*"], # what HTTP request headers are allowed(hui znaet)
)

# routers 
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def main_page():
    return {"message": "Main page"}
