import torch
import random
from typing import Dict, List


def bigrams_count_to_probabilities(
    bigram_counts: torch.Tensor, smooth_factor: int = 0
) -> torch.Tensor:
    """
    Convert bigram counts to a probability distribution.

    This function normalizes the counts of bigrams to create a probability distribution
    for each starting character, representing the likelihood of each subsequent character.

    Args:
        bigram_counts: torch.Tensor. A 2D tensor where each cell (i, j) contains the count
                       of the bigram formed by the i-th and j-th characters in the alphabet.
        smooth_factor: int. A value to add to each bigram count for smoothing purposes.

    Returns:
        torch.Tensor. A 2D tensor where each row is a normalized probability distribution,
        indicating the likelihood of each character following the character corresponding
        to the row index.
    """
    # Normalize each row to sum to 1, converting counts to probabilities, remember to add smooth_factor
    # TODO

    row_sum = torch.sum(bigram_counts, dim=1, keepdim=True)

    smoothed_bigrams = bigram_counts + smooth_factor
    row_sum_smoothed = row_sum + smooth_factor*bigram_counts.size(1)

    probability_tensor = smoothed_bigrams / row_sum_smoothed
    
    return probability_tensor



def calculate_neg_mean_log_likelihood(
    words: List[str],
    bigram_probabilities: torch.tensor,
    char_to_index: Dict[str, int],
    start_token: str = "<S>",
    end_token: str = "<E>",
) -> float:
    """
    Calculate the negative mean log likelihood of a list of words based on bigram probabilities.

    This function computes the negative mean log likelihood for a list of words using the provided bigram
    probability matrix. Each word's log likelihood is calculated using the 'calculate_log_likelihood'
    function, and the negative mean of these log likelihoods is returned.

    Args:
        words: List[str]. A list of words for which to calculate the mean log likelihood.
        bigram_probabilities: torch.Tensor. A 2D tensor representing the probability of each bigram.
        char_to_index: Dict. A dictionary mapping characters to their indices in the probability matrix.
        start_token: str. The character that denotes the start of a word. Shall be a single character.
        end_token: str. The character that denotes the end of a word. Shall be a single character.

    Returns:
        float. The negative mean log likelihood of the list of words.
    """
    # Initialize total log likelihood
    # TODO
    total_log_likelihood: torch.tensor = torch.tensor(0.0)

    # Calculate the log likelihood for each word and accumulate
    # TODO
    for word in words:
        total_log_likelihood += calculate_log_likelihood(word.lower(), bigram_probabilities, char_to_index, start_token, end_token)

    # Calculate and return the negative mean log likelihood
    # TODO
    mean_log_likelihood: float = (total_log_likelihood.item() / len(words))
    
    return mean_log_likelihood * (-1)


def sample_next_character(
    current_char_index: int,
    probability_distribution: torch.Tensor,
    idx_to_char: Dict[int, str],
) -> str:
    """
    Sample the next character based on the current character index and probability distribution.

    Args:
        current_char_index: int. Index of the current character.
        probability_distribution: torch.Tensor. A 2D tensor of character probabilities.
        idx_to_char: Dict. Mapping from character indices to characters.

    Returns:
        str. The next character sampled based on the probability distribution.
    """
    # Get the probability distribution for the current character
    # TODO
    current_probs: torch.Tensor[float] = probability_distribution[current_char_index]

    # Sample an index from the distribution using the torch.multinomial function
    # TODO
    next_char_index: int = torch.multinomial(current_probs, 1).item()

    # Map the index back to a character
    # TODO
    next_char: str = idx_to_char[next_char_index]
    
    return next_char


def generate_name(
    start_token: str,
    end_token: str,
    char_to_idx: Dict[str, int],
    idx_to_char: Dict[int, str],
    bigram_probabilities: torch.Tensor,
    max_length: int = 15,
) -> str:
    """
    Generate a new name based on the bigram probabilities.

    This function starts from the start token and iteratively samples the next character
    based on the current character's probability distribution until it reaches the end token
    or the maximum length.

    Args:
        start_token: str. The start token indicating the beginning of a name.
        end_token: str. The end token indicating the end of a name.
        char_to_idx: Dict[str, int]. A mapping from characters to their indices.
        idx_to_char: Dict[int, str]. A mapping from indices back to characters.
        bigram_probabilities: torch.Tensor. A 2D tensor representing the bigram probabilities.
        max_length: int. The maximum length for the generated name.

    Returns:
        str. A newly generated name.
    """
    # Start with the start token and an empty name
    # TODO
    current_char: str = start_token
    generated_name: str = ""

    # Iterate to build the name
    # TODO
    while len(generated_name) < max_length:
        next_char = sample_next_character(char_to_idx[current_char], bigram_probabilities, idx_to_char)
        if next_char == end_token:
            break
        generated_name += next_char
        current_char = next_char
        
    return generated_name

def calculate_log_likelihood(
    word: str,
    bigram_probabilities: torch.Tensor,
    char_to_index: Dict[str, int],
    start_token: str = "<S>",
    end_token: str = "<E>",
) -> torch.Tensor:
    """
    Calculate the log likelihood of a word based on bigram probabilities.

    This function computes the log likelihood of a given word using the provided bigram
    probability matrix. The function requires the start and end characters to be specified,
    which are used to process the word for bigram analysis.

    The function iterates through each pair of characters (bigram) in the word, including the
    start and end characters. For each bigram, it looks up the corresponding probability in the
    bigram probability matrix and computes the log of this probability. The log likelihood of the
    word is the sum of these log probabilities.

    Args:
        word: str. The word for which to calculate the log likelihood.
        bigram_probabilities: torch.Tensor. A 2D tensor representing the probability of each bigram.
        char_to_index: dict. A dictionary mapping characters to their indices in the probability matrix.
        start_char: str. The character that denotes the start of a word. Shall be a single character.
        end_char: str. The character that denotes the end of a word. Shall be a single character.

    Returns:
        Tensor. The log likelihood of the word.
    """
    # Add start and end characters to the word
    # TODO
    processed_word: str = start_token + word + end_token

    # Initialize log likelihood
    # TODO
    log_likelihood: torch.tensor = torch.tensor(0.0)

    # Iterate through bigrams in the word and accumulate their log probabilities
    # TODO

    for i in range(len(processed_word) - 1):
        char1 = processed_word[i]
        char2 = processed_word[i+1]

        row = char_to_index[char1]
        col = char_to_index[char2]

        log_likelihood += torch.log(bigram_probabilities[row, col])
    
    return log_likelihood

if __name__ == "__main__":
    pass
