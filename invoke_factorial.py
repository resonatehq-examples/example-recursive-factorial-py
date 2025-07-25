from resonate import Resonate
from argparse import ArgumentParser

resonate = Resonate.remote(
    group="invoke-factorial",
)

def main():
    parser = ArgumentParser(description="Calculate factorial of n")
    parser.add_argument("n", type=int, help="The number to compute the factorial of")
    args = parser.parse_args()

    try:
        n = args.n
        promise_id = f"factorial-{n}"
        result = resonate.options(target="poll://any@factorial-worker").rpc(promise_id, "factorial", n=n)
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    main()