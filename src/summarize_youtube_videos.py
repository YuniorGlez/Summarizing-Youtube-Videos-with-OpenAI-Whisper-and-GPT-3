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

def summarize_text(transcript, language, summary_type):
    system_prompt = "I would like for you to assume the role of a Life Coach"
    user_prompt = f"""Generate a {summary_type} summary of the text below in {language}.
    Text: {transcript}
    
    Add a title to the summary.

    Make sure your summary has useful and true information about the main points of the topic.
    Begin with a short introduction explaining the topic. If you can, use bullet points to list important details,
    and finish your summary with a concluding sentence"""
    
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
    youtube_url_prompt = {
        'English': "Please, enter the URL of the YouTube video you want to summarize: ",
        'Spanish': "Por favor, introduce la URL del video de YouTube que quieres resumir: ",
        'French': "Veuillez entrer l'URL de la vidéo YouTube que vous souhaitez résumer : ",
        'German': "Bitte geben Sie die URL des YouTube-Videos ein, das Sie zusammenfassen möchten: ",
        'Italian': "Per favore, inserisci l'URL del video di YouTube che vuoi riassumere: ",
    }
    YOUTUBE_VIDEO_URL = input(youtube_url_prompt[language_answer['language']])
    download_youtube_video(YOUTUBE_VIDEO_URL, OUTPUT_AUDIO)
    transcript = transcribe_audio(OUTPUT_AUDIO)
    
    summary = summarize_text(transcript, language_answer['language'], summary_type_answer['summary_type'])
    print(f'\n\n--------------------------\n{summary}')
    continue_prompt = {
        'English': "Do you want to summarize another video? (y/n): ",
        'Spanish': "¿Quieres resumir otro video? (s/n): ",
        'French': "Voulez-vous résumer une autre vidéo ? (o/n) : ",
        'German': "Möchten Sie ein weiteres Video zusammenfassen? (j/n): ",
        'Italian': "Vuoi riassumere un altro video? (s/n): ",
    }
    continue_answer = input(continue_prompt[language_answer['language']])
    return continue_answer.lower() == 'y'