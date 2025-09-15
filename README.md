# Telematics-Based Auto Insurance Solution

This project implements a telematics-based auto insurance solution, featuring a Flask backend and a React frontend. It captures mock driving behavior, calculates dynamic risk scores, and provides a user dashboard with gamification and feedback.

## Project Structure

```
telematics_insurance_solution/
├── telematics_dashboard/          # React Frontend
│   ├── public/
│   ├── src/                       # React source code
│   │   ├── App.jsx
│   │   ├── components/
│   │   │   ├── Dashboard.jsx
│   │   │   ├── RealTimeFeedback.jsx
│   │   └── assets/
│   ├── package.json               # Node.js dependencies
│   ├── pnpm-lock.yaml             # pnpm lock file
│   ├── vite.config.js             # Vite configuration
│   ├── index.html                 # HTML entry point
│   └── Dockerfile                 # Dockerfile for the React frontend
├── design_document.md             # Overall system design document
├── api_documentation.md           # Detailed API documentation
├── telematics_solution_documentation.md # Comprehensive solution overview
├── README.md                      # Project README and local run instructions
└── docker-compose.yml             # Docker Compose file for orchestration
├── telematics_insurance_backend/  # Flask Backend
│   ├── src/                       # Python source code
│   │   ├── main.py
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   └── telematics.py
│   │   ├── routes/
│   │   │   ├── user.py
│   │   │   ├── telematics.py
│   │   │   ├── data_processing.py
│   │   │   ├── gamification.py
│   │   │   └── external_data.py
│   │   └── static/                # Frontend build files (copied here for deployment)
│   ├── venv/                      # Python virtual environment (local, not in Docker)
│   ├── requirements.txt           # Python dependencies
│   ├── test_simulation.py         # Script for testing and data simulation
│   └── Dockerfile                 # Dockerfile for the Flask backend

```

## How to Run Locally

To run the entire solution locally on your computer, you will need to have **Python 3.11+** (with `pip`) and **Node.js 18+** (with `pnpm` or `npm`) installed.

### Step 1: Clone the Repository

First, clone this repository to your local machine:

```bash
git clone https://github.com/IselaJuarez-Cendejas/telematics_insurance_solution.git
cd telematics_solution
```

### Step 2: Set up and Run the Backend

1.  **Navigate to the backend directory:**
    ```bash
    cd telematics_insurance_backend
    ```

2.  **Create a Python Virtual Environment:**
    It's highly recommended to use a virtual environment to manage dependencies.
    ```bash
    python3.11 -m venv venv
    ```

3.  **Activate the Virtual Environment:**
    *   On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```
    *   On Windows (Command Prompt):
        ```bash
        venv\Scripts\activate.bat
        ```
    *   On Windows (PowerShell):
        ```bash
        venv\Scripts\Activate.ps1
        ```

4.  **Install Python Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Create the Database Directory:**
    The application uses an SQLite database, which needs a directory to store its file.
    ```bash
    mkdir -p src/database
    ```

6.  **Run the Flask Backend Server:**
    ```bash
    python src/main.py
    ```
    The Flask server should start and be accessible at `http://127.0.0.1:5000`. Keep this terminal open.

### Step 3: Set up and Run the Frontend

1.  **Open a new terminal or command prompt window.**

2.  **Navigate to the frontend directory:**
    ```bash
    cd telematics_dashboard
    ```

3.  **Install Node.js Dependencies:**
    You can use `pnpm`, `npm`, or `yarn`.
    ```bash
    pnpm install
    # OR
    # npm install
    # OR
    # yarn install
    ```

4.  **Run the React Development Server:**
    ```bash
    pnpm run dev --host
    # OR
    # npm run dev -- --host
    # OR
    # yarn dev --host
    ```
    The React development server should start, typically accessible at `http://127.0.0.1:5173`. Keep this terminal open.

### Step 4: Access the Application

Open your web browser and navigate to `http://127.0.0.1:5173`. You should see the Telematics Insurance Dashboard.

### Step 5: (Optional) Run the Simulation Script

To populate the database with test data and see the system in action, you can run the simulation script in a *third* terminal:

1.  **Navigate to the backend directory:**
    ```bash
    cd telematics_insurance_backend
    ```

2.  **Activate the Virtual Environment (if not already active):**
    ```bash
    source venv/bin/activate
    ```

3.  **Run the Simulation Script:**
    ```bash
    python test_simulation.py
    ```
    This script will create test policyholders, simulate trips, and interact with all backend APIs, populating the dashboard with data. Refresh your browser to see the changes.
