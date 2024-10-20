import csv
import os
import sys

def read_files_labels(csv_file):
    """Read the CSV file containing filenames and labels."""
    files_labels = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')  # Set delimiter to ';'
        next(reader)  # Skip header if there is one
        for row in reader:
            topic = row[0].strip()  # Get the topic from the first column
            filename = row[1].strip()  # Get the file name from the second column
            labels = [label.strip() for label in row[2].split(',')]  # Split labels by comma
            files_labels.append((topic, filename, labels))
    print("Read Files and Labels:", files_labels)  # Debug output
    return files_labels

def read_themes(csv_file):
    """Read the themes CSV file and return a structured dictionary."""
    themes = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')  # Ensure the correct delimiter
        next(reader)  # Skip header if there is one
        for row in reader:
            # Skip empty lines or rows with insufficient columns
            if not row or len(row) < 3:
                print(f"Warning: Skipping invalid or empty row: {row}")
                continue

            theme_name = row[0].strip()
            parent_theme = row[1].strip() if row[1].strip() != '' else None  # Allow for top-level themes
            try:
                hierarchy = int(row[2].strip())  # Convert to integer
            except ValueError:
                print(f"Warning: Hierarchy value for theme '{theme_name}' is not an integer: {row[2]}")
                continue  # Skip this row if hierarchy is not valid

            themes.append({'theme_name': theme_name, 'parent_theme': parent_theme, 'hierarchy': hierarchy})
    print("Read Themes:", themes)  # Debug output
    return themes

def build_theme_hierarchy(themes):
    """Build a hierarchy tree from the themes list."""
    hierarchy_tree = []
    theme_dict = {theme['theme_name']: theme for theme in themes}  # Create a dictionary for quick lookup
    for theme in themes:
        if theme['parent_theme'] is None:
            hierarchy_tree.append(theme)  # Top-level theme
        else:
            parent = theme_dict.get(theme['parent_theme'])
            if parent:
                if 'children' not in parent:
                    parent['children'] = []
                parent['children'].append(theme)
            else:
                print(f"Warning: Parent theme '{theme['parent_theme']}' not found for theme '{theme['theme_name']}'")
    return hierarchy_tree

def generate_latex_for_themes(theme, files_labels, label_to_include, hierarchy_level=1):
    """Recursively generate LaTeX content for the themes and their hierarchy."""
    latex_content = []
    section_command = ["\\section", "\\subsection", "\\subsubsection", "\\paragraph", "\\subparagraph"]

    # Store matched exercises for this theme
    matched_exercises = []
    
    # Find matching exercises
    for topic, filename, labels in files_labels:
        if topic.strip().lower() == theme['theme_name'].strip().lower():
            if label_to_include in labels:
                matched_exercises.append(filename)  # Store matched exercise for later use

    # Only add the theme section if there are matched exercises
    if matched_exercises:
        if hierarchy_level <= len(section_command):
            latex_content.append(f"{section_command[hierarchy_level - 1]}{{{theme['theme_name']}}}")

        # Add exercises related to the theme
        for filename in matched_exercises:
            latex_content.append(f"\\input{{{filename}}}")

    # Recurse for children themes (if any)
    if 'children' in theme:
        for child_theme in sorted(theme['children'], key=lambda t: t['hierarchy']):
            latex_content.extend(generate_latex_for_themes(child_theme, files_labels, label_to_include, hierarchy_level + 1))
    
    return latex_content

def save_latex_file(content, filename):
    """Save the generated LaTeX content to a file."""
    with open(filename, 'w', encoding='utf-8') as f:  # Use utf-8 encoding
        f.write("\n".join(content))
    print(f"Latex content saved to {filename}")

def main(files_labels_csv, themes_csv, label_to_include, output_file):
    # Step 1: Read the CSV files
    files_labels = read_files_labels(files_labels_csv)
    themes = read_themes(themes_csv)

    # Step 2: Build the theme hierarchy
    hierarchy_tree = build_theme_hierarchy(themes)

    # Step 3: Generate LaTeX content for each theme recursively
    latex_content = []
    for top_level_theme in sorted(hierarchy_tree, key=lambda t: t['hierarchy']):
        latex_content.extend(generate_latex_for_themes(top_level_theme, files_labels, label_to_include))

    # Step 4: Save the LaTeX content to the output file
    save_latex_file(latex_content, output_file)
    print(f"LaTeX file for label '{label_to_include}' saved to {output_file}")

if __name__ == "__main__":
    # Ensure proper usage
    if len(sys.argv) != 4:
        print("Usage: python build_latex_files.py <files_labels.csv> <temes.csv> <label_to_include>")
        sys.exit(1)

    files_labels_csv = sys.argv[1]
    themes_csv = sys.argv[2]
    label_to_include = sys.argv[3]
    
    output_file = f"{label_to_include}_organized.tex"
    
    main(files_labels_csv, themes_csv, label_to_include, output_file)
