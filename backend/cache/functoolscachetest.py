from functools import lru_cache
import time

@lru_cache(maxsize=1024)
def expensive_lookup(term: str) -> dict:
    time.sleep(10.0)
    return {"term": term, "result": term.upper()}

def main():
    print(expensive_lookup("mars"))
    time.time()
    print(expensive_lookup("mars"))
    time.time()

if __name__ == "__main__":
    main()
