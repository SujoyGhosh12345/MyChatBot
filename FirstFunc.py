def printMyName(name: str) -> str:
    greeting = f"Hi, {name}!"
    return greeting

def main() -> None:
    lname = str(input("Enter your Name!: "))
    finalGreet = printMyName(lname)
    print(finalGreet)

if __name__ == "__main__":
    main()
