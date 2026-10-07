from langchain.agents import create_agent


def sum(n1: int, n2: int) -> int:
    """Sums two integers and returns the result of the sum."""
    print("calling sum method")
    return n1 + n2


agent = create_agent(
    model="claude-sonnet-5-5",
    tools=[sum],
    system_prompt="You are a helpful assistant",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What is 9135 + 1352"}]}
)

print(result, "\n\n--- --- ---\n\n")
print(result["messages"], "\n\n--- --- ---\n\n")
print(result["messages"][-1].content_blocks)
