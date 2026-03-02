import sys
import inspect


def caching_fibonacci():
    cache = {}

    def fibonacci(n):
        if n <= 0:
            return 0
        if n == 1:
            return 1
        if n in cache:
            return cache[n]
        cache[n] = fibonacci(n - 1) + fibonacci(n - 2)
        return cache[n]

    def safe_fibonacci(n):
        if n <= 1:
            return fibonacci(n)

        cached_keys = [k for k in cache if k <= n]
        max_cached = max(cached_keys) if cached_keys else 1
        depth_needed = n - max_cached
        available_depth = sys.getrecursionlimit() - len(inspect.stack())

        if depth_needed >= available_depth:
            raise RecursionError(
                f"Cannot compute fibonacci({n}): needs ~{depth_needed} recursive calls, "
                f"but only {available_depth} frames available. "
                f"Try calling with smaller values first to warm up the cache."
            )
        
        return fibonacci(n)

    return safe_fibonacci


if __name__ == "__main__":
    fib = caching_fibonacci()
    
    print(fib(10))
    print(fib(15))
    print(fib(900))
    print(fib(1807))
    try:
        print(fib(5007))
    except RecursionError as e:
        print(f"Error: {e}")