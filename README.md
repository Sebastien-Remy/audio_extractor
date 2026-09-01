# 🎵 Audio Extractor

A simple desktop application for extracting audio from online videos.

Paste a video URL, choose an audio format, and Audio Extractor handles the rest — without ad-filled converter websites, pop-ups, redirects or fake download buttons.

Built with Python, PySide6, yt-dlp and FFmpeg.

## ✨ Features

- Simple desktop interface
- Extract audio from online videos
- Choose between **MP3**, **M4A**, and **WAV**
- Download progress indicator
- Conversion status
- Choose where extracted files are saved
- Files are never silently overwritten
- Open the destination folder directly from the application
- No API key
- No account
- No subscription

Tested with:

- YouTube
- TikTok
- Instagram

## 📋 Requirements

- Python 3
- [PySide6](https://pypi.org/project/PySide6/)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [FFmpeg](https://ffmpeg.org/)
- [curl_cffi](https://github.com/lexiforest/curl_cffi)

FFmpeg must be installed separately and available from your system PATH.

## 🚀 Installation

Clone the repository:

```bash
git clone YOUR_REPOSITORY_URL
cd audio_extractor
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it on macOS or Linux:

```bash
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

### Install FFmpeg

#### macOS

Using Homebrew:

```bash
brew install ffmpeg
```

#### Windows

Using WinGet:

```bash
winget install Gyan.FFmpeg
```

#### Ubuntu / Debian

```bash
sudo apt install ffmpeg
```

Check that FFmpeg is available:

```bash
ffmpeg -version
```

## ▶️ Usage

Start the application:

```bash
python main.py
```

Then:

1. Paste a YouTube, TikTok or Instagram video URL.
2. Choose MP3, M4A or WAV.
3. Choose the destination folder if necessary.
4. Click **Extract Audio**.
5. Wait for the download and conversion to complete.

The application displays download progress and indicates when FFmpeg is converting the audio.

## 🔒 File Safety

Audio Extractor does not overwrite an existing audio file.

If a file with the same name already exists, a new filename is automatically generated:

```text
My Video.mp3
My Video (1).mp3
My Video (2).mp3
```

Downloads and conversions are performed inside a temporary working directory before the finished file is moved to its destination.

## ⚠️ A Note About Copyright

This project provides a tool — not ownership of somebody else's content.

Only download content you own, content you have permission to download, or material whose licence allows it.

Copyright and the terms of the platforms you use still apply.

## 🧪 Project Status

### v0.1 — First functional version

This is an early version of Audio Extractor.

The core workflow is functional:

- video URL input
- MP3, M4A and WAV output
- background extraction without freezing the interface
- download progress
- conversion status
- safe file handling
- configurable destination folder

## 📄 License

MIT
