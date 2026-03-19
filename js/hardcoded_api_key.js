// BAD: Hardcoded OpenAI API key in source — security and cost risk
const { OpenAI } = require("openai");

// Hardcoded key triggers js-hardcoded-api-key rule
const openai = new OpenAI({ apiKey: "sk-proj-abc123hardcodedkeyXYZ456" });

async function generateText(prompt) {
  const response = await openai.chat.completions.create({
    model: "gpt-3.5-turbo",
    messages: [{ role: "user", content: prompt }],
    max_tokens: 100
  });
  return response.choices[0].message.content;
}

module.exports = { generateText };
