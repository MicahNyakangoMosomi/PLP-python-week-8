# 🧠 CORD-19 Metadata Explorer

This project provides a **comprehensive data exploration and visualization** of the [CORD-19 Dataset](https://allenai.org/data/cord-19), a large collection of scientific papers related to COVID-19 research.  
The goal is to **clean**, **analyze**, and **visualize** publication metadata, and then deploy an **interactive Streamlit app** for exploring trends across years, journals, and research focus.

---

## 📁 Project Overview

This project is divided into five main parts:

1. **Data Loading & Exploration**  
   - Load the `metadata.csv` file  
   - Explore structure, missing values, and distributions  

2. **Data Cleaning & Preparation**  
   - Handle missing values  
   - Parse and extract dates  
   - Engineer features like word counts  

3. **Data Analysis & Visualization**  
   - Papers per year  
   - Top journals  
   - Most frequent words in titles  
   - Word Cloud, Bar Charts, and Distributions  

4. **Streamlit Application**  
   - Interactive dashboard for exploring publication trends  

5. **Documentation & Reflection**  
   - This README file summarizes objectives, methods, and findings  

---

## 🧩 Dataset Description

The **CORD-19 Metadata** file contains structured metadata for COVID-19-related scientific literature.  
It includes columns such as:
- `title`: Paper title  
- `abstract`: Summary of research  
- `publish_time`: Publication date  
- `journal`: Source journal name  
- `source_x`: Origin source (e.g., PMC, bioRxiv)  
- Other identifiers (DOI, authors, etc.)

**Note:** The dataset is **large**; ensure your environment can handle 100MB+ CSV files.

---

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/cord19-explorer.git
cd cord19-explorer

### 2 . Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate        # On Mac/Linux
venv\Scripts\activate           # On Windows
### 3. Install Required Libraries
```bash
pip install pandas numpy matplotlib seaborn wordcloud streamlit

### 4. Download the Dataset
cord19-explorer/
 ┣ metadata.csv
 ┣ analysis.py
 ┣ app.py
 ┗ README.md


### 5. Run the Project
```bash
python analysis.py

