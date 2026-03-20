const openai = new OpenAI();

const TOOLS = [{ type: "function", function: { name: "search", description: "Search the web", parameters: { type: "object", properties: { query: { type: "string" } }, required: ["query"] } } }];

async function processDocuments(docs) {
  for (const doc of docs) {
    const response = await openai.chat.completions.create({
      model: "gpt-4o",
      messages: [{ role: "user", content: doc.text }],
      tools: TOOLS
    });
  }
}
