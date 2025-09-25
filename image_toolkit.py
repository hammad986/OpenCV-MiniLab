"""
image_toolkit.py
A consolidated, menu-driven OpenCV project script for:
 - image drawing (line / circle / rectangle / text)
 - image operations (grayscale / edge / face-detect)
 - video capture & save from webcam/device

Usage:
    python image_toolkit.py

Dependencies:
    pip install opencv-python

Author: <Your Name>
"""

import cv2
import os
import sys

HAAR_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"

def safe_input(prompt):
    try:
        return input(prompt)
    except EOFError:
        return ""

def read_image(path):
    if not os.path.exists(path):
        print("File not found:", path)
        return None
    img = cv2.imread(path)
    if img is None:
        print("cv2 failed to read the file (maybe unsupported format).")
    return img

def ask_color():
    s = safe_input("Enter color as b,g,r (e.g. 255,0,0): ").strip()
    try:
        vals = tuple(map(int, s.split(",")))
        if len(vals) != 3:
            raise ValueError
        return vals
    except:
        print("Invalid color, using default (0,255,0).")
        return (0,255,0)

def ask_point(prompt):
    s = safe_input(prompt).strip()
    try:
        x,y = tuple(map(int, s.split(",")))
        return (x,y)
    except:
        print("Invalid point. Using (10,10).")
        return (10,10)

def save_image(img):
    save_img = input("DO you want to save the image (yes/no): ")
    if save_img == "yes":
        name = safe_input("Enter filename to save (with extension, e.g. out.jpg): ").strip()
        if not name:
            print("No name given. Skipping save.")
            return
        if os.path.exists(name):
            over = safe_input(f"'{name}' exists. Overwrite? (y/n): ").strip().lower()
            if over != "y":
                print("Not saved.")
                return
        ok = cv2.imwrite(name, img)
        if ok:
            print("Saved as:", name)
        else:
            print("Failed to save image.")
    else:
        return


def draw_line(img):
    pt1 = ask_point("Enter pt1 (x,y): ")
    pt2 = ask_point("Enter pt2 (x,y): ")
    color = ask_color()
    try:
        thickness = int(safe_input("Enter thickness (e.g. 2): "))
    except:
        thickness = 2
    out = img.copy()
    cv2.line(out, pt1, pt2, color, thickness)
    cv2.imshow("Line", out); cv2.waitKey(0); cv2.destroyAllWindows()
    save_image(out)

def draw_circle(img):
    center = ask_point("Enter center (x,y): ")
    try:
        radius = int(safe_input("Enter radius (e.g. 50): "))
    except:
        radius = 50
    color = ask_color()
    try:
        thickness = int(safe_input("Enter thickness (-1 for fill): "))
    except:
        thickness = 2
    out = img.copy()
    cv2.circle(out, center, radius, color, thickness)
    cv2.imshow("Circle", out); cv2.waitKey(0); cv2.destroyAllWindows()
    save_image(out)

def draw_rectangle(img):
    pt1 = ask_point("Enter pt1 (x,y): ")
    pt2 = ask_point("Enter pt2 (x,y): ")
    color = ask_color()
    try:
        thickness = int(safe_input("Enter thickness (-1 for fill): "))
    except:
        thickness = 2
    out = img.copy()
    cv2.rectangle(out, pt1, pt2, color, thickness)
    cv2.imshow("Rectangle", out); cv2.waitKey(0); cv2.destroyAllWindows()
    save_image(out)

def draw_text(img):
    text = safe_input("Enter text: ")
    org = ask_point("Enter origin (x,y) for text: ")
    try:
        font_scale = float(safe_input("Enter font scale (e.g. 1.0): "))
    except:
        font_scale = 1.0
    color = ask_color()
    try:
        thickness = int(safe_input("Enter thickness: "))
    except:
        thickness = 2
    out = img.copy()
    cv2.putText(out, text, org, cv2.FONT_HERSHEY_COMPLEX, font_scale, color, thickness)
    cv2.imshow("Text", out); cv2.waitKey(0); cv2.destroyAllWindows()
    save_image(out)

def do_grayscale(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow("Grayscale", gray); cv2.waitKey(0); cv2.destroyAllWindows()
    save_image(gray)

def do_edge(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    try:
        th1 = int(safe_input("Enter lower threshold for Canny (e.g. 50): "))
        th2 = int(safe_input("Enter upper threshold for Canny (e.g. 150): "))
    except:
        th1, th2 = 50, 150
    edges = cv2.Canny(gray, th1, th2)
    cv2.imshow("Edges", edges); cv2.waitKey(0); cv2.destroyAllWindows()
    save_image(edges)

def do_face_detect(img):
    if not os.path.exists(HAAR_PATH):
        print("Haar cascade not found. Skipping face detection.")
        return
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(HAAR_PATH)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    out = img.copy()
    for (x,y,w,h) in faces:
        cv2.rectangle(out, (x,y), (x+w, y+h), (0,255,0), 2)
    print(f"Faces found: {len(faces)}")
    cv2.imshow("Faces", out); cv2.waitKey(0); cv2.destroyAllWindows()
    save_image(out)

def image_menu():
    path = safe_input("Enter image path: ").strip()
    img = read_image(path)
    if img is None:
        return
    while True:
        print("\nImage operations:")
        print(" 1) draw line")
        print(" 2) draw circle")
        print(" 3) draw rectangle")
        print(" 4) draw text")
        print(" 5) grayscale")
        print(" 6) edge detection (Canny)")
        print(" 7) face detection")
        print(" 0) back to main menu")
        choice = safe_input("Choose (0-7): ").strip()
        if choice == "1": draw_line(img)
        elif choice == "2": draw_circle(img)
        elif choice == "3": draw_rectangle(img)
        elif choice == "4": draw_text(img)
        elif choice == "5": do_grayscale(img)
        elif choice == "6": do_edge(img)
        elif choice == "7": do_face_detect(img)
        elif choice == "0": break
        else:
            print("Invalid choice.")

def video_capture_menu():
    try:
        cam = int(safe_input("Enter device index (0 for webcam): "))
    except:
        cam = 0
    cap = cv2.VideoCapture(cam)
    if not cap.isOpened():
        print("Cannot open video device.")
        return
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) or 640
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) or 480
    fps = 20
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    name = safe_input("Enter filename to save (without extension): ").strip() or "output"
    filename = name + ".avi"
    out = cv2.VideoWriter(filename, fourcc, fps, (w,h))
    print("Recording... Press 'q' in the window to stop.")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Frame grab failed, stopping.")
            break
        out.write(frame)
        cv2.imshow("Recording", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release(); out.release(); cv2.destroyAllWindows()
    print("Saved video:", filename)

def main_menu():
    while True:
        print("\n=== Image Toolkit ===")
        print("1) Image operations (draw / grayscale / edge / face)")
        print("2) Video capture from device")
        print("0) Exit")
        choice = safe_input("Choose option: ").strip()
        if choice == "1":
            image_menu()
        elif choice == "2":
            video_capture_menu()
        elif choice == "0":
            print("Goodbye.")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main_menu()
