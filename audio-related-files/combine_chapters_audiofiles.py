import os
import argparse
from pydub import AudioSegment

def get_chapter_number(filename):
    # Extract chapter number from filename like "Chapter-1-Introduction.mp3"
    if filename.startswith("Chapter-") and filename.endswith(".mp3"):
        parts = filename.split("-")
        if len(parts) >= 3:
            try:
                return int(parts[1])
            except ValueError:
                pass
    return float('inf')  # Put invalid files at the end

def main():
    parser = argparse.ArgumentParser(description="Combine MP3 chapter files in order.")
    parser.add_argument("-i", "--input_folder", required=True, help="Path to the folder containing MP3 files")
    args = parser.parse_args()

    folder_path = args.input_folder
    if not os.path.isdir(folder_path):
        print(f"Error: '{folder_path}' is not a valid directory.")
        return

    # Get all MP3 files
    mp3_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".mp3")]

    # Sort by chapter number
    sorted_mp3_files = sorted(mp3_files, key=get_chapter_number)

    if not sorted_mp3_files:
        print("No MP3 files found in the folder.")
        return

    # Combine audio
    combined_audio = AudioSegment.empty()
    for filename in sorted_mp3_files:
        file_path = os.path.join(folder_path, filename)
        audio_segment = AudioSegment.from_mp3(file_path)
        combined_audio += audio_segment
        print(f"Added: {filename}")

    # Save the combined file
    output_file = os.path.join(folder_path, "combined_chapters.mp3")
    combined_audio.export(output_file, format="mp3")
    print(f"\nCombined MP3 saved to: {output_file}")

if __name__ == "__main__":
    main()