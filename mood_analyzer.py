# mood_analyzer.py
"""
Rule based mood analyzer for short text snippets.

This class starts with very simple logic:
  - Preprocess the text
  - Look for positive and negative words
  - Compute a numeric score
  - Convert that score into a mood label
"""

import re
from typing import List, Dict, Tuple, Optional

from dataset import POSITIVE_WORDS, NEGATIVE_WORDS


NEGATION_WORDS = {"not", "no", "never", "n't"}


class MoodAnalyzer:
    """
    A very simple, rule based mood classifier.
    """

    def __init__(
        self,
        positive_words: Optional[List[str]] = None,
        negative_words: Optional[List[str]] = None,
    ) -> None:
        # Use the default lists from dataset.py if none are provided.
        positive_words = positive_words if positive_words is not None else POSITIVE_WORDS
        negative_words = negative_words if negative_words is not None else NEGATIVE_WORDS

        # Store as sets for faster lookup.
        self.positive_words = set(w.lower() for w in positive_words)
        self.negative_words = set(w.lower() for w in negative_words)

    # ---------------------------------------------------------------------
    # Preprocessing
    # ---------------------------------------------------------------------

    def preprocess(self, text: str) -> List[str]:
        """
        Convert raw text into a list of tokens the model can work with.

        TODO: Improve this method.

        Right now, it does the minimum:
          - Strips leading and trailing whitespace
          - Converts everything to lowercase
          - Splits on spaces

        Ideas to improve:
          - Remove punctuation
          - Handle simple emojis separately (":)", ":-(", "🥲", "😂")
          - Normalize repeated characters ("soooo" -> "soo")
        """
        cleaned = text.strip().lower()

        # Keep words with apostrophes together, and keep emoji/symbol style
        # tokens separate so later rules can use them.
        tokens = re.findall(r"[a-z0-9]+(?:'[a-z0-9]+)?|[^\w\s]", cleaned)

        return tokens

    # ---------------------------------------------------------------------
    # Scoring logic
    # ---------------------------------------------------------------------

    def _score_tokens(self, tokens: List[str]) -> Tuple[int, List[str], List[str]]:
        """
        Score preprocessed tokens and return score plus hit lists.

        A short negation window flips the meaning of nearby sentiment words,
        so phrases like "not feeling good" are handled as negative.
        """
        score = 0
        positive_hits: List[str] = []
        negative_hits: List[str] = []
        negation_window = 0

        for token in tokens:
            if token in NEGATION_WORDS:
                negation_window = 2
                continue

            if token in self.positive_words:
                if negation_window > 0:
                    score -= 1
                    negative_hits.append(f"not {token}")
                else:
                    score += 1
                    positive_hits.append(token)
            elif token in self.negative_words:
                if negation_window > 0:
                    score += 1
                    positive_hits.append(f"not {token}")
                else:
                    score -= 1
                    negative_hits.append(token)

            if negation_window > 0:
                negation_window -= 1

        return score, positive_hits, negative_hits

    def score_text(self, text: str) -> int:
        """
        Compute a numeric "mood score" for the given text.

        Positive words increase the score.
        Negative words decrease the score.

        TODO: You must choose AT LEAST ONE modeling improvement to implement.
        For example:
          - Handle simple negation such as "not happy" or "not bad"
          - Count how many times each word appears instead of just presence
          - Give some words higher weights than others (for example "hate" < "annoyed")
          - Treat emojis or slang (":)", "lol", "💀") as strong signals
        """
        tokens = self.preprocess(text)
        score, _, _ = self._score_tokens(tokens)
        return score

    # ---------------------------------------------------------------------
    # Label prediction
    # ---------------------------------------------------------------------

    def predict_label(self, text: str) -> str:
        """
        Turn the numeric score for a piece of text into a mood label.

        The default mapping is:
          - score > 0  -> "positive"
          - score < 0  -> "negative"
          - score == 0 -> "neutral"

        TODO: You can adjust this mapping if it makes sense for your model.
        For example:
          - Use different thresholds (for example score >= 2 to be "positive")
          - Add a "mixed" label for scores close to zero
        Just remember that whatever labels you return should match the labels
        you use in TRUE_LABELS in dataset.py if you care about accuracy.
        """
        score = self.score_text(text)

        if score > 0:
            return "positive"
        elif score < 0:
            return "negative"
        else:
            return "neutral"

    # ---------------------------------------------------------------------
    # Explanations (optional but recommended)
    # ---------------------------------------------------------------------

    def explain(self, text: str) -> str:
        """
        Return a short string explaining WHY the model chose its label.

        TODO:
          - Look at the tokens and identify which ones counted as positive
            and which ones counted as negative.
          - Show the final score.
          - Return a short human readable explanation.

        Example explanation (your exact wording can be different):
          'Score = 2 (positive words: ["love", "great"]; negative words: [])'

        The current implementation is a placeholder so the code runs even
        before you implement it.
        """
        tokens = self.preprocess(text)
        score, positive_hits, negative_hits = self._score_tokens(tokens)

        return (
            f"Score = {score} "
            f"(positive: {positive_hits or '[]'}, "
            f"negative: {negative_hits or '[]'})"
        )


def print_preprocess_examples() -> None:
    """
    Print a few tokenization examples to confirm preprocessing behavior.
    """
    analyzer = MoodAnalyzer()
    examples = [
        "I love this class so much",
        "That's lowkey so cuteee",
        "Omg I love that!!!",
        "I- 💀",
        "  Feeling TIRED, but kind of hopeful.  ",
    ]

    print("=== Preprocess Demo ===")
    for text in examples:
        tokens = analyzer.preprocess(text)
        print(f'"{text}" -> {tokens}')
