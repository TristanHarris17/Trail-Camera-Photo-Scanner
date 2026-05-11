from ultralytics import YOLO

def main():
    print("Downloading YOLOv8n model...")
    # This will download yolov8n.pt to the current directory if it doesn't exist
    model = YOLO("yolov8n.pt")
    print("Model downloaded successfully. You can now use the scanner offline.")

if __name__ == "__main__":
    main()
