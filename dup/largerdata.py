import pandas as pd

old_scan_file = "old_scan.xlsx"
new_scan_file = "new_scan.xlsx"
output_file = "filtered_new_scan.xlsx"


key_columns = ["ID"]   

old_keys = pd.read_excel(
    old_scan_file,
    usecols=key_columns,
    dtype=str
)

old_key_set = set(map(tuple, old_keys.values))

new_df = pd.read_excel(
    new_scan_file,
    dtype=str
)

mask = ~new_df[key_columns].apply(tuple, axis=1).isin(old_key_set)
filtered_new_df = new_df[mask]

filtered_new_df.to_excel(output_file, index=False)

print("✅ Large-file-safe deduplication completed")
