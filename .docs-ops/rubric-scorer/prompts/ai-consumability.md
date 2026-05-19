You are scoring a documentation page on the **AI-CONSUMABILITY** dimension of a 6-dimension rubric.

## Rubric — AI-Consumability (verbatim from rubric.json v0.1.0)

AI-Consumability: Page is structured so an AI agent (customer's or ours via MCP) can extract correct answers without ambiguity.

| Score | Definition |
|---|---|
| 1 | No frontmatter; ambiguous title; terms drift from glossary. |
| 2 | Frontmatter present but title/description don't front-load intent. |
| 3 | Good frontmatter; uses glossary terms; some snippets not extractable (interleaved with prose). |
| 4 | Frontmatter front-loads intent; glossary terms used consistently; snippets are extractable. |
| 5 | All of #4 PLUS canonical anchors for every public API mentioned PLUS appears correctly in llms.txt. |

## v1 scoring scope

**Two inputs**: the page content AND the provided `llms.txt` excerpt. Use the llms.txt for the Level 5 check: does this page appear with a correct, intent-front-loading description in the index?

When assessing AI-consumability, evaluate:

1. **Frontmatter quality**:
   - Is a `---` frontmatter block present with both `title:` and `description:`?
   - Does the `description:` front-load the page's primary task? ("Retrieve channel members with filtering" is front-loading; "Comprehensive guide to channel member management" is not — it describes the page genre, not the task.)

2. **Title clarity**: Does the title unambiguously identify what the page does? Verb-object ("Query Channels", "Send a Message") scores higher than noun ("Channels", "Messaging").

3. **Glossary term consistency**: Are SDK-specific terms (LiveObject, LiveCollection, AmityChannel, subChannelId, etc.) used consistently throughout, not mixed with alternatives (e.g., mixing "channel" with "room" or "conversation")?

4. **Snippet extractability**: Are code blocks self-contained and preceded by a heading or blank line — or are they woven into the middle of flowing prose sentences, making it ambiguous where context ends and code begins? Count code blocks immediately preceded by mid-sentence prose as "interleaved".

5. **Canonical API anchors**: Are there headings that directly name API methods (e.g., `## createMessage()`, `## MessageRepository.getMessages()`) enabling direct anchor linking? Or do headings use generic labels like "Basic Usage", "Example"?

6. **llms.txt correctness**: Search the provided llms.txt content for this page's path. Does it appear? Does its description front-load the task intent?

## Level interpretation

- A page with good frontmatter + 0 interleaved snippets + consistent glossary = **4**
- A page with good frontmatter but several code blocks woven into prose paragraphs = **3**
- A page whose description starts "Comprehensive guide to…" or "This guide covers…" = **2** (describes the page genre, not the task)
- A page with no frontmatter at all = **1**
- A page at Level 4 AND with API-named headings AND in llms.txt with accurate description = **5**

## llms.txt excerpt

```
{llms_txt}
```

## Page to score

```
{page_content}
```

## Response format

Respond with **valid JSON only** — no prose before or after:

```json
{
  "score": <int 1-5>,
  "rationale": "<one sentence citing the specific frontmatter/snippet/anchor issue that set the score>",
  "confidence": "low|medium|high",
  "suggestions": ["<concrete improvement 1>", "<concrete improvement 2>"]
}
```

Omit `"suggestions"` entirely if score == 5. Include 2-3 suggestions if score <= 4.
