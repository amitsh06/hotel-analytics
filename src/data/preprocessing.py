import pandas as pd
import numpy as np
import os

def preprocess_data():
    # Path to the raw CSV file
    raw_file_path = "C:\\Users\\maith\\OneDrive - Manipal University Jaipur\\Desktop\\hotel analytics\\src\\data\\raw\\hotel_bookings.csv"
    # Read the raw data
    try:
        df = pd.read_csv(raw_file_path)
        print("Raw data loaded successfully.")
    except Exception as e:
        print("Error loading raw data:", e)
        return

    # Handle missing values
    # Filling missing values for columns that require it
    df['children'] = df['children'].fillna(0)
    df['country'] = df['country'].fillna('unknown')
    df['agent'] = df['agent'].fillna(0)
    df['company'] = df['company'].fillna(0)

    # Convert data types to ensure consistency
    df['children'] = df['children'].astype(int)
    df['agent'] = df['agent'].astype(int)
    df['company'] = df['company'].astype(int)

    # Create a new column for total nights stayed
    df['total_nights'] = df['stays_in_weekend_nights'] + df['stays_in_week_nights']

    # Calculate the total price for each booking
    df['total_price'] = df['adr'] * df['total_nights']

    # Remove rows with non-positive values for adr or total_nights
    df = df[df['adr'] > 0]
    df = df[df['total_nights'] > 0]

    # Define the path for saving the processed data
    processed_file_path = "C:\\Users\\maith\\OneDrive - Manipal University Jaipur\\Desktop\\hotel analytics\\src\\data\\processed\\hotel_bookings_processed.csv"
    os.makedirs(os.path.dirname(processed_file_path), exist_ok=True)
    
    # Save the cleaned data to CSV
    df.to_csv(processed_file_path, index=False)
    print("Data preprocessing completed. Processed file saved to:")
    print(processed_file_path)

if __name__ == "__main__":
    preprocess_data()
