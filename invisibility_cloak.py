import argparse
import cv2
import numpy as np

# Preset HSV ranges for common colors (in OpenCV HSV: H:0-179, S:0-255, V:0-255)
COLOR_PRESETS = {
    "red": [
        (np.array([0, 120, 70]),   np.array([10, 255, 255])),  # lower red
        (np.array([170, 120, 70]), np.array([180, 255, 255])), # upper red
    ],
    "blue": [
        (np.array([94, 80, 2]), np.array([126, 255, 255]))
    ],
    "green": [
        (np.array([40, 40, 40]), np.array([80, 255, 255]))
    ],
}


def get_args():
    p = argparse.ArgumentParser(description="OpenCV Invisibility Cloak")
    p.add_argument("--color", default="red", choices=list(COLOR_PRESETS.keys()),
                   help="Target color to turn invisible")
    p.add_argument("--camera-id", type=int, default=0, help="Webcam device index")
    p.add_argument("--blur", type=int, default=5, help="Kernel size for Gaussian blur (odd number)")
    p.add_argument("--erode", type=int, default=1, help="Erosion iterations")
    p.add_argument("--dilate", type=int, default=2, help="Dilation iterations")
    return p.parse_args()


def make_mask(hsv, ranges, blur_k=5, erode_i=1, dilate_i=2):
    # Handle single or dual ranges (red uses two)
    mask = None
    for (lo, hi) in ranges:
        m = cv2.inRange(hsv, lo, hi)
        mask = m if mask is None else cv2.bitwise_or(mask, m)

    if blur_k and blur_k % 2 == 1 and blur_k > 1:
        mask = cv2.GaussianBlur(mask, (blur_k, blur_k), 0)

    kernel = np.ones((3, 3), np.uint8)
    if erode_i > 0:
        mask = cv2.erode(mask, kernel, iterations=erode_i)
    if dilate_i > 0:
        mask = cv2.dilate(mask, kernel, iterations=dilate_i)

    return mask


def main():
    args = get_args()

    if args.color not in COLOR_PRESETS:
        print(f"Unknown color '{args.color}'. Choose from: {list(COLOR_PRESETS.keys())}")
        return

    cap = cv2.VideoCapture(args.camera_id)
    if not cap.isOpened():
        print("[ERROR] Could not open webcam. Try a different --camera-id")
        return

    print("Press 'b' to capture background when frame is empty. Press 'q' to quit.")

    background = None

    while True:
        ok, frame = cap.read()
        if not ok:
            print("[ERROR] Frame grab failed.")
            break

        frame = cv2.flip(frame, 1)  # mirror for a natural webcam feel
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        if background is None:
            display = frame.copy()
            cv2.putText(display, "Press 'b' to capture background", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2, cv2.LINE_AA)
            cv2.imshow("Invisibility Cloak", display)
        else:
            mask = make_mask(hsv, COLOR_PRESETS[args.color], args.blur, args.erode, args.dilate)
            inv_mask = cv2.bitwise_not(mask)

            # Segment the regions
            res_background = cv2.bitwise_and(background, background, mask=mask)
            res_current = cv2.bitwise_and(frame, frame, mask=inv_mask)

            # Final composite
            final = cv2.addWeighted(res_background, 1, res_current, 1, 0)
            cv2.imshow("Invisibility Cloak", final)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('b'):
            # Capture several frames and take a median to reduce noise
            frames = []
            for _ in range(20):
                ok2, f2 = cap.read()
                if not ok2:
                    continue
                f2 = cv2.flip(f2, 1)
                frames.append(f2)
            if frames:
                background = np.median(np.stack(frames, axis=0), axis=0).astype(np.uint8)
                print("[INFO] Background captured.")

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
