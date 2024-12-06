app.py:
from flask import Flask, request, redirect, render_template
from flask_cors import CORS
import assemblyai as aai
import os

app = Flask(__name__)
CORS(app)

# Set your AssemblyAI API key
aai.settings.api_key = "a8414083bc4b4e298baf9d23e128da59"

@app.route('/', methods=['GET'])
def get_alerts():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload_audio():
    if 'file' not in request.files:
        return 'No file part', 400
    audio_file = request.files['file']

    # Save the uploaded file temporarily
    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)
    file_path = os.path.join(temp_dir, audio_file.filename)

    blob = audio_file.read()
    with open(file_path, 'wb') as f:
        f.write(blob)

    # Now use the saved file path for transcription
    try:
        # Set the content safety and entity detection config
        config = aai.TranscriptionConfig(
            entity_detection=True,  # Enable entity detection
            content_safety=True,
            content_safety_confidence=60  # 60% confidence threshold
        )

        # Transcribe the audio file with entity detection enabled
        transcript = aai.Transcriber().transcribe(file_path, config)

        # Check if entities exist in the transcript
        if not transcript.entities:
            return "No entities detected in the transcript.", 200

        # content to look out for
        flagged_content = ["credit_card_cvv"]

        flagged_found = False
        # Loop through detected entities
        for entity in transcript.entities:
            if entity.entity_type in flagged_content:
                flagged_found = True
                break

        # If flagged entity is found, redirect to the main page with the summary transcript
        if flagged_found:
            # Set summarization config
            summary_config = aai.TranscriptionConfig(
                summarization=True,
                summary_model=aai.SummarizationModel.informative,
                summary_type=aai.SummarizationType.bullets
            )
            # Transcribe with summarization enabled
            summary_transcript = aai.Transcriber().transcribe(file_path, summary_config)

            # Redirect to the main page with the summary transcript
            return redirect(f'/summary?summary={summary_transcript.summary}')

        # If no flagged entity is found, print in the terminal
        if not flagged_found:
            print(f"No 'credit_card_cvv' entity detected in {audio_file.filename}.")

        # Return success message
        return "Processed the audio file successfully", 200

    except Exception as e:
        print(e)
        return f"An error occurred: {str(e)}", 500

    finally:
        # Clean up temporary file
        os.remove(file_path)

@app.route('/summary', methods=['GET'])
def show_summary():
    summary = request.args.get('summary')
    return render_template('index.html', summary=summary)

if __name__ == '__main__':
    app.run(debug=True, port=5001)