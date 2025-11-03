import json
import os
import re
from bson import ObjectId
import google.generativeai as genai
from app.agents.tools import tools
from app.agents.agent_manager import AgentManager

# ✅ Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ✅ Initialize agent manager
agent_manager = AgentManager()


class SupervisorLLM:
    """Supervisor powered by Gemini that routes user queries to the correct backend agent."""
    def _sanitize_result(self, data):
        if isinstance(data, list):
            return [self._sanitize_result(i) for i in data]
        if isinstance(data, dict):
            return {k: self._sanitize_result(v) for k, v in data.items()}
        if isinstance(data, ObjectId):
            return str(data)
        return data



    def handle_query(self, user_query: str):
        try:
            # Debug info
            print("🧰 Available tools:", [t["function"]["name"] for t in tools])

            # Build model prompt
            prompt = f"""
            You are a supervisor model that routes user queries to the correct backend agent.
            The available tools are: {[t['function']['name'] for t in tools]}.

            Based on the user's query, respond with a valid JSON (no markdown or code block)
            containing the fields:
            {{
              "tool_name": "<tool_function_name>",
              "tool_arguments": {{ "<arg_name>": "<value>" }}
            }}

            Example:
            {{
              "tool_name": "get_all_products",
              "tool_arguments": {{}}
            }}

            User query: {user_query}
            """

            # 🔹 Call Gemini model
            model = genai.GenerativeModel("gemini-2.0-flash")
            response = model.generate_content(prompt)

            raw_text = response.text.strip()
            print("🔹 Raw model output:", raw_text)

            # 🧹 Clean markdown wrappers like ```json ... ```
            clean_text = self._clean_json(raw_text)

            # 🔸 Parse cleaned text as JSON
            try:
                parsed = json.loads(clean_text)
            except json.JSONDecodeError as e:
                print("❌ JSON Decode Error:", e)
                return {"error": "Model response not in JSON format.", "raw": raw_text}

            # Extract tool + args
            tool_name = parsed.get("tool_name")
            args = parsed.get("tool_arguments", {})

            if not tool_name:
                return {"error": "No 'tool_name' found in model output.", "raw": raw_text}

            print(f"🧩 LLM decided to call: {tool_name}({args})")

            # 🔧 Execute actual service method
            func = agent_manager.get_agent_function(tool_name)
            if func:
                result = func(**args)
                return {"tool_used": tool_name, "result": self._sanitize_result(result)}
            else:
                return {"error": f"Tool '{tool_name}' not found."}

        except Exception as e:
            print("❌ Exception in SupervisorLLM:", e)
            return {"error": str(e)}

    def _clean_json(self, text: str) -> str:
        """
        Remove ```json or ``` wrappers from LLM response.
        """
        text = text.strip()
        # Remove opening and closing code fences
        text = re.sub(r"^```(?:json)?", "", text)
        text = re.sub(r"```$", "", text)
        return text.strip()
