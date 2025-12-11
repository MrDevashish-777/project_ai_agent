# Supabase Cloud Setup Guide

This guide will help you set up your project with a cloud-hosted Supabase database.

## Step 1: Create a Supabase Project

1.  Go to [https://supabase.com/](https://supabase.com/) and sign up or log in.
2.  Click on **"New Project"**.
3.  Select your organization.
4.  Enter a **Name** for your project (e.g., "Nagpur Hotel Agent").
5.  Enter a strong **Database Password** (save this somewhere safe, though you likely won't need it for this setup).
6.  Choose a **Region** close to you (e.g., Mumbai, India).
7.  Click **"Create new project"**.
8.  Wait a few minutes for the project to be provisioned.

## Step 2: Get Your API Credentials

1.  Once your project is ready, go to the **Project Settings** (the gear icon at the bottom of the left sidebar).
2.  Click on **"API"** in the sidebar. 
3.  Find the **Project URL** and copy it. https://vohjboalxbpwsbmnsrzt.supabase.co
4.  Find the **Project API keys** section. Copy the `anon` `public` key.

## Step 3: Configure Your Environment

1.  In your project folder, look for a file named `.env`. If it doesn't exist, create one by copying `.env.example`.
    ```bash
    cp .env.example .env
    ```
    (Or just create a new file named `.env`)

2.  Open `.env` in your text editor.

3.  Update the following lines with the values you copied in Step 2:

    ```env
    SUPABASE_URL=https://your-project-id.supabase.co
    SUPABASE_KEY=your-anon-public-key
    ```

    *Note: Replace the placeholder text with your actual URL and Key.*

## Step 4: Create Database Tables

Since you are using the cloud version, the easiest way to set up your tables is to run the SQL script in the Supabase Dashboard.

1.  Open the file `supabase_tables.sql` in your project folder and copy all its content.
2.  Go back to your Supabase project dashboard.
3.  Click on the **"SQL Editor"** icon in the left sidebar.
4.  Click **"New query"**.
5.  Paste the content of `supabase_tables.sql` into the editor.
6.  Click **"Run"** (the green button).
7.  You should see "Success" in the results.

## Step 5: Verify the Setup

Run the verification script to ensure your application can connect to the cloud database.

```bash
python verify_cloud_setup.py
```

If successful, you will see a message confirming the connection to the remote DB.

## Troubleshooting

-   **Connection Failed**: Double-check your `SUPABASE_URL` and `SUPABASE_KEY` in the `.env` file. Ensure there are no extra spaces or quotes.
-   **Tables not found**: Ensure you ran the SQL script in the Supabase SQL Editor.
-   **Dependencies**: Make sure you have installed the requirements:
    ```bash
    pip install -r requirements.txt
    ```
