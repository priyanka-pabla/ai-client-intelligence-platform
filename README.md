# 🚀 AI Client Intelligence Platform

> **An AI-powered CRM and Lead Intelligence Platform that captures enquiries, analyzes lead quality, predicts conversion probability using Machine Learning, and helps businesses prioritize high-value opportunities.**

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red?logo=streamlit)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-orange?logo=scikitlearn)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-black?logo=pandas)
![Plotly](https://img.shields.io/badge/Plotly-Analytics-blue?logo=plotly)
![Git](https://img.shields.io/badge/Git-Version%20Control-orange?logo=git)

---

# 📌 Project Overview

The **AI Client Intelligence Platform** is an end-to-end AI-powered CRM application designed to help businesses manage enquiries, prioritize leads, and make smarter sales decisions.

The project evolved through two major versions:

* **Version 1:** Built a complete CRM with lead capture, rule-based lead scoring, analytics dashboard, and email automation.
* **Version 2:** Enhanced the platform with Machine Learning by creating realistic buyer personas, generating synthetic CRM data, training predictive models, and integrating real-time lead conversion prediction into the application.

This project demonstrates the complete lifecycle of an AI solution—from business problem identification and data generation to model deployment and interactive visualization.

---

# ⭐ Key Highlights

* Built an end-to-end AI-powered CRM using Python and Streamlit
* Designed **20 realistic buyer personas** across four business services
* Generated a synthetic CRM dataset for Machine Learning training
* Trained and compared **Logistic Regression** and **Random Forest** classifiers
* Integrated the trained ML model into the live Streamlit application
* Predicts lead conversion probability in real time
* Interactive analytics dashboard for business insights
* Demonstrates the complete Machine Learning development lifecycle

---

# 🎯 Business Problem

Businesses often receive enquiries from multiple potential customers, but every lead has a different probability of converting into a paying client.

Without intelligent prioritization, businesses risk:

* Spending equal effort on low-value and high-value leads
* Delayed responses to high-intent enquiries
* Missed business opportunities
* Limited visibility into sales performance

The AI Client Intelligence Platform addresses these challenges by combining CRM functionality with predictive analytics.

---

# 🚀 Project Evolution

## 📘 Version 1 — CRM Foundation

Version 1 focused on building a modern CRM capable of collecting and managing business enquiries.

### Features

* CRM Lead Capture Form
* Company & Contact Information
* Service Selection
* Lead Status Management
* Rule-Based Lead Scoring
* Hot / Warm / Cold Lead Classification
* Admin Dashboard
* Interactive Analytics
* Recent Activity Tracking
* Client Acknowledgement Email
* AI-Assisted Follow-up Email Generation
* CSV Data Storage

Version 1 provided businesses with an organized workflow for managing leads but relied on manually defined scoring rules.

---

## 🤖 Version 2 — AI & Machine Learning

Version 2 transformed the CRM into an intelligent decision-support system by replacing static scoring with predictive Machine Learning.

Instead of only classifying leads based on predefined rules, the application now estimates the probability that a lead will convert.

---

# 🧠 Machine Learning Development Journey

## Step 1 — Buyer Persona Engineering

Since real CRM training data was unavailable, realistic buyer personas were designed.

A total of **20 buyer personas** were created across four business services:

### AI Chatbots

* 5 Personas

### Business Automation

* 5 Personas

### Data Dashboards

* 5 Personas

### Website Development

* 5 Personas

Each persona included realistic business characteristics such as:

* Industry
* Company Size
* Decision Maker
* Technical Maturity
* Business Challenges
* Business Goals
* Budget Range
* Timeline
* Communication Preference
* Sample Business Enquiries
* Base Conversion Probability

---

## Step 2 — Synthetic Dataset Generation

A synthetic data generator was developed to simulate realistic business enquiries.

Each generated lead contains realistic variations of:

* Company
* Contact Person
* Industry
* Service
* Company Size
* Budget
* Timeline
* Business Message
* Lead Intent
* Communication Style

This produced a representative dataset for supervised Machine Learning without using sensitive customer information.

---

## Step 3 — Feature Engineering

The synthetic dataset was transformed into Machine Learning features.

Examples include:

* Service
* Industry
* Company Size
* Budget
* Timeline
* Technical Maturity
* Lead Intent
* Communication Preference

Categorical variables were encoded before model training.

---

## Step 4 — Model Training

Two supervised Machine Learning algorithms were trained and evaluated.

### Logistic Regression

* Strong baseline model
* Fast training
* High interpretability

### Random Forest

* Handles complex relationships
* Robust against overfitting
* Captures feature interactions
* Improved predictive capability

---

## Step 5 — Model Evaluation

Both models were evaluated using:

* Accuracy
* Precision
* Recall
* F1 Score

The best-performing model was selected and serialized for deployment.

---

## Step 6 — Model Deployment

The trained Machine Learning model was integrated into the Streamlit application.

Whenever a new lead is submitted, the application predicts:

* Conversion Probability
* Lead Score
* Lead Priority

The prediction is displayed instantly within the CRM dashboard.

---

# 🔄 End-to-End AI Pipeline

```text
Business Problem
        │
        ▼
CRM Development (Version 1)
        │
        ▼
Buyer Persona Design
        │
        ▼
Synthetic Dataset Generation
        │
        ▼
Feature Engineering
        │
        ▼
Model Training
(Logistic Regression vs Random Forest)
        │
        ▼
Model Evaluation
        │
        ▼
Best Model Selection
        │
        ▼
Model Deployment
        │
        ▼
Real-Time Lead Prediction
        │
        ▼
Interactive CRM Dashboard
```

---

# ✨ Platform Features

## CRM

* Lead Capture Form
* Company & Contact Details
* Service Selection
* Lead Status Management
* CSV-Based Lead Storage

### AI & Machine Learning

* Predictive Lead Conversion
* Conversion Probability
* Intelligent Lead Prioritization
* Real-Time Model Inference

### Dashboard

* Total Leads
* Hot Leads
* Warm Leads
* Cold Leads
* Conversion Probability
* Lead Status Overview
* Recent Activity

### Analytics

* Service Demand Analysis
* Lead Quality Distribution
* CRM Performance Overview

### Email Automation

* Client Acknowledgement Email
* AI-Assisted Follow-up Email Suggestions

---

# 🛠 Technology Stack

### Programming

* Python

### Frontend

* Streamlit

### Machine Learning

* Scikit-learn

### Data Processing

* Pandas
* NumPy

### Data Visualization

* Plotly

### Model Persistence

* Joblib

### Version Control

* Git
* GitHub

---

# 📊 Project Statistics

* CRM Application
* 20 Buyer Personas
* 4 Business Service Categories
* Synthetic Training Dataset
* Logistic Regression Model
* Random Forest Model
* Interactive Dashboard
* Machine Learning Deployment
* Real-Time Lead Prediction

---

# 📂 Project Structure

```text
ai-client-intelligence-platform/
│
├── data/
│   ├── buyer_personas.json
│   ├── synthetic_leads.csv
│   └── leads.csv
│
├── ml/
│   ├── generate_training_data.py
│   ├── train_conversion_model.py
│   └── predict_conversion.py
│
├── models/
│   └── conversion_model.pkl
│
├── utils/
├── assets/
├── streamlit_app.py
├── requirements.txt
└── README.md
```

---

# 🚀 Installation

```bash
git clone https://github.com/YOUR_USERNAME/ai-client-intelligence-platform.git
cd ai-client-intelligence-platform
pip install -r requirements.txt
streamlit run streamlit_app.py
```

---

# 🌍 Live Demo

**Streamlit:** *https://ai-client-intelligence-platform.streamlit.app/*

**GitHub:** *https://github.com/priyanka-pabla*

---

# 🔮 Future Roadmap

* User Authentication
* PostgreSQL Integration
* REST API
* CRM Integrations
* Multi-user Support
* Explainable AI for Predictions
* Revenue Forecasting
* Advanced Sales Analytics
* LLM-Powered Lead Insights

---

# 👩‍💻 Author

**Priyanka Pabla**

**Licensed UAE Freelance AI Developer | AI Consultant | Python Developer**

⭐ If you found this project useful, consider giving it a star on GitHub.
