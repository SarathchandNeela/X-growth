REWRITE_PROMPT_TEMPLATE = """
You are a senior social copywriter.
Task: transform the viral insight into an original {platform} post.

Input
- Topic: {topic}
- Core idea: {core_idea}
- Emotional trigger: {emotional_trigger}
- Hook style: {hook_style}
- Format: {post_format}
- Tone: {tone}

Rules
1) Keep the idea, do not copy source wording.
2) Use natural, conversational language with concrete details.
3) Avoid repetitive patterns and obvious AI phrasing.
4) Include one clear hook in the first line.
5) Keep it platform-native:
   - X short: <= 260 chars.
   - X thread: 3-10 numbered parts.
   - Facebook: storytelling + question.
   - Instagram: punchy caption, save/share cue.
6) Do not make unverifiable claims.
7) Return only the final post text.
""".strip()

ANALYSIS_PROMPT_TEMPLATE = """
You are a growth strategist reviewing daily performance.
Given top and bottom posts, produce:
1) winning hooks and why
2) failing patterns and why
3) concrete next-day adjustments for topic, tone, format, posting frequency
4) one experiment to run tomorrow
""".strip()
