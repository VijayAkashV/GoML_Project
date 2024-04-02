# Audio Analysis

Welcome! This Streamlit application provides insights and analysis on audio files, including call transcripts and call metrics.

## Features

- **File Uploader**: Upload either a folder containing audio files or a zip file containing audio files.
- **Silent Ratio Calculation**: Calculate the silence ratio for each audio file.
- **Overall Call Ratio**: Calculate the overall call ratio.
- **Transcription**: Transcribe audio files and provide insights such as First Call Resolution (FCR), Call Resolution Rate, Call Transfer Rate, and Error Rate.
- **Charts**: Visualize call data with interactive charts.

## Installation

1. Clone the repository:

2. Navigate to the project directory:

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Run the Streamlit app:

```bash
streamlit run app.py
```

2. Upload audio files either in a folder or zip format.
3. Explore the insights provided by the app!

## Requirements

- Python 3.6+
- Streamlit
- Pandas
- Matplotlib
- Seaborn
- Pydub
- Librosa
- Lyzr
- OpenAI's GPT API

## Credits

This project utilizes various libraries and APIs, including Streamlit, Pandas, Matplotlib, Seaborn, Pydub, Librosa, and OpenAI's GPT API.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
