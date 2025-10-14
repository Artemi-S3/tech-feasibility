from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache
import time

app = FastAPI(title="FastAPI cache demo")

@app.on_event("startup")
def _init_cache():
    # for demo simplicity
    class MemoryBackend:
        store = {}
        async def get(self, key): return self.store.get(key)
        async def set(self, key, value, ttl=None): self.store[key] = value
    FastAPICache.init(MemoryBackend(), prefix="artemis3")

def compute_heavy(x): 
    # pretend heavy load
    time.sleep(0.5)
    return x * x

@cache(expire=120)
@app.get("/square/{x}")
async def square(x: int) -> dict:
    return {"s": x, "x^2": compute_heavy(x)} 
