# Network Security System for Phishing URL Detection

This project is a full-stack web application designed to detect malicious phishing URLs using a   machine learning model with the best performance amongst a pool of scikit models. Dagshub and mlflow are being used to track all the experiments. The backend is built with FastAPI, storage is being handled by MongoDB Atlas, the frontend with Streamlit, and the entire application is containerized with Docker for seamless deployment to AWS EC2 using a CI/CD pipeline with GitHub Actions.

## ✨ Features

*   **ML-Powered Predictions**: Leverages a pre-trained model to classify URLs as safe or malicious.
*   **Interactive UI**: A clean and user-friendly Streamlit frontend for uploading data and viewing predictions.
*   **Model Training**: An API endpoint to trigger a retraining pipeline for the latest version of the machine learning model.
*   **Automated Deployment**: A full CI/CD pipeline using GitHub Actions to automatically build and deploy the application to AWS.
*   **Scalable Architecture**: Containerized with Docker and managed with Supervisor to run both the frontend and backend services in a single container.

## 🏛️ Architecture Diagram

The diagram below illustrates the flow from code push to a live application running on AWS EC2.

```mermaid
graph TD
    subgraph "Developer"
        A[Developer pushes code] --> B{GitHub Repository};
    end

    subgraph "CI/CD Pipeline"
        B -- Triggers --> C[GitHub Actions Workflow];
        C -- Builds & Pushes Docker Image --> D[AWS ECR];
    end

    subgraph "AWS Cloud Infrastructure"
        C -- via Self-Hosted Runner --> E[EC2 Instance];
        E -- Pulls Image from --> D;
        E -- Runs --> F[Docker Container];
    end
    
    subgraph "Inside Docker Container"
        F --> G[Supervisor];
        G -- Manages --> H[FastAPI Backend on Port 8000];
        G -- Manages --> I[Streamlit Frontend on Port 8501];
    end

    subgraph "End User"
        J[User] -- Accesses Public IP --> E;
        E -- Port 80 maps to 8501 --> I;
        I -- Sends API requests to --> H;
    end
```

## 📋 Prerequisites

Before you begin, ensure you have the following:
*   An [AWS Account](https://aws.amazon.com/)
*   A [GitHub Account](https://github.com/)
*   [Git](https://git-scm.com/) installed on your local machine
*   A MongoDB Atlas account and a connection string URL (for the backend)

---

## 🚀 Deployment Guide

Follow these steps to deploy the application to your own AWS account.

### Step 1: AWS Infrastructure Setup

1.  **Create an IAM User for GitHub Actions**:
    *   Go to the IAM dashboard in your AWS Console.
    *   Create a new user with "programmatic access".
    *   Attach the following policies:
        *   `AmazonEC2ContainerRegistryFullAccess` (to push images to ECR)
        *   `AmazonEC2FullAccess` (to manage the EC2 instance, can be restricted further for production)
    *   Save the `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`. You will need these for GitHub Secrets.

2.  **Create an ECR Repository**:
    *   Go to the Amazon ECR dashboard.
    *   Create a new **private** repository. Name it something like `network-security` or `phishing-detector`.
    *   Note the repository URI.

3.  **Launch an EC2 Instance**:
    *   Go to the EC2 dashboard and launch a new instance.
    *   **OS**: Choose **Ubuntu 22.04 LTS**.
    *   **Instance Type**: `t2.micro` is sufficient for this project.
    *   **Key Pair**: Create or select an existing key pair (`.pem` file) to SSH into your instance.
    *   **Network Settings / Security Group**: Create a new security group with the following inbound rules:
        *   **Rule 1**: Type `SSH`, Port `22`, Source `My IP` (for secure access).
        *   **Rule 2**: Type `HTTP`, Port `80`, Source `Anywhere (0.0.0.0/0)`. This allows public access to our Streamlit app.
    *   Launch the instance.

### Step 2: GitHub Project Setup

1.  **Fork/Clone the Repository**:
    *   Fork this repository to your own GitHub account.
    *   Clone it to your local machine.

2.  **Configure GitHub Secrets**:
    *   In your forked repository, go to `Settings` > `Secrets and variables` > `Actions`.
    *   Create the following repository secrets. These are used by the workflow file to interact with AWS.

| Secret Name             | Description                                                   | Example Value                                                 |
| ----------------------- | ------------------------------------------------------------- | ------------------------------------------------------------- |
| `AWS_ACCESS_KEY_ID`     | The access key for the IAM user created in Step 1.            | `AKIAIOSFODNN7EXAMPLE`                                        |
| `AWS_SECRET_ACCESS_KEY` | The secret key for the IAM user.                              | `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY`                    |
| `AWS_REGION`            | The AWS region where your resources are located.              | `us-east-1`                                                   |
| `AWS_ECR_LOGIN_URI`     | The URI of your ECR repository, without the repository name.  | `123456789012.dkr.ecr.us-east-1.amazonaws.com`                |
| `ECR_REPOSITORY_NAME`   | The name of your ECR repository.                              | `network-security`                                            |
| `MONGO_DB_URL`          | Your MongoDB Atlas connection string for the backend.         | `mongodb+srv://user:pass@cluster.mongodb.net/mydatabase`      |

### Step 3: EC2 Instance Preparation

This step connects your EC2 instance to GitHub Actions so the workflow can deploy to it.

1.  **SSH into your EC2 Instance**:
    ```bash
    ssh -i "your-key-pair.pem" ubuntu@your-ec2-public-ip
    ```

2.  **Install Docker**:
    The following commands will download and install Docker, and allow the `ubuntu` user to run Docker commands without `sudo`.
    ```bash
    # Update package lists
    sudo apt-get update -y
    sudo apt-get upgrade -y
    
    # Download and run the official Docker installation script
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    
    # Add the 'ubuntu' user to the 'docker' group
    sudo usermod -aG docker ubuntu
    
    # Apply the group changes to the current session
    newgrp docker
    ```

3.  **Install and Configure the GitHub Actions Self-Hosted Runner**:
    *   In your forked GitHub repository, go to `Settings` > `Actions` > `Runners`.
    *   Click `New self-hosted runner`.
    *   Select **Linux** as the operating system.
    *   Follow the exact "Download" and "Configure" commands provided on that page. Copy and paste them into your EC2 terminal. This will download the runner, link it to your repository, and start it.
    *   It is recommended to configure the runner as a service so it starts automatically if the instance reboots. The instructions are on the same page.

### Step 4: Trigger the Deployment

You are all set! Simply **push a change** to the `main` branch of your forked repository.

```bash
git commit -m "Triggering deployment" --allow-empty
git push origin main