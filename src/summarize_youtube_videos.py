import os
from pytube import YouTube
from openai import OpenAI
from pathlib import Path
import inquirer

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_MODEL = os.getenv('OPENAI_MODEL')
OUTPUT_AUDIO = Path(__file__).resolve().parent.parent.joinpath('data', 'podcast.webm')

client = OpenAI(api_key=OPENAI_API_KEY)

def download_youtube_video(url, output_audio):
    youtube_video = YouTube(url)
    streams = youtube_video.streams.filter(only_audio=True, file_extension='webm').order_by('abr').asc()
    stream = streams.first()
    stream.download(filename=output_audio)

def transcribe_audio(file_path):
    audio_file= open(file_path, "rb")
    response = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file,
        timestamp_granularities=["segment"]
    )
    return response.text

def summarize_text(transcript):
    system_prompt = "I would like for you to assume the role of a Life Coach"
    user_prompt = f"""Generate a concise summary of the text below.
    Text: {transcript}
    
    Add a title to the summary.

    Make sure your summary has useful and true information about the main points of the topic.
    Begin with a short introduction explaining the topic. If you can, use bullet points to list important details,
    and finish your summary with a concluding sentence"""
    
    print('summarizing ... ')
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_prompt}
        ],
        max_tokens=4096,
        temperature=1
    )
    
    summary = response.choices[0].message.content
    return summary

def boot():
    language_question = [
        inquirer.List('language',
                      message="What language do you prefer for the summaries?",
                      choices=['English', 'Spanish', 'French', 'German', 'Italian'],
                      ),
    ]
    language_answer = inquirer.prompt(language_question)

    summary_type_question = {
        'English': "What type of summary do you prefer?",
        'Spanish': "¿Qué tipo de resumen prefieres?",
        'French': "Quel type de résumé préférez-vous?",
        'German': "Welche Art von Zusammenfassung bevorzugen Sie?",
        'Italian': "Che tipo di riassunto preferisci?",
    }

    summary_type_choices = {
        'English': ['With lists', 'Very short', 'More extensive', 'Formal', 'Informal'],
        'Spanish': ['Con listas', 'Muy cortos', 'Más extensos', 'Formales', 'Informales'],
        'French': ['Avec des listes', 'Très court', 'Plus étendu', 'Formel', 'Informel'],
        'German': ['Mit Listen', 'Sehr kurz', 'Umfangreicher', 'Formell', 'Informell'],
        'Italian': ['Con liste', 'Molto corto', 'Più esteso', 'Formale', 'Informale'],
    }

    summary_type_question = [
        inquirer.List('summary_type',
                      message=summary_type_question[language_answer['language']],
                      choices=summary_type_choices[language_answer['language']],
                      ),
    ]
    summary_type_answer = inquirer.prompt(summary_type_question)

    print(language_answer, summary_type_answer)
    YOUTUBE_VIDEO_URL = input("Please, enter the URL of the YouTube video you want to summarize: ")
    download_youtube_video(YOUTUBE_VIDEO_URL, OUTPUT_AUDIO)
    transcript = transcribe_audio(OUTPUT_AUDIO)
    summary = summarize_text(transcript)
    print(f'Summary for the Youtube Video:\n{summary}')