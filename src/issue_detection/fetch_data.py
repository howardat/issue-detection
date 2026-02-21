import pandas as pd

def get_reviews(data_path='../../data/tickets.csv'):
    df = pd.read_csv(data_path)

    df = df['Описание ']

    return df

if __name__ == "__main__":
    print(get_reviews())
    print("fetch_data.py is running")