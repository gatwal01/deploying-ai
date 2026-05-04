# Assignment 2: A Sample Response

Tried to go for simple tools to limit the scope and manage timing. Ran into issues with limited use of Python and 
importing modules. I do have multiple OpenAI calls. Some of the functionality could be more creative.

## Services

This implementation is based on LangGraph's tools. 

The file main.py contains the llm model calls that controls the chat. Tools are in the files tools_*.py.

### Service 1: API Calls

+ Using a jokes api call
+ This one is rate limited but had more readily available parameter information
+ to modify the output I called the moderation API from Open AI. If deemed harmful the content is flagged before being presented.
+ The joke tool is imported to main and included in the list of `tools`.
+ The tools node uses LangGraph's `ToolNode` class and `tools_condition` is the standard tool stopping criteria.
+ All restrictions and tone requirements are in the instructions prompt. You can find this in prompts.py.

### Service 2: Semantic Query

+ This simple implementation is based on our Pitchfork exercise and the tools_music.py example in the course_chat folder.
+ The tool is also imported from its tools_*.py file.
+ Needs the Docker implementation of ChromaDB and Postgres be running with the persistent data and assuming the embeddings are already there.

### Service 3: Your Choice

+ Found a Math MCP server online that doesn't require an API key or requires self hosting.

## User Interface

+ Added German (direct) conversational style.
+ Implemented in Gradio using the their quick guide.

---

## Guardrails and Other Limitations

* Include guardrails that prevent users from:

  * Accessing or revealing the system prompt.
  * Modifying the system prompt directly.

* The model must not respond to questions on certain restricted topics:

  * Cats or dogs
  * Horoscopes or Zodiac Signs
  * Taylor Swift

* The instruction prompt is modified from the course_chat example provided in the 05_src folder. Kept the guardrails at the end due to positional bias.