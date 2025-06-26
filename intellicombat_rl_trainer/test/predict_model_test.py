import numpy as np
from tensorflow.keras.models import load_model

model = load_model("../model/intellicombat_model.keras")

state = np.array([[50, 30, 0, 60, 40, 0]], dtype=np.float32)
pred = model.predict(state)
print("Index prediction:", np.argmax(pred))
