import tkinter as tk
from tkinter import messagebox

# Content structure
ebook_content = {
    "Chapter 1: A Scandal in Bohemia": {
        "content": (
            "To Sherlock Holmes she is always the woman. I have seldom heard him mention her under any other name.\n\n"
            "Click here to go to [Chapter 2: The Red-Headed League]."
        ),
        "links": {"[Chapter 2: The Red-Headed League]": "Chapter 2: The Red-Headed League"},
    },
    "Chapter 2: The Red-Headed League": {
        "content": (
            "I had called upon my friend Sherlock Holmes one day in the autumn of last year and found him in deep conversation.\n\n"
            "Click here to go to [Chapter 1: A Scandal in Bohemia] or [Chapter 3: A Case of Identity]."
        ),
        "links": {
            "[Chapter 1: A Scandal in Bohemia]": "Chapter 1: A Scandal in Bohemia",
            "[Chapter 3: A Case of Identity]": "Chapter 3: A Case of Identity",
        },
    },
    "Chapter 3: A Case of Identity": {
        "content": (
            "My dear fellow,’ said Sherlock Holmes as we sat on either side of the fire in his lodgings at Baker Street.\n\n"
            "Go back to [Chapter 2: The Red-Headed League]."
        ),
        "links": {"[Chapter 2: The Red-Headed League]": "Chapter 2: The Red-Headed League"},
    },
}

# Global variables for navigation and visited tracking
visited_nodes = []
visited_links = set()

# Function to display content for a specific chapter


def display_content(chapter_name, keyword=None):
    global visited_nodes, visited_links

    # Clear the text widget
    text_widget.config(state=tk.NORMAL)
    text_widget.delete("1.0", tk.END)

    # Add content to the text widget
    chapter = ebook_content[chapter_name]
    content = chapter["content"]
    text_widget.insert(tk.END, content)

    # Highlight keywords if provided
    if keyword:
        start = "1.0"
        while True:
            start = text_widget.search(
                keyword, start, stopindex=tk.END, nocase=True)
            if not start:
                break
            end = f"{start}+{len(keyword)}c"
            text_widget.tag_add("highlight", start, end)
            text_widget.tag_config("highlight", background="yellow")
            start = end

    # Highlight and bind links
    for link_text, target_chapter in chapter["links"].items():
        start_index = text_widget.search(link_text, "1.0", tk.END)
        if start_index:
            end_index = f"{start_index}+{len(link_text)}c"
            text_widget.tag_add(link_text, start_index, end_index)

            # Set color for visited and unvisited links
            link_color = "purple" if target_chapter in visited_links else "blue"
            text_widget.tag_config(
                link_text, foreground=link_color, underline=True)
            text_widget.tag_bind(link_text, "<Button-1>",
                                 lambda e, t=target_chapter: navigate_to(t))

    # Disable editing
    text_widget.config(state=tk.DISABLED)

    # Update visited nodes and links
    if visited_nodes and visited_nodes[-1] != chapter_name:
        visited_nodes.append(chapter_name)
    elif not visited_nodes:
        visited_nodes.append(chapter_name)

    visited_links.add(chapter_name)

# Navigation function


def navigate_to(chapter_name):
    display_content(chapter_name)

# Back button function


def go_back():
    if len(visited_nodes) > 1:
        visited_nodes.pop()  # Remove current chapter
        previous_chapter = visited_nodes[-1]
        display_content(previous_chapter)
    else:
        messagebox.showinfo("Navigation", "No previous chapter available.")

# Search functionality


def search_keyword():
    keyword = search_entry.get().strip()
    if not keyword:
        messagebox.showwarning("Search", "Please enter a keyword to search.")
        return

    search_results.delete(0, tk.END)  # Clear previous results
    for chapter, details in ebook_content.items():
        if keyword.lower() in details["content"].lower():
            search_results.insert(tk.END, chapter)

    if not search_results.size():
        messagebox.showinfo("Search", f"No results found for '{keyword}'.")


def go_to_search_result(event):
    selected_chapter = search_results.get(search_results.curselection())
    display_content(selected_chapter, keyword=search_entry.get().strip())


# GUI setup
root = tk.Tk()
root.title("E-book Reader")
root.geometry("800x600")
root.configure(bg="#f2f2f2")

# Menu bar
menu_bar = tk.Menu(root)
chapter_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Chapters", menu=chapter_menu)

# Populate menu
for chapter in ebook_content.keys():
    chapter_menu.add_command(
        label=chapter, command=lambda c=chapter: display_content(c))

# Search bar
search_frame = tk.Frame(root, bg="#e6e6e6")
search_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

search_label = tk.Label(search_frame, text="Search:",
                        bg="#e6e6e6", font=("Arial", 12))
search_label.pack(side=tk.LEFT, padx=5)

search_entry = tk.Entry(search_frame, width=30, font=("Arial", 12))
search_entry.pack(side=tk.LEFT, padx=5)
# Bind the Enter key to trigger the search
search_entry.bind("<Return>", lambda event: search_keyword())


search_button = tk.Button(search_frame, text="Search",
                          command=search_keyword, bg="#4d79ff", fg="white", font=("Arial", 10))
search_button.pack(side=tk.LEFT, padx=5)

# Text widget for content
text_widget = tk.Text(root, wrap=tk.WORD, font=("Arial", 12), bg="#ffffcc")
text_widget.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

# Search results list
search_results_frame = tk.Frame(root, bg="#f2f2f2")
search_results_frame.pack(side=tk.RIGHT, fill=tk.Y)

search_results_label = tk.Label(
    search_results_frame, text="Search Results:", bg="#f2f2f2", font=("Arial", 12, "bold"))
search_results_label.pack(anchor=tk.NW, padx=5, pady=5)

search_results = tk.Listbox(
    # Increased width
    search_results_frame, height=10, width=40, font=("Arial", 12))
search_results.pack(fill=tk.Y, padx=5, pady=5)
search_results.bind("<<ListboxSelect>>", go_to_search_result)

# Navigation buttons
nav_frame = tk.Frame(root, bg="#f2f2f2")
nav_frame.pack(side=tk.BOTTOM, fill=tk.X)

back_button = tk.Button(nav_frame, text="Back", command=go_back,
                        bg="#4d79ff", fg="white", font=("Arial", 10))
back_button.pack(side=tk.LEFT, padx=5, pady=5)

exit_button = tk.Button(nav_frame, text="Exit", command=root.quit,
                        bg="#ff4d4d", fg="white", font=("Arial", 10))
exit_button.pack(side=tk.RIGHT, padx=5, pady=5)

# Load the first chapter initially
display_content("Chapter 1: A Scandal in Bohemia")

# Run the application
root.mainloop()
