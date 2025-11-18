"""
 Contact me:
   e-mail:   enrique@enriquecatala.com 
   Linkedin: https://www.linkedin.com/in/enriquecatala/
   Web:      https://enriquecatala.com
   Twitter:  https://twitter.com/enriquecatala
   Support:  https://github.com/sponsors/enriquecatala
   Youtube:  https://www.youtube.com/enriquecatala
   
"""
from os import environ
import json
from typing import Optional
from loguru import logger

from fastapi import FastAPI

app = FastAPI()

@app.get("/ready", tags=["health"])
def readiness_check():
    """
    Readiness check endpoint for Kubernetes readiness probe.
    Returns 200 if the application is ready to serve traffic.
    Add your checks here (database, cache, etc.)
    """
    # Add your readiness checks here
    # Example: check database connection, cache availability, etc.
    
    # For now, simple check
    ready = True
    
    if ready:
        return {
            "status": "ready",
            "service": "fastapi-helloworld"
        }
    else:
        return Response(
            content=json.dumps({"status": "not ready"}),
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            media_type="application/json"
        )


@app.get("/startup", tags=["health"])
def startup_check():
    """
    Startup check endpoint for Kubernetes startup probe.
    Returns 200 when application has finished starting up.
    """
    return {
        "status": "started",
        "service": "fastapi-helloworld"
    }


@app.get("/")
def root():
    """Root endpoint"""
    return {"message": "FastAPI Hello World", "status": "running"}

@app.get("/health")
def read_root():
    return {"status": "healthy"}

@app.get("/one/hello")
def read_root():
    if "HELLOWORLD_ENV" in environ:
        txt = environ.get('HELLOWORLD_ENV')
    else:
        txt = "HELLOWORLD_ENV not found!"
    return {"HELLOWORLD_ENV: {}".format(txt): "from /one/hello"}


@app.get("/get_api_key")
def read_api_key():
    api_key = ""    
    
    try:
        with open('/app/secrets/appconfig.conf') as f:
            js = json.load(f)
            api_key = js["api_key"]
            # Do something with the file

    except (IOError, FileNotFoundError, json.JSONDecodeError, KeyError) as e:
        logger.error(f"Failed to read API key: {e}")
        print("/app/secrets/appconfig.conf not accessible")

    return {"API_KEY": api_key}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
