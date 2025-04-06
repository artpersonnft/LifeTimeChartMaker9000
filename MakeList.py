import os
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

# --- New Function to Remove Everything After Hyphen ---

def preprocess_remove_hyphen(input_file):
    """Remove everything after a hyphen on each line and save to a temporary file."""
    temp_file = Path(input_file).stem + "_preprocessed.txt"
    print(f"\nPreprocessing {input_file} to remove everything after '-'...")
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Process each line to remove everything after the hyphen
        cleaned_lines = []
        for line in lines:
            cleaned_line = line.split('-')[0].strip()
            if cleaned_line:  # Only keep non-empty lines
                cleaned_lines.append(cleaned_line)
        
        # Write the preprocessed lines to a temporary file
        with open(temp_file, 'w', encoding='utf-8') as f:
            for line in cleaned_lines:
                f.write(line + '\n')
        
        print(f"Preprocessed file saved to {temp_file}.")
        return temp_file
    except Exception as e:
        print(f"Error during preprocessing: {e}")
        return None

# --- Functions from the First Script (Duplicate Removal) ---

def get_file_choice():
    """Prompt the user to select a text file from the current working directory."""
    print("\nAvailable text files in the current directory:")
    files = [f for f in os.listdir() if f.endswith('.txt')]
    if not files:
        print("No .txt files found in the current directory.")
        return None

    for i, file in enumerate(files, 1):
        print(f"{i}: {file}")
    
    while True:
        choice = input(f"\nEnter the number of the file to process (1-{len(files)}) or 0 to exit: ").strip()
        try:
            file_idx = int(choice) - 1
            if choice == "0":
                print("Exiting.")
                return None
            if 0 <= file_idx < len(files):
                return files[file_idx]
            else:
                print(f"Please enter a number between 1 and {len(files)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def process_chunk(chunk, seen_words):
    """Process a chunk of lines, keeping only the first occurrence of each word."""
    unique_chunk = []
    for word in chunk:
        word = word.strip()
        if word and word not in seen_words:
            unique_chunk.append(word)
            seen_words.add(word)
    return unique_chunk

def remove_duplicates(input_file):
    """Remove duplicates from the input file using multithreading, return the output filename."""
    output_file = Path(input_file).stem + "~!.txt"
    seen_words = set()
    unique_words = []
    
    # Read the file in chunks to manage memory for large files
    chunk_size = 10000  # Number of lines per chunk
    chunks = []
    current_chunk = []

    print(f"\nReading {input_file} to remove duplicates...")
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            current_chunk.append(line)
            if len(current_chunk) >= chunk_size:
                chunks.append(current_chunk)
                current_chunk = []
        if current_chunk:  # Don't forget the last chunk
            chunks.append(current_chunk)

    print(f"Processing {len(chunks)} chunks with multithreading to remove duplicates...")
    # Process chunks using ThreadPoolExecutor
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_chunk, chunk, seen_words) for chunk in chunks]
        for future in futures:
            unique_words.extend(future.result())

    # Write the unique words to the output file
    print(f"Writing unique words to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        for word in unique_words:
            f.write(word + '\n')

    print(f"Removed duplicates and saved to {output_file}.")
    print(f"Original file had {len(chunks) * chunk_size + len(current_chunk)} lines.")
    print(f"Output file has {len(unique_words)} unique words.")
    return output_file

# --- Functions from the Second Script (Ticker Extraction and Formatting) ---

def extract_tickers_from_file(input_filename):
    """
    Extracts plain stock tickers from a text file and returns them as a sorted list.
    Assumes tickers are one per line (e.g., VZ, WCC).
    """
    tickers = set()  # Using a set to ensure uniqueness
    try:
        with open(input_filename, 'r') as file:
            for line in file:
                # Strip whitespace and add non-empty lines as tickers
                ticker = line.strip()
                if ticker:  # Ignore empty lines
                    tickers.add(ticker)
    except FileNotFoundError:
        print(f"Error: File '{input_filename}' not found.")
        return []
    except Exception as e:
        print(f"Error reading file: {e}")
        return []
    
    return sorted(list(tickers))  # Return sorted list of unique tickers

def write_ticker_list(tickers, output_filename):
    """
    Writes the list of tickers to a file in Python block format with max 10 items per row.
    Format: tickers = ["TICKER1", "TICKER2", ..., "TICKER10",]
    """
    try:
        with open(output_filename, 'w') as file:
            file.write("tickers = [\n")
            for i in range(0, len(tickers), 10):  # Step by 10 items
                row_tickers = tickers[i:i + 10]  # Get up to 10 tickers for this row
                row = "    "  # Indent with 4 spaces
                for j, ticker in enumerate(row_tickers):
                    row += f'"{ticker}"'
                    if j < len(row_tickers) - 1 or i + 10 < len(tickers):  # Add comma unless it's the last ticker in the last row
                        row += ", "
                    else:
                        row += ","  # Last row, last item gets a comma for consistency
                file.write(row + "\n")
            file.write("]\n")
        print(f"Saved ticker list to: {output_filename}")
    except Exception as e:
        print(f"Error writing to file: {e}")

def process_file_to_ticker_list(input_filename):
    """
    Main function to process the input file and generate the ticker list file.
    First removes everything after hyphens, then removes duplicates, then formats the tickers.
    """
    # Step 1: Preprocess to remove everything after hyphens and save to a temporary file
    preprocessed_file = preprocess_remove_hyphen(input_filename)
    if not preprocessed_file:
        print("Failed to preprocess file. Exiting.")
        return

    # Step 2: Remove duplicates from the preprocessed file and save to another temporary file with ~!
    temp_file = remove_duplicates(preprocessed_file)
    if not temp_file:
        print("Failed to remove duplicates. Exiting.")
        return

    # Step 3: Generate output filename by appending '~1' to the original filename
    base, ext = os.path.splitext(input_filename)
    output_filename = f"{base}~1{ext}"

    # Step 4: Extract tickers from the temporary file and write them to the final file
    tickers = extract_tickers_from_file(temp_file)
    if tickers:
        write_ticker_list(tickers, output_filename)
    else:
        print("No tickers found or error occurred. No output file created.")

    # Step 5: Clean up the temporary files
    try:
        os.remove(preprocessed_file)
        print(f"Cleaned up temporary file: {preprocessed_file}")
        os.remove(temp_file)
        print(f"Cleaned up temporary file: {temp_file}")
    except Exception as e:
        print(f"Error cleaning up temporary files: {e}")

def main():
    """Main function to run the script."""
    print("=== Ticker List Processor with Hyphen Removal and Duplicate Removal ===")
    input_file = get_file_choice()
    if not input_file:
        return

    start_time = time.time()
    process_file_to_ticker_list(input_file)
    end_time = time.time()
    print(f"Total processing took {end_time - start_time:.2f} seconds.")

if __name__ == "__main__":
    main()
