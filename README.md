
# YouTube Transcript API Flask App

This project is a Flask application that retrieves YouTube video transcripts and provides two endpoints: one for plain text transcripts and another for JSON formatted transcripts. The application also includes simple token-based authentication for secure access.

## Features

- Retrieve YouTube video transcripts.
- Provide transcripts in plain text and JSON formats.
- Simple token-based authentication.

## Prerequisites

- Python 3.x
- pip

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/IvanAquino/Youtube-Transcription-Flask-Api.git
   cd Youtube-Transcription-Flask-Api
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

AUTH_TOKEN is used to prevent unauthorized users from transcribing videos without your permission.

1. Update the `AUTH_TOKEN` in `app.py` with your secret token:
   ```python
   AUTH_TOKEN = "change_your_secret_here"
   ```

## Usage

### Running in Development

1. Run the Flask application:
   ```bash
   export FLASK_APP=app.py
   export FLASK_ENV=development
   flask run
   ```

2. Access the application at `http://127.0.0.1:5000`.

### Endpoints

- `/transcript_text?video_id=VIDEO_ID` - Returns the transcript in plain text.
- `/transcript_json?video_id=VIDEO_ID` - Returns the transcript in JSON format.

### Example Request

```bash
curl -H "Authorization: change_your_secret_here" "http://127.0.0.1:5000/transcript_text?video_id=VIDEO_ID"
```

### Running in Production

1. Install Gunicorn:
   ```bash
   pip install gunicorn
   ```

2. Run the application with Gunicorn:
   ```bash
   gunicorn --bind 127.0.0.1:8000 main:app
   ```

3. (Optional) Configure Nginx as a reverse proxy:
   
   - Install Nginx:
     ```bash
     sudo apt-get update
     sudo apt-get install nginx
     ```

   - Configure Nginx to proxy requests to Gunicorn. Create a file at `/etc/nginx/sites-available/yourproject` with the following content:
     ```nginx
     server {
         listen 80;
         server_name localhost;

         location / {
             proxy_pass http://127.0.0.1:8000;
             proxy_set_header Host $host;
             proxy_set_header X-Real-IP $remote_addr;
             proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
             proxy_set_header X-Forwarded-Proto $scheme;
         }
     }
     ```

   - Enable the Nginx configuration:
     ```bash
     sudo ln -s /etc/nginx/sites-available/yourproject /etc/nginx/sites-enabled/
     sudo nginx -t
     sudo systemctl restart nginx
     ```

## Error Handling

The application includes global error handling to return a JSON response with a message key for any errors. The response will have a status code 500 for internal server errors.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
