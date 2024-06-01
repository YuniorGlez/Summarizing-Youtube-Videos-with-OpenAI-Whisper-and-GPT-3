from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.

from src.summarize_youtube_videos import boot

if __name__ == '__main__':
    while True:
        continue_summarizing = boot()
        if not continue_summarizing:
            break