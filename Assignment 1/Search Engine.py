import os
import re
from collections import defaultdict
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Step 1: Define the index data structure
index = defaultdict(list)  # Dictionary to hold the index
doc_names = {}  # Dictionary to map doc_id to document names

# Step 2: Function to clean and tokenize text by comma separation


def clean_and_tokenize(text):
    # Split by comma and strip whitespace
    words = [word.strip().lower() for word in text.split(',') if word.strip()]
    return words

# Step 3: Function to read and index documents


def build_index(folder_path):
    doc_id = 1  # Document ID starts from 1
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                # Tokenize based on comma separation
                words = clean_and_tokenize(content)

                # Store the document name in doc_names dictionary
                doc_names[doc_id] = filename

                # Add each word to the index
                for position, word in enumerate(words):
                    index[word].append((doc_id, position))

            doc_id += 1  # Increment document ID after processing each document

# Step 4: Search function to search by word, sorted by frequency and displayed in a more readable format


def search_word(query):
    query = query.lower()
    if query in index:
        results = index[query]

        # Count occurrences in each document
        doc_count = defaultdict(int)
        for doc_id, position in results:
            doc_count[doc_id] += 1

        # Sort documents by frequency in descending order
        sorted_results = sorted(
            doc_count.items(), key=lambda x: x[1], reverse=True)

        # Display results in a more readable, colored, table-like format
        print(f"\n{Fore.GREEN}Word '{
              query}' found in the following documents:{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{'Document Name':<30}{
              'Frequency':<21}{'Positions'}{Style.RESET_ALL}")
        print("-" * 60)
        for doc_id, frequency in sorted_results:
            positions = [pos for d_id, pos in results if d_id == doc_id]
            doc_name = doc_names.get(doc_id, f"Document {doc_id}")
            print(f"{Fore.GREEN}{doc_name:<30}{
                  frequency:<21}{positions}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Word '{
            query}' not found in any document.{Style.RESET_ALL}")

# Step 5: Search function to search by title (filename without extension)


def search_title(folder_path, title):
    title = title.lower()
    for filename in os.listdir(folder_path):
        file_name_only, _ = os.path.splitext(filename)  # Remove file extension
        if file_name_only.lower() == title:
            print(f"{Fore.GREEN}Document '{title}' found as '{
                  filename}'.{Style.RESET_ALL}")
            return
    print(f"{Fore.RED}Document '{title}' not found.{Style.RESET_ALL}")

# Step 6: Main function to tie everything together


def main():
    # Prompt the user to input the directory path
    folder_path = input(
        f"\n {Fore.MAGENTA} Enter the folder path containing documents: {Style.RESET_ALL}")

    # Build the index from the documents
    print("Building the index from documents...")
    build_index(folder_path)
    print(f"{Fore.GREEN}Index built successfully!{Style.RESET_ALL}")

    # Interactive menu
    while True:
        print(f"{Fore.MAGENTA}\nSelect an option:{Style.RESET_ALL}")
        print("1. Search by word")
        print("2. Search by document title")
        print("3. Exit")

        choice = input("\nEnter your choice (1/2/3): ")

        if choice == '1':
            query = input("\n Enter the word to search: ")
            search_word(query)
        elif choice == '2':
            title = input(
                "\n Enter the document title (without extension) to search: ")
            search_title(folder_path, title)
        elif choice == '3':
            print(f"{Fore.GREEN} \n Exiting the search engine. Goodbye!{
                  Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.RED}\n Invalid choice. Please try again.{
                  Style.RESET_ALL}")


# This will ensure the script is run directly and not imported
if __name__ == "__main__":
    main()
