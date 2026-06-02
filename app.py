import os
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# 1. Load Environment Variables
load_dotenv()

def main():
    print("🎭 Personality-Shifting AI (Terminal Version)")
    print("-" * 45)
    print("Select a mode:")
    print("1. Funny AI 😂")
    print("2. Angry AI 🔥")
    print("3. Sad AI 😭")
    
    # Mode selection
    choice = input("\nEnter choice (1/2/3): ").strip()
    
    mode_prompts = {
        "1": ("Funny AI", "You are a funny AI chatbot you respond with humor and jokes. 😂"),
        "2": ("Angry AI", "You are an angry AI agent. You respond aggresively and impatiently. 🔥"),
        "3": ("Sad AI", "You are a sad AI chatbot you respond with deep melancholy and sighs. 😭")
    }
    
    # Default to Funny AI if invalid choice
    selected_mode, current_mode_prompt = mode_prompts.get(choice, mode_prompts["1"])
    print(f"\n🚀 System initialized as: **{selected_mode}**")
    print("Type 'exit' or 'quit' to stop the conversation.\n" + "="*45 + "\n")

    # Initialize model and message history with SystemMessage
    model = ChatMistralAI(model="mistral-small-2506", temperature=0.9)
    messages = [SystemMessage(content=current_mode_prompt)]

    # Conversation loop
    while True:
        try:
            user_input = input("👤 You: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ['exit', 'quit']:
                print("\nGoodbye!")
                break

            # 1. Append user message to history
            messages.append(HumanMessage(content=user_input))

            # 2. Invoke Mistral AI
            print("🤖 AI is thinking...")
            response = model.invoke(messages)

            # 3. Print response and append to history
            print(f"🤖 AI: {response.content}\n")
            messages.append(AIMessage(content=response.content))

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")

if __name__ == "__main__":
    main()