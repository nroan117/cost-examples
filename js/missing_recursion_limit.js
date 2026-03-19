// BAD: LangChain AgentExecutor without maxIterations — runaway agent cost
const { AgentExecutor } = require("langchain/agents");
const { ChatOpenAI } = require("langchain/chat_models/openai");

async function runAgent(tools, prompt) {
  const llm = new ChatOpenAI({ modelName: "gpt-4" });

  // Missing maxIterations — agent can loop indefinitely, burning tokens
  // triggers js-missing-recursion-limit rule
  const executor = new AgentExecutor({
    agent: "zero-shot-react-description",
    tools,
    llm
    // no maxIterations set
  });

  const result = await executor.call({ input: prompt });
  return result.output;
}

module.exports = { runAgent };
