import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Load cleaned data
@st.cache_data
def load_data(path="metadata_cleaned.csv"):
    df = pd.read_csv(path)
    # convert publish_time_parsed to datetime
    df['publish_time_parsed'] = pd.to_datetime(df['publish_time_parsed'], errors='coerce')
    return df

df = load_data()

st.title("CORD-19 Metadata Explorer")
st.write("Interactive exploration of COVID-19 research metadata")

# Sidebar filters
min_year = int(df['year'].min())
max_year = int(df['year'].max())
year_range = st.slider("Select publication year range", min_year, max_year, (min_year, max_year))

filtered = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]

# Show sample
st.subheader("Sample of filtered data")
st.write(filtered.head(10))

# Plot: number of publications over time (filtered)
year_counts2 = filtered['year'].value_counts().sort_index()
fig1, ax1 = plt.subplots()
ax1.bar(year_counts2.index, year_counts2.values)
ax1.set_xlabel("Year")
ax1.set_ylabel("Number of papers")
ax1.set_title("Publications by Year (filtered)")
st.pyplot(fig1)

# Plot: top journals
st.subheader("Top Journals in filtered data")
top_j = filtered['journal'].value_counts().head(10)
fig2, ax2 = plt.subplots()
sns.barplot(x=top_j.values, y=top_j.index, ax=ax2)
ax2.set_xlabel("Paper count")
ax2.set_ylabel("Journal")
st.pyplot(fig2)

# Word cloud of titles (filtered)
st.subheader("Word Cloud of Titles (filtered)")
from collections import Counter
import re
def tokenize(text):
    return re.findall(r"\\b\\w+\\b", text.lower())
stopwords = set(["the","and","of","in","to","for","on","with","a","an"])
all_tokens = filtered['title'].dropna().map(tokenize).sum()
counts = Counter(all_tokens)
for w in stopwords:
    counts.pop(w, None)
wc = WordCloud(width=800, height=400, background_color='white', stopwords=stopwords).generate(" ".join(filtered['title'].dropna()))
fig3, ax3 = plt.subplots(figsize=(12,6))
ax3.imshow(wc, interpolation='bilinear')
ax3.axis('off')
st.pyplot(fig3)
