from __future__ import annotations

import asyncio
import os
from typing import TYPE_CHECKING

from resonate.resonate import Resonate

if TYPE_CHECKING:
    from resonate.context import Context


async def factorial(ctx: Context, n: int) -> int:
    print(f"Calculating factorial of {n}")
    if n <= 1:
        return 1
    result = await ctx.options(target="factorial-worker").rpc("factorial", n - 1)
    return n * result


async def main() -> None:
    r = Resonate(
        url=os.environ.get("RESONATE_URL", "http://localhost:8001"),
        group="factorial-worker",
    )
    r.register(factorial)
    print("Factorial worker is running...", flush=True)
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
