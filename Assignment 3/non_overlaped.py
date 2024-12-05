import os
import re
from colorama import init, Fore, Style
from tabulate import tabulate

# Initialize colorama for colored terminal output
init(autoreset=True)

# ------------------------- Noun Extraction and Preprocessing -------------------------


def is_noun(word, previous_word=None):
    """
    Determine if a word is a noun using comprehensive heuristics.

    Args:
        word (str): The word to evaluate
        previous_word (str, optional): The previous word for context

    Returns:
        bool: True if the word is likely a noun, False otherwise
    """
    # Domain-specific proper nouns and technical terms
    domain_proper_nouns = {
        "ai", "ml", "nlp", "iot", "blockchain", "cybersecurity",
        "dataframe", "algorithm", "tensorflow", "pytorch",
        "quantum", "neural", "cloud", "microservice", "api",
        "database", "software", "hardware", "network"
    }

    # Words to exclude from noun consideration
    trivial_words = {
        "and", "in", "of", "to", "for", "the", "a", "an",
        "from", "by", "as", "however", "when", "moreover"
    }

    # Typical noun-forming suffixes
    noun_suffixes = [
        "tion", "ics", "ism", "logy", "ment",
        "ance", "ence", "ship", "ity", "ness",
        "ware", "er", "or", "ist", "able"
    ]

    # Clean the word
    clean_word = word.strip(",.!?\"'").lower()

    # Check against domain-specific proper nouns
    if clean_word in domain_proper_nouns:
        return True

    # Ignore trivial words
    if clean_word in trivial_words:
        return False

    # Check for capitalization (potential proper noun)
    if word[0].isupper() and clean_word not in trivial_words:
        return True

    # Check noun suffixes
    if any(clean_word.endswith(suffix) for suffix in noun_suffixes):
        return True

    return False


def tokenize_nouns(content):
    """
    Extract meaningful nouns from text content.

    Args:
        content (str): Input text to process

    Returns:
        list: Extracted meaningful nouns
    """
    # Normalize text
    content = content.lower()

    # Remove special characters, keeping alphanumeric and spaces
    content = re.sub(r'[^a-zA-Z\s]', ' ', content)

    # Split into words
    words = content.split()

    # Extract nouns
    nouns = []
    for i, word in enumerate(words):
        previous_word = words[i-1] if i > 0 else None
        if is_noun(word, previous_word):
            nouns.append(word)

    # Remove duplicates while preserving order
    return list(dict.fromkeys(nouns))

# ------------------------- Linked List Implementation -------------------------


class Node:
    """Represents a node in a linked list."""

    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    """Custom linked list with advanced operations."""

    def __init__(self):
        self.head = None

    def append(self, data):
        """Add a unique item to the linked list."""
        if not self.contains(data):
            new_node = Node(data)
            if not self.head:
                self.head = new_node
                return

            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def contains(self, data):
        """Check if the list contains a specific value."""
        current = self.head
        while current:
            if current.data == data:
                return True
            current = current.next
        return False

    def to_list(self):
        """Convert linked list to a standard Python list."""
        return [node.data for node in self.traverse()]

    def traverse(self):
        """Generator to traverse the linked list."""
        current = self.head
        while current:
            yield current
            current = current.next

    def union(self, other_list):
        """Create a union of two linked lists without duplicates."""
        result = LinkedList()

        # Add items from current list
        for node in self.traverse():
            result.append(node.data)

        # Add unique items from other list
        for node in other_list.traverse():
            result.append(node.data)

        return result

# ------------------------- Non-Overlapped List Model -------------------------


def build_inverted_index(directory_path):
    """
    Build an inverted index using linked lists and noun extraction.

    Args:
        directory_path (str): Path to directory containing text files

    Returns:
        dict: Inverted index mapping terms to documents
    """
    inverted_index = {}

    # Process each text file
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory_path, filename)

            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()

                    # Extract nouns from the content
                    nouns = tokenize_nouns(content)

                    # Build inverted index
                    for noun in nouns:
                        if noun not in inverted_index:
                            inverted_index[noun] = LinkedList()

                        # Add document to the linked list if not already present
                        inverted_index[noun].append(filename)

                # Preview file name with first 5 nouns
                preview_nouns = nouns[:5]
                print(f"{Fore.GREEN}{filename}{Fore.CYAN}{
                      preview_nouns}{Style.RESET_ALL}")

            except Exception as e:
                print(f"{Fore.RED}Error processing {
                      filename}: {e}{Style.RESET_ALL}")

    return inverted_index


def main():
    """Main execution flow for the Non-Overlapped List Model."""
    print(f"{Fore.CYAN}Non-Overlapped List Model with Noun Extraction{Style.RESET_ALL}")

    while True:
        # Get directory path
        directory_path = input(
            f"{Fore.YELLOW}Enter directory path containing .txt files (or 'exit' to quit): {Style.RESET_ALL}")

        # Exit condition
        if directory_path.lower() == 'exit':
            print(f"{Fore.GREEN}Exiting the program. Goodbye!{Style.RESET_ALL}")
            break

        # Validate directory
        if not os.path.exists(directory_path):
            print(f"{Fore.RED}Directory not found. Please try again.{
                  Style.RESET_ALL}")
            continue

        # Build inverted index
        print(f"{Fore.GREEN}Building inverted index...{Style.RESET_ALL}")
        inverted_index = build_inverted_index(directory_path)

        # Search and retrieval loop
        while True:
            search_input = input(
                f"\n{Fore.YELLOW}Enter search terms (comma-separated) or 'b' to go back: {Style.RESET_ALL}")

            # Back to directory selection
            if search_input.lower() == 'b':
                break

            search_terms = [term.strip().lower()
                            for term in search_input.split(',')]

            # Retrieve documents
            results = {}
            for term in search_terms:
                results[term] = inverted_index.get(term, LinkedList())

            # Compute non-overlapping documents
            non_overlapping_docs = LinkedList()
            for doc_list in results.values():
                non_overlapping_docs = non_overlapping_docs.union(doc_list)

            # Display results
            print(f"\n{Fore.CYAN}Search Results:{Style.RESET_ALL}")

            # Tabulate results
            table_data = [
                [term, ", ".join(results[term].to_list())] for term in search_terms
            ]
            table_data.append(["Non-Overlapping Documents",
                              ", ".join(non_overlapping_docs.to_list())])

            print(tabulate(table_data, headers=[
                  f"{Fore.LIGHTCYAN_EX}Term{Style.RESET_ALL}",
                  f"{Fore.LIGHTCYAN_EX}Documents{Style.RESET_ALL}"], tablefmt="fancy_grid"))


# Entry point of the program
if __name__ == "__main__":
    main()
