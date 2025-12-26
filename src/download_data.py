import os
import pandas as pd
from ucimlrepo import fetch_ucirepo 

def download_and_save():

    print("Fetching data from UCI...")
    dataset = fetch_ucirepo(id=270) 
    
    X = dataset.data.features 
    y = dataset.data.targets 
    
    full_df = pd.concat([X, y], axis=1)
    
    if not os.path.exists('data/raw'):
        os.makedirs('data/raw')
        
    full_df.to_csv('data/raw/gas_data.csv', index=False)
    print("Success! Data saved to data/raw/gas_data.csv")

if __name__ == "__main__":
    download_and_save()