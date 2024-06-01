# YouTube Video Summarizer with OpenAI Whisper and GPT

This Python script allows you to summarize YouTube videos using OpenAI's Whisper for audio transcription and GPT for generating concise video summaries. The pipeline involves downloading a YouTube video's audio, transcribing it with Whisper, and then generating a summary using GPT. Additionally, it allows users to ask questions about the video, which are answered based on the video's transcript.

## Prerequisites

Before you begin, ensure you have the necessary Python libraries and an OpenAI API key:

- Python (>=3.6)
- The necessary libraries are listed in the `requirements.txt` file. You can install them with `pip install -r requirements.txt`.

You should also set up your OpenAI API key as an environment variable in a `.env` file. The `.env` file should be in the root of the project and should contain the following variables:

```env
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=your_openai_model
```

## Usage

- Set up your OpenAI API key as an environment variable in a `.env` file.
- Install the required Python libraries using `pip install -r requirements.txt`.
- Run the script using `python main.py`.

## Contributions

This is an open-source project and contributions are welcome. If you have any improvements or features you'd like to add, feel free to fork the repository and submit a pull request.