@echo off
echo Installing dependencies...
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install transformers datasets accelerate flask webview sentence-transformers scikit-learn numpy

echo Starting training...
python train_model.py

echo Training completed! Starting the app...
python app.py