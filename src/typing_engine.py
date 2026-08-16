#      TinyType is a minimal typing test software that sits in the corner of your screen while you work!
#      Copyright (C) 2026  Jon Evans
#
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.

from typing import List, Dict, Tuple, Optional
import random
import time


class TypingEngine:
    """Core typing test engine."""
    
    COMMON_WORDS: List[str] = [
        "the", "be", "to", "of", "and", "a", "in", "that", "have", "I",
        "it", "for", "not", "on", "with", "he", "as", "you", "do", "at",
        "this", "but", "his", "by", "from", "they", "we", "say", "her", "she",
        "or", "an", "will", "my", "one", "all", "would", "there", "their", "what",
        "so", "up", "out", "if", "about", "who", "get", "which", "go", "me",
        "when", "make", "can", "like", "time", "no", "just", "him", "know", "take",
        "people", "into", "year", "your", "good", "some", "could", "them", "see", "other",
        "than", "then", "now", "look", "only", "come", "its", "over", "think", "also",
        "back", "after", "use", "two", "how", "our", "work", "first", "well", "way",
        "even", "new", "want", "because", "any", "these", "give", "day", "most", "us"
    ]
    
    def __init__(self) -> None:
        """Initialize typing engine."""
        self.text: str = ""
        self.position: int = 0
        self.mistakes: Dict[str, int] = {}
        self.error_positions: List[int] = []
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None
        self.total_chars: int = 0
        self.error_count: int = 0
        self.ngram_errors: Dict[str, int] = {}
        self.ngram_total: Dict[str, int] = {}
        self._markov: Optional[Dict[str, Dict[str, int]]] = None
    
    def generate_text(
        self,
        word_count: int = 50,
        problem_chars: Optional[List[str]] = None,
        custom_text: Optional[str] = None
    ) -> str:
        """
        Generate typing test text.
        
        Args:
            word_count: Number of words to generate
            problem_chars: Optional list of problematic characters
            custom_text: Optional custom text to use instead of generated
            
        Returns:
            Generated text string
        """
        if custom_text and custom_text.strip():
            self.text = custom_text.strip()
            words: List[str] = self.text.split(" ")
            words = random.choices(words, k=word_count)
            self.text = " ".join(words)
        elif problem_chars and len(problem_chars) > 0:
            words: List[str] = self._generate_focused_text(problem_chars, word_count)
            self.text = " ".join(words)
        else:
            words = random.choices(self.COMMON_WORDS, k=word_count)
            self.text = " ".join(words)

        # self.text = random.choices(self.text.split(), k=word_count)

        self.position = 0
        self.mistakes = {}
        self.error_positions = []
        self.start_time = None
        self.end_time = None
        self.total_chars = 0
        self.error_count = 0
        self.ngram_errors = {}
        self.ngram_total = {}
        return self.text
    
    def _generate_focused_text(
        self,
        problem_chars: List[str],
        word_count: int
    ) -> List[str]:
        """
        Generate text focused on problem characters.
        
        Args:
            problem_chars: List of problematic characters
            word_count: Number of words to generate
            
        Returns:
            List of words
        """
        focused_words: List[str] = [
            w for w in self.COMMON_WORDS 
            if any(c in w for c in problem_chars)
        ]
        
        if len(focused_words) < word_count // 2:
            focused_words = self.COMMON_WORDS
        
        words: List[str] = []
        for i in range(word_count):
            if i % 3 == 0 and focused_words:
                words.append(random.choice(focused_words))
            else:
                words.append(random.choice(self.COMMON_WORDS))
        
        return words

    # ------------------------------------------------------------------
    # Error Gen: synthesize made-up English-like words from problem
    # letters and n-grams (bigrams, trigrams, polygrams).
    # ------------------------------------------------------------------

    def _build_markov(self, corpus: List[str]) -> None:
        """Build a character-level Markov model (contexts of length 1 and 2)
        from a corpus of English words so generated words fit English structure."""
        self._markov: Dict[str, Dict[str, int]] = {}
        for word in corpus:
            w = "^" + word.lower() + "$"
            for i in range(len(w) - 1):
                ctx = w[i]
                nxt = w[i + 1]
                self._markov.setdefault(ctx, {})
                self._markov[ctx][nxt] = self._markov[ctx].get(nxt, 0) + 1
            for i in range(len(w) - 2):
                ctx = w[i:i + 2]
                nxt = w[i + 2]
                self._markov.setdefault(ctx, {})
                self._markov[ctx][nxt] = self._markov[ctx].get(nxt, 0) + 1

    def _sample_next(self, context: str, problem_letters: Optional[List[str]]) -> str:
        """Sample the next character from the Markov model, boosting problem letters."""
        counts: Optional[Dict[str, int]] = self._markov.get(context) if self._markov else None
        if counts is None and context:
            counts = self._markov.get(context[-1]) if self._markov else None
        if counts:
            if problem_letters:
                counts = {
                    c: w * (3 if c in problem_letters else 1)
                    for c, w in counts.items()
                }
            return random.choices(list(counts.keys()), weights=list(counts.values()))[0]
        return random.choice("abcdefghijklmnopqrstuvwxyz")

    def _generate_word(
        self,
        problem_letters: Optional[List[str]],
        problem_ngrams: Optional[List[str]]
    ) -> str:
        """Generate one made-up word, seeding it with a problem n-gram when possible."""
        max_len: int = random.randint(3, 9)
        long_grams: List[str] = [g for g in (problem_ngrams or []) if len(g) >= 3]
        seed: Optional[str] = (
            random.choice(long_grams) if long_grams
            else (random.choice(problem_ngrams) if problem_ngrams else None)
        )
        word: str = ""
        context: str = "^"
        seed_used: bool = False
        while len(word) < max_len:
            if seed and not seed_used and len(word) + len(seed) <= max_len and random.random() < 0.6:
                word += seed
                seed_used = True
                context = ("^" + word)[-2:]
                continue
            nxt: str = self._sample_next(context, problem_letters)
            if nxt == "$":
                break
            word += nxt
            context = (context + nxt)[-2:]
        if not word:
            word = "word"
        return word

    def generate_error_gen_words(
        self,
        count: int,
        problem_letters: Optional[List[str]] = None,
        problem_ngrams: Optional[List[str]] = None,
        corpus: Optional[List[str]] = None
    ) -> List[str]:
        """Generate a list of made-up words biased toward the user's problem
        letters and n-grams."""
        if self._markov is None:
            self._build_markov(corpus or self.COMMON_WORDS)
        return [
            self._generate_word(problem_letters, problem_ngrams)
            for _ in range(count)
        ]

    def generate_error_gen_text(
        self,
        word_count: int,
        problem_letters: Optional[List[str]] = None,
        problem_ngrams: Optional[List[str]] = None,
        corpus: Optional[List[str]] = None
    ) -> str:
        """Generate a full Error Gen test, resetting engine state."""
        words: List[str] = self.generate_error_gen_words(
            word_count, problem_letters, problem_ngrams, corpus
        )
        self.text = " ".join(words)
        self.position = 0
        self.mistakes = {}
        self.error_positions = []
        self.start_time = None
        self.end_time = None
        self.total_chars = 0
        self.error_count = 0
        self.ngram_errors = {}
        self.ngram_total = {}
        return self.text

    def _ngrams_at(self, position: int) -> List[str]:
        """Return the alphabetic bigrams/trigrams/4-grams of the expected text
        that contain the character at `position`."""
        text: str = self.text
        grams: List[str] = []
        for n in (2, 3, 4):
            start: int = max(0, position - n + 1)
            end: int = min(position, len(text) - n)
            for i in range(start, end + 1):
                gram: str = text[i:i + n]
                if gram.isalpha():
                    grams.append(gram)
        return grams

    def process_char(self, char: str) -> Tuple[bool, bool]:
        """
        Process typed character.
        
        Args:
            char: Character typed by user
            
        Returns:
            Tuple of (is_correct, test_complete)
        """
        if self.start_time is None:
            self.start_time = time.time()
        
        if self.position >= len(self.text):
            return False, True
        
        expected: str = self.text[self.position]
        is_correct: bool = char == expected
        
        if not is_correct:
            self.error_count += 1
            self.error_positions.append(self.position)
            if expected not in self.mistakes:
                self.mistakes[expected] = 0
            self.mistakes[expected] += 1

        grams: List[str] = self._ngrams_at(self.position)
        for g in grams:
            self.ngram_total[g] = self.ngram_total.get(g, 0) + 1
        if not is_correct:
            for g in grams:
                self.ngram_errors[g] = self.ngram_errors.get(g, 0) + 1
        
        self.position += 1
        self.total_chars += 1
        
        test_complete: bool = self.position >= len(self.text)
        if test_complete:
            self.end_time = time.time()
        
        return is_correct, test_complete
    
    def backspace(self) -> bool:
        """
        Handle backspace key.
        
        Returns:
            True if backspace processed, False if at start
        """
        if self.position > 0:
            self.position -= 1
            if self.position in self.error_positions:
                self.error_positions.remove(self.position)
            return True
        return False
    
    def backspace_word(self) -> bool:
        """
        Delete entire word (backspace to previous space).
        
        Returns:
            True if word deleted, False if at start
        """
        if self.position == 0:
            return False
        
        while self.position > 0:
            self.position -= 1
            if self.position in self.error_positions:
                self.error_positions.remove(self.position)
            
            if self.position == 0 or self.text[self.position - 1] == ' ':
                break
        
        return True
    
    def calculate_wpm(self) -> float:
        """
        Calculate words per minute.
        
        Returns:
            WPM value
        """
        if not self.start_time or not self.end_time:
            return 0.0
        
        duration: float = self.end_time - self.start_time
        if duration == 0:
            return 0.0
        
        words: float = self.total_chars / 5.0
        minutes: float = duration / 60.0
        return words / minutes
    
    def calculate_accuracy(self) -> float:
        """
        Calculate typing accuracy.
        
        Returns:
            Accuracy percentage
        """
        if self.total_chars == 0:
            return 100.0
        
        correct: int = self.total_chars - self.error_count
        return (correct / self.total_chars) * 100.0
    
    def get_duration(self) -> float:
        """
        Get test duration in seconds.
        
        Returns:
            Duration in seconds
        """
        if not self.start_time:
            return 0.0
        
        end: float = self.end_time if self.end_time else time.time()
        return end - self.start_time
    
    def reset(self) -> None:
        """Reset the typing test."""
        self.position = 0
        self.mistakes = {}
        self.error_positions = []
        self.start_time = None
        self.end_time = None
        self.total_chars = 0
        self.error_count = 0
        self.ngram_errors = {}
        self.ngram_total = {}
