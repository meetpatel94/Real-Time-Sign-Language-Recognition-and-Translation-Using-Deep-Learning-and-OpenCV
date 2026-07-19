from database.db import get_connection


# ==========================================
# Save Prediction
# ==========================================

def save_prediction(
    gesture,
    confidence,
    processing_time,
    image_path="",
    status="Success"
):

    connection = get_connection()

    cursor = connection.cursor()

    query = """
    INSERT INTO prediction_history
    (gesture, confidence, processing_time, image_path, status)
    VALUES (%s,%s,%s,%s,%s)
    """

    values = (
        gesture,
        confidence,
        processing_time,
        image_path,
        status
    )

    cursor.execute(query, values)

    connection.commit()

    cursor.close()

    connection.close()
    
# ==========================================
# Get All Predictions
# ==========================================

def get_predictions():

    connection = get_connection()

    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT *
    FROM prediction_history
    ORDER BY prediction_time DESC
    """

    cursor.execute(query)

    data = cursor.fetchall()

    cursor.close()

    connection.close()

    return data

# ==========================================
# History Statistics
# ==========================================

def get_statistics():

    connection = get_connection()

    cursor = connection.cursor(dictionary=True)

    # Total Predictions
    cursor.execute(
        "SELECT COUNT(*) AS total FROM prediction_history"
    )

    total = cursor.fetchone()["total"]

    # Average Confidence
    cursor.execute(
        "SELECT AVG(confidence) AS average FROM prediction_history"
    )

    average = cursor.fetchone()["average"]

    # Today's Predictions
    cursor.execute("""
        SELECT COUNT(*) AS today
        FROM prediction_history
        WHERE DATE(prediction_time)=CURDATE()
    """)

    today = cursor.fetchone()["today"]

    # Highest Confidence
    cursor.execute("""
        SELECT MAX(confidence) AS highest
        FROM prediction_history
    """)

    highest = cursor.fetchone()["highest"]

    cursor.close()

    connection.close()

    return {

        "total": total,

        "today": today,

        "average": round(average,2) if average else 0,

        "highest": highest if highest else 0

    }