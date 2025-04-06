from python_model import SimpleCNN, data_transforms, create_dataset
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
import io
import os
import torch
app = FastAPI()

# --- Load Model ---
# Define the path to your model state dictionary
MODEL_PATH = "person_name_model.pth"  # Or wherever you saved it

# Check if the model file exists
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file not found at: {MODEL_PATH}.  Make sure you have trained and saved the model.")

# Load the dataset to access name_to_index and num_classes for model initialization.
data_dir = 'data'
_, _, _, num_classes, name_to_index = create_dataset(data_dir, transform=data_transforms)

# Initialize the model
model = SimpleCNN(num_classes=num_classes)

# Load the state dictionary
model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device('cpu')))  # Load to CPU initially
model.eval()  # Set to evaluation mode
print("Model loaded successfully.")

# Move model to GPU if available
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model.to(device)


# --- Prediction Endpoint ---
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    Endpoint to predict the person's name from an image.

    Args:
        file: UploadFile - The image file to process.

    Returns:
        JSONResponse: A JSON response containing the predicted person's name and confidence score.
    """
    try:
        # 1. Image Processing
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB") # Convert to RGB to handle potential Grayscale/RGBA
        transform = data_transforms['val']  # Use the validation transform (no augmentation)
        image = transform(image).unsqueeze(0).to(device)  # Add batch dimension and move to device

        # 2. Model Prediction
        with torch.no_grad():
            outputs = model(image)
            probabilities = torch.exp(outputs)  # Convert from LogSoftmax to probabilities
            predicted_probability, predicted_idx = torch.max(probabilities, 1)  # Get the max probability and index
            predicted_idx = predicted_idx.item()  # Get the integer index
            confidence_score = predicted_probability.item()  # Get the confidence score (probability)

        # 3. Result Mapping and Response
        # Create a reverse mapping from index to name
        index_to_name = {v: k for k, v in name_to_index.items()}
        predicted_name = index_to_name.get(predicted_idx, "Unknown")  # Use .get() for safety

        return JSONResponse(content={"predicted_name": predicted_name, "confidence_score": confidence_score})

    except Exception as e:
        print(f"Error occurred during prediction: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# --- Health Check Endpoint (Optional) ---
@app.get("/health")
async def health_check():
    """
    Endpoint for a health check to verify the API is running.
    """
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
