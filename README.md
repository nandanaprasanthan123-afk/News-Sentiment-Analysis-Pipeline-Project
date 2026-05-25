# Automated News Sentiment Analysis Pipeline & Dashboard

An automated, end-to-end serverless data pipeline that fetches live news articles, performs real-time sentiment analysis, archives raw data, and processes structured metrics into a database to serve an interactive analytics dashboard. Built using AWS cloud architecture and containerized microservices.

---

## 🏗️ System Architecture & Workflow

1. **Data Ingestion:** AWS EventBridge acts as a scheduler, triggering an AWS Lambda function automatically every 1 hour.
2. **Sentiment Analysis:** The Lambda function runs `newsapi.py` to pull data from the external News API and uses VADER Sentiment to score the text.
3. **Dual-Storage:** Structured data (metadata + sentiment scores) is stored in an Amazon RDS (PostgreSQL) database, while raw payloads are archived as `.json` files in an Amazon S3 bucket.
4. **Dashboard Deployment:** A Streamlit application is containerized locally using Docker, pushed to Amazon ECR, and served serverlessly on port 8051 using AWS ECS Fargate.

---

## 📁 Project Structure

This repository contains the following core files and directories:

```text
NEWSAPI/
├── rds_test/
│   └── test_rds.py         # Utility script to test connectivity to Amazon RDS
├── Dockerfile              # Docker instructions to build the Streamlit application container
├── lambdafunction.py           # Core AWS Lambda handler script (fetches, parses, saves data)
├── newsapi.py              # Ingestion script communicating with the News API
├── streamlitrun.py         # Main entry point for the interactive Streamlit user dashboard
├── requirements.txt        # List of Python dependencies required for the project
└── README.md               # Project documentation (this file)