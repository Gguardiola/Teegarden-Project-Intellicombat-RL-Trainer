import tensorflow as tf
import tf2onnx
import datetime

KERAS_MODEL_PATH = "model/intellicombat_model.keras"
ONNX_MODEL_PATH = "model/intellicombat_model_ready_{}.onnx".format(
    datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
)

print(f"Loading model from {KERAS_MODEL_PATH}...")
model = tf.keras.models.load_model(KERAS_MODEL_PATH)

print(f"Conversion to ONNX at {ONNX_MODEL_PATH}...")
onnx_model, _ = tf2onnx.convert.from_keras(
    model, 
    opset=13,
    output_path=ONNX_MODEL_PATH
)

print("Conversion done successfully!")
