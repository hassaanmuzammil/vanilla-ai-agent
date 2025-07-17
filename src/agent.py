import json
import re

class Agent():
    def __init__(
        self, 
        llm, 
        system_prompt, 
        known_actions,
        react_json=True,
        max_iterations=10,
        stop_words=("PAUSE",)
    ):
        self.llm = llm
        self.system_prompt = system_prompt
        self.known_actions = known_actions
        self.stop_words = stop_words
        self.react_json = react_json
        self.max_iterations = max_iterations
        self.messages = []
        if self.system_prompt:
            self.messages.append({"role": "system", "content": self.system_prompt})

    async def generate(self, prompt):
        stop = False
        res = ""
        for chunk in self.llm.stream(prompt):
            res += chunk
            yield chunk

            for word in self.stop_words:
                if word in res:
                    stop = True
                    break
            if stop:
                break
    
    def apply_chat_template(
        self, 
        messages,
        add_generation_prompt=True,
        start_token="<|im_start|>",
        end_token="<|im_end|>",
    ):
        prompt = ""
        for message in messages:
            role = message["role"]
            content = message["content"]

            prompt += f"{start_token}{role}\n{content}\n{end_token}\n"

        if add_generation_prompt:
            prompt += f"{start_token}assistant\n"
             
        return prompt

    def parse_action(self, text):
        
        action, action_input = None, None
        if self.react_json:
            """
            ```json
            {{
                "action": "<action>",
                "action_input": "<single_action_input>"
            }}
            ```
            """
            # from langchain.agents.output_parsers.react_json_single_input import ReactJsonSingleInputOutputParser
            # self.parser = ReactJsonSingleInputOutputParser()
            # parsed = self.parser.parse(text)
            # action = parsed.tool
            # action_input = parsed.tool_input
            pattern = re.compile(r"^.*?`{3}(?:json)?\n?(.*?)`{3}.*?$", re.DOTALL)
            found = pattern.search(text)
            if not found:
                raise ValueError("Action not found")
            action = found.group(1)
            try:
                response = json.loads(action.strip())
            except json.JSONDecodeError as e:
                raise ValueError(f"Failed to decode JSON action block: {e}")
            return {
                "action": response["action"], 
                "action_input": response.get("action_input", {})
            }
        else:
            """
            Action: <action>: <single_action_input>
            """
            pattern = re.compile(r"^Action: (w+): (.*)$")
            actions = [
                pattern.match(a) for a in text.split("\n") if pattern.match(a)
            ]
            if actions:
                action, action_input = actions[0].groups()
        return {
            "action": action, 
            "action_input": action_input
        }

    async def execute_tool(self, action, action_input):
        observation = await self.known_actions[action](action_input)
        return observation

    async def run(self, message):
        next_prompt = message

        for _ in range(self.max_iterations):
            self.messages.append({"role": "user", "content": next_prompt})

            prompt = self.apply_chat_template(self.messages)
            
            res = ""
            async for chunk in self.generate(prompt):
                res += chunk
                yield chunk
            self.messages.append({"role": "assistant", "content": res})

            if "Action:" in res:
                try:
                    parsed = self.parse_action(res)
                    action = parsed["action"]
                    action_input = parsed["action_input"]
                except Exception as e:
                    observation = (
                        "Error: Failed to parse action from response. "
                        "Carefully review the `Thought`, `Action`, `Action Input` format. "
                        f"Details: {str(e)}"
                    )
                    next_prompt = f"\nObservation: {observation}\n"
                    yield next_prompt
                    continue

                if action not in self.known_actions:
                    observation = f"Error: Unknown action: {action}"
                else:
                    try:
                        observation = await self.execute_tool(action, action_input)
                    except Exception as e:
                        observation = f"Error: Failed to execute tool: `{action}`. Details: {str(e)}"
                next_prompt = f"\nObservation: {observation}\n"
                yield next_prompt
            
            elif "Final Answer:" in res:
                break # Exit loop if final answer is provided
            else:
                observation = "Missing `Action` or `Final Answer` in response."

        return

if __name__ == "__main__":
    
    from src.llm import llm
    from src.config import SYSTEM_PROMPT_TEMPLATE, DB_SCHEMA
    from src.db import execute_sql

    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(schema=DB_SCHEMA)

    agent = Agent(
        llm=llm,
        system_prompt=system_prompt,
        known_actions={"execute_sql": execute_sql},
        react_json=True,
        max_iterations=10,
        stop_words=("PAUSE",)
    )

    async def main():
        async for response in agent.run("Provide the total number of orders by their statuses?"):
            print(response, end="", flush=True)

    import asyncio
    asyncio.run(main())