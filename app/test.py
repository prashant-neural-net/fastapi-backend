import asyncio
import time

async def make_tea() -> str:
    print("started making tea")
    await asyncio.sleep(5)
    print("tea is ready")
    return "tea"


async def make_toast() -> str:
    print("started making toast")
    await asyncio.sleep(3)
    print("toast is ready")
    return "toast"

async def main():
    start = time.perf_counter()

    toast_task = asyncio.create_task(make_toast())
    tea_task = asyncio.create_task(make_tea())

    tea, toast = await asyncio.gather(tea_task, toast_task)

    print(f"Finished in {time.perf_counter() - start:.2f} seconds")

asyncio.run(main())
