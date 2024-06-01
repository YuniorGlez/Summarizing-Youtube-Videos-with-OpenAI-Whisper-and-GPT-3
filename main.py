from dotenv import load_dotenv
from src.summarize_youtube_videos import boot
load_dotenv()  # take environment variables from .env.

if __name__ == '__main__':
    while True:
        boot()
        continue_prompt = input("Do you want to summarize another video? (y/n): ")
        if continue_prompt.lower() != 'y':
            break