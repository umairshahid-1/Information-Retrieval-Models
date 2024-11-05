import os
import re

# Step 1: Define the index data structure
index = {}  # Dictionary to hold the index

# Step 2: Function to clean and tokenize text


def clean_and_tokenize(text):
    # Use regex to remove punctuation and split words
    # \b\w+\b finds word boundaries
    words = re.findall(r'\b\w+\b', text.lower())
    return words

# Step 3: Function to read and index documents


def build_index(folder_path):
    doc_id = 1  # Document ID starts from 1
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()  # Read file content
                # Clean and tokenize the text
                words = clean_and_tokenize(content)

                # Add each word to the index
                for position, word in enumerate(words):
                    if word not in index:
                        # Initialize the list if the word is new
                        index[word] = []
                    # Add doc_id and position
                    index[word].append((doc_id, position))
            doc_id += 1  # Increment document ID after processing each document

# Step 4: Search function to search by word


def search_word(query):
    query = query.lower()
    if query in index:
        results = index[query]
        print(f"Word '{query}' found in the following documents at positions:")
        for doc_id, position in results:
            print(f"Document {doc_id}, Position {position}")
            print(index)
    else:
        print(f"Word '{query}' not found in any document.")

# Step 5: Search function to search by title (filename)


def search_title(folder_path, title):
    for filename in os.listdir(folder_path):
        if filename.lower() == title.lower():
            print(f"Document '{title}' found.")
            return
    print(f"Document '{title}' not found.")

# Step 6: Main function to tie everything together


def main():
    # Replace with your folder path
    folder_path = r"D:\University Files\7th Semester\IR\Assignment 1\Assignment 1 Text Folder"

    # Build the index from the documents
    print("Building the index from documents...")
    build_index(folder_path)
    print("Index built successfully!")

    # Interactive menu
    while True:
        print("\nSelect an option:")
        print("1. Search by word")
        print("2. Search by document title")
        print("3. Exit")

        choice = input("Enter your choice (1/2/3): ")

        if choice == '1':
            query = input("Enter the word to search: ")
            search_word(query)
        elif choice == '2':
            title = input("Enter the document title to search: ")
            search_title(folder_path, title)
        elif choice == '3':
            print("Exiting the search engine. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


# This will ensure the script is run directly and not imported
if __name__ == "__main__":
    main()
