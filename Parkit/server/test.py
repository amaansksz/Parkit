import cv2
import pytesseract
import time
import re

# Path to Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

def recognize_plate():
    # Load the trained Haar cascade classifier for license plate detection
    plate_cascade = cv2.CascadeClassifier("C:\\Users\\amaan\\OneDrive\\Desktop\\Parkit-master\\Parkit-master\\server\\plate_recog.xml")

    # Initialize video capture from mobile phone screen
    cap = cv2.VideoCapture(0)

    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera")
        return None

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Check if the frame was read successfully
        if not ret:
            print("Error: Could not read frame")
            continue

        # Resize frame to a smaller resolution
        frame = cv2.resize(frame, (640, 480))

        # Draw a frame for the user to place the license plate
        cv2.rectangle(frame, (100, 100), (540, 360), (0, 255, 0), 2)

        # Convert frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Denoise using Gaussian blur
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Perform adaptive thresholding
        thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

        # Detect potential license plate regions using the Haar cascade
        plates = plate_cascade.detectMultiScale(thresh, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Iterate over potential license plate regions
        for (x, y, w, h) in plates:
            if 100 < x < 440 and 100 < y < 380:  # Check if the license plate is placed inside the frame
                roi = frame[y:y + h, x:x + w]  # Region of interest containing potential license plate
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Draw rectangle around the region

                # Preprocess the ROI for OCR
                roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

                # Perform OCR using Tesseract on the region of interest
                plate_text = pytesseract.image_to_string(roi_gray, config='--psm 7')

                # Display the captured characters on the frame
                cv2.putText(frame, f"Plate Text: {plate_text}", (x, y - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

                # Check if the recognized text matches the expected format for Indian license plates
                cleaned_plate_number = clean_text(plate_text)
                if re.match(r'^[A-Z]{2}\d{2}[A-Z]{2}\d{4}$', cleaned_plate_number):
                    print("License Plate Number:", cleaned_plate_number)
                    cap.release()
                    cv2.destroyAllWindows()
                    return  # Stop running the program after printing the license plate number

        # Display the processed frame
        cv2.imshow('Frame', frame)

        # Check for 'q' key to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the capture
    cap.release()
    cv2.destroyAllWindows()

def clean_text(text):
    # Perform post-processing operations to clean and format the text
    # Example: Removing special characters, correcting errors, etc.
    
    # Strip leading and trailing whitespace
    cleaned_text = text.strip()
    
    # Remove non-alphanumeric characters
    cleaned_text = re.sub(r'[^a-zA-Z0-9]', '', cleaned_text)
    
    # Convert to uppercase (assuming license plate characters are typically uppercase)
    cleaned_text = cleaned_text.upper()
    
    # Keep only the first 10 characters
    cleaned_text = cleaned_text[:10]
    
    return cleaned_text

# Example usage:
recognize_plate()
