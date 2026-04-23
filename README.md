# 🔬 Lumina Auto EDA

**Lumina Auto EDA** is a powerful automated exploratory data analysis (EDA) web application built with Python. It enables users to quickly analyze datasets, generate insights, and visualize data without writing complex code.

---

## 🚀 Features

* 📂 Upload any CSV file (custom delimiter & encoding support)
* 📊 Dataset overview (shape, data types, preview)
* ❌ Missing values analysis (bar & pie charts)
* 📈 Statistical summary (mean, median, std, skewness, kurtosis)
* 🔢 Numerical visualizations (histogram, box plot, violin plot)
* 🏷️ Categorical analysis (bar, pie, treemap)
* 🔗 Correlation analysis (Pearson, Spearman, Kendall heatmaps)
* 🔍 High correlation pair detection
* 🧩 Pair plot (auto-disabled for large datasets)
* 🎨 Custom visualizer (user-defined x, y, color, chart type)
* 🔁 Duplicate detection & preview
* 💾 Memory usage analysis (per column)
* 🧹 Data cleaning tools:

  * Remove duplicates
  * Handle missing values
  * Fill with median
* 📥 Export cleaned dataset

---

## 🛠️ Tech Stack

* Python
* Streamlit (Web App Framework)
* Pandas (Data Processing)
* NumPy (Numerical Computing)
* Matplotlib & Seaborn (Static Visualization)
* Plotly (Interactive Charts)
* OpenPyXL (Excel Support)
* Pyngrok (Optional: for remote access)

---

## ⚙️ Installation & Setup

### ▶️ Run Locally (Recommended)

#### Step 1 — Install Dependencies

```bash
pip install streamlit pandas numpy matplotlib seaborn plotly openpyxl
```

#### Step 2 — Launch the App

```bash
streamlit run app.py
```

#### Step 3 — Open in Browser

Streamlit will generate a local URL like:

```
http://localhost:8501
```

Open it in your browser to use the app.

---

## 📦 Full Dependency List

| Library    | Purpose                       |
| ---------- | ----------------------------- |
| streamlit  | Web app framework             |
| pandas     | Data loading & manipulation   |
| numpy      | Numerical operations          |
| matplotlib | Backend for seaborn rendering |
| seaborn    | Statistical visualization     |
| plotly     | Interactive charts            |
| openpyxl   | Excel file support            |
| pyngrok    | Expose local app (Colab use)  |

---

## 📸 Screenshots
<img width="1365" height="622" alt="image" src="https://github.com/user-attachments/assets/4b2487c3-6325-46bb-a278-31145e24a9b3" />
<img width="1348" height="618" alt="image" src="https://github.com/user-attachments/assets/e51e11b7-543c-4ab5-84f2-dbac53c0ea75" />




---

## 📌 Use Cases

* Quick data exploration
* Data preprocessing before ML models
* Business data insights
* Academic data analysis

---

## 🔮 Future Improvements

* 🤖 Auto ML integration
* 📊 Advanced dashboard customization
* ☁️ Cloud deployment support
* 🧠 AI-powered insights generation

---

## 👨‍💻 Author

**Annas Wains**

---

## 📄 License

This project is licensed under the MIT License.

---

## ⭐ Support

If you like this project, consider giving it a ⭐ on GitHub!
