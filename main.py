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
                print(f"Error fetching transcript in {transcript.language}: {e}")
    except TranscriptsDisabled:
        print("Transcripts are disabled for this video.")
    except NoTranscriptFound:
        print("No transcript found for this video.")
    except Exception as e:
        print(f"Error fetching transcripts: {e}")
    return []

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"error": "Token is missing!"}), 401
        if token != AUTH_TOKEN:
            return jsonify({"error": "Invalid token!"}), 403
        return f(*args, **kwargs)
    return decorated

@app.route('/transcript_text', methods=['GET'])
@token_required
def transcript_text():
    video_id = request.args.get('video_id')
    if not video_id:
        return "Please provide a video ID.", 400
    
    transcript = get_transcript(video_id)
    if not transcript:
        return "Unable to fetch transcript.", 404

    transcript_text = "\n".join([entry['text'] for entry in transcript])
    return transcript_text

@app.route('/transcript_json', methods=['GET'])
@token_required
def transcript_json():
    video_id = request.args.get('video_id')
    if not video_id:
        return jsonify({"error": "Please provide a video ID."}), 400

    transcript = get_transcript(video_id)
    if not transcript:
        return jsonify({"error": "Unable to fetch transcript."}), 404

    return jsonify(transcript)

if __name__ == '__main__':
    app.run(debug=True)
