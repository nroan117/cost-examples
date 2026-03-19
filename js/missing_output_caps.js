// BAD: OpenAI chat completion without max_tokens — unbounded output cost
const { OpenAI } = require("openai");

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

async function summarize(text) {
  // Missing max_tokens — model can generate arbitrarily long response
  const response = await openai.chat.completions.create({
    model: "gpt-4",
    messages: [
      { role: "user", content: `Summarize this: ${text}` }
    ]
    // no max_tokens set — triggers js-missing-output-caps
  });
  return response.choices[0].message.content;
}

module.exports = { summarize };
