# 🛡️ DeepGuard — Deepfake Detection System

DeepGuard is an AI-powered deepfake detection system that analyzes facial images and classifies them as **Real** or **Potential Deepfake**.

The project uses a **MobileNetV2 transfer-learning model** trained with TensorFlow and provides an interactive web interface built with **Streamlit**.

> ⚠️ **Note:** This system is an academic/project prototype. Its prediction should be treated as an assistive screening result, not definitive proof of image authenticity.

---

## ✨ Features

- 🖼️ Upload JPG, JPEG, and PNG images
- 🧠 Deepfake classification using MobileNetV2
- 📊 Confidence score and prediction probability
- 🎨 Modern dark/glassmorphism Streamlit interface
- ⚡ Fast image inference
- 📱 Responsive web interface
- 🔍 Real vs. potentially manipulated image detection

---

## 🧠 Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| TensorFlow / Keras | Deep learning framework |
| MobileNetV2 | Image feature extraction and classification |
| NumPy | Numerical processing |
| Pillow | Image processing |
| Streamlit | Web application |
| Git & GitHub | Version control |

---

## 🔬 How It Works

The system follows this pipeline:

```text
User Uploads Image
        ↓
Image Preprocessing
        ↓
Resize to 224 × 224
        ↓
MobileNetV2 Feature Extraction
        ↓
Global Average Pooling
        ↓
Dense Classification Layer
        ↓
Sigmoid Prediction
        ↓
Real / Potential Deepfake
```

### Model

The model is based on **MobileNetV2**, a lightweight convolutional neural network architecture commonly used for image classification and transfer learning.

The pretrained ImageNet weights are used as the feature extractor, followed by custom classification layers for binary classification.

---

## 📂 Project Structure

```text
DeepFake-Detection-System/
│
├── app.py
├── deepfake_detector.keras
├── requirements.txt
├── README.md
└── .gitignore
```

### File Description

- `app.py` — Streamlit web application
- `deepfake_detector.keras` — Trained TensorFlow/Keras model
- `requirements.txt` — Python dependencies
- `.gitignore` — Files excluded from version control
- `README.md` — Project documentation

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/DeepFake-Detection-System.git
cd DeepFake-Detection-System
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

On macOS/Linux:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🚀 Run the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your browser at:

```text
http://localhost:8501
```
Check the application live at [Link](https://deepgaurd-deepfake-detection-system.streamlit.app/)
---

## 🖼️ Using the Application

1. Open the DeepGuard web application.
2. Upload a facial image in JPG, JPEG, or PNG format.
3. The image is resized to `224 × 224`.
4. The trained MobileNetV2 model analyzes the image.
5. The application displays:
   - Prediction
   - Confidence score
   - Real probability
   - Deepfake probability

---

## 📊 Model Training

The model was trained in **Google Colab** using a labeled deepfake facial-image dataset containing two classes:

```text
fake/
real/
```

The dataset was divided into:

- **80% training data**
- **20% validation data**

Transfer learning was used with MobileNetV2 to reduce training time and computational requirements.

### Input

```text
224 × 224 × 3
```

### Output

A sigmoid probability representing the model's estimated probability for the **Real** class.

---

## 📈 Model Evaluation

The model should be evaluated using more than accuracy alone.

Recommended metrics:

- Accuracy
- Precision
- Recall
- F1-score
- Confusion Matrix

Example:

```text
Accuracy
Precision
Recall
F1-score
```

> Add your final validation metrics here after completing model evaluation.

---

## 🔐 Limitations

Deepfake detection is a challenging computer-vision problem. Performance can vary depending on:

- Image quality
- Compression
- Lighting
- Face orientation
- Deepfake generation method
- Dataset characteristics
- Unseen manipulation techniques

A model trained on a relatively small dataset may not generalize to every type of synthetic media.

Therefore, DeepGuard should be considered a **screening/assistive tool**, rather than a forensic authentication system.

---

## 🔮 Future Improvements

Possible future enhancements include:

- 🎥 Video deepfake detection
- 👤 Automatic face detection and cropping
- 🤖 More advanced architectures such as EfficientNet or Xception
- 🔬 Explainable AI using Grad-CAM
- 📊 Larger and more diverse datasets
- ⚡ Model optimization for faster inference
- ☁️ Cloud deployment
- 🔐 Detection of AI-generated audio and multimedia
- 📱 Mobile-friendly deployment

---

## 🧪 Development Environment

The model training was performed using:

- Google Colab
- TensorFlow / Keras
- GPU acceleration

The web application is implemented using Streamlit.

---

## 👩‍💻 Author

**Simran Kaur**



---

## 📄 License

This project is intended for educational and academic purposes.

If you use external datasets, models, or third-party resources, follow their respective licenses and attribution requirements.

---

## ⭐ Acknowledgements

- TensorFlow / Keras
- MobileNetV2
- Streamlit
- Google Colab
- Dataset contributors
