import tkinter as tk
from tkinter import ttk
import csv

# Load data from CSV file


def load_data(file_path):
    smartphones = []
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            smartphones.append({
                "Model": row["Model"],
                "Megapixels": float(row["Megapixels"]),
                "Aperture": float(row["Aperture"]),
                "Optical Zoom": float(row["Optical Zoom"]),
                "User Rating": float(row["User Rating"]),
                "Expert Rating": float(row["Expert Rating"]),
            })
    return smartphones


def compute_PQ(smartphones, user_rating, expert_rating):
    """
    Compute P(Q) as the probability that a randomly chosen smartphone from the dataset
    meets the user's rating criteria (both user and expert ratings).
    """
    count = sum(1 for phone in smartphones if phone["User Rating"]
                >= user_rating and phone["Expert Rating"] >= expert_rating)
    if len(smartphones) == 0:
        return 0.0001  # avoid division by zero
    return count / len(smartphones)


def infer_camera_quality(smartphones, user_rating, expert_rating):
    """
    Bayesian Inference:
    P(R|Q) = [P(Q|R) * P(R)] / P(Q)

    Interpretation:
    - Q: The event that the smartphone meets the user's query criteria.
    - R: The event that the smartphone is "relevant" (here relevance is a simplified concept).

    Assumptions:
    - P(R) = 0.5 (uniform prior for simplicity)
    - P(Q|R): Probability that a relevant phone meets the user's query. 
      We approximate relevance as being correlated with the phone's own ratings.
      If the phone meets or exceeds user_rating and expert_rating, P(Q|R)=1, else lower.
    - P(Q): Computed from the dataset as the fraction of phones that meet the query criteria.
    """
    P_R = 0.5
    P_Q = compute_PQ(smartphones, user_rating, expert_rating)
    if P_Q == 0:
        P_Q = 0.0001  # Avoid division by zero

    results = []
    for phone in smartphones:
        # Define P(Q|R):
        # If the phone meets both user and expert criteria, make P(Q|R) higher.
        # Here we can either do a step function (1 if meets criteria, 0 otherwise)
        # or a scaled version. For simplicity, let's do a step function.

        meets_criteria = (phone["User Rating"] >= user_rating) and (
            phone["Expert Rating"] >= expert_rating)
        P_Q_given_R = 1.0 if meets_criteria else 0.0

        # P(R|Q) = [P(Q|R)*P(R)]/P(Q)
        P_R_given_Q = (P_Q_given_R * P_R) / P_Q

        results.append((phone["Model"], P_R_given_Q))

    return sorted(results, key=lambda x: x[1], reverse=True)


def belief_network(smartphones, user_rating, expert_rating):
    """
    Belief Network model:
    P(R|Q,D) = [P(Q|D)*P(R|D)*P(D)] / P(Q)

    Interpretation:
    - Q: User's query (meeting user_rating and expert_rating).
    - D: The document (phone) itself.
    - R: Relevance (again, a simplified notion).

    Assumptions:
    - P(D) = 0.5 as a prior.
    - P(R|D): Probability of relevance given the phone's attributes.
      We'll use the existing heuristic: 
      P(R|D) = (0.4 * (Megapixels/200)) + (0.3*(1/Aperture))
    - P(Q|D): Probability that this specific phone meets the query criteria.
    - P(Q): Computed as before from the dataset.
    """
    P_D = 0.5
    P_Q = compute_PQ(smartphones, user_rating, expert_rating)
    if P_Q == 0:
        P_Q = 0.0001

    results = []
    for phone in smartphones:
        # Compute P(R|D)
        # Example heuristic:
        # Assuming max meaningful megapixels ~200 for normalization
        # Aperture: smaller number = better, so use 1/aperture
        P_R_given_D = (0.4 * (phone["Megapixels"] / 200)
                       ) + (0.3 * (1 / phone["Aperture"]))
        # Clip P_R_given_D to [0,1] if needed
        P_R_given_D = max(0, min(1, P_R_given_D))

        # P(Q|D): Probability that the phone meets the criteria given its attributes.
        meets_criteria = (phone["User Rating"] >= user_rating) and (
            phone["Expert Rating"] >= expert_rating)
        P_Q_given_D = 1.0 if meets_criteria else 0.0

        # P(R|Q,D) = [P(Q|D)*P(R|D)*P(D)]/P(Q)
        P_R_given_Q_and_D = (P_Q_given_D * P_R_given_D * P_D) / P_Q

        results.append((phone["Model"], P_R_given_Q_and_D))

    return sorted(results, key=lambda x: x[1], reverse=True)


def run_inference():
    user_rating_input = float(user_rating_var.get())
    expert_rating_input = float(expert_rating_var.get())
    results = infer_camera_quality(
        smartphones, user_rating_input, expert_rating_input)
    update_results(inference_tree, results)


