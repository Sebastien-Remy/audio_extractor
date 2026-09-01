import os
import shutil
import tempfile
from pathlib import Path
from typing import Callable

import yt_dlp
from yt_dlp.utils import sanitize_filename


SUPPORTED_FORMATS = {"mp3", "m4a", "wav"}

ProgressCallback = Callable[[int], None]
StatusCallback = Callable[[str], None]


def get_unique_path(path: Path) -> Path:
    if not path.exists():
        return path

    counter = 1

    while True:
        candidate = path.with_name(
            f"{path.stem} ({counter}){path.suffix}"
        )

        if not candidate.exists():
            return candidate

        counter += 1


def move_without_overwrite(
    source: Path,
    destination: Path,
) -> Path:
    candidate = destination

    while True:
        try:
            # The temporary directory is created inside the destination
            # folder, so both files are normally on the same filesystem.
            os.link(source, candidate)
            source.unlink()

            return candidate

        except FileExistsError:
            candidate = get_unique_path(candidate)

        except OSError:
            # Fallback for filesystems where hard links are unavailable.
            candidate = get_unique_path(candidate)

            try:
                with source.open("rb") as source_file:
                    with candidate.open("xb") as destination_file:
                        shutil.copyfileobj(
                            source_file,
                            destination_file,
                        )

                source.unlink()

                return candidate

            except FileExistsError:
                continue


def extract_audio(
    url: str,
    audio_format: str,
    output_folder: str,
    progress_callback: ProgressCallback | None = None,
    status_callback: StatusCallback | None = None,
) -> Path:
    audio_format = audio_format.lower()

    if audio_format not in SUPPORTED_FORMATS:
        raise ValueError(
            f"Unsupported audio format: {audio_format}"
        )

    output_path = Path(output_folder)
    output_path.mkdir(
        parents=True,
        exist_ok=True,
    )

    # Get the video metadata without downloading anything.
    metadata_options = {
        "quiet": True,
        "noplaylist": True,
    }

    with yt_dlp.YoutubeDL(metadata_options) as ydl:
        info = ydl.extract_info(
            url,
            download=False,
        )

    title = info.get("title") or "audio"

    # Make sure the video title can safely be used as a filename.
    safe_title = sanitize_filename(title)

    final_path = get_unique_path(
        output_path / f"{safe_title}.{audio_format}"
    )

    def progress_hook(data: dict) -> None:
        status = data.get("status")

        if status == "downloading":
            if status_callback is not None:
                status_callback("downloading")

            if progress_callback is None:
                return

            downloaded = data.get(
                "downloaded_bytes",
                0,
            )

            total = (
                data.get("total_bytes")
                or data.get("total_bytes_estimate")
            )

            if not total:
                return

            progress = int(
                downloaded * 100 / total
            )

            progress = max(
                0,
                min(progress, 100),
            )

            progress_callback(progress)

        elif status == "finished":
            # yt-dlp has finished downloading the source file.
            # FFmpeg post-processing starts after this point.
            if status_callback is not None:
                status_callback("converting")

    # Work inside our own temporary directory.
    # It is automatically removed when this block ends.
    with tempfile.TemporaryDirectory(
        prefix=".audio_extractor_",
        dir=output_path,
    ) as temporary_directory:
        temporary_path = Path(
            temporary_directory
        )

        options = {
            "format": "bestaudio/best",
            "outtmpl": str(
                temporary_path / "audio.%(ext)s"
            ),
            "noplaylist": True,
            "progress_hooks": [
                progress_hook,
            ],
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": audio_format,
                }
            ],
        }

        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([url])

        converted_file = (
            temporary_path
            / f"audio.{audio_format}"
        )

        if not converted_file.exists():
            raise RuntimeError(
                "The converted audio file could not be found."
            )

        return move_without_overwrite(
            converted_file,
            final_path,
        )
