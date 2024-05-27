import pandas as pd

# Read and merge CSV files
df1 = pd.read_csv('A_201023_260324.csv')
df2 = pd.read_csv('A_260323_201223.csv')
merged_df = pd.concat([df1, df2], ignore_index=True)

# Select columns containing location, username, content and item id
selected_columns = merged_df[["data.core.user_results.result.legacy.location",
                              "data.core.user_results.result.legacy.screen_name",
                              "data.legacy.full_text",
                              "item_id"]]

# Rename columns accordingly
selected_columns = selected_columns.rename(columns={"data.core.user_results.result.legacy.location": "Location",
                                                    "data.core.user_results.result.legacy.screen_name": "Username",
                                                    "data.legacy.full_text": "Content",
                                                    "item_id": "Item_ID"})

# Exclude rows with any empty values
selected_columns_filtered = selected_columns.dropna()

# Exclude rows where "nyx" is present in the screen name
selected_columns_filtered = selected_columns_filtered[~selected_columns_filtered['Username'].str.contains(r'nyx', case=False)]

# Save the data where "nyx" is in the full_text column to a new CSV file
nyx_mentions = selected_columns_filtered[selected_columns_filtered['Content'].str.contains(r'nyx', case=False)]
nyx_mentions.to_csv('B_nyx_mentions.csv', index=False)

# Group by Screen_Name and count occurrences of "nyx" in each user's tweets
nyx_mentions_count = nyx_mentions.groupby('Username').size().reset_index(name='Nyx_Mentions_Count')

# Sort users based on the count of "nyx" mentions
nyx_mentions_count = nyx_mentions_count.sort_values(by='Nyx_Mentions_Count', ascending=False)

# Write the result to a new CSV file
nyx_mentions_count.to_csv('C_nyx_mentions_count.csv', index=False)

