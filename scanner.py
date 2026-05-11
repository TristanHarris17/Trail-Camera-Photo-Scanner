import os
import sys
import shutil
from pathlib import Path
try:
    import tkinter as tk
    from tkinter import filedialog
    TK_AVAILABLE = True
except ImportError:
    TK_AVAILABLE = False

from ultralytics import YOLO

# COCO Dataset Classes we care about
# People: 0
# Vehicles: 2 (car), 3 (motorcycle), 5 (bus), 7 (truck)
# Animals: 14 (bird), 15 (cat), 16 (dog), 17 (horse), 18 (sheep), 
#          19 (cow), 20 (elephant), 21 (bear), 22 (zebra), 23 (giraffe)
TARGET_CLASSES = [0, 2, 3, 5, 7, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
CONFIDENCE_THRESHOLD = 0.40 # Adjust if getting too many false positives or missing things

def get_directory():
    """Opens a UI dialog to select a directory, or falls back to terminal input."""
    if TK_AVAILABLE:
        print("Opening folder selection dialog...")
        root = tk.Tk()
        root.withdraw() # Hide the main window
        root.attributes('-topmost', True)
        folder_path = filedialog.askdirectory(title="Select folder with trail camera photos")
        return folder_path
    else:
        print("Graphical interface not available.")
        folder_path = input("Please enter the full path to the folder with trail camera photos: ").strip()
        return folder_path

def is_image_file(filename):
    """Check if a file is a supported image type."""
    ext = filename.lower()
    return ext.endswith(('.jpg', '.jpeg', '.png'))

def scan_directory():
    if len(sys.argv) > 1:
        input_dir = sys.argv[1]
    else:
        input_dir = get_directory()
        
    if not input_dir:
        print("No directory selected. Exiting.")
        sys.exit(0)
        
    input_path = Path(input_dir)
    if not input_path.exists() or not input_path.is_dir():
        print(f"Error: {input_dir} is not a valid directory.")
        sys.exit(1)
        
    output_dir = input_path / "Matches_Copied"
    
    # Get all image files
    image_files = [f for f in input_path.iterdir() if f.is_file() and is_image_file(f.name)]
    
    if not image_files:
        print(f"No .jpg or .png image files found in {input_dir}.")
        sys.exit(0)
        
    print(f"Found {len(image_files)} image files. Starting scan...")
    
    # Create output directory if it doesn't exist
    if not output_dir.exists():
        output_dir.mkdir()
        print(f"Created output folder: {output_dir}")
    else:
        print(f"Using existing output folder: {output_dir}")

    # Load YOLOv8 model
    print("Loading AI model...")
    try:
        model = YOLO("yolov8n.pt")
    except Exception as e:
        print(f"Failed to load the model. Ensure you have internet on first run or ran download_model.py previously.\nError: {e}")
        sys.exit(1)

    matched_count = 0
    error_count = 0
    
    for i, file_path in enumerate(image_files, 1):
        try:
            print(f"[{i}/{len(image_files)}] Scanning: {file_path.name} ... ", end="", flush=True)
            
            # Run inference
            # verbose=False keeps the console clean from YOLO's internal logging
            results = model.predict(source=str(file_path), conf=CONFIDENCE_THRESHOLD, verbose=False)
            
            match_found = False
            for result in results:
                # result.boxes.cls contains the class IDs detected
                if result.boxes is not None:
                    detected_classes = result.boxes.cls.cpu().numpy()
                    
                    for cls_id in detected_classes:
                        if int(cls_id) in TARGET_CLASSES:
                            match_found = True
                            break
                            
                if match_found:
                    break
                    
            if match_found:
                print("FOUND TARGET! Copying file.")
                dest_path = output_dir / file_path.name
                shutil.copy2(file_path, dest_path)
                matched_count += 1
            else:
                print("Clear.")
                
        except Exception as e:
            print(f"Error processing file: {e}")
            error_count += 1
            
    print("\n--- Scan Complete ---")
    print(f"Total scanned: {len(image_files)}")
    print(f"Total matched (copied): {matched_count}")
    if error_count > 0:
        print(f"Files with errors: {error_count}")
    print(f"Matches saved to: {output_dir}")

if __name__ == "__main__":
    scan_directory()
