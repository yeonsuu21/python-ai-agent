from agent import run_agent


def main():
    print("🤖 AI 업무 Agent")
    print("종료하려면 exit를 입력하세요.")

    while True:
        user_input = input("\n> ")

        if user_input.lower() == "exit":
            break

        try:
            result = run_agent(user_input)

            print("\n🤖 Agent")
            print(result)

        except Exception as e:
            print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()