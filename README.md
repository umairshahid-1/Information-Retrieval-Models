# Information Retrieval Models

This repository contains various implementations and assignments for **Information Retrieval (IR)** models that were taught by **Dr. Khaldoon** at **UET** in the **Information Retrieval** subject during **Fall 2024**. The code is organized into different assignments, each focusing on specific IR concepts and techniques.

<img src="https://i.imgur.com/ZpiqsbO.jpeg" alt="IR Models" style="width:50%; height:auto;">

## Assignment 1: Search Engine

### File: `Assignment 1/Search Engine.py`

This file implements a basic search engine that performs the following tasks:
1. **Indexing Documents**: Reads and indexes documents from a specified folder. It cleans, tokenizes, and extracts nouns from the text.
2. **Search by Word**: This feature allows users to search for a word in the indexed documents and displays its frequency and position in each document.
3. **Search by Document Title**: Allows users to search for a document by its title.
4. **Interactive Menu**: Provides an interactive menu for users to choose different search options and re-index documents if needed.

<div style="display: flex; justify-content: space-between;">
    <img src="https://i.imgur.com/3aCxMJG.png" alt="Search Engine" style="width:50%; height:auto;">
    <img src="https://i.imgur.com/fPE7EEC.png" alt="Search Engine" style="width:48%; height:auto;">
</div>

---

## Assignment 2: TF-IDF and Cosine Similarity

### File: `Assignment 2/Assignment2.py`

This file implements the following functionalities:
1. **Tokenize Nouns**: Extract nouns from documents using heuristics optimized for technology-related text.
2. **TF-IDF Calculation**: Calculates Term Frequency (TF), Inverse Document Frequency (IDF), and TF-IDF scores for search queries.
3. **Cosine Similarity**: Computes cosine similarity scores to rank documents based on their relevance to the search query.
4. **Interactive Search**: Provides an interactive search interface to query documents and display results in a well-formatted table.

<div style="display: flex; justify-content: space-between;">
<img src="https://i.imgur.com/6wKu5rv.png" alt="Assignment2" style="width:48%; height:auto;">
<img src="https://i.imgur.com/P44tjRZ.png" alt="Search Engine" style="width:48%; height:auto;">
</div>

---

## Assignment 3: Binary Independence Model (BIM)

### Files:
- `Assignment 3/BIM.py`
- `Assignment 3/pnm.py`
- `Assignment 3/non_overlaped.py`

These files implement different aspects of the Binary Independence Model (BIM) and document indexing:
1. **Noun Extraction and Tokenization**: Extracts meaningful nouns from text content.
2. **Binary Vector Creation**: Creates binary vectors for documents based on the presence of terms.
3. **Term Probability Calculation**: Calculates term probabilities for BIM.
4. **Document Ranking**: Ranks documents using BIM scores computed via the Dice Coefficient.
5. **Graph Representation**: Builds a graph where documents and nouns are nodes, and edges connect documents to their nouns.
6. **Non-Overlapped List Model**: Implements a linked list model for non-overlapping document lists and performs search and retrieval.

<img src="https://i.imgur.com/OJNLpYa.png" alt="BIM" style="width:50%; height:auto;">

---

## Assignment 4: Graph-Based Models

### Files:
- `Assignment 4/sgb.py`
- `Assignment 4/hypertext.py`

These files implement graph-based models for organizing and retrieving information:
1. **Udemy Course Browser**: Creates a GUI using Tkinter to browse Udemy-like course hierarchy with descriptions.
2. **Hypertext E-book Reader**: Implements an e-book reader with hypertext navigation and search functionality using Tkinter.

<div style="display: flex; justify-content: space-between;">
    <img src="https://i.imgur.com/SL8bxpw.png" alt="SGB" style="width:48%; height:auto;">
    <img src="https://i.imgur.com/9WXaPJ0.png" alt="Hypertext" style="width:48%; height:auto;">
</div>

---

## Assignment 5: Boolean Extended Search

### File: `Assignment 5/boolean.py`

This file implements an extended Boolean search system for e-commerce products:
1. **Product Data Loading**: Loads product data from a CSV file.
2. **Boolean Query Processing**: Processes Boolean queries with relational operators (AND, OR, NOT) and field-based conditions.
3. **Search Interface**: Provides a GUI for entering search queries and displaying results using Tkinter.

<img src="https://i.imgur.com/OZBAwIg.png" alt="Extended Boolean" style="width:50%; height:auto;">

---

## Assignment 6: Neural Network for Document Query

### File: `Assignment 6/NeuralNetwork.py`

This file implements a neural network-based document query system:
1. **Noun Extraction and Tokenization**: Extracts nouns from documents and builds a vocabulary.
2. **Bag-of-Words Vector Creation**: Creates Bag-of-Words (BoW) vectors for documents.
3. **Neural Network**: Trains a simple neural network to rank documents based on their relevance to a search query.
4. **GUI for Query and Results**: Provides a GUI for entering search queries and displaying top matching documents using Tkinter.

<img src="https://i.imgur.com/Axr0jon.png" alt="Neural Network" style="width:50%; height:auto;">

---

## Assignment 7: Belief Network for Smartphone Analysis

### File: `Assignment 7/beliefNetwork.py`

This file implements a belief network model for analyzing smartphone camera quality:
1. **Data Loading**: Loads smartphone data from a CSV file.
2. **Bayesian Inference**: Performs Bayesian inference to rank smartphones based on user-defined criteria.
3. **Belief Network Model**: Uses a belief network model to rank smartphones based on their attributes and relevance to the query.
4. **GUI for Input and Results**: Provides a GUI for entering user ratings and displaying ranked smartphones using Tkinter.

<img src="https://i.imgur.com/SE2hzlx.png" alt="Belief Network" style="width:50%; height:auto;">

---
