def print_pyramid(n: int) -> None:
    for i in range(1, n + 1):
        print(' ' * (n - i) + '*' * (2 * i - 1))

def main() -> None:
    try:
        n = int(input("Enter number of rows (default 5): ") or 5)
        if n <= 0:
            raise ValueError
    except ValueError:
        print("Please enter a positive integer.")
        return
    print_pyramid(n)

if __name__ == "__main__":
    main()