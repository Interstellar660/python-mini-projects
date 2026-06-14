def calculate_pi(iterations: int = 1000000) -> float:
    pi = 0.0
    sign = 1.0
    for i in range(iterations):
        pi += sign / (2 * i + 1)
        sign = -sign
    return pi * 4


if __name__ == "__main__":
    import sys

    n = int(sys.argv[1]) if len(sys.argv) > 1 else 1000000
    pi = calculate_pi(n)
    print(f"π ≈ {pi} (iterations: {n})")
