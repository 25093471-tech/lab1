# Smart Agriculture EDA - Crop Recommendation Dataset
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd

# Load data (same CSV included with submission)
df = pd.read_csv('crop_data1.csv')
df.head()

print('Shape:', df.shape)
print('Columns:', df.columns.tolist())
print('
Data types:')
print(df.dtypes)
print('
Missing values:')
print(df.isna().sum())
print('
Crop label counts:')
print(df['label'].value_counts().sort_index())

num_cols = ['N','P','K','temperature','humidity','ph','rainfall']
df[num_cols].describe().T.round(2)

# Crop class balance
plt.figure(figsize=(10,4))
df['label'].value_counts().sort_index().plot(kind='bar')
plt.title('Number of samples for each crop label')
plt.xlabel('Crop label')
plt.ylabel('Number of records')
plt.xticks(rotation=60, ha='right')
plt.tight_layout()
plt.show()

# Correlation matrix
corr = df[num_cols].corr()
plt.figure(figsize=(7,5))
im = plt.imshow(corr, vmin=-1, vmax=1)
plt.colorbar(im)
plt.xticks(range(len(num_cols)), num_cols, rotation=45, ha='right')
plt.yticks(range(len(num_cols)), num_cols)
for i in range(len(num_cols)):
    for j in range(len(num_cols)):
        plt.text(j, i, f'{corr.iloc[i,j]:.2f}', ha='center', va='center', fontsize=8)
plt.title('Correlation matrix')
plt.tight_layout()
plt.show()

# Average rainfall by crop
rain_mean = df.groupby('label')['rainfall'].mean().sort_values(ascending=False)
plt.figure(figsize=(10,4))
rain_mean.plot(kind='bar')
plt.title('Average rainfall requirement by crop')
plt.xlabel('Crop label')
plt.ylabel('Mean rainfall (mm)')
plt.xticks(rotation=60, ha='right')
plt.tight_layout()
plt.show()
rain_mean.round(2)

# Mean NPK values for selected crops
selected = ['rice','maize','cotton','apple','grapes','muskmelon','coconut','coffee']
npk = df.groupby('label')[['N','P','K']].mean().loc[selected]
npk.plot(kind='bar', figsize=(10,4))
plt.title('Mean N, P and K values for selected crops')
plt.xlabel('Selected crop')
plt.ylabel('Mean value')
plt.xticks(rotation=35, ha='right')
plt.tight_layout()
plt.show()
npk.round(2)

groups = [g['rainfall'].values for _, g in df.groupby('label')]
F, p = stats.f_oneway(*groups)
levene = stats.levene(*groups, center='median')
kruskal = stats.kruskal(*groups)

grand_mean = df['rainfall'].mean()
ss_between = sum(len(g) * (g['rainfall'].mean() - grand_mean)**2 for _, g in df.groupby('label'))
ss_total = ((df['rainfall'] - grand_mean)**2).sum()
eta_sq = ss_between / ss_total

print(f'One-way ANOVA: F = {F:.2f}, p = {p:.3g}')
print(f'Levene test: W = {levene.statistic:.2f}, p = {levene.pvalue:.3g}')
print(f'Kruskal-Wallis: H = {kruskal.statistic:.2f}, p = {kruskal.pvalue:.3g}')
print(f'Eta squared = {eta_sq:.3f}')

# Exploratory post-hoc comparison
tukey = pairwise_tukeyhsd(df['rainfall'], df['label'], alpha=0.05)
tukey_df = pd.DataFrame(tukey.summary().data[1:], columns=tukey.summary().data[0])
tukey_df['abs_diff'] = tukey_df['meandiff'].abs()
tukey_df.sort_values('abs_diff', ascending=False).head(10)

rows = []
for col in num_cols:
    groups = [g[col].values for _, g in df.groupby('label')]
    F, p = stats.f_oneway(*groups)
    eta = sum(len(g) * (g[col].mean() - df[col].mean())**2 for _, g in df.groupby('label')) / ((df[col] - df[col].mean())**2).sum()
    rows.append([col, F, p, eta])

anova_summary = pd.DataFrame(rows, columns=['Variable','F statistic','p-value','eta squared'])
anova_summary.round(4)