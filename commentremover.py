def remove_comments(input_file, output_file):
    try:
        with open(input_file, "r") as file:
            lines = file.readlines()

        with open(output_file, "w") as file:
            for line in lines:
                # Check if the line contains a comment character #
                index = line.find("#")
                if index != -1:
                    # Remove the comment part
                    line = line[:index]

                # Write the modified line to the output file
                file.write(line)

        print("Clean file saved as", output_file)

    except FileNotFoundError:
        print(f'Error reading file: "{input_file}"')


def main():
    # Get input and output file names from the user
    input_file_name = input("File to read: ")
    output_file_name = input("File to save: ")

    remove_comments(input_file_name, output_file_name)


if __name__ == "__main__":
    main()
