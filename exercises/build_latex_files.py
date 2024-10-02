import csv
import os
import sys

def read_files_labels(csv_file):
    """Read the CSV file containing filenames and labels."""
    files_labels = []
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header if there is one
        for row in reader:
            filename = row[0].strip()
            labels = [label.strip() for label in row[1].split(',')]
            files_labels.append((filename, labels))
    return files_labels

def read_themes(csv_file):
    """Read the themes CSV file and return a structured dictionary."""
    themes = []
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header if there is one
        for row in reader:
            theme_name = row[0].strip()
            parent_theme = row[1].strip() if row[1].strip() != '' else None  # Allow for top-level themes
            hierarchy = int(row[2].strip())  # Hierarchy is assumed to be an integer
            themes.append({'theme_name': theme_name, 'parent_theme': parent_theme, 'hierarchy': hierarchy})
    return themes

def build_theme_hierarchy(themes):
    """Build a nested structure of themes using the parent-child relationship."""
    theme_dict = {theme['theme_name']: theme for theme in themes}
    hierarchy_tree = []

    # Link children to their parents
    for theme in themes:
        if theme['parent_theme']:
            parent = theme_dict.get(theme['parent_theme'])
            if 'children' not in parent:
                parent['children'] = []
            parent['children'].append(theme)
        else:
            hierarchy_tree.append(theme)

    return hierarchy_tree

def generate_latex_for_themes(theme, files_labels, label_to_include, hierarchy_level=1):
    """Recursively generate LaTeX content for the themes and their hierarchy."""
    latex_content = []
    section_command = ["\\section", "\\subsection", "\\subsubsection", "\\paragraph", "\\subparagraph"]

    # Add the section heading based on the hierarchy level
    if hierarchy_level <= len(section_command):
        latex_content.append(f"{section_command[hierarchy_level - 1]}{{{theme['theme_name']}}}")

    # Add exercises related to the label for this theme
    for filename, labels in files_labels:
        if label_to_include in labels:
            latex_content.append(f"\\input{{{filename}}}")

    # Recurse for children themes (if any)
    if 'children' in theme:
        for child_theme in sorted(theme['children'], key=lambda t: t['hierarchy']):
            latex_content.extend(generate_latex_for_themes(child_theme, files_labels, label_to_include, hierarchy_level + 1))

    return latex_content

def save_latex_file(latex_content, output_file):
    """Save the LaTeX content to a file."""
    with open(output_file, 'w') as f:
        f.write("\n".join(latex_content))

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
        print("Usage: python script.py <files_labels.csv> <temes.csv> <label_to_include>")
        sys.exit(1)

    files_labels_csv = sys.argv[1]
    themes_csv = sys.argv[2]
    label_to_include = sys.argv[3]
    
    output_file = f"{label_to_include}_organized.tex"
    
    main(files_labels_csv, themes_csv, label_to_include, output_file)
