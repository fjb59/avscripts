from striprtf.striprtf import rtf_to_text

def convert_rtf_to_ascii(input_file, output_file):
    try:
        # Read the RTF file
        with open(input_file, 'r', encoding='utf-8') as rtf_file:
            rtf_content = rtf_file.read()

        # Convert RTF to plain text
        plain_text = rtf_to_text(rtf_content)

        # Save the plain text to an output file
        with open(output_file, 'w', encoding='ascii', errors='ignore') as txt_file:
            txt_file.write(plain_text)

        print(f"Conversion complete. ASCII text saved to {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    input_rtf = "/Users/frank/Downloads/4K Video Downloader+/Interview With The Vampire - Part 1.rtf"  # Change this to your input file path
    output_txt = "/Users/frank/Downloads/4K Video Downloader+/Interview With The Vampire - Part 1.txt"  # Change this to your desired output file path
    convert_rtf_to_ascii(input_rtf, output_txt)
