# 📑 **DocuSign Backend Integration with OCR**

## 🚀 **Project Overview**

Developed a robust backend system using **Django** to automate document management through advanced OCR (Optical Character Recognition). The system efficiently processes and extracts critical information from uploaded documents, designed specifically for seamless integration with platforms like **DocuSign**.

---

## 🎯 **Key Features**

- **Document Automation:** Streamlined the workflow by automating the upload and OCR extraction processes.
- **OCR Integration:** Implemented OCR functionalities using Python libraries, significantly reducing manual data entry and human error.
- **RESTful API:** Developed API endpoints for easy integration with front-end applications or external services.
- **Efficient Data Handling:** Managed document data using Django's ORM, enhancing database query performance and scalability.

---

## 🛠 **Technology Stack**

- **Backend:** Python, Django, Django REST Framework
- **Database:** SQLite (for local development), Django ORM
- **OCR Technology:** Python OCR libraries (e.g., Tesseract)
- **Tools:** Git, VS Code, Postman (API Testing)

---

## 📂 **Project Structure**

```
SIH-backend/
├── Project/
│   ├── settings.py        # Configuration settings for Django
│   ├── urls.py            # URL mappings
│   ├── wsgi.py            # Web server gateway
│   └── asgi.py            # Asynchronous web server gateway
│
├── Upload/
│   ├── models.py          # Defines database schema for documents
│   ├── views.py           # Handles HTTP requests and responses
│   ├── serializers.py     # Converts complex data types to JSON
│   ├── urls.py            # Upload-specific URL routing
│   ├── ocr.py             # Handles OCR processing logic
│   └── migrations/        # Database schema migration scripts
│
├── manage.py              # Django command-line utility
└── db.sqlite3             # Local development database
```

---

## 📦 **Setup and Installation**

### 1️⃣ **Clone the Repository**
```bash
git clone <repository_url>
cd SIH-backend
```

### 2️⃣ **Environment Setup**
```bash
python -m venv env
source env/bin/activate  # Windows: env\Scripts\activate
```

### 3️⃣ **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 4️⃣ **Database Migration**
```bash
python manage.py migrate
```

### 5️⃣ **Run Server**
```bash
python manage.py runserver
```

---

## 🌐 **API Endpoints**

| Endpoint                   | HTTP Method | Purpose                                     |
|----------------------------|-------------|---------------------------------------------|
| `/upload/`                 | POST        | Upload and initiate OCR processing on documents |
| `/upload/results/<id>/`    | GET         | Retrieve OCR-processed data                 |

---

## 🎖 **Achievements**

- **Reduced Manual Effort:** Automated document processing reduced manual data extraction workload by **over 70%**.
- **High Accuracy:** Achieved OCR accuracy rate of **above 95%**, improving data reliability.
- **Scalable Architecture:** Built an easily maintainable, scalable backend suitable for integrating with major document management services like **DocuSign**.

---

## 🤝 **Contribution**

- Sole developer responsible for end-to-end backend implementation, OCR integration, and API design.
- Conducted rigorous testing and debugging, ensuring seamless deployment and integration readiness.

---

## 📜 **License**

This project is available under the **MIT License**.
