# Water Dam Flood Barrier Estimation System

A Django-based web application for preliminary estimation of water dam flood barriers and their associated material and construction costs.

## 📌 Project Overview

The Water Dam Flood Barrier Estimation System is a web-based application developed using Python and Django.

It helps users enter project and barrier details and calculate:

- Required barrier height
- Barrier volume
- Required material quantity
- Material cost
- Labour cost
- Equipment cost
- Transportation cost
- Other costs
- Total estimated cost

The system also provides project management, material management, estimation history, reports, dashboard statistics, and estimation comparison features.

> **Note:** This application is intended for preliminary educational and planning purposes. It is not a substitute for professional engineering design, structural analysis, or safety approval.

## 🚀 Main Features

### 1. Project Management
- Add projects
- Edit projects
- Delete projects
- View project details
- View project estimation summary

### 2. Material Management
- Add materials
- Edit materials
- Delete materials
- Search materials
- Store material density and unit price

### 3. Flood Barrier Estimation
The system calculates the required barrier height using:

**Required Barrier Height = Water Level − Ground Level + Safety Allowance**

It then calculates:

**Barrier Volume = Length × Width × Barrier Height**

**Material Quantity = Barrier Volume × Material Density**

**Material Cost = Material Quantity × Material Unit Price**

**Total Cost = Material Cost + Labour Cost + Equipment Cost + Transportation Cost + Other Cost**

### 4. Estimation History
- View previous estimations
- Search estimations
- Open estimation reports
- Edit estimations
- Delete estimations

### 5. Dashboard
The dashboard provides:
- Total projects
- Total estimations
- Total estimated cost
- Recent estimations
- Quick access to important functions

### 6. Estimation Comparison
Users can select multiple estimations and compare their calculated values.

### 7. Django Admin
The project includes a Django administration panel for managing project data, materials, and estimations.

## 🛠️ Technologies Used

- Python
- Django
- SQLite
- HTML
- CSS
- JavaScript
- Bootstrap
- Git
- GitHub

## 📂 Project Structure

```text
WaterDamFloodBarrier/
│
├── estimation/
│   ├── migrations/
│   ├── templates/
│   ├── static/
│   ├── models.py
│   ├── views.py
│   └── ...
│
├── materials/
│   ├── migrations/
│   ├── templates/
│   ├── models.py
│   ├── views.py
│   └── ...
│
├── projects/
│   ├── migrations/
│   ├── templates/
│   ├── models.py
│   ├── views.py
│   └── ...
│
├── templates/
│
├── users/
│
├── water_dam_project/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── .gitignore
├── manage.py
├── README.md
└── requirements.txt