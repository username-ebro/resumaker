"""Transcription Service - Convert audio to text using Gemini"""

import google.generativeai as genai
import os
import subprocess
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

class TranscriptionService:
    def __init__(self):
        # Use gemini-2.0-flash-exp for audio transcription (same model as OCR service)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')

    async def transcribe_audio(self, audio_file_path: str) -> str:
        """
        Transcribe audio file to text using Gemini

        Args:
            audio_file_path: Path to the audio file

        Returns:
            Transcribed text
        """
        wav_path = None
        try:
            # Convert WebM to WAV (Gemini prefers WAV format)
            wav_path = audio_file_path.replace('.webm', '.wav')
            print(f"Converting {audio_file_path} to WAV format...")

            # Use ffmpeg to convert (should already be available on macOS)
            result = subprocess.run(
                ['ffmpeg', '-i', audio_file_path, '-ar', '16000', '-ac', '1', wav_path, '-y'],
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                print(f"FFmpeg conversion failed: {result.stderr}")
                # Fall back to original file
                upload_path = audio_file_path
            else:
                print(f"Successfully converted to WAV: {wav_path}")
                upload_path = wav_path

            # Upload audio file to Gemini Files API
            print(f"Uploading audio file to Gemini: {upload_path}")
            audio_file = genai.upload_file(path=upload_path)

            print(f"File uploaded: {audio_file.name}, state: {audio_file.state.name}")

            # Wait for file to be processed
            import time
            while audio_file.state.name == "PROCESSING":
                print("Waiting for file processing...")
                time.sleep(1)
                audio_file = genai.get_file(audio_file.name)

            if audio_file.state.name == "FAILED":
                raise Exception("Audio file processing failed")

            # Generate transcription
            prompt = """
            Please transcribe this audio recording accurately.
            Return ONLY the transcribed text, nothing else.
            Do not add any commentary or formatting.
            """

            print("Generating transcription...")
            response = self.model.generate_content([audio_file, prompt])

            # Clean up uploaded file from Gemini
            genai.delete_file(audio_file.name)
            print("Transcription complete")

            return response.text.strip()

        except Exception as e:
            print(f"Transcription error details: {type(e).__name__}: {str(e)}")
            raise Exception(f"Gemini transcription failed: {str(e)}")

        finally:
            # Clean up WAV file if it was created
            if wav_path and os.path.exists(wav_path):
                os.remove(wav_path)

# Singleton
transcription_service = TranscriptionService()
