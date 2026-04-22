# Vehicle Repair Estimates Application

A full-stack web application for managing vehicle repair estimates with user authentication, built with FastAPI, React, SQLAlchemy, and SQLite.

## Features

- **User Authentication**: JWT-based login system
- **Estimate Management**: Create, read, and update repair estimates
- **Status Filtering**: Filter estimates by status (pending, approved, rejected)
- **Responsive UI**: Built with React and TypeScript
- **API Documentation**: Auto-generated Swagger UI at `/docs`

## Architecture

- **Backend**: FastAPI + SQLAlchemy + SQLite
- **Frontend**: React + TypeScript + Vite
- **Deployment**: Docker & Docker Compose

## Prerequisites

- Docker & Docker Compose (for containerized setup)
- OR
- Python 3.12+ (for local backend development)
- Node.js 20+ (for local frontend development)

## Quick Start with Docker

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd vehicle-estimates-app
   ```

2. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

   The application will be available at:
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

3. **Login with demo credentials**
   - Username: `admin`
   - Password: `Admin123`

## Local Development

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the server**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

   Backend will be available at `http://localhost:8000`

5. **Run tests**
   ```bash
   pytest tests/
   ```

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Run development server**
   ```bash
   npm run dev
   ```

   Frontend will be available at `http://localhost:5173`

4. **Build for production**
   ```bash
   npm run build
   ```

## API Endpoints

### Authentication
- `POST /login` - Login with username and password
  - Request: `{ "username": "admin", "password": "Admin123" }`
  - Response: `{ "access_token": "...", "token_type": "bearer" }`

### Estimates
- `GET /estimates?status=pending` - List all estimates (optional status filter)
- `POST /estimates` - Create a new estimate
- `PATCH /estimates/{estimate_id}/status` - Update estimate status

All estimate endpoints require Bearer token authentication.

## Input Validation

### Estimate Creation
- **Customer Name**: Min 2 characters
- **Vehicle Model**: Min 2 characters
- **Vehicle Year**: Must be greater than 1885
- **Vehicle Mileage**: Must be >= 0
- **Repair Description**: Min 5 characters
- **Estimated Cost**: Must be > 0

### Status Update
- **Status**: Must be one of: `pending`, `approved`, `rejected`

## Error Handling

### HTTP Status Codes
- `200 OK`: Successful request
- `400 Bad Request`: Invalid input data (validation failed)
- `401 Unauthorized`: Missing or invalid authentication token
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server-side error

### Example Error Response
```json
{
  "detail": "Estimate 999 not found"
}
```

## Project Structure

```
vehicle-estimates-app/
├── backend/
│   ├── app/
│   │   ├── auth.py              # JWT token management
│   │   ├── db.py                # Database configuration
│   │   ├── main.py              # FastAPI app setup
│   │   ├── models.py            # SQLAlchemy models
│   │   ├── schemas.py           # Pydantic schemas for validation
│   │   └── routes/
│   │       ├── auth.py          # Authentication endpoints
│   │       └── estimates.py     # Estimate endpoints
│   ├── tests/
│   │   └── test_estimates.py    # API tests
│   ├── requirements.txt
│   ├── Dockerfile
│   └── vehicle_estimates.db     # SQLite database
├── frontend/
│   ├── src/
│   │   ├── api/                 # API client configuration
│   │   ├── context/             # React context for auth state
│   │   ├── hooks/               # Custom React hooks
│   │   ├── pages/               # Page components
│   │   ├── components/          # Reusable components
│   │   └── main.tsx             # Entry point
│   ├── package.json
│   ├── Dockerfile
│   └── vite.config.ts
├── docker-compose.yml
└── README.md
```

## Database Schema

### Estimates Table
```sql
CREATE TABLE estimates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name VARCHAR NOT NULL,
    vehicle_model VARCHAR NOT NULL,
    vehicle_year INTEGER NOT NULL,
    vehicle_mileage INTEGER NOT NULL,
    repair_description VARCHAR NOT NULL,
    estimated_cost FLOAT NOT NULL,
    status VARCHAR DEFAULT 'pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## Running Tests

Run the backend tests:
```bash
cd backend
pytest tests/ -v
```

This will test:
- User login endpoint
- Estimate creation
- Estimate listing
- Token validation

## AWS Deployment Overview

### Option 1: ECS/Fargate + S3/CloudFront (Recommended for Scalability)

For production deployment on AWS with maximum scalability, here's a high-level architecture outline:

- **Backend**: Deploy FastAPI using **AWS ECS** (Elastic Container Service) with Fargate for serverless container management, or use **Lambda** with API Gateway for API endpoints
- **Frontend**: Build React app and deploy static assets to **S3** with **CloudFront** CDN for global distribution and caching
- **Database**: Replace SQLite with **Amazon RDS** (PostgreSQL recommended) for scalability, backups, and multi-AZ failover
- **Secrets Management**: Use **AWS Secrets Manager** or **Parameter Store** to store JWT secret key, database credentials, and API keys securely
- **Identity & Access**: Configure **IAM roles** and policies for ECS tasks, S3 bucket access, and RDS database access with least-privilege principle
- **CI/CD Pipeline**: Set up **AWS CodePipeline** with **CodeBuild** to automatically test, build Docker images, push to ECR (Elastic Container Registry), and deploy on code commits
- **Monitoring**: Enable **CloudWatch** logs and metrics for application monitoring, set up alarms for errors, and use **X-Ray** for distributed tracing
- **API Gateway**: Use **Amazon API Gateway** to manage rate limiting, request throttling, and CORS policies for the backend API



### Option 2: Elastic Beanstalk (Simpler, Managed Approach)

For a faster, more managed deployment with less infrastructure overhead:

- **Unified Deployment**: Deploy the full stack (backend + frontend) or backend-only using **AWS Elastic Beanstalk** with Docker support—EB handles load balancing, auto-scaling, and environment management
- **Docker Configuration**: Use a single `Dockerfile` or `docker-compose.yml` in the Beanstalk environment; EB automatically pulls, builds, and runs your containers
- **Database**: Attach **RDS PostgreSQL** instance to your EB environment; connection strings managed via environment variables
- **Environment Variables**: Store sensitive data (JWT secret, DB credentials) in **EB environment properties** or **Systems Manager Parameter Store** for secure access
- **Auto-scaling**: Configure **Application Load Balancer (ALB)** with target groups; EB auto-scales based on CPU/memory metrics
- **Static Frontend**: Deploy React build to **S3 + CloudFront**, or serve directly from EB if bundled with backend
- **CI/CD Integration**: Use **AWS CodePipeline** with **CodeBuild** to automatically deploy to EB on git pushes; EB CLI simplifies local testing and deployments
- **Monitoring & Logs**: EB integrates with **CloudWatch** for logs, metrics, and alarms; built-in health monitoring for application status

