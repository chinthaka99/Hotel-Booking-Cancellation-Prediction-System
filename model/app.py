from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import pandas as pd

app = Flask(__name__)
CORS(app)

# Load the machine learning model
with open('booking_cancellation_d.pickle', 'rb') as model_file:
    model = pickle.load(model_file)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Parse the JSON request
        data = request.get_json()

        # Extract features from the data
        features = {
            'lead_time': data['lead_time'],
            'arrival_date_month': data['arrival_date_month'],
            'arrival_date_week_number': data['arrival_date_week_number'],
            'arrival_date_day_of_month': data['arrival_date_day_of_month'],
            'stays_in_weekend_nights': data['stays_in_weekend_nights'],
            'stays_in_week_nights': data['stays_in_week_nights'],
            'adults': data['adults'],
            'children': data['children'],
            'babies': data['babies'],
            'is_repeated_guest': data['is_repeated_guest'],
            'previous_cancellations': data['previous_cancellations'],
            'previous_bookings_not_canceled': data['previous_bookings_not_canceled'],
            'agent': data['agent'],
            'adr': data['adr'],
            'required_car_parking_spaces': data['required_car_parking_spaces'],
            'total_of_special_requests': data['total_of_special_requests'],
            'hotel': data['hotel'],
            'meal': data['meal'],
            'market_segment': data['market_segment'],
            'distribution_channel': data['distribution_channel'],
            'reserved_room_type': data['reserved_room_type'],
            'deposit_type': data['deposit_type'],
            'customer_type': data['customer_type']
        }

        # Convert features to DataFrame
        features_df = pd.DataFrame([features])

        # Convert 'arrival_date_month' to numerical values
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        features_df['arrival_date_month'] = features_df['arrival_date_month'].apply(lambda x: months.index(x) + 1)

        # One-hot encode the specified columns
        one_hot_cols = ['hotel', 'meal', 'market_segment', 'distribution_channel', 'reserved_room_type', 'deposit_type', 'customer_type']
        features_df = pd.get_dummies(features_df, columns=one_hot_cols, drop_first=False)

        # Ensure that all dummy columns are present
        model_columns = ['lead_time', 'arrival_date_month', 'arrival_date_week_number', 'arrival_date_day_of_month',
                         'stays_in_weekend_nights', 'stays_in_week_nights', 'adults', 'children', 'babies',
                         'is_repeated_guest', 'previous_cancellations', 'previous_bookings_not_canceled', 'agent', 'adr',
                         'required_car_parking_spaces', 'total_of_special_requests', 'hotel_Resort Hotel', 'meal_FB', 
                         'meal_HB', 'meal_SC', 'meal_Undefined', 'market_segment_Complementary', 'market_segment_Corporate',
                         'market_segment_Direct', 'market_segment_Groups', 'market_segment_Offline TA/TO', 'market_segment_Online TA', 
                         'market_segment_Undefined', 'distribution_channel_Direct', 'distribution_channel_GDS', 
                         'distribution_channel_TA/TO', 'distribution_channel_Undefined', 'reserved_room_type_B', 
                         'reserved_room_type_C', 'reserved_room_type_D', 'reserved_room_type_E', 'reserved_room_type_F',
                         'reserved_room_type_G', 'reserved_room_type_H', 'reserved_room_type_L', 'deposit_type_Non Refund',
                         'deposit_type_Refundable', 'customer_type_Group', 'customer_type_Transient', 'customer_type_Transient-Party']

        for col in model_columns:
            if col not in features_df.columns:
                features_df[col] = 0

        # Ensure columns are in the correct order
        features_df = features_df[model_columns]

        # Convert to numpy array
        features_array = features_df.values

        # Make prediction
        prediction = model.predict(features_array)

        # Return the prediction as JSON
        return jsonify({'cancellation': int(prediction[0])})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
