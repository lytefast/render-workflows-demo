from render_sdk import Workflows, Retry
import asyncio
import os
import random

app = Workflows()


@app.task
def calculate_square(a: int) -> int:
    return a * a


@app.task
async def sum_squares(a: int, b: int) -> int:
    result1, result2 = await asyncio.gather(
        calculate_square(a),
        calculate_square(b),
    )
    return result1 + result2


@app.task(
    retry=Retry(
        max_retries=3,
        wait_duration_ms=1000,
        backoff_scaling=1.5,
    )
)
def flip_coin() -> str:
    if random.random() < 0.95:
        raise Exception("Flipped tails! Retrying.")
    return "Flipped heads!"

@app.task(
    retry=Retry(
        max_retries=3,
        wait_duration_ms=3000,
        backoff_scaling=1.5,
    )
)
def flip_coin_2() -> str:
    if random.random() < 0.55:
        raise Exception("Flipped tails! Retrying.")
    return "Flipped heads!"

@app.task
async def double_flip_coin() -> int:
    result1, result2 = await asyncio.gather(
        flip_coin_2(),
        flip_coin_2(),
    )
    return result1 == result2


@app.task
def print_env_vars() -> dict[str, str]:
    env_vars = dict(os.environ)
    for key, value in env_vars.items():
        print(f"{key}={value}")
    return env_vars


if __name__ == "__main__":
    app.start()
