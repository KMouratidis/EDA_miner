# This module is responsible for creating the docs. Read through
# the comments to understand the flow. If you have a better
# implementation, or questions, just ask.

import os

# The text is a list of lines / strings that comprise the
# auto-generated docs file (at the final stage these will
# be concatenated).
text = []

# The text implementation might change later, so the handler
# defined here is to make any other changes easier
handler = text.append

# Since the docs are made with dash, we need to import the
# necessary dependencies. Note that each file in the project
# is represented as a key-value pair in the `layouts` dict.
handler("""
# THIS IS AN AUTO-GENERATED FILE. IT IS NEITHER MEANT TO BE READ NOR
# TO BE WRITTEN / MODIFIED. REFER TO `doc_maker.py` FOR SPECIFICS.

import dash
import dash_core_components as dcc
import dash_html_components as html

layouts = {}

""")

# Count the total number of functions/classes
# Useful for counting doc-coverage.
total_funcs_classes = 0
# Same bur for documented functions/classes
documented_funcs_classes = 0


# This function removes instances of "class" and "def". We swap the
# word subclass to a temporary token because it is sometimes found
# in comments
def cleaning(string):
    return (string.replace("subclass", "==TEMP==")
                  .replace("class ", "")
                  .replace("==TEMP==", "subclass")
                  .replace("def ", "").strip())


# This function whether a line defines a class or function.
def is_declaration(line):
    # Remove whitespace so that we correctly get the start of line
    line = line.strip()

    return ("def " in line) or ("class " in line)


# This function whether a line defines a PRIVATE class or function.
def is_private_or_comment(line):
    # Remove whitespace so that we correctly get the start of line
    line = line.strip()

    return (line.startswith("def _") or
            line.startswith("class _") or
            line.startswith("#"))


# Ignore some files and folders. Some (e.g. reportapp) are only
# in the private version (aka untested / underdeveloped / paused),
# some are sensitive files (user database, environment variables),
# some are temporary files, caches, etc. Ignore the flask app
# because the views don't really need documentation
ignore_files = ["reportapp", "printable_layout", "users.db",
                "coverage", "cache", "base_dash.py", "temp_",
                "flask_app", "config", ".env", "devops"]

# Same, but for whole folders. This folder and the templates folder
# don't really need to be in the docs.
ignore_folders = ["templates", "docs"]

# the EDA_miner/EDA_miner folder
grand_parent_folder = os.path.dirname(os.path.dirname(__file__))

for folder, folders, files in os.walk(grand_parent_folder):

    # Ignore specified folders
    if any(x in folder for x in ignore_folders):
        continue

    for file in files:

        # Ignore specified files (above) and non-python files
        if any(x in file for x in ignore_files) or (not file.endswith(".py")):
            continue

        # Read the file's lines
        file_path = os.path.join(folder, file)
        with open(file_path) as f:
            rd = f.readlines()

        # indicator: whether the line is within a docstring or not
        open_docstring = False
        # indicator: whether to add the line together with the previous
        #            in the same docstring
        add_to_next = False
        # accumulator: Docstring parts that span multiple lines are
        #              expected to end with a "\". This accumulator
        #              is the concatenation of those into 1 string.
        prev_line = ""

        # Add a new line to the document, for the file we are currently parsing
        # It is a Dash Div element which will contain the docstrings
        handler(f"""\n\nlayouts["{file_path[:-3]}"] = html.Div([""")

        for i, line in enumerate(rd):

            # If func/class and not private
            if (is_declaration(line) and
                (not is_private_or_comment(line)) and
                 not open_docstring):

                # Increase the total number of functions/classes.
                total_funcs_classes += 1

            # If the like has triple quotes...
            if '"""' in line:
                # we toggle the `open_docstring`
                open_docstring = not open_docstring

                # If i == 0 then we are dealing with a module-level docstring
                if i == 0 and open_docstring:
                    # If the file is an __init__.py file, then change the name
                    file = file.replace("__init__.py", folder.split("/")[-1])
                    # Add the file name as the first element of the Div
                    # NOTE THE COMMA! These elements items within a list
                    handler(f'html.H2("""{file}""", className="filename"), ')

                    # We need to open a new div, containing ........
                    handler('html.Div([')

                # If i >=1 then we are (probably) dealing with a
                # function or class
                elif i >= 1 and open_docstring:

                    # Since the line we are currently at is the line containing
                    # the END triple quotes, we need to go to the previous
                    # line(s) in search for the def/class declaration.
                    correct_line = i
                    # Move up the lines until you find the declaration
                    # Ignore (for now) the edge-case that the declaration
                    # is not found
                    while not is_declaration(rd[correct_line]):
                        correct_line -= 1

                    # Increase the number of documented functions/classes.
                    documented_funcs_classes += 1

                    # Since the current line is the END triple quotes and
                    # the START/END triple quotes are on their own lines
                    # Then the correct line must have at least a distance
                    # of 2 (empty docstring) or more (2+x for x lines)
                    # from the current line
                    if correct_line < i - 1:
                        # Join the lines of the docstring
                        docstring = " ".join(rd[j].strip()
                                             for j in range(correct_line, i))

                    # The line with the declaration is the one containing the
                    # name of the function/class. Add it after cleaning it.
                    handler(f'html.Br(), '
                            f'html.H3("""{cleaning(rd[correct_line])} """, '
                            f'className="docstring-contents"), ')

                    # We need to open a new div, containing ........
                    handler('html.Div([')

                # The docstring ended, so close the Div
                elif i >= 1 and not open_docstring:
                    # handler(line)
                    handler('], className="func_docstring"),\n')

            # The contents of the docstring
            elif open_docstring:

                # skip empty lines
                if len(line.strip()) == 0:
                    continue

                # Lines in the docstrings end with a "\" to indicate
                # line continuation. Add line to the accumulator. The
                # "\" indicates that we also need to add the next line.
                if line.strip().endswith("\\"):
                    line = line.rstrip()[:-1]
                    add_to_next = True
                    prev_line = prev_line + line.strip()
                    continue

                # These are the sections, e.g.: "Args:"
                elif line.strip().endswith(":"):
                    line = f'{line.strip()}, '
                    className = "section"

                # These are the parameters, e.g.: "- n_clicks: blah"
                elif line.strip().startswith("-"):
                    line = f'{line.strip()[1:]}, '
                    className = "funcParam"

                # Add the "next" line from the previous run because there
                # was a continuation mark.
                elif add_to_next:
                    line = prev_line + line
                    className = "funcParam"

                # Last line in the list of args
                else:
                    className = "funcParam"
                    line = prev_line + line.strip()

                # Add the (indented) line to the file
                # Also add a space to avoid weird behaviors like
                # closing quotes and escaping characters
                handler(f'    html.P("""{line.strip()[:-1]} """, '
                        f'className="{className}"),')

                # When we reach a line that doesn't end with a "\",
                # end the block and reset the accumulator.
                if not line.strip().endswith("\\"):
                    prev_line = ""
                    add_to_next = False

        # Close the div for the file
        handler("], className='file_container')\n")


# Create/rewrite the layouts file
cur_dir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(cur_dir, "all_layouts.py"), "w") as f:
    f.write("\n".join(text))
