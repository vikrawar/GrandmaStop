import os
from dotenv import load_dotenv
import assemblyai as aai
from flask import Flask, request

load_dotenv()
aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")

 
app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_audio():
    if 'file' not in request.files:
        return 'No file part', 400
    audio_file = request.files['file']
    if audio_file.filename == '':
        return 'No selected file', 400

    # Save the uploaded file temporarily
    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)
    file_path = os.path.join(temp_dir, audio_file.filename)
    audio_file.save(file_path)

    # Set the content safety and entity detection config
    config = aai.TranscriptionConfig(
        entity_detection=True,  
        content_safety=True, 
        content_safety_confidence=60 
    )

    try:
        # Transcribe the audio file
        transcript = aai.Transcriber().transcribe(file_path, config)

        # Debug: Check the transcript response
        print(f"Transcript Response: {transcript}")

        # Check if entities exist in the transcript
        if not transcript.entities:
            return "No entities detected in the transcript.", 400

        # Flagged content will be written to this text file
        output_dir = "flagged_content"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f"{audio_file.filename}_flagged.txt")

        # content to look out for
        flagged_content = ["credit_card_cvv"]

        # Open the text file for writing
        with open(output_path, "w") as text_file:
            flagged_found = False
            # Loop through detected entities
            for entity in transcript.entities:
                if entity.entity_type in flagged_content :
                    text_file.write(f"Entity Detected: {entity.text}\n")
                    text_file.write(f"Entity Type: {entity.entity_type}\n")
                    text_file.write("\n")
                    flagged_found = True

            # If flagged entity is found, summarize the audio and add to the file
            if flagged_found:
                # Set summarization config
                summary_config = aai.TranscriptionConfig(
                    summarization=True,
                    summary_model=aai.SummarizationModel.informative,
                    summary_type=aai.SummarizationType.bullets
                )
                # Transcribe with summarization enabled
                summary_transcript = aai.Transcriber().transcribe(file_path, summary_config)

                text_file.write("\nSummary of the Audio:\n")
                text_file.write(summary_transcript.summary)  # Write the summary to the file

            # If no flagged entity is found, print in the terminal
            if not flagged_found:
                print(f"No 'credit_card_cvv' entity detected in {audio_file.filename}.")

        # Return success message
        return f"Flagged content (if any) has been saved to {output_path}", 200

    except Exception as e:
        return f"An error occurred: {str(e)}", 500

    finally:
        # Clean up temporary file
        os.remove(file_path)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
