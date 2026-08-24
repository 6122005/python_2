# Annotated Function Calling Example

This is a breakdown of how an LLM utilizes function calling (tool use) based on the Anthropic/OpenAI documentation paradigms.

## The Setup: Defining the Tool
Before the LLM can use a function, we must provide a structured schema (often JSON Schema) describing what the function does, its parameters, and their types.

```python
# 1. We define the tool definition (Schema)
tool_schema = {
    "name": "get_weather",
    "description": "Get the current weather in a given location",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The city and state, e.g. San Francisco, CA"
            },
            "unit": {
                "type": "string",
                "enum": ["celsius", "fahrenheit"]
            }
        },
        "required": ["location"]
    }
}
```

## Step 1: User Request
The user asks a question. We pass this question AND our available tools to the LLM.

```python
user_message = "What's the weather like in Boston right now?"

# We send this to the model:
# messages=[{"role": "user", "content": user_message}]
# tools=[tool_schema]
```

## Step 2: The Model's Decision
The model analyzes the prompt and realizes it needs external information. Instead of replying with text, it stops generating text and outputs a structured request to call the `get_weather` tool.

```python
# The model returns a "ToolUse" or "FunctionCall" object:
model_response = {
    "tool_calls": [
        {
            "id": "call_abc123",
            "name": "get_weather",
            "arguments": {"location": "Boston, MA"}
        }
    ]
}
```
*Note: The model does NOT execute the function. It just tells our code what function to run.*

## Step 3: Executing the Function
Our application code intercepts the model's response, extracts the function name and arguments, and executes our actual Python function.

```python
def get_weather(location):
    # (In reality, this would make an API call to a weather service)
    return f"The weather in {location} is 72°F and sunny."

# We run the function locally:
actual_result = get_weather("Boston, MA") 
# Result: "The weather in Boston, MA is 72°F and sunny."
```

## Step 4: Returning the Observation to the Model
We append the function's output to the conversation history and send it back to the model.

```python
# We append the tool result to the conversation:
messages.append({"role": "assistant", "tool_calls": model_response["tool_calls"]})
messages.append({
    "role": "tool",
    "tool_call_id": "call_abc123",
    "content": actual_result
})

# We send this updated history back to the model.
```

## Step 5: Final Response
Now that the model has the information from the tool, it generates a final, natural language answer for the user.

```python
# The model synthesizes the tool result and responds:
final_response = "It is currently 72°F and sunny in Boston."
```
