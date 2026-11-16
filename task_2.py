from typing import Callable, Iterator
import re
def sum_profit(text: str, func: Callable[[str],Iterator[float] ]) -> float:
    """Return the sum of all numbers produced by (func) for the given text."""
    total = 0
    for num in func(text):
        total += num
    return total

def generator_numbers(text: str) -> Iterator[float]:
    """Yield every real number in the text that is separated by whitespace."""
    text_list = text.split()
    for word in text_list:
        if re.fullmatch(r"\d+\.\d+", word):
            yield float(word)

if __name__ == "__main__":   
    text = "Загальний дохід працівника складається з декількох частин: 1000.01 як основний дохід, доповнений додатковими надходженнями 27.45 і 324.00 доларів."
    total_income = sum_profit(text, generator_numbers)
    print(f"Загальний дохід: {total_income}")


