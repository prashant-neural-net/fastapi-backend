from fastapi import FastAPI

from . import models
from .database import engine
from .routers import user, post, auth, votes
from . import config

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(votes.router)


## root path
@app.get("/")
def root():
    return {"message": "jai mata di"}
    
