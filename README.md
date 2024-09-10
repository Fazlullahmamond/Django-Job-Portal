# Django Job Portal

Welcome to the Django Job Portal, a comprehensive web application designed to connect job seekers with employers. Built using Django, this project provides an efficient platform for job management and application.

## Features

- **User Authentication**: Secure login and registration for job seekers and employers.
- **Job Listings**: Post and manage job openings with detailed descriptions.
- **Search and Filters**: Search and filter job listings by location, type, and industry.
- **Application Tracking**: Apply for jobs and track application status.
- **Resume Management**: Upload and manage resumes.
- **Profile Management**: Customizable profiles for job seekers and employers.
- **Admin Dashboard**: Manage users, job postings, and applications.
- **Responsive Design**: Optimized for both desktop and mobile devices.

## Technologies Used

- **Django**: High-level Python web framework.
- **PostgreSQL**: Open-source relational database system.
- **Bootstrap**: Front-end framework for responsive design.
- **Heroku** (optional): Scalable hosting (if deployed).

## Getting Started

To set up the project locally, follow these steps:

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/django-job-portal.git

2. **Navigate to the Project Directory**
   ```bash
   cd django-job-portal
   
3. **Create and Activate a Virtual Environment**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt

5. **Apply Migrations**
   ```bash
   python manage.py migrate
   
6. **Run the Development Server**
   ```bash
   python manage.py runserver
