# Cartoonify Image (OpenCV + Flask)

Photo ko cartoon me convert karne wala tool. Web app (upload/download) aur CLI dono.

## Features
- 2 styles: Classic (smooth + bold edges) aur Painted (K-Means color reduction)
- Adjustable number of colors
- Upload validation (type + 5 MB limit), error handling
- Deploy-ready (Render / Railway)

## Tech Stack
Python, OpenCV, NumPy, Flask, HTML/CSS, Gunicorn

## Run locally
```
python -m pip install -r requirements.txt
python app.py            # http://localhost:5000
```
CLI:
```
python cartoonify.py photo.jpg -o cartoon.jpg -s painted -k 8
```

## Deploy on Render
Build: `pip install -r requirements.txt` | Start: `gunicorn app:app`

## How it works (algorithm)
1. **Edges:** BGR -> Gray -> Median Blur (noise hatao) -> Adaptive Threshold (black lines)
2. **Colors:** Bilateral Filter (colors smooth, edges sharp)
3. **Painted style:** K-Means se colors ko k tak reduce
4. **Combine:** `bitwise_and(color, color, mask=edges)` -> edges ke saath cartoon

## Resume bullet
Developed an image cartoonification tool using OpenCV (adaptive thresholding, bilateral
filtering, K-Means color quantization) with a Flask web interface for upload and download.

## Viva Q&A
- **Cartoon effect kaise banta hai?** Bold edges + flat/smooth colors ko combine karke.
- **Median blur kyu?** Noise hatane ke liye, taaki edges clean aayein.
- **Adaptive threshold kyu, normal nahi?** Har region ki lighting alag hoti hai; adaptive local threshold use karta hai, isliye uneven light me bhi edges aate hain.
- **Bilateral filter kyu, Gaussian nahi?** Gaussian edges bhi blur kar deta hai; bilateral sirf similar colors ko smooth karta hai, edges bachi rehti hain.
- **K-Means ka role?** Pixels ko k clusters me baantke har pixel ko cluster center ka color dena, isse painted look aata hai.
- **bitwise_and kyu?** Edge mask ke black pixels color image ko black kar dete hain, yaani lines ban jaati hain.
- **OpenCV me color order?** BGR, RGB nahi.
- **Limitation?** Bahut dark/noisy photos me edges kharab aate hain; deep-learning (CartoonGAN) behtar result deta hai (future scope).
