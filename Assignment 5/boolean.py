import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import re


class EcommerceSearchSystem:
    def __init__(self, master):
        """
        Initialize the E-commerce Boolean Extended Search Application
        """
        self.master = master
        master.title("Boolean Extended Product Search")
        master.geometry("800x600")

        # Step 2: Search Criteria Definition
        self.products = []
        self.create_search_interface()

    def load_product_data(self):
        """
        Load product data from CSV file
        """
        try:
            file_path = filedialog.askopenfilename(
                title="Select Product CSV",
                filetypes=[("CSV files", "*.csv")]
            )

            if not file_path:
                messagebox.showwarning("Warning", "No file selected.")
                return

            with open(file_path, 'r', encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
                self.products = list(reader)

            # Update term matrix and display loaded products
            self.create_term_representation()
            self.display_products(self.products)

            messagebox.showinfo("Success", "Product data loaded successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not load file: {e}")

    def display_products(self, products):
        """
        Display products in the results tree
        """
        # Clear existing rows
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)

        # Populate with new data
        for product in products:
            self.results_tree.insert('', 'end', values=(
                product.get("id"),
                product.get("name"),
                product.get("category"),
                product.get("price"),
                product.get("brand"),
            ))

    def create_search_interface(self):
        """
        Create search interface with Boolean query support
        """
        # Search Frame
        search_frame = ttk.Frame(self.master)
        search_frame.pack(padx=10, pady=10, fill=tk.X)

        # Query Entry
        ttk.Label(search_frame, text="Search Products:").pack(side=tk.LEFT)
        self.query_entry = ttk.Entry(search_frame, width=50)
        self.query_entry.pack(side=tk.LEFT, padx=5)

        # Load CSV Button
        ttk.Button(search_frame, text="Load CSV",
                   command=self.load_product_data).pack(side=tk.LEFT, padx=5)

        # Search Button
        ttk.Button(search_frame, text="Search",
                   command=self.process_boolean_query).pack(side=tk.LEFT, padx=5)

        # Results Display
        self.results_tree = ttk.Treeview(
            self.master,
            columns=("ID", "Name", "Category", "Price", "Brand"),
            show='headings'
        )
        for col in ("ID", "Name", "Category", "Price", "Brand"):
            self.results_tree.heading(col, text=col)
        self.results_tree.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

    def create_term_representation(self):
        """
        Enhanced Term Representation
        """
        self.term_matrix = {}
        for product in self.products:
            # Aggregate searchable terms
            terms = set()
            for key, value in product.items():
                if value:  # Ensure value is not None
                    # Split by non-alphanumeric as well to handle punctuation
                    val_terms = re.split(r'\W+', value.lower())
                    # remove empty strings
                    val_terms = [t for t in val_terms if t]
                    terms.update(val_terms)
            self.term_matrix[product['id']] = terms

    def process_boolean_query(self):
        """
        Process Boolean queries with relational operators
        """
        query = self.query_entry.get().strip()
        if not query:
            messagebox.showwarning("Warning", "Enter a search query.")
            return

        # Perform search
        results = self.boolean_search(query.lower())

        # Display Results
        self.display_products(results)

    def tokenize_query(self, query):
        """
        Tokenize the query into terms, operators, and conditions.
        This handles:
        - Boolean operators: and, or, not
        - Field-based queries: field:value or field:not value
        - Numeric conditions: price<100, price>200, price=799.99
        - Regular terms

        Assumes query is lowercased already.
        """

        # Split on whitespace first
        raw_tokens = query.split()

        tokens = []
        i = 0
        while i < len(raw_tokens):
            token = raw_tokens[i]

            # Check for boolean operators
            if token in ["and", "or", "not"]:
                tokens.append(token)
                i += 1
                continue

            # Check for field conditions (with :, <, >, =)
            # Pattern: field:value or field<value or field>value or field=value
            field_condition_match = re.match(r'(\w+)([:<>=])(.*)', token)
            if field_condition_match:
                # It's a single-token condition like category:electronics or price<100
                tokens.append(token)
                i += 1
                continue

            # If we get something like "brand:not" "SoundWave", we should merge
            # But let's handle "not" as a separate token. If user wrote brand:not SoundWave
            # Then next token "SoundWave" is a separate term. We'll handle the "not" within evaluate_field_condition.

            # If it's just a term, check if next tokens combine into a condition
            # For example: "price", "<", "100"
            if i + 2 < len(raw_tokens):
                # Check if next two tokens form a numeric condition: field < value
                combined = token + raw_tokens[i+1] + raw_tokens[i+2]
                if re.match(r'(\w+)(<|>|=)(\S+)', combined):
                    tokens.append(combined)
                    i += 3
                    continue

            # If none of the above, just a term
            tokens.append(token)
            i += 1

        return tokens

    def boolean_search(self, query):
        """
        Implement Boolean Extended Search Logic with Relational Operators
        """
        tokens = self.tokenize_query(query)
        matching_products = []

        for product in self.products:
            product_terms = self.term_matrix[product['id']]  # Extract terms
            match = self.evaluate_boolean_expression(
                tokens, product, product_terms)
            if match:
                matching_products.append(product)

        return matching_products

    def evaluate_boolean_expression(self, tokens, product, product_terms):
        """
        Evaluate Boolean Expression for a single product with numeric and field-based conditions.
        We'll go through tokens linearly:
        - Terms or conditions produce True/False
        - "not" flips the next condition
        - "and"/"or" combine with accumulated result
        """

        result = None
        current_op = "and"
        negate_next = False

        for token in tokens:
            if token in ["and", "or"]:
                current_op = token
                negate_next = False
                continue
            elif token == "not":
                negate_next = not negate_next
                continue
            else:
                # Evaluate the token as a condition or a term
                match = self.evaluate_token_condition(
                    token, product, product_terms)

                # Apply negation if needed
                if negate_next:
                    match = not match
                    negate_next = False

                # Combine with result using current_op
                if result is None:
                    result = match
                else:
                    if current_op == "and":
                        result = result and match
                    elif current_op == "or":
                        result = result or match

        return bool(result)

    def evaluate_token_condition(self, token, product, product_terms):
        """
        Evaluate a single token which could be:
        - A simple term
        - A field:value or field<value or field>value or field=value condition
        """

        # Check for field-based conditions or numeric conditions
        field_condition_match = re.match(r'(\w+)([:<>=])(.*)', token)
        if field_condition_match:
            field = field_condition_match.group(1)
            operator = field_condition_match.group(2)
            value = field_condition_match.group(3).strip()

            if field == "price":
                return self.evaluate_price_condition(operator, value, product["price"])
            else:
                return self.evaluate_field_condition(field, operator, value, product)

        # Otherwise, it's just a term check
        return token in product_terms

    def evaluate_field_condition(self, field, operator, value, product):
        """
        Evaluate field-specific conditions.
        Supports:
        field:value (substring match),
        field:not <value>,
        where operator can be ':' indicating a substring match in product[field].
        If 'not' appears at the start of value, it negates the condition.
        """
        field = field.lower()
        if field not in product:
            return False

        product_val = str(product[field]).lower()

        # Handle "not" inside the value for field conditions
        # e.g. brand:not soundwave
        # If so, we strip "not" and check negation
        negation = False
        # If value starts with "not ", remove it and set negation
        if value.startswith("not "):
            negation = True
            value = value[4:].strip()

        if operator == ":":
            # substring check
            match = (value in product_val)
            if negation:
                match = not match
            return match

        # If other operators appear here (like '='), we could do equality checks
        if operator == "=":
            match = (product_val == value)
            if negation:
                match = not match
            return match

        # By default, if unsupported operator for fields, return False
        return False

    def evaluate_price_condition(self, operator, value, product_price):
        """
        Evaluate Price conditions like:
        price<100, price=199.99, price>500
        """
        try:
            product_price = float(product_price)
            target = float(value)
        except ValueError:
            return False  # Invalid numeric value

        if operator == "<":
            return product_price < target
        elif operator == ">":
            return product_price > target
        elif operator == "=":
            return product_price == target
        else:
            return False


def main():
    """
    Main application launcher
    """
    root = tk.Tk()
    app = EcommerceSearchSystem(root)
    root.mainloop()


if __name__ == "__main__":
    main()
