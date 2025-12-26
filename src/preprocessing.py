import pandas as pd
import os

# 1. Setup paths
script_dir = os.path.dirname(os.path.abspath(__file__))
raw_dir = os.path.join(script_dir, '..', 'data', 'raw')
processed_dir = os.path.join(script_dir, '..', 'data', 'processed')

# 2. Define your target batches
batches = ['batch2.dat', 'batch3.dat', 'batch6.dat', 'batch7.dat', 'batch10.dat']
all_rows = []

def parse_libsvm(filepath):
    data = []
    with open(filepath, 'r') as f:
        for line in f:
            if not line.strip(): continue
            parts = line.split()
            
            # Extract ID and Concentration
            meta = parts[0].split(';')
            gas_id = int(meta[0])
            ppmv = float(meta[1]) if len(meta) > 1 else 0.0
            
            # Extract 128 Features
            features = [float(p.split(':')[-1]) for p in parts[1:]]
            if len(features) == 128:
                data.append([gas_id, ppmv] + features)
    return data

# 3. Process and Combine
for b in batches:
    file_path = os.path.join(raw_dir, b)
    if os.path.exists(file_path):
        print(f"Parsing {b}...")
        all_rows.extend(parse_libsvm(file_path))

# 4. Create DataFrame and Map Names
cols = ['gas_id', 'ppmv'] + [f'Feat_{i}' for i in range(1, 129)]
df_final = pd.DataFrame(all_rows, columns=cols)

gas_map = {1:"Ethanol", 2:"Ethylene", 3:"Ammonia", 4:"Acetaldehyde", 5:"Acetone", 6:"Toluene"}
df_final['gas_name'] = df_final['gas_id'].map(gas_map)

# 5. Save to CSV
if not os.path.exists(processed_dir):
    os.makedirs(processed_dir)

save_path = os.path.join(processed_dir, 'combined_gas_data.csv')
df_final.to_csv(save_path, index=False)

print(f"\nSaved {len(df_final)} measurements to {save_path}")
print(df_final['gas_name'].value_counts())