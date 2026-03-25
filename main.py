from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
import requests
import re
import time
from functools import lru_cache

app = FastAPI()

CRAWLERS_URL = "https://raw.githubusercontent.com/JayBizzle/Crawler-Detect/master/raw/Crawlers.json"
BLOCKED_PATTERNS = []
LAST_UPDATE = 0
UPDATE_INTERVAL = 86400


def fetch_bot_patterns():
    global BLOCKED_PATTERNS, LAST_UPDATE
    try:
        patterns = []
        crawlers = requests.get(CRAWLERS_URL, timeout=10).json()
        print(crawlers)
        patterns.extend([bot['pattern'] for bot in crawlers])

        BLOCKED_PATTERNS = patterns
        LAST_UPDATE = time.time()
        is_bot.cache_clear()
        return True
    except:
        return False


fetch_bot_patterns()


@lru_cache(maxsize=1024)
def is_bot(user_agent: str):
    if time.time() - LAST_UPDATE > UPDATE_INTERVAL:
        fetch_bot_patterns()

    if not user_agent:
        return True

    for pattern in BLOCKED_PATTERNS:
        try:
            if re.search(pattern, user_agent, re.IGNORECASE):
                return True
        except re.error:
            continue
    return False


@app.middleware("http")
async def block_bots_middleware(request: Request, call_next):
    ua = request.headers.get("user-agent", "")
    if is_bot(ua):
        return JSONResponse(status_code=403, content={"detail": "Access denied for bots"})
    return await call_next(request)


@app.get("/run")
async def root():
    return {"message": "Welcome, human!"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5050, reload=True)