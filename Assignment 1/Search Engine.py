import os
import re
from collections import defaultdict
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Define the index data structure
index = defaultdict(list)
doc_names = {}
nouns_in_docs = defaultdict(list)  # Store nouns for each document

# Function to clean, tokenize, and extract nouns


def clean_and_tokenize(text):
    # Remove punctuation using regex and split by spaces
    # Extract words ignoring punctuation
    words = re.findall(r'\b\w+\b', text.lower())

    # Heuristic for nouns: Collect capitalized words as nouns (simple assumption)
    nouns = [word for word in re.findall(r'\b[A-Z][a-z]*\b', text)]

    return words, nouns

# Function to read and index documents


def build_index(folder_path):
    # Clear the existing index and doc_names for re-indexing
    index.clear()
    doc_names.clear()
    nouns_in_docs.clear()

    doc_id = 1
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                words, nouns = clean_and_tokenize(content)

                # Store document name
                doc_names[doc_id] = filename

                # Store nouns for this document
                nouns_in_docs[doc_id] = nouns

                # Add each word to the index
                for position, word in enumerate(words):
                    index[word].append((doc_id, position))

            doc_id += 1
    print(f"{Fore.GREEN}Index built successfully!{Style.RESET_ALL}")

# Function to display nouns in a document


def display_nouns(doc_id):
    doc_name = doc_names.get(doc_id, f"Document {doc_id}")
    nouns = nouns_in_docs.get(doc_id, [])
    print(f"\n{Fore.BLUE}Nouns in {doc_name}:{Style.RESET_ALL}")
    print(", ".join(nouns) if nouns else "No nouns found.")

# Function to search by word


def search_word(query):
    query = query.lower()
    if query in index:
        results = index[query]

        # Count occurrences in each document
        doc_count = defaultdict(int)
        for doc_id, position in results:
            doc_count[doc_id] += 1

        # Sort by frequency
        sorted_results = sorted(
            doc_count.items(), key=lambda x: x[1], reverse=True)

        print(f"\n{Fore.GREEN}Word '{
              query}' found in the following documents:{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{'Document Name':<30}{
              'Frequency':<20}{'Positions'}{Style.RESET_ALL}")
        print("-" * 60)
        for doc_id, frequency in sorted_results:
            positions = [pos for d_id, pos in results if d_id == doc_id]
            doc_name = doc_names.get(doc_id, f"Document {doc_id}")
            print(f"{Fore.GREEN}{doc_name:<30}{
                  frequency:<20}{positions}{Style.RESET_ALL}")
            display_nouns(doc_id)  # Show nouns in this document

# Function to search by title


def search_title(folder_path, title):
    title = title.lower()
    for filename in os.listdir(folder_path):
        file_name_only, _ = os.path.splitext(filename)
        if file_name_only.lower() == title:
            print(f"{Fore.GREEN}Document '{title}' found as '{
                  filename}'.{Style.RESET_ALL}")
            return
    print(f"{Fore.RED}Document '{title}' not found.{Style.RESET_ALL}")

# Main function


def main():
    folder_path = input(
        f"\n {Fore.MAGENTA}Enter the folder path containing documents: {Style.RESET_ALL}")

    # Initial index build
    print("Building the index from documents...")
    build_index(folder_path)

    # Interactive menu
    while True:
        print(f"{Fore.MAGENTA}\nSelect an option:{Style.RESET_ALL}")
        print("1. Search by word")
        print("2. Search by document title")
        print("3. Re-index documents")
        print("4. Exit")

        choice = input("\nEnter your choice (1/2/3/4): ")

        if choice == '1':
            query = input("\nEnter the word to search: ")
            search_word(query)
        elif choice == '2':
            title = input(
                "\nEnter the document title (without extension) to search: ")
            search_title(folder_path, title)
        elif choice == '3':
            print("\nRe-indexing documents...")
            build_index(folder_path)  # Rebuild the index
        elif choice == '4':
            print(f"{Fore.GREEN}\nExiting the search engine. Goodbye!{
                  Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.RED}\nInvalid choice. Please try again.{
                  Style.RESET_ALL}")


if __name__ == "__main__":
    main()
