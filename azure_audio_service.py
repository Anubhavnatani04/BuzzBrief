import azure.cognitiveservices.speech as speechsdk
from supabase import create_client
from uuid import uuid4
import os
from dotenv import load_dotenv

load_dotenv()

# Load from environment (recommended)
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
SUPABASE_STORAGE_BUCKET = "audio-files"

# Azure credentials
speech_key = os.getenv("AZURE_SPEECH_KEY")
service_region = "centralindia" 

if not speech_key:
    raise ValueError("AZURE_SPEECH_KEY environment variable is not set. Please set it in your environment or .env file.")

if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY environment variables must be set. Please set them in your environment or .env file.")

# Initialize speech config
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
speech_config.speech_synthesis_voice_name = "en-IN-AnanyaNeural"  # Use neural voice

# Set output format to MP3 for speaker playback
speech_config.set_speech_synthesis_output_format(
    speechsdk.SpeechSynthesisOutputFormat.Audio16Khz128KBitRateMonoMp3
)

# Set up synthesizer to play audio through default speaker
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

def generate_audio_from_text(text: str) -> str:
    """Generate audio from text using Azure TTS, upload to Supabase, and return the public URL."""
    result = synthesizer.speak_text_async(text).get()
    if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
        raise Exception(f"TTS synthesis failed: {result.error_details}")

    audio_data = result.audio_data
    file_name = f"summary_{uuid4().hex}.mp3"

    # Directly use audio_data (bytes) instead of wrapping in BytesIO
    print(f"Audio data size: {len(audio_data)} bytes")

    # Upload raw bytes
    response = supabase.storage.from_(SUPABASE_STORAGE_BUCKET).upload(file_name, audio_data)
    if hasattr(response, 'error') and response.error:
        raise Exception(f"Upload failed: {response.error}")
    
    # Return public URL
    return supabase.storage.from_(SUPABASE_STORAGE_BUCKET).get_public_url(file_name)
