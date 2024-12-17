# Grandma Stop (Scam Call Detection System)

## Overview
This project was developed at AssemblyAI's hackathon and aims to safeguard vulnerable individuals, such as seniors, from scams over phone calls. It utilizes **AssemblyAI**'s robust transcription and content safety features to analyze audio conversations, detect sensitive keywords (e.g., bank details, CVV), and generate a summary of the flagged content.

## Key Features
- **Keyword Detection**: Identifies sensitive entities in audio conversations like `credit_card_cvv`.
- **Content Summarization**: Summarizes the conversation into bullet points for quick understanding.

## How It Works
1. **Audio Upload**: Users upload an audio file via the Flask backend.
2. **Transcription**: The audio is transcribed using AssemblyAI with content safety and entity detection enabled.
3. **Entity Detection**: Sensitive entities like `credit_card_cvv` are flagged.
4. **Output**: The flagged content and summary are saved in a text file for review.

## Installation
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory with your AssemblyAI API key:
   ```env
   ASSEMBLYAI_API_KEY=your_api_key_here
   ```
4. Run the Flask app:
   ```bash
   python app.py
   ```
5. Test the app using the provided `test.py` script:
   ```bash
   python test.py
   ```

## Future Improvements
In the future, the goal is to have the phone call summary sent automatically if flagged content is detected, eliminating the need for manual uploads.