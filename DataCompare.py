import pandas as pd

pre = pd.read_csv(r'Data/Step 0 - pre - Food-Inspections-20251023.csv')
post = pd.read_csv(r'Data/Step 1 - After Open Refine Data.csv')

merged_df = pd.merge(
	pre, post, 
	on='Inspection ID', 
	suffixes=('_pre', '_post')
)

compare_cols = [col for col in pre.columns if col != 'Inspection ID']

diff_summary = {}
for col in compare_cols:
	pre_col = f"{col}_pre"
	post_col = f"{col}_post"
	
	differences = merged_df[pre_col] != merged_df[post_col]
	both_nan = merged_df[pre_col].isna() & merged_df[post_col].isna()
	
	actual_diff = differences & ~both_nan

	diff_summary[col] = int(actual_diff.sum())

summary_df = pd.DataFrame(
	list(diff_summary.items()), 
	columns=['Column', 'Number of Differences']
)

summary_df = summary_df.sort_values('Number of Differences', ascending=False).reset_index(drop=True)

print("Column Comparison Summary:")
print("-" * 40)
print(summary_df.to_string(index=False))
