import os
from colorama import init, Fore, Style
from tabulate import tabulate

init(autoreset=True)

# ------------------------- Noun Extraction Functions -------------------------


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
                noun_store[filename] = nouns

                # Preview file name with first 5 nouns
                preview_nouns = nouns[:5]
                print(f"{Fore.GREEN}{filename}{Fore.CYAN}{
                      preview_nouns}{Style.RESET_ALL}")

            except Exception as e:
                print(f"{Fore.RED}Error reading {
                      filename}: {e}{Style.RESET_ALL}")
    return noun_store

# ------------------------- Vector and Probability Calculations -------------------------


def create_binary_vector(doc, all_terms):
    """
    Create a binary vector for a document based on the presence of terms.
    """
    return [1 if term in doc else 0 for term in all_terms]


def calculate_term_probabilities(doc_vectors):
    """
    Calculate term probabilities for BIM (Binary Independence Model).
    """
    num_docs = len(doc_vectors)
    term_probabilities = []
    non_probabilities = []

    for i in range(len(doc_vectors[0])):
        term_count = sum(doc[i] for doc in doc_vectors)
        prob = term_count / num_docs
        term_probabilities.append(prob)
        non_probabilities.append(1 - prob)

    return term_probabilities, non_probabilities


def rank_documents_bim(doc_vectors, query_vector, probabilities, non_probabilities):
    """
    Rank documents using BIM scores computed via the Dice Coefficient.
    """
    ranked_docs = []
    for i, doc_vector in enumerate(doc_vectors):
        # Compute Dice coefficient between query and document vectors
        intersection = sum(1 for d, q in zip(doc_vector, query_vector) if d == 1 and q == 1)
        union = sum(doc_vector) + sum(query_vector)  # Total terms in both sets

        # print("Intersection: ", intersection, "\t union", union)

        # Dice coefficient formula
        dice_score = (2 * intersection) / union if union > 0 else 0
        ranked_docs.append((i, dice_score))
        # print("dice_score for ", i+1, dice_score, "\n")

    # Sort documents by score in descending order
    ranked_docs.sort(key=lambda x: x[1], reverse=True)
    return ranked_docs

# ------------------------- Display Results -------------------------


def display_results(filenames, ranked_docs, K):
    """
    Display the top-K results based on Dice Coefficient.
    """
    print(f"{Fore.GREEN}Top-{K} Matching Documents:{Style.RESET_ALL}")
    table = [[filenames[doc_id], f"{score:.4f}"]
             for doc_id, score in ranked_docs[:K]]
    print(tabulate(
        table,
        headers=[f"{Fore.LIGHTCYAN_EX}Document Name{Style.RESET_ALL}",
                 f"{Fore.LIGHTCYAN_EX}Dice Coefficient{Style.RESET_ALL}"],
        tablefmt="grid"
    ))

# ------------------------- Main Function -------------------------


def main():
    while True:
        # 1. Directory path containing .txt files
        folder_path = input(
            f"{Fore.BLUE}Enter the directory path containing .txt files: {Style.RESET_ALL}")
        while not os.path.exists(folder_path):
            print(f"{Fore.RED}Invalid directory. Please try again.{
                  Style.RESET_ALL}")
            folder_path = input(
                f"{Fore.BLUE}Enter the directory path containing .txt files: {Style.RESET_ALL}")

        # 2. Process files and extract nouns
        noun_store = process_files(folder_path)
        filenames = list(noun_store.keys())
        documents = list(noun_store.values())
        if not documents:
            print(f"{Fore.RED}No text documents found in the directory.{
                  Style.RESET_ALL}")
            continue

        # 3. Create binary vectors for all documents
        # All unique terms in the collection
        all_terms = list(set(sum(documents, [])))

        doc_vectors = [create_binary_vector(
            doc, all_terms) for doc in documents]

        # 4. Calculate term probabilities for BIM
        probabilities, non_probabilities = calculate_term_probabilities(
            doc_vectors)

        while True:
            # 5. Query input from the user
            query = input(f"\n{Fore.CYAN}Enter your query (or type 'p' to change path, 'exit' to quit): {
                          Style.RESET_ALL}")
            if query.lower() == 'exit':
                print(f"{Fore.GREEN}Exiting program. Goodbye!{Style.RESET_ALL}")
                return
            elif query.lower() == 'p':
                break

            # Tokenize the query to extract nouns
            preprocessed_query = tokenize_nouns(query)
            # Highlight terms in red if they do not exist in the corpus
            missing_terms = []
            for term in preprocessed_query:
                if term not in all_terms:
                    missing_terms.append(term)
                    print(f"{Fore.RED}The term '{
                          term}' does not exist in the corpus.{Style.RESET_ALL}")

            if not preprocessed_query or not all_terms:
                print(f"{Fore.RED}The query does not match any extracted nouns. Try again with relevant terms.{
                      Style.RESET_ALL}")
                continue

            # Continue with creating the query vector and ranking documents
            query_vector = create_binary_vector(preprocessed_query, all_terms)

            # 6. Rank the documents based on BIM scores
            ranked_docs = rank_documents_bim(
                doc_vectors, query_vector, probabilities, non_probabilities)

            # 7. Retrieve and present top-K documents
            try:
                k = int(input(f"{Fore.YELLOW}Enter the number of top documents to retrieve (K): {
                        Style.RESET_ALL}"))
                if k <= 0:
                    print(f"{Fore.RED}Please enter a positive integer for K.{
                          Style.RESET_ALL}")
                    continue
            except ValueError:
                print(f"{Fore.RED}Invalid input for K. Please enter a valid integer.{
                      Style.RESET_ALL}")
                continue

            display_results(filenames, ranked_docs, k)


if __name__ == "__main__":
    main()
