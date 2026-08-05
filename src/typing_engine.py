"""
Typing test engine and text generation.
"""
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
