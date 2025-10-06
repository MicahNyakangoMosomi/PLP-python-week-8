# === PART 1: DATA LOADING & BASIC EXPLORATION ===

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud  # for later visualization in Part 3

# 1. Load the metadata
# (You must download the metadata.csv file first and provide its path)
metadata_path = "metadata.csv"  # change this path as needed
df = pd.read_csv(metadata_path, low_memory=False)  
# low_memory=False helps pandas infer dtypes more consistently across big files

# 2. Examine first rows and structure
print("== HEAD ==")
print(df.head(5))
print("\n== INFO ==")
print(df.info())
print("\n== SHAPE ==")
print(df.shape)

# 3. Check missing values (especially in important columns)
print("\n== NULL COUNTS ==")
print(df.isnull().sum().sort_values(ascending=False).head(20))

# 4. Basic statistics
# Only numeric columns will show stats; many columns are non-numeric
print("\n== DESCRIPTIVE STATS ==")
print(df.describe(include='all'))  
# include='all' shows non-numerical stats (counts, uniques, top, freq)

# 5. Also look at some distributions or value counts for categorical columns
print("\n== SAMPLE VALUE COUNTS ==")
if 'journal' in df.columns:
    print(df['journal'].value_counts().head(10))
if 'publish_time' in df.columns:
    print(df['publish_time'].value_counts().head(10))

# === PART 2: DATA CLEANING & PREPARATION ===

# 6. Handle missing data

# 6a. Decide which columns are “important” for your analysis and focus on them.
important_cols = ['title', 'abstract', 'publish_time', 'journal', 'source_x']
# you may adjust this list depending on which columns exist in your version

# 6b. View fraction of missing values in those important columns
for col in important_cols:
    if col in df.columns:
        missing_frac = df[col].isnull().mean()
        print(f"Missing fraction in {col}: {missing_frac:.3f}")

# 6c. Strategy: drop rows missing critical fields or fill missing values
# Example: drop rows missing title or publish_time
df_clean = df.dropna(subset=['title', 'publish_time'])

# Optionally: for abstract, you could fill missing abstracts as empty strings:
if 'abstract' in df_clean.columns:
    df_clean['abstract'] = df_clean['abstract'].fillna("")

# 7. Convert dates and extract year

# 7a. Parse publish_time into datetime
# Some publish_time entries might be malformed — wrap in errors='coerce' to force invalid ones to NaT
df_clean['publish_time_parsed'] = pd.to_datetime(df_clean['publish_time'], errors='coerce')

# 7b. Extract year
df_clean['year'] = df_clean['publish_time_parsed'].dt.year

# 7c. You can drop rows for which publish_time couldn’t be parsed
df_clean = df_clean.dropna(subset=['publish_time_parsed'])

# 8. Feature engineering: e.g. word count of abstract, title
df_clean['abstract_word_count'] = df_clean['abstract'].str.split().apply(len)
df_clean['title_word_count'] = df_clean['title'].str.split().apply(len)

# Optionally, you could lowercase, remove punctuation in abstracts / titles for later text analysis.

# === PART 3: DATA ANALYSIS & VISUALIZATION ===

# 9. Count papers by year
year_counts = df_clean['year'].value_counts().sort_index()
print("Papers per year:")
print(year_counts)

# 10. Top journals publishing COVID-19 papers
top_journals = df_clean['journal'].value_counts().head(10)
print("Top journals:")
print(top_journals)

# 11. Most frequent words in titles (simple approach)
from collections import Counter
import re

def tokenize(text):
    # simple tokenizer: lowercase, split on non-word characters
    tokens = re.findall(r"\b\w+\b", text.lower())
    return tokens

# aggregate all titles
all_title_tokens = df_clean['title'].dropna().map(tokenize).sum()
title_word_counts = Counter(all_title_tokens)
# remove common stopwords (you can extend this list)
stopwords = set(["the", "and", "of", "in", "to", "for", "on", "with", "a", "an"])
for sw in stopwords:
    if sw in title_word_counts:
        del title_word_counts[sw]

most_common_title = title_word_counts.most_common(20)
print("Most common title words:")
print(most_common_title)

# 12. Visualizations

# 12a. Publications over time (bar plot)
plt.figure(figsize=(10, 6))
sns.barplot(x=year_counts.index, y=year_counts.values, palette='viridis')
plt.xlabel("Year")
plt.ylabel("Number of papers")
plt.title("Number of CORD-19 Publications by Year")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 12b. Top journals bar chart
plt.figure(figsize=(10, 6))
sns.barplot(x=top_journals.values, y=top_journals.index, palette='magma')
plt.xlabel("Number of papers")
plt.ylabel("Journal")
plt.title("Top Journals in CORD-19 Metadata")
plt.tight_layout()
plt.show()

# 12c. Word cloud of titles
wc = WordCloud(width=800, height=400, background_color='white', stopwords=stopwords).generate(" ".join(df_clean['title'].dropna()))
plt.figure(figsize=(12, 6))
plt.imshow(wc, interpolation='bilinear')
plt.axis('off')
plt.title("Word Cloud: Most Frequent Terms in Titles")
plt.show()

# 12d. Distribution of papers by source (source_x column)
if 'source_x' in df_clean.columns:
    plt.figure(figsize=(8, 6))
    sns.countplot(data=df_clean, y='source_x', order=df_clean['source_x'].value_counts().index[:10])
    plt.title("Top Sources in CORD-19 Metadata")
    plt.tight_layout()
    plt.show()

# === PART 4: STREAMLIT APPLICATION ===

# Save the cleaned DataFrame to CSV (optional) so Streamlit app can load quickly
cleaned_path = "metadata_cleaned.csv"
df_clean.to_csv(cleaned_path, index=False)
