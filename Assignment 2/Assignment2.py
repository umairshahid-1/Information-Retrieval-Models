import os  # For reading from the system
import math  # For log
from colorama import init, Fore, Style  # For coloring
from tabulate import tabulate  # For better table formatting

init(autoreset=True)

# Cosine Similarity Function


def cosine_similarity(vec1, vec2):
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = math.sqrt(sum(a**2 for a in vec1))
    norm2 = math.sqrt(sum(b**2 for b in vec2))
    return dot_product / (norm1 * norm2) if norm1 and norm2 else 0


def is_noun(word, previous_word=None):
    """
    Determine if a word is a noun based on heuristics optimized for technology-related text.
    """
    domain_proper_nouns = {"ai", "iot", "ml", "ethics",
                           "robotics", "automation", "technology", "quantum"}
    if word.lower() in domain_proper_nouns:
        return True

    trivial_words = {"and", "in", "of", "to", "for", "the", "a", "an",
                     "from", "by", "as", "however", "another", "when", "moreover"}
    if word[0].isupper() and word.lower() not in trivial_words:
        return True

    noun_suffixes = ["tion", "ics", "ism", "logy", "ment",
                     "ance", "ence", "ship", "ity", "ness", "ware"]
    if any(word.lower().endswith(suffix) for suffix in noun_suffixes):
        return True

    return False


def tokenize_nouns(content):
    """
    Tokenize content and extract only nouns optimized for technology-related text.
    """
    words = content.split()
    tokens = []
    previous_word = None

    for word in words:
        # Remove punctuation and convert to lowercase
        clean_word = word.strip(",.!?\"'").lower()
        if is_noun(clean_word, previous_word):
            tokens.append(clean_word)
        previous_word = clean_word

    return tokens


def process_files(folder_path):
    """
    Read files from folder, tokenize content, and extract nouns.
    """
    noun_store = {}
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path) and filename.endswith(".txt"):  # Process only text files
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read().lower()  # Read content and convert to lowercase
                nouns = tokenize_nouns(content)
                # Store extracted nouns for each file
                noun_store[filename] = nouns

                # # Print filename with its nouns
                # print(f"{Fore.GREEN}{filename}: {
                #       Fore.CYAN}{nouns}{Style.RESET_ALL}")

            except Exception as e:
                print(f"{Fore.RED}Error reading {
                      filename}: {e}{Style.RESET_ALL}")
    return noun_store


def calculate_tf(word, nouns):
    """
    Calculate Term Frequency (TF).
    """
    word_count = nouns.count(word)
    total_words = len(nouns)
    return word_count, total_words, word_count / total_words if total_words > 0 else 0


def calculate_idf(word, noun_store):
    """
    Calculate Inverse Document Frequency (IDF).
    """
    N = len(noun_store)
    n = sum(1 for nouns in noun_store.values() if word in nouns)

    # print(f"{N} \t {n}")
    return math.log10(N / (n + 1))


def search_and_calculate_scores(noun_store, search_query):
    """
    Search for a word and calculate TF, IDF, and TF-IDF for each document.
    """
    search_query = search_query.lower()
    results = []

    # Calculate IDF for the word
    idf = calculate_idf(search_query, noun_store)

    for filename, nouns in noun_store.items():
        frequency, total_words, tf = calculate_tf(
            search_query, nouns)  # Term Frequency
        tf_idf = tf * idf  # TF-IDF
        if tf > 0:  # If the term exists in the document
            results.append((filename, frequency, total_words, tf, idf, tf_idf))

    # Sort results by TF-IDF score in descending order
    results.sort(key=lambda x: x[5], reverse=True)

    return results, idf


def calculate_document_vectors(noun_store, search_query, idf):
    """
    Generate TF-IDF vectors for all documents with respect to the search query.
    """
    vectors = {}
    for filename, nouns in noun_store.items():
        _, _, tf = calculate_tf(search_query, nouns)  # Calculate TF
        tf_idf = tf * idf  # Calculate TF-IDF
        vectors[filename] = tf_idf
    return vectors


def display_results(search_query, results, idf, cosine_scores):
    """
    Display the results in a well-formatted table.
    """
    if results:
        # Display the IDF
        print(f"\n{Fore.MAGENTA}IDF for '{search_query}': {
              Style.RESET_ALL}{idf:.4f}\n")

        # Display TF table
        tf_table = [
            [filename, frequency, total_words, f"{tf:.4f}"]
            for filename, frequency, total_words, tf, _, _ in results
        ]
        print(f"{Fore.YELLOW}TF Scores:{Style.RESET_ALL}")
        print(tabulate(
            tf_table,
            headers=[f"{Fore.LIGHTYELLOW_EX}{header}{Style.RESET_ALL}"
                     for header in ["Document Name", "Frequency", "Total Words", "TF Score"]],
            tablefmt="grid"
        ))

        # Display TF-IDF table
        tf_idf_table = [
            [filename, f"{tf_idf:.4f}"]
            for filename, _, _, _, _, tf_idf in results
        ]
        print(f"\n{Fore.GREEN}TF-IDF Scores:{Style.RESET_ALL}")
        print(tabulate(
            tf_idf_table,
            headers=[f"{Fore.LIGHTGREEN_EX}{header}{Style.RESET_ALL}"
                     for header in ["Document Name", "TF-IDF Score"]],
            tablefmt="grid"
        ))

        # Display Cosine Similarity Rankings
        print(f"\n{Fore.BLUE}Cosine Similarity Rankings:{Style.RESET_ALL}")
        cosine_table = [
            [filename, f"{score:.4f}"]
            for filename, score in cosine_scores
        ]
        print(tabulate(
            cosine_table,
            headers=[f"{Fore.LIGHTBLUE_EX}{header}{Style.RESET_ALL}"
                     for header in ["Document Name", "Cosine Similarity Score"]],
            tablefmt="grid"
        ))
    else:
        print(f"{Fore.RED}No results found for '{
              search_query}'.{Style.RESET_ALL}")


def search_and_display_with_similarity(noun_store, search_query):
    """
    Perform search, calculate scores, and display in a user-friendly format.
    """
    search_query = search_query.lower()

    # Calculate IDF for the word
    idf = calculate_idf(search_query, noun_store)

    # Calculate TF, TF-IDF, and prepare for Cosine Similarity
    results, _ = search_and_calculate_scores(noun_store, search_query)
    vectors = calculate_document_vectors(noun_store, search_query, idf)

    # Query vector (since it's only one term, just TF-IDF of the query itself)
    query_vector = [vectors.get(doc, 0) for doc in vectors]
    # print(f"Query Vector: {query_vector}")

    # Cosine Similarity Calculation
    cosine_scores = [
        (doc, cosine_similarity([vectors[doc]], query_vector))
        for doc in vectors
    ]
    cosine_scores.sort(key=lambda x: x[1], reverse=True)  # Sort by similarity

    # Display Results
    display_results(search_query, results, idf, cosine_scores)


def main():
    folder_path = input(
        f"\n {Fore.BLUE}Enter the folder path containing documents: {Style.RESET_ALL}")

    while True:
        if not os.path.exists(folder_path):
            print(f"{Fore.RED}The folder does not exist: {
                  folder_path}{Style.RESET_ALL}")
            folder_path = input(
                f"{Fore.BLUE}Please re-enter the folder path: {Style.RESET_ALL}")
            continue

        # Process files and extract nouns
        noun_store = process_files(folder_path)

        while True:
            search_query = input(
                f"\n{Fore.CYAN}Enter a word to search (or type 'p' to update folder path, 'exit' to quit): {Style.RESET_ALL}").strip()
            if search_query.lower() == "exit":
                print(f"{Fore.GREEN}Exiting program. Goodbye!{Style.RESET_ALL}")
                return
            elif search_query.lower() == "p":
                folder_path = input(
                    f"{Fore.BLUE}Please enter the new folder path: {Style.RESET_ALL}")
                break

            # Perform search and display
            search_and_display_with_similarity(noun_store, search_query)


if __name__ == "__main__":
    main()
