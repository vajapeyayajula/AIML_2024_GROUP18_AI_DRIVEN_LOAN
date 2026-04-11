# Full AWS Deployment Guide (Automated)

This project is now configured for **Full Automation** using GitHub Actions. You don't need to install any deployment tools (like Docker or AWS CLI) on your local computer.

## Prerequisites

1.  **AWS Account**: An active AWS account.
2.  **GitHub Secrets**: You need to add your AWS credentials to your GitHub repository.

## Step 1: Set Up AWS Credentials in GitHub

1.  On GitHub, go to your repository: `https://github.com/vajapeyayajula/AIML_2024_GROUP18_AI_DRIVEN_LOAN`
2.  Navigate to **Settings** > **Secrets and variables** > **Actions**.
3.  Click **New repository secret** and add the following:

| Secret Name | Description |
| :--- | :--- |
| `AWS_ACCESS_KEY_ID` | Your AWS Access Key |
| `AWS_SECRET_ACCESS_KEY` | Your AWS Secret Access Key |
| `ECR_REPOSITORY` | (Optional/Auto-created) You can leave this for now or provide an ECR URI if you have one. |

## Step 2: Deploy

Simply push your code to the `main` branch!

```bash
git add .
git commit -m "Configure AWS hosting and automation"
git push origin main
```

## Step 3: Access Your Website

1.  Once the "Deploy to AWS" action finishes in the **Actions** tab of your GitHub repo:
2.  Check the "SAM Deploy" or "Get Stack Outputs" step logs.
3.  Look for the `FrontendWebsiteUrl`. This is your live website!

---

### How it works:
- **GitHub Actions** spins up a server, builds your ML container, and deploys it to **AWS Lambda**.
- It then automatically finds the new API URL, injects it into your frontend code, and uploads your UI to an **AWS S3 Bucket**.
- Your whole site is now hosted in the cloud for free (under the AWS Free Tier)!
