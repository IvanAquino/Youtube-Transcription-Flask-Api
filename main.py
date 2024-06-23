from flask import Flask, jsonify, request
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from functools import wraps

app = Flask(__name__)

# Define the authentication token
AUTH_TOKEN = "change_your_secret_here"

def get_transcript(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        for transcript in transcript_list:
            try:
                return transcript.fetch()
            except Exception as e:
                raise Exception(f"Error fetching transcript in {transcript.language}: {e}")
    except TranscriptsDisabled:
        raise Exception("Transcripts are disabled for this video.")
    except NoTranscriptFound:
        raise Exception("No transcript found for this video.")
    except Exception as e:
        raise Exception(f"Error fetching transcripts: {e}")

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"message": "Token is missing!"}), 401
        if token != AUTH_TOKEN:
            return jsonify({"message": "Invalid token!"}), 403
        return f(*args, **kwargs)
    return decorated

@app.route('/transcript_text', methods=['GET'])
@token_required
def transcript_text():
    video_id = request.args.get('video_id')
    if not video_id:
        return jsonify({"message": "Please provide a video ID."}), 400
    
    transcript = get_transcript(video_id)
    if not transcript:
        return jsonify({"message": "Unable to fetch transcript."}), 404

    transcript_text = "\n".join([entry['text'] for entry in transcript])
    return transcript_text

@app.route('/transcript_json', methods=['GET'])
@token_required
def transcript_json():
    video_id = request.args.get('video_id')
    if not video_id:
        return jsonify({"message": "Please provide a video ID."}), 400

    transcript = get_transcript(video_id)
    if not transcript:
        return jsonify({"message": "Unable to fetch transcript."}), 404

    return jsonify(transcript)

@app.errorhandler(Exception)
def handle_exception(e):
    response = jsonify({"message": str(e)})
    response.status_code = 500
    return response

if __name__ == '__main__':
    app.run(debug=True)
