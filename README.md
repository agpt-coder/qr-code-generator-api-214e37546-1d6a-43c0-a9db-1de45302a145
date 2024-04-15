---
date: 2024-04-15T18:06:37.436496
author: AutoGPT <info@agpt.co>
---

# QR Code Generator API 2

The project focuses on developing an endpoint that primarily receives various types of data, including URLs, text, and contact information, to generate QR codes. Key features of the endpoint include: 

1. **Data Handling:** The endpoint is adept at processing different data formats, with a particular emphasis on text inputs, which are the primary type of data it will handle. This capability ensures versatility in the QR codes' applications, enabling users to encode a wide range of information.

2. **Customization:** Users have specific customization requirements for the QR codes, emphasizing the need for distinctive branding elements. The desired customizations include the ability to alter the QR code's color to match the brand identity and the incorporation of a logo within the QR code. This customization extends to modifying the QR code's size to ensure it remains easily scannable from standard distances.

3. **Output Formats:** The preferred format for the generated QR codes is PNG. This choice reflects a balance between wide compatibility across platforms and the quality of the image suitable for various display sizes.

4. **Technical Approach:** The project will leverage Python as the programming language of choice, given its rich ecosystem for image processing and web development. For generating and customizing QR codes, exploration in the `qrcode` library has provided a solid foundation, highlighting capabilities such as basic QR code generation, color customization, and integration of logos. Further customization options have been identified, including altering shapes and patterns within the QR code for aesthetic and functional purposes.

5. **API and Database Design:** FastAPI is selected as the API framework for its performance and ease of use in creating web applications with Python. PostgreSQL will serve as the database solution, ensuring robust data management capabilities for storing information related to the QR codes, such as creation parameters and user data. The ORM of choice will be Prisma, which offers a powerful and easy-to-use interface for connecting the application's Python code with the PostgreSQL database.

This project summary encapsulates the task requirements and the chosen tech stack for the development of a feature-rich, customizable QR code generation endpoint.

## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'QR Code Generator API 2'

1. Unpack the ZIP file containing this package

2. Adjust the values in `.env` as you see fit.

3. Open a terminal in the folder containing this README and run the following commands:

    1. `poetry install` - install dependencies for the app

    2. `docker-compose up -d` - start the postgres database

    3. `prisma generate` - generate the database client for the app

    4. `prisma db push` - set up the database schema, creating the necessary tables etc.

4. Run `uvicorn project.server:app --reload` to start the app

## How to deploy on your own GCP account
1. Set up a GCP account
2. Create secrets: GCP_EMAIL (service account email), GCP_CREDENTIALS (service account key), GCP_PROJECT, GCP_APPLICATION (app name)
3. Ensure service account has following permissions: 
    Cloud Build Editor
    Cloud Build Service Account
    Cloud Run Developer
    Service Account User
    Service Usage Consumer
    Storage Object Viewer
4. Remove on: workflow, uncomment on: push (lines 2-6)
5. Push to master branch to trigger workflow
