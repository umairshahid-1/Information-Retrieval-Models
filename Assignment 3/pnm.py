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
        clean_word = word.strip(",.!?\"'").lower()
        if is_noun(clean_word, previous_word):
            tokens.append(clean_word)
        previous_word = clean_word

    return tokens


# ------------------------- Graph Representation -------------------------

class Graph:
    def __init__(self):
        self.adjacency_list = {}

    def add_node(self, node):
        """Adds a node to the graph."""
        if node not in self.adjacency_list:
            self.adjacency_list[node] = set()

    def add_edge(self, node1, node2):
        """Creates an undirected edge between two nodes."""
        self.add_node(node1)
        self.add_node(node2)
        self.adjacency_list[node1].add(node2)
        self.adjacency_list[node2].add(node1)

    def get_neighbors(self, node):
        """Returns all neighbors of a node."""
        return self.adjacency_list.get(node, set())

    def bfs(self, start_node):
        """Performs BFS to find all connected nodes."""
        visited = set()
        queue = [start_node]
        connected_nodes = []

        while queue:
            node = queue.pop(0)
            if node not in visited:
                visited.add(node)
                connected_nodes.append(node)
                queue.extend(self.adjacency_list[node] - visited)

        return connected_nodes

    def display_graph(self):
        """Prints the adjacency list representation of the graph."""
        for node, neighbors in self.adjacency_list.items():
            print(f"{node}: {', '.join(neighbors)}")


# ------------------------- Document-Node Index Construction -------------------------

def build_document_graph(folder_path):
    """
    Build a graph where documents and nouns are nodes, and edges connect documents to their nouns.
    """
    graph = Graph()

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path) and filename.endswith(".txt"):
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read().lower()
                nouns = tokenize_nouns(content)

                # Add edges between the document and extracted nouns
                for noun in nouns:
                    graph.add_edge(filename, noun)

                print(f"{Fore.GREEN}{filename}{Fore.CYAN}{
                      nouns[:5]}{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}Error reading {
                      filename}: {e}{Style.RESET_ALL}")

    return graph


# ------------------------- Proximal Nodes Identification and Document Retrieval -------------------------

def find_proximal_nodes(query, graph):
    # Check if the entire query is a node in the graph
    if query.lower() in graph.adjacency_list:
        return [query.lower()]

    # Extract individual nouns from the query
    query_nouns = [noun.lower() for noun in tokenize_nouns(query)]

    # Find the nouns that are present in the graph
    proximal_nodes = [
        noun for noun in query_nouns if noun in graph.adjacency_list]

    return proximal_nodes


def retrieve_connected_documents(graph, proximal_nodes):
    connected_docs = set()

    for node in proximal_nodes:
        neighbors = graph.get_neighbors(node)
        for neighbor in neighbors:
            if neighbor.endswith(".txt"):
                connected_docs.add(neighbor)

    # If no documents are connected, check if the full query is a node
    if not connected_docs and any(node in graph.adjacency_list for node in proximal_nodes):
        for node in proximal_nodes:
            if node in graph.adjacency_list:
                connected_docs.update(graph.get_neighbors(node))

    return connected_docs


# ------------------------- Results Presentation -------------------------

def display_results(graph, connected_docs, proximal_nodes):
    print(f"{Fore.GREEN}Top Matching Documents:{Style.RESET_ALL}")

    if connected_docs:
        # Filter connected nouns to include only proximal nodes
        table = [
            [doc, ", ".join([noun for noun in graph.get_neighbors(
                doc) if noun in proximal_nodes])]
            for doc in connected_docs
        ]
        print(tabulate(
            table,
            headers=[f"{Fore.LIGHTMAGENTA_EX}Document Name{Style.RESET_ALL}",
                     f"{Fore.LIGHTMAGENTA_EX}Connected Nouns{Style.RESET_ALL}"],
            tablefmt="grid"
        ))
    else:
        print(f"{Fore.RED}No documents matched your query. Please try a different search term.{
              Style.RESET_ALL}")

    print(f"\n{Fore.YELLOW}Proximal Nodes:{
          Style.RESET_ALL} {', '.join(proximal_nodes)}")


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

        # 2. Build the graph
        graph = build_document_graph(folder_path)

        while True:
            # 3. Query input from the user
            query = input(f"\n{Fore.CYAN}Enter your query (or type 'p' to change path, 'exit' to quit): {
                          Style.RESET_ALL}")
            if query.lower() == 'exit':
                print(f"{Fore.GREEN}Exiting program. Goodbye!{Style.RESET_ALL}")
                return
            elif query.lower() == 'p':
                break

            # 4. Identify proximal nodes from the query
            proximal_nodes = find_proximal_nodes(query, graph)
            if not proximal_nodes:
                print(f"{Fore.RED}The query does not match any extracted nouns. Try again with relevant terms.{
                      Style.RESET_ALL}")
                continue

            # 5. Retrieve connected documents
            connected_docs = retrieve_connected_documents(
                graph, proximal_nodes)

            # 6. Present the results
            display_results(graph, connected_docs, proximal_nodes)


if __name__ == "__main__":
    main()
