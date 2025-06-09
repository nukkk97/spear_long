PROMPT = """
## Task: Longform Text-to-Speech Evaluation

**Longform TTS** is a task that involves evaluating the quality of synthesized speech generated from longform text inputs, focusing on speech naturalness and fluency.

You are given two speech clips, in the following order:

1. Audio A
2. Audio B

**Your task:**  
Ignore background noise and content — focus only on the naturalness and fluency of the speech. Decide which speech sounds more natural and fluent? (a) Audio A (b) Audio B.
"""

STRICT_OUTPUT = """
**Output format:**
Respond with either **(a)** or **(b)** only.
"""


def getPrompt(
    strict: bool = False,
):
    if strict:
        return PROMPT + STRICT_OUTPUT
    else:
        return PROMPT