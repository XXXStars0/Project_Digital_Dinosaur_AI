# Digital Dinosaur AI

This project is a simple web application built with Python and Flask.

## Getting Started

Follow these instructions to set up and run the project on your local machine.

### Prerequisites

- Python 3.x
- A virtual environment tool (like `venv`)

### Setup

1.  **Activate the Virtual Environment:**

    The project includes a pre-configured virtual environment in the `.venv` directory. To activate it on Windows, run the following command in your terminal:

    ```bash
    .\.venv\Scripts\activate
    ```

2.  **Install Dependencies:**

    All required packages are listed in the `requirements.txt` file. With the virtual environment activated, install them using pip:

    ```bash
    pip install -r requirements.txt
    ```

3.  **API Keys:**

    An `.env` file has been created for you to store your API keys. Add your keys to this file as needed.

    *   **File Path:** `.env`
    *   **Git Ignore:** The `.gitignore` file is configured to ignore the `.env` and `.venv` directories, ensuring that your keys and local environment settings are not committed to the repository.

### Running the Application

Once the setup is complete, start the Flask web server by running:

```bash
python main.py
```

The application will be available at `http://127.0.0.1:5000` in your web browser.
