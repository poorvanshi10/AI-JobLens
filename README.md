# AI-JobLens

**AI-JobLens** is an AI-powered Chrome extension that analyzes job descriptions in real time and compares them with a candidate's resume using Natural Language Processing and Machine Learning techniques.

The goal of this project is to help students, freshers, and job seekers understand how well their resume matches a job role, what skills they are missing, and how they can improve their profile before applying.

---

## Project Status

Currently in development.

This repository is being built step by step with a focus on:

- NLP-based job description analysis
- Resume skill extraction
- Semantic similarity matching
- AI-powered skill gap detection
- Chrome Extension integration using JavaScript
- Python-based ML backend

---

## Problem Statement

Job seekers often apply to multiple roles without clearly knowing whether their resume actually matches the job description. Manual comparison of resumes and job descriptions is time-consuming and usually misses important keywords, technical skills, and role-specific requirements.

AI-JobLens solves this by automatically analyzing job descriptions and comparing them with resume data to generate a meaningful match score and personalized improvement suggestions.

---

## Key Features

- Extracts job descriptions from job portals and career pages
- Identifies important technical and soft skills from job descriptions
- Parses resume content and extracts candidate skills
- Calculates resume-job match score
- Detects missing skills and keyword gaps
- Suggests improvements for better ATS and recruiter visibility
- Classifies job roles into categories such as:
  - AI/ML
  - Data Science
  - Software Development
  - Full Stack Development
  - Backend Engineering
- Provides an easy-to-use Chrome extension interface

---

## AI/ML and NLP Focus

This project is designed to demonstrate practical use of AI/ML in a real-world hiring and job-search problem.

Planned NLP and ML techniques include:

- Text preprocessing
- Tokenization
- Stopword removal
- Lemmatization
- Skill keyword extraction
- TF-IDF vectorization
- Cosine similarity
- Semantic similarity using sentence embeddings
- Role classification
- Resume-job relevance scoring

---

## Tech Stack

### Machine Learning / NLP

- Python
- scikit-learn
- spaCy
- NLTK
- Sentence Transformers
- TF-IDF
- Cosine Similarity

### Backend

- FastAPI
- Python REST APIs
- Resume parsing logic
- NLP processing pipeline

### Chrome Extension

- JavaScript
- Chrome Extension Manifest V3
- Content Scripts
- Chrome Storage API
- DOM text extraction

### Data Handling

- JSON
- CSV
- Resume text data
- Job description text data

---

## How AI-JobLens Works

```text
User opens a job posting
        |
        v
Chrome extension extracts job description
        |
        v
Job description is sent to Python ML backend
        |
        v
NLP pipeline extracts skills and keywords
        |
        v
Resume skills are compared with job requirements
        |
        v
Match score and missing skills are generated
        |
        v
Extension displays personalized suggestions
