import os
import random
import re
import tkinter as tk
from tkinter import ttk, messagebox


def is_noun(word, previous_word=None):
    domain_proper_nouns = {
        "ai", "ml", "nlp", "iot", "blockchain", "cybersecurity",
        "dataframe", "algorithm", "tensorflow", "pytorch",
        "quantum", "neural", "cloud", "microservice", "api",
        "database", "software", "hardware", "network"
    }

    trivial_words = {
        "and", "in", "of", "to", "for", "the", "a", "an",
        "from", "by", "as", "however", "when", "moreover"
    }

    noun_suffixes = [
        "tion", "ics", "ism", "logy", "ment",
        "ance", "ence", "ship", "ity", "ness",
        "ware", "er", "or", "ist", "able"
    ]

    clean_word = word.strip(",.!?\"'").lower()

    if clean_word in domain_proper_nouns:
        return True

    if clean_word in trivial_words:
        return False

    if word[0].isupper() and clean_word not in trivial_words:
        return True

    if any(clean_word.endswith(suffix) for suffix in noun_suffixes):
        return True

    return False


def tokenize_nouns(content):
    content = content.lower()
    content = re.sub(r'[^a-zA-Z\s]', ' ', content)
    words = content.split()
    nouns = []
    for i, word in enumerate(words):
        previous_word = words[i-1] if i > 0 else None
        if is_noun(word, previous_word):
            nouns.append(word)
    return list(dict.fromkeys(nouns))


def load_txt_files(folder_path):
    documents = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            filepath = os.path.join(folder_path, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as file:
                    text = file.read()
                    nouns = tokenize_nouns(text)
                    document_text = ' '.join(nouns)
                    documents.append(
                        {"filename": filename, "text": document_text, "nouns": nouns})
            except Exception as e:
                print(f"Error reading {filename}: {e}")
    return documents


def build_vocabulary(documents):
    vocab = set()
    for doc in documents:
        vocab.update(doc["nouns"])
    return sorted(list(vocab))


def create_bow_vector(document, vocabulary):
    tokens = document.split()
    vector = [0] * len(vocabulary)
    for token in tokens:
        if token in vocabulary:
            index = vocabulary.index(token)
            vector[index] += 1
    return vector


def prepare_bow_vectors(documents, vocabulary):
    return [create_bow_vector(doc["text"], vocabulary) for doc in documents]


class NeuralNetwork:
    def __init__(self, input_dim, hidden_dim, output_dim):
        self.W1 = [[random.uniform(-0.01, 0.01)
                    for _ in range(hidden_dim)] for _ in range(input_dim)]
        self.B1 = [0.0 for _ in range(hidden_dim)]
        self.W2 = [[random.uniform(-0.01, 0.01) for _ in range(output_dim)]
                   for _ in range(hidden_dim)]
        self.B2 = [0.0 for _ in range(output_dim)]

    def relu(self, x):
        return [max(0, xi) for xi in x]

    def relu_derivative(self, x):
        return [1 if xi > 0 else 0 for xi in x]

    def forward(self, x):
        self.Z1 = [sum(x[i] * self.W1[i][j] for i in range(len(x))
                       ) + self.B1[j] for j in range(len(self.B1))]
        self.A1 = self.relu(self.Z1)
        self.Z2 = [sum(self.A1[j] * self.W2[j][k]
                       for j in range(len(self.A1))) + self.B2[k] for k in range(len(self.B2))]
        return self.Z2

    def backward(self, x, y_true, y_pred, learning_rate):
        dZ2 = y_pred - y_true
        dW2 = [dZ2 * a1 for a1 in self.A1]
        dB2 = dZ2

        dA1 = [dZ2 * self.W2[j][0] for j in range(len(self.A1))]
        dZ1 = [dA1[j] * self.relu_derivative([self.Z1[j]])[0]
               for j in range(len(dA1))]

        dW1 = [[dZ1[j] * x[i] for j in range(len(dZ1))] for i in range(len(x))]
        dB1 = dZ1

        for j in range(len(self.W2)):
            for k in range(len(self.W2[0])):
                self.W2[j][k] -= learning_rate * dW2[j]
        for k in range(len(self.B2)):
            self.B2[k] -= learning_rate * dB2

        for i in range(len(self.W1)):
            for j in range(len(self.W1[0])):
                self.W1[i][j] -= learning_rate * dW1[i][j]
        for j in range(len(self.B1)):
            self.B1[j] -= learning_rate * dB1[j]


def train_model(model, X_train, y_train, epochs=50, learning_rate=0.01, gui=None):
    for epoch in range(1, epochs + 1):
        total_loss = 0.0
        for x, y_true in zip(X_train, y_train):
            y_pred = model.forward(x)[0]
            loss = (y_pred - y_true) ** 2
            total_loss += loss
            model.backward(x, y_true, y_pred, learning_rate)
        avg_loss = total_loss / len(X_train)
        if gui:
            gui.update_training_status(epoch, avg_loss)


def query_model(model, query, vocabulary, documents, bow_vectors):
    query_nouns = tokenize_nouns(query)
    query_text = ' '.join(query_nouns)
    query_vector = create_bow_vector(query_text, vocabulary)
    scores = [sum(query_vector[j] * bow_vectors[i][j] for j in range(len(query_vector)))
              for i in range(len(bow_vectors))]
    ranked_docs = sorted(zip(documents, scores),
                         key=lambda x: x[1], reverse=True)
    return ranked_docs[:5]


class Application:
    def __init__(self, root):
        self.root = root
        self.root.title("Document Query System")

        # Allow resizing, in case it was too small before
        self.root.resizable(True, True)
        self.root.geometry("800x600")

        self.documents = []
        self.vocabulary = []
        self.bow_vectors = []
        self.model = None

        self.folder_path = r'D:\University Files\7th Semester\IR\Information-Retrieval-24-Assignments\Dataset'

        self.create_widgets()
        self.load_and_train()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="20 20 20 20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        title_label = ttk.Label(
            main_frame, text="Document Query System", font=("Helvetica", 20, "bold"))
        title_label.pack(pady=20)

        training_frame = ttk.LabelFrame(
            main_frame, text="Training Status", padding="10 10 10 10")
        training_frame.pack(fill=tk.BOTH, expand=False, pady=10)
        self.training_box = tk.Text(
            training_frame, height=10, width=70, state='normal', bg='#f7f7f7', wrap="word")
        self.training_box.pack(fill=tk.BOTH, expand=True)
        self.training_box.delete(1.0, tk.END)
        self.training_box.config(state='disabled')

        query_frame = ttk.LabelFrame(
            main_frame, text="Enter Your Query", padding="10 10 10 10")
        query_frame.pack(fill=tk.X, expand=False, pady=10)

        self.query_entry = ttk.Entry(query_frame, width=50)
        self.query_entry.pack(side=tk.LEFT, padx=(0, 10))
        self.query_entry.delete(0, tk.END)  # Ensure it's clear
        self.query_entry.configure(state='normal')
        self.query_entry.focus_set()

        search_button = ttk.Button(
            query_frame, text="Search", command=self.search_query)
        search_button.pack(side=tk.LEFT)

        results_frame = ttk.LabelFrame(
            main_frame, text="Top Matching Documents", padding="10 10 10 10")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        self.result_box = tk.Text(
            results_frame, height=10, width=70, state='normal', bg='#f7f7f7', wrap="word")
        self.result_box.pack(fill=tk.BOTH, expand=True)
        self.result_box.delete(1.0, tk.END)
        self.result_box.config(state='disabled')

        exit_frame = ttk.Frame(main_frame, padding="10 0 0 0")
        exit_frame.pack(fill=tk.X, expand=False)
        exit_button = ttk.Button(
            exit_frame, text="Exit", command=self.root.quit)
        exit_button.pack(side=tk.RIGHT, pady=(10, 0))

    def load_and_train(self):
        try:
            self.documents = load_txt_files(self.folder_path)
            if not self.documents:
                messagebox.showerror("Error", f"No .txt files found in {
                                     self.folder_path}")
                return

            self.vocabulary = build_vocabulary(self.documents)
            self.bow_vectors = prepare_bow_vectors(
                self.documents, self.vocabulary)

            self.y = [random.random() for _ in self.bow_vectors]
            split_index = int(0.8 * len(self.bow_vectors))
            X_train = self.bow_vectors[:split_index]
            y_train = self.y[:split_index]

            input_dim = len(self.vocabulary)
            self.model = NeuralNetwork(
                input_dim=input_dim, hidden_dim=10, output_dim=1)
            train_model(self.model, X_train, y_train,
                        epochs=10, learning_rate=0.01, gui=self)

            messagebox.showinfo("Success", f"Loaded {len(
                self.documents)} documents and trained the model.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def update_training_status(self, epoch, loss):
        self.training_box.config(state='normal')
        self.training_box.insert(tk.END, f"Epoch {epoch}, Loss: {loss:.4f}\n")
        self.training_box.see(tk.END)
        self.training_box.config(state='disabled')

    def search_query(self):
        query = self.query_entry.get().strip()
        if not query:
            messagebox.showwarning("Input Error", "Please enter a query.")
            return

        if not self.documents:
            messagebox.showwarning(
                "No Data", "Documents are not loaded properly.")
            return

        try:
            ranked_docs = query_model(
                self.model, query, self.vocabulary, self.documents, self.bow_vectors)
            self.display_results(ranked_docs)
        except Exception as e:
            messagebox.showerror(
                "Error", f"An error occurred during the search: {e}")

    def display_results(self, ranked_docs):
        self.result_box.config(state='normal')
        self.result_box.delete(1.0, tk.END)
        if not ranked_docs:
            self.result_box.insert(tk.END, "No documents found.\n")
        else:
            for idx, (doc, score) in enumerate(ranked_docs, start=1):
                self.result_box.insert(
                    tk.END, f"{idx}. {doc['filename']} - Relevance: {score:.4f}\n")
        self.result_box.config(state='disabled')


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
