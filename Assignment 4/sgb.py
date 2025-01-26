import tkinter as tk
from tkinter import ttk

# Udemy-like course hierarchy with descriptions
udemy_content = {
    "Programming & Development": {
        "Web Development": {
            "HTML & CSS": [
                {"name": "HTML Basics",
                    "description": "Learn the foundation of web development with HTML."},
                {"name": "Advanced CSS",
                    "description": "Master CSS techniques for responsive and modern web design."}
            ],
            "JavaScript": [
                {"name": "Introduction to JavaScript",
                    "description": "Understand the basics of JavaScript programming."},
                {"name": "ES6 Features",
                    "description": "Explore advanced features of modern JavaScript (ES6)."}
            ]
        },
        "Data Science": {
            "Python for Data Science": [
                {"name": "NumPy Basics",
                    "description": "Get started with NumPy for numerical computations."},
                {"name": "Data Visualization with Matplotlib",
                    "description": "Visualize data effectively using Matplotlib."}
            ],
            "Machine Learning": [
                {"name": "Supervised Learning",
                    "description": "Understand the principles of supervised machine learning."},
                {"name": "Unsupervised Learning",
                    "description": "Explore clustering and other unsupervised techniques."}
            ]
        }
    },
    "Business": {
        "Entrepreneurship": [
            {"name": "Startup Basics",
                "description": "Learn how to launch a successful startup."},
            {"name": "Pitch Deck Preparation",
                "description": "Master creating compelling pitch decks for investors."}
        ],
        "Management": [
            {"name": "Leadership Skills",
                "description": "Develop effective leadership qualities."},
            {"name": "Time Management Techniques",
                "description": "Learn to prioritize tasks and manage time effectively."}
        ]
    },
    "Design": {
        "Graphic Design": {
            "Adobe Photoshop": [
                {"name": "Getting Started with Photoshop",
                    "description": "Learn essential Photoshop tools and techniques."},
                {"name": "Advanced Photo Editing",
                    "description": "Master advanced photo manipulation and editing."}
            ],
            "UI/UX Design": [
                {"name": "Figma for Beginners",
                    "description": "Create UI prototypes with ease using Figma."},
                {"name": "Prototyping Techniques",
                    "description": "Understand advanced prototyping methods for UX."}
            ]
        }
    }
}

# Recursive function to add content to the tree view


def add_tree_nodes(tree, parent, content):
    """
    Add nodes to the tree view recursively.
    """
    for key, value in content.items():
        if isinstance(value, dict):
            node = tree.insert(parent, "end", text=key)  # Add categories
            add_tree_nodes(tree, node, value)  # Recurse for subcategories
        elif isinstance(value, list):
            for course in value:
                tree.insert(parent, "end", text=course["name"], values=(
                    course["description"],))  # Add courses

# Callback function to display course details


def display_course_details(event, details_text):
    """
    Display the selected course details in the details section.
    """
    selected_item = tree.focus()  # Get the currently selected item
    if not selected_item:
        return
    item_text = tree.item(selected_item, "text")
    item_values = tree.item(selected_item, "values")
    if item_values:
        details_text.configure(state="normal")
        details_text.delete(1.0, tk.END)
        details_text.insert(tk.END, f"Course: {item_text}\n\n")
        details_text.insert(tk.END, f"Description: {item_values[0]}\n")
        details_text.configure(state="disabled")

# Main GUI function


def main():
    """
    Main function to create an enhanced Tkinter GUI for browsing Udemy content.
    """
    # Create the main application window
    root = tk.Tk()
    root.title("Udemy Course Browser")
    root.geometry("1000x600")

    # Split the layout into two frames
    left_frame = ttk.Frame(root, width=400)
    right_frame = ttk.Frame(root, width=600)
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    # Tree view for hierarchical content
    global tree
    tree = ttk.Treeview(left_frame, columns=("Description"),
                        show="tree headings", selectmode="browse")
    tree.heading("#0", text="Courses", anchor="w")
    tree.heading("Description", text="Description", anchor="w")
    tree.column("#0", stretch=True, width=300)
    tree.column("Description", stretch=False, width=0)
    tree.pack(fill=tk.BOTH, expand=True)

    # Add Udemy content to the tree view
    add_tree_nodes(tree, "", udemy_content)

    # Text widget for course details
    details_label = ttk.Label(
        right_frame, text="Course Details", font=("Arial", 16, "bold"))
    details_label.pack(pady=10)
    details_text = tk.Text(right_frame, wrap=tk.WORD, font=(
        "Arial", 14), state="disabled", width=60, height=30)
    details_text.pack(fill=tk.BOTH, padx=10, pady=10)

    # Bind tree selection event to display details
    tree.bind("<<TreeviewSelect>>",
              lambda event: display_course_details(event, details_text))

    # Run the application
    root.mainloop()


# Run the program
if __name__ == "__main__":
    main()
