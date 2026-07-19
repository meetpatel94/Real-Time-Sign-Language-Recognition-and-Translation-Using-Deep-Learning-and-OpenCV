from database.history_db import save_prediction

save_prediction(

    gesture="Hello",

    confidence=98.76,

    processing_time=21.3

)

print("Prediction Saved Successfully")