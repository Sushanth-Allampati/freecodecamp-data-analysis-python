import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1 - Import data
df = pd.read_csv('medical_examination.csv')

# 2 - Add 'overweight' column
df['overweight'] = ((df['weight'] / ((df['height'] / 100) ** 2)) > 25).astype(int)

# 3 - Normalize cholesterol and glucose: 0 is good, 1 is bad
df['cholesterol'] = (df['cholesterol'] > 1).astype(int)
df['gluc'] = (df['gluc'] > 1).astype(int)

# 4
def draw_cat_plot():
    # 5 - Melt dataframe
    df_cat = pd.melt(df, 
                     id_vars='cardio', 
                     value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])

    # 6 - Group and count values
    df_cat = df_cat.groupby(['cardio', 'variable', 'value']).size().reset_index(name='total')

    # 7 - Draw catplot
    plot = sns.catplot(
        x='variable', y='total', hue='value', col='cardio',
        data=df_cat, kind='bar'
    )

    # 8 - Save figure
    fig = plot.fig
    fig.savefig('catplot.png')
    return fig


# 10
def draw_heat_map():
    # 11 - Clean data
    df_heat = df[
        (df['ap_lo'] <= df['ap_hi']) &
        (df['height'] >= df['height'].quantile(0.025)) &
        (df['height'] <= df['height'].quantile(0.975)) &
        (df['weight'] >= df['weight'].quantile(0.025)) &
        (df['weight'] <= df['weight'].quantile(0.975))
    ]

    # 12 - Correlation matrix
    corr = df_heat.corr()

    # 13 - Upper triangle mask
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # 14 - Set up figure
    fig, ax = plt.subplots(figsize=(12, 10))

    # 15 - Draw heatmap
    sns.heatmap(corr, 
                mask=mask, 
                annot=True, 
                fmt=".1f", 
                center=0, 
                square=True, 
                linewidths=0.5, 
                cbar_kws={'shrink': 0.5},
                ax=ax)

    # 16 - Save figure
    fig.savefig('heatmap.png')
    return fig

draw_cat_plot()
draw_heat_map()