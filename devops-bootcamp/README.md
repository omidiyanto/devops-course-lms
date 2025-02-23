# DevOps Bootcamp - Gamified Learning Management System

A unique DevOps learning platform that simulates real-world scenarios through gamified experiences. This platform aims to provide hands-on learning experiences for aspiring DevOps engineers through practical challenges and real-world problem-solving scenarios.

## Tech Stack

- Frontend:
  - HTML
  - Tailwind CSS
  - SweetAlert JS
  - JavaScript
- Backend:
  - Python (Flask)
  - Firebase (Authentication & Database)
- Deployment:
  - Vercel

## Features

### User Features
- Google OAuth Authentication
- Course Browse/Explore
- Course Purchase (QRIS/Virtual Account)
- Interactive Learning Management System
- Scenario-based Learning Games
- Video Submission for Assignments
- Progress Tracking
- Certificate Generation (upon completion within 1 month)

### Admin Features
- Course Content Management
- Payment Verification
- Assignment Evaluation
- Certificate Management
- User Management

## Course Curriculum

1. Server Virtualization with Proxmox
   - VM Creation and Management
   - Template Management
   - High Availability Configuration

2. Networking Fundamentals
   - Basic Network Concepts
   - DNS (Cloudflare & BIND9)
   - MikroTik Routing
   - Subnetting

3. Ubuntu Linux System Administration
   - File Management
   - Network & Firewall Management
   - Web Server Configuration
   - LVM Storage Management

4. Automation & Configuration Management
   - Bash Scripting
   - Ansible Basics
   - Configuration Management

5. Containerization with Docker
   - Docker Basics
   - Container Management
   - Docker Networking
   - Docker Compose

6. Kubernetes Administration
   - Cluster Setup
   - Application Deployment
   - Service Management
   - Storage Management

7. CI/CD & Security
   - Jenkins Pipeline
   - Secure SDLC
   - Container Security
   - Vulnerability Scanning

8. Version Control
   - Git Basics
   - GitHub Repository Management
   - Collaboration Workflows

9. Monitoring
   - Prometheus Setup
   - Grafana Dashboard
   - Alert Management

10. Infrastructure as Code
    - Terraform with Proxmox Provider
    - Ansible Integration
    - Infrastructure Management

## Project Structure

```
devops-bootcamp/
├── frontend/
│   ├── assets/
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   ├── components/
│   └── pages/
├── backend/
│   ├── app.py
│   ├── config/
│   ├── models/
│   ├── routes/
│   ├── services/
│   └── utils/
└── README.md
```

## Benefits

1. Affordable pricing (200k IDR)
2. Lifetime access to course materials
3. Practical, real-world scenarios
4. Portfolio-building projects
5. Achievement-based certification
6. Gamified learning experience
7. 24/7 community support

## Development Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd devops-bootcamp
   ```

2. **Set up a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r backend/requirements.txt
   ```

4. **Create a `.env` file:**
   - Copy the `.env.example` to `.env` and fill in the required values.
   ```bash
   cp backend/.env.example backend/.env
   ```

5. **Run the application:**
   ```bash
   ./run.sh
   ```

## Deployment

The application will be deployed on Vercel with Firebase integration for authentication and database management.
