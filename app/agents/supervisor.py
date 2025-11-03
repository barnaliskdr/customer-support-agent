# from openai import OpenAI
# import json
# from app.agents.tools import tools
# from app.agents.agent_manager import AgentManager
# import google.generativeai as genai

# client = genai.configure(api_key="YOUR_API_KEY")
# agent_manager = AgentManager()

# class SupervisorLLM:
#     """Supervisor powered by LLM that routes user queries to the right agent."""

#     def handle_query(self, user_query: str):
#         messages = [
#             {
#                 "role": "system",
#                 "content": (
#                     "You are a supervisor model that routes user queries "
#                     "to the correct backend agent (like Product, User, or Cart). "
#                     "Use available tools wisely."
#                 ),
#             },
#             {"role": "user", "content": user_query},
#         ]

#         # response = client.chat.completions.create(
#         #     model="gpt-4o-mini",
#         #     messages=messages,
#         #     tools=tools,
#         #     tool_choice="auto",
#         # )

#         response = client.chat.completions.create(
#             model="gemini-1.5-flash",  # recommended Groq model
#             messages=messages
#         )

#         message = response.choices[0].message

#         if message.tool_calls:
#             tool_call = message.tool_calls[0]
#             func_name = tool_call.function.name
#             args = json.loads(tool_call.function.arguments)

#             print(f"🧩 LLM decided to call: {func_name}({args})")

#             func = agent_manager.get_agent_function(func_name)
#             if func:
#                 result = func(**args)
#                 return result
#             else:
#                 return {"error": f"Tool '{func_name}' not found."}

#         return {"response": message.content or "I’m not sure what to do."}


import json
import os
import google.generativeai as genai
from app.agents.tools import tools
from app.agents.agent_manager import AgentManager

# ✅ Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ✅ Initialize agent manager
agent_manager = AgentManager()

class SupervisorLLM:
    """Supervisor powered by Gemini that routes user queries to the correct backend agent."""

    def handle_query(self, user_query: str):
        try:
            # Print available tools for debugging
            print(
                f"Available tools:\n{json.dumps([t['function']['name'] for t in tools], indent=2)}"
            )

            # Prepare context
            prompt = f"""
            You are a supervisor model that routes user queries to the correct backend agent.
            The available tools are: {[t['function']['name'] for t in tools]}.
            Based on the user query, decide which tool and arguments should be used.Call the tool, 
            and share the exact response received from the toolin json format.

            User query: {user_query}
            """

            model = genai.GenerativeModel("gemini-2.0-flash")
            response = model.generate_content(prompt)

            # Parse JSON safely
            raw_text = response.text.strip()
            print("🔹 LLM raw response:", raw_text)

            try:
                parsed = json.loads(raw_text)
            except json.JSONDecodeError:
                return {"error": "Model response not in JSON format.", "raw": raw_text}

            tool_name = parsed.get("tool")
            args = parsed.get("arguments", {})

            if not tool_name:
                return {"error": "No tool selected by the model.", "raw": raw_text}

            print(f"🧩 LLM decided to call: {tool_name}({args})")

            # Get and call agent function
            func = agent_manager.get_agent_function(tool_name)
            if func:
                result = func(**args)
                return {"tool_used": tool_name, "result": result}
            else:
                return {"error": f"Tool '{tool_name}' not found."}

        except Exception as e:
            print("❌ Error in SupervisorLLM:", e)
            return {"error": str(e)}