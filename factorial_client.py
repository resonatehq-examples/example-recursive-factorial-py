from __future__ import annotations

import asyncio
import os
from argparse import ArgumentParser
from typing import TYPE_CHECKING

from resonate.resonate import Resonate

if TYPE_CHECKING:
    from resonate.context import Context


async def main() -> None:
    parser = ArgumentParser(description="Calculate factorial of n")
    parser.add_argument("n", type=int, help="The number to compute the factorial of")
    args = parser.parse_args()

    r = Resonate(
        url=os.environ.get("RESONATE_URL", "http://localhost:8001"),
        group="factorial-client",
    )

    try:
        n = args.n
        promise_id = f"factorial-{n}"
        handle = r.options(target="factorial-worker").rpc(promise_id, "factorial", n)
        result = await handle.result()
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        await r.stop()


if __name__ == "__main__":
    asyncio.run(main())
