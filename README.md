# OpenCV Invisibility Cloak – Mini Repo

This mini‑repo contains everything you need to run the classic **Harry Potter–style invisibility cloak** demo using OpenCV. It works by capturing a clean background, detecting a target color in the live video (default: **red**), and replacing those pixels with the background—so the cloth appears invisible.

---

## 📁 Files

* `invisibility_cloak.py` – main script (supports color presets + basic CLI flags)
* `requirements.txt` – Python dependencies
* `README.md` – quick start, how it works, troubleshooting

---

## 📄 README.md

````markdown
# Invisibility Cloak (OpenCV)

Make a color cloak “disappear” on camera using background substitution and color masking in HSV space.

git clone (https://github.com/vishal-singh22/OpenCv.git)

## Demo (What it does)
1. Capture a static background frame.
2. Detect a target color (default: red) in the live webcam feed.
3. Replace those color pixels with the background → the cloth looks invisible.

## Requirements
- Python 3.8+
- A webcam (built-in or USB)
- Lighting that is not too dim or flickery

Install deps:
```bash
pip install -r requirements.txt
````

## Usage

Run with defaults (red cloak, camera 0):

```bash
python invisibility_cloak.py
```

Capture background:

* Stand **out of frame** and press **`b`** to capture a clean background.
* Then bring the cloak into view.

Controls:

* **`b`** → capture background
* **`q`** → quit

Optional flags:

```bash
python invisibility_cloak.py --color red --camera-id 0 --blur 5 --erode 1 --dilate 2
```

Supported color presets: `red`, `blue`, `green` (you can tweak HSV in code for others).

## How It Works

* Convert BGR → **HSV** (hue‑saturation‑value) for better color segmentation.
* Create a binary mask for the target color (handles red wrap‑around with two ranges).
* Clean mask using **morphological ops** (erode/dilate) + optional blur.
* Combine foreground (non‑cloak) with background (where mask is true).

## Tips

* Avoid shiny or mixed lighting.
* Use a **solid, bright** cloth for best results.
* For red, avoid skin tones by adjusting lower/upper HSV thresholds if needed.

## Troubleshooting

* **Webcam not opening**: try `--camera-id 1` (external cam) or close other apps using the cam.
* **Mask flickers**: increase blur/dilate; improve lighting; avoid patterned cloth.
* **Wrong color gets masked**: tune HSV ranges in code or switch preset.

## License

MIT

```
```

---

