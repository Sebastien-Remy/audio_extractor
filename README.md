# 🎵 Audio Extractor

A simple desktop application for extracting audio from online videos.

Paste a video URL, choose an audio format, and Audio Extractor handles the rest — without ad-filled converter websites, pop-ups, redirects or fake download buttons.

Available for **macOS, Windows and Linux**.

Built with **Python, PySide6, yt-dlp and FFmpeg**.

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

## 📥 Download

Pre-built versions of Audio Extractor are available for:

- 🍎 **macOS**
- 🪟 **Windows**
- 🐧 **Linux**

Go to the **Releases** section of this GitHub repository and download the latest version for your operating system.

### macOS

Download the macOS archive from the latest release, extract it and launch **Audio Extractor**.

Because the application is currently distributed outside the Mac App Store and is not notarized by Apple, macOS may display a security warning the first time you open it.

### Windows

Download the Windows archive from the latest release, extract it and launch **Audio Extractor**.

Windows SmartScreen may display a warning because the application is not currently code-signed.

### Linux

Download the Linux build from the latest release, extract it and run **Audio Extractor**.

Depending on your Linux distribution, you may need to make the downloaded file executable before launching it.

## 🛠️ Run from Source

If you prefer to run Audio Extractor directly from the source code, you need:

- Python 3
- [PySide6](https://pypi.org/project/PySide6/)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [FFmpeg](https://ffmpeg.org/)
- [curl_cffi](https://github.com/lexiforest/curl_cffi)

FFmpeg must be installed separately and available from your system PATH.

### Clone the repository

```bash
git clone YOUR_REPOSITORY_URL
cd audio_extractor
