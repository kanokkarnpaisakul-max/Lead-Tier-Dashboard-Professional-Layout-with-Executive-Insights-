# 📊 Lead Tier Dashboard – Professional Layout with Executive Insights

### 🔎 Overview

This project provides a **Lead Tiering Dashboard** built with **Python + Streamlit**.
It helps classify leads into tiers (A/B/C) based on multiple factors such as:

* Vehicle Age (อายุรถ)
* Occupation (อาชีพ)
* Region (ภูมิภาค)
* Credit Bureau Score (เครดิตบูโร)

The dashboard is designed with a **professional executive layout**, making it suitable for both data analysts and business executives.

---

## ✨ Features

* **Lead Scoring System** → Assigns scores based on business rules.
* **Automatic Tier Classification** → Group leads into Tier A, B, or C.
* **Interactive Dashboard** → Built with Streamlit for real-time insights.
* **Professional Layout** → Clean design for management reporting.
* **Ready-to-Use Sample Data** → Quickly test with included dataset.

---

## 📂 Data Structure

The input dataset should include the following fields:

| Column (English) | คำอธิบาย (ไทย) | Example           |
| ---------------- | -------------- | ----------------- |
| Lead_ID          | รหัสลูกค้า     | 1                 |
| Vehicle_Age      | อายุรถ (ปี)    | 7                 |
| Occupation       | อาชีพ          | พนักงานบริษัทใหญ่ |
| Region           | ภูมิภาค        | กรุงเทพฯ          |
| Credit_Bureau    | เครดิตบูโร     | ดีมาก             |

The system will generate:

* Individual Scores (per factor)
* Total Score (คะแนนรวม)
* Tier Classification (Tier A/B/C)

---

## 📝 Sample Data

A sample dataset is provided for quick testing:

📂 [sample_leads.csv](./sample_leads.csv)

Example rows:

| Lead_ID | อายุรถ(ปี) | อาชีพ             | ภูมิภาค      | เครดิตบูโร |
| ------- | ---------- | ----------------- | ------------ | ---------- |
| 1       | 7          | พนักงานบริษัทใหญ่ | ภาคอีสาน     | ดีมาก      |
| 2       | 4          | ค้าขาย            | หัวเมืองใหญ่ | ปานกลาง    |
| 3       | 10         | ฟรีแลนซ์          | กรุงเทพฯ     | แย่        |

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/kanokkarnpaisakul-max/Lead-Tier-Dashboard-Professional-Layout-with-Executive-Insights-.git
cd Lead-Tier-Dashboard-Professional-Layout-with-Executive-Insights-
```

### 2. Install Dependencies

```bash
pip install streamlit pandas plotly numpy
```

### 3. Run the Dashboard

```bash
streamlit run lead_dashboard26.final.py
```

---

## 📸 Example Output

![Dashboard Screenshot](./Lead_Tier_Board.png)

---

## 📊 Tiering Logic

* **8–10 points** → Tier A (High Quality)
* **5–7 points** → Tier B (Medium Quality)
* **< 5 points** → Tier C (Low Quality)

(คะแนนจะถูกปรับจากอายุรถ, อาชีพ, ภูมิภาค, เครดิตบูโร)

---

## 🌐 Live Demo

👉 [Lead Tier Dashboard – Streamlit Cloud](https://lead-tier-board.streamlit.app/)

---

## 🔮 Future Improvements

* Add more business rules (e.g., income, engagement)
* Enhance visualizations with advanced filters
* Database integration (MySQL / PostgreSQL)
* Export results (Excel, PDF)

---

## 👩‍💻 Author

Developed by **Kanokkarn Paisakul**

* 💼 [LinkedIn Profile](https://www.linkedin.com/in/kanokkarnpaisakul-max/)
* 📧 Contact: kanokkarn.paisakul@gmail.com

---

✨ *This project is part of my professional portfolio. Feel free to fork, explore, and connect with me on LinkedIn!*



