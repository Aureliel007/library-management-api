from fastapi import FastAPI

import app.models
from app.lifespan import lifespan


app = FastAPI(
    title="Library RESTful API",
    description="RESTful API for library management",
    version="1.0.0",
    lifespan=lifespan
)
