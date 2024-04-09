def functions_without_comments(files):
    for file_name in files:
        file_name = file_name.strip()
        try:
            with open(file_name, "r") as file:  # reads file
                lines = file.readlines()  # reads all lines and stores in a list
                function_name = None
                comment_found = False
                for line_num, line in enumerate(lines):  # iterates while keeping count of line number
                    if line.strip().startswith("#"):  # identifies comment after def
                        function_name = None  # set to none so it searching for other def with #
                        comment_found = True
                    elif line.startswith("def "):
                        function_name = line.split("def ")[1].split("(")[0]
                        if not comment_found:
                            print(
                                f"File: {file_name} contains a function [{function_name}()] on line [{line_num + 1}]"
                                " without a preceding comment."
                            )
                        comment_found = False
                        function_name = None
                        # split[1] grabs function name, split('(')[0] splits () grabbing only the name and removing
                        # anything after
        except FileNotFoundError:
            print(f"Error reading file: {file_name}")


def main():
    file_name = input("Enter: ")
    files = file_name.split(",")
    functions_without_comments(files)


if __name__ == "__main__":
    main()
