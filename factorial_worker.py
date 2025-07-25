from resonate import Resonate
from threading import Event

resonate = Resonate.remote(
    group="factorial-worker",
)

@resonate.register
def factorial(ctx, n):
    print(f"Calculating factorial of {n}")
    if n <= 1:
        return 1
    result = yield ctx.rpc("factorial", n - 1).options(target="poll://any@factorial-worker", id=f"factorial-{n-1}")
    return n * result

def main():
    resonate.start()
    print("Factorial worker is running...")
    Event().wait()

if __name__ == "__main__":
    main()