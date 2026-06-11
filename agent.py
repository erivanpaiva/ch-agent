# Before running the sample:
#    pip install azure-ai-projects>=2.1.0

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

endpoint = "https://ch-erivan-paiva-agent-resource.services.ai.azure.com/api/projects/ch-agent"

project_client = AIProjectClient(
    endpoint=endpoint,
    credential=DefaultAzureCredential(),
)

agent_name = "computing-historian"
agent_version = "1"

openai_client = project_client.get_openai_client()

def get_agent_response(prompt: str):
    return openai_client.responses.create(
        input=[{"role": "user", "content": prompt}],
        extra_body={"agent_reference": {"name": agent_name, "version": agent_version, "type": "agent_reference"}},
    )


def main_loop():
    print("Type 'quit' to exit.")
    while True:
        try:
            user_input = input("Agent prompt: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break

        if user_input.lower() == "quit":
            print("Exiting.")
            break

        if not user_input:
            continue

        try:
            response = get_agent_response(user_input)
            print(f"Response output: {response.output_text}")
        except Exception as e:
            print(f"Error getting response: {e}")


if __name__ == "__main__":
    main_loop()