import os

class CustomIndex:
    def __init__(self):
        self.index = {}

    def add_document(self, doc_id, content):
        words = content.lower().split()
        for word in words:
            if word not in self.index:
                self.index[word] = set()
            self.index[word].add(doc_id)

    def search(self, query):
        query_words = query.lower().split()
        if not query_words:
            return set()
        result = self.index.get(query_words[0], set())
        for word in query_words[1:]:
            result = result.intersection(self.index.get(word, set()))
        return result

class Document:
    def __init__(self, doc_id, title, content):
        self.doc_id = doc_id
        self.title = title
        self.content = content

class SimpleSearchEngine:
    def __init__(self):
        self.documents = {}
        self.title_index = CustomIndex()
        self.content_index = CustomIndex()

    def add_document(self, title, content):
        doc_id = len(self.documents) + 1
        document = Document(doc_id, title, content)
        self.documents[doc_id] = document
        self.title_index.add_document(doc_id, title)
        self.content_index.add_document(doc_id, content)

    def search_by_title(self, query):
        doc_ids = self.title_index.search(query)
        return [self.documents[doc_id] for doc_id in doc_ids]

    def search_by_content(self, query):
        doc_ids = self.content_index.search(query)
        return [self.documents[doc_id] for doc_id in doc_ids]

def read_documents(directory):
    search_engine = SimpleSearchEngine()
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            with open(os.path.join(directory, filename), 'r') as file:
                title = filename[:-4]  # Remove .txt extension
                content = file.read()
                search_engine.add_document(title, content)
    return search_engine

def main():
    documents_directory = r"D:\University Files\7th Semester\IR\Assignment 1\Assignment 1 Text Folder"  # Replace with actual path
    search_engine = read_documents(documents_directory)

    while True:
        print("\nCustom Document Search Engine")
        print("1. Search by title")
        print("2. Search by content")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            query = input("Enter title to search: ")
            results = search_engine.search_by_title(query)
        elif choice == '2':
            query = input("Enter content to search: ")
            results = search_engine.search_by_content(query)
        elif choice == '3':
            print("Thank you for using the Custom Document Search Engine!")
            break
        else:
            print("Invalid choice. Please try again.")
            continue

        if results:
            print("Matching documents:")
            for doc in results:
                print(f"- Title: {doc.title}, ID: {doc.doc_id}")
        else:
            print("No matching documents found.")

if __name__ == "__main__":
    main()