import subprocess

def MDtoPDF(inputMD, outputPDF):
    """
    Converts a Markdown file to a PDF using pandoc.
    
    :param input_md: Path to the input Markdown file.
    :param output_pdf: Desired path for the output PDF file.
    """
    # Build the pandoc command
    command = ["pandoc", inputMD, "-o", outputPDF]

    try:
        # Run the command and check for errors
        subprocess.run(command, check=True)
        print(f"Successfully converted '{inputMD}' to pdf")
    except subprocess.CalledProcessError as e:
        print("An error occurred during conversion:")
        print(e)