def run_belief_network():
    user_rating_input = float(user_rating_var.get())
    expert_rating_input = float(expert_rating_var.get())
    results = belief_network(
        smartphones, user_rating_input, expert_rating_input)
    update_results(belief_tree, results)


def update_results(tree, results):
    for row in tree.get_children():
        tree.delete(row)
    for model, score in results:
        # Display the score as a percentage
        tree.insert("", "end", values=(model, f"{score*100:.1f}%"))


# Load data
file_path = r"D:\University Files\7th Semester\IR\Information-Retrieval-24-Assignments\Assignment 7\Smartphones.csv"
smartphones = load_data(file_path)

# GUI Setup
root = tk.Tk()
root.title("Smartphone Camera Quality Analysis")
root.geometry("1000x600")
root.configure(bg="#ffffff")

# Header
header = tk.Label(root, text="Smartphone Camera Quality Analysis", font=(
    "Segoe UI", 24, "bold"), pady=20, bg="#ffffff")
header.pack()

# Input Section
input_frame = tk.Frame(root, bg="#ffffff")
input_frame.pack(pady=10)

tk.Label(input_frame, text="User Inputs", font=("Segoe UI", 16, "bold"),
         bg="#ffffff").grid(row=0, column=0, columnspan=2, pady=10)

# User Rating
tk.Label(input_frame, text="Minimum User Rating (0-5):", font=("Segoe UI",
         12), bg="#ffffff").grid(row=1, column=0, sticky="e", padx=10)
user_rating_var = tk.StringVar(value="4.0")
tk.Entry(input_frame, textvariable=user_rating_var, font=(
    "Segoe UI", 12)).grid(row=1, column=1, pady=5)

# Expert Rating
tk.Label(input_frame, text="Minimum Expert Rating (0-5):", font=("Segoe UI",
         12), bg="#ffffff").grid(row=2, column=0, sticky="e", padx=10)
expert_rating_var = tk.StringVar(value="4.0")
tk.Entry(input_frame, textvariable=expert_rating_var,
         font=("Segoe UI", 12)).grid(row=2, column=1, pady=5)

# Optional: Automatically re-run inference when user changes input
user_rating_var.trace("w", lambda *args: run_inference())
expert_rating_var.trace("w", lambda *args: run_inference())

button_frame = tk.Frame(root, bg="#ffffff")
button_frame.pack(pady=10)

tk.Button(button_frame, text="Run Inference", command=run_inference, bg="#4CAF50",
          fg="white", font=("Segoe UI", 14), width=15).grid(row=0, column=0, padx=10, pady=10)
tk.Button(button_frame, text="Run Belief Network", command=run_belief_network, bg="#2196F3",
          fg="white", font=("Segoe UI", 14), width=15).grid(row=0, column=1, padx=10, pady=10)

# Results Section
result_frame = tk.Frame(root, bg="#ffffff")
result_frame.pack(pady=20, fill="both", expand=True)

result_inner_frame = tk.Frame(result_frame, bg="#ffffff")
result_inner_frame.pack(side="top", fill="x", padx=20)

# Inference Results Section
inference_frame = tk.Frame(result_inner_frame, bg="#ffffff")
inference_frame.pack(side="left", fill="both", expand=True, padx=10)

inference_label = tk.Label(inference_frame, text="Inference Results", font=(
    "Segoe UI", 16, "bold"), bg="#ffffff")
inference_label.pack(anchor="n", pady=5)

inference_tree = ttk.Treeview(inference_frame, columns=(
    "Model", "Score"), show="headings", height=10)
inference_tree.heading("Model", text="Model")
inference_tree.heading("Score", text="Score")
inference_tree.column("Model", width=300, anchor="w")
inference_tree.column("Score", width=100, anchor="center")
scrollbar = ttk.Scrollbar(
    inference_frame, orient="vertical", command=inference_tree.yview)
inference_tree.configure(yscrollcommand=scrollbar.set)
inference_tree.pack(side="left", fill="both", expand=True, pady=10)
scrollbar.pack(side="left", fill="y")

# Belief Network Results Section
belief_frame = tk.Frame(result_inner_frame, bg="#ffffff")
belief_frame.pack(side="left", fill="both", expand=True, padx=10)

belief_label = tk.Label(belief_frame, text="Belief Network Results", font=(
    "Segoe UI", 16, "bold"), bg="#ffffff")
belief_label.pack(anchor="n", pady=5)

belief_tree = ttk.Treeview(belief_frame, columns=(
    "Model", "Score"), show="headings", height=10)
belief_tree.heading("Model", text="Model")
belief_tree.heading("Score", text="Score")
belief_tree.column("Model", width=300, anchor="w")
belief_tree.column("Score", width=100, anchor="center")
scrollbar2 = ttk.Scrollbar(
    belief_frame, orient="vertical", command=belief_tree.yview)
belief_tree.configure(yscrollcommand=scrollbar2.set)
belief_tree.pack(side="left", fill="both", expand=True, pady=10)
scrollbar2.pack(side="left", fill="y")

root.mainloop()
