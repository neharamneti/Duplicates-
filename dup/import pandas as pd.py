import pandas as pd
old_scan_file = "Book1.xlsx"
new_scan_file = "Book2.xlsx"
output_file = "filtered_new_scan.xlsx"

key_columns = ["ID"]


old_df = pd.read_excel(old_scan_file)

new_df = pd.read_excel(new_scan_file)

filtered_new_df = new_df.merge(
    old_df[key_columns],
    on=key_columns,
    how="left",
    indicator=True
)

filtered_new_df = filtered_new_df[filtered_new_df["_merge"] == "left_only"]

filtered_new_df.drop(columns=["_merge"], inplace=True)

filtered_new_df.to_excel(output_file, index=False)

print("✅ Duplicates removed. New scan data saved to:", output_file)