# PIT Podcast Transcription Service Uploader

This is how Productivity in Tech creates the initial transcript file. This is
not the final transcription, but the starting point for all transcriptions.

## Requirements

* [Python 3.8+](https://www.python.org/downloads/)
* Python Modules included in [requirements.txt]

## Optional
* virtual environment of some type. I'm using virtualenvwrapper
* direnv for auto loading and unloading of environment variables

## Instructions

1. Create a new virtual environment (Recommended but Optional) running.
2. Add your amazon environment variables.
  - example using aws key auth:
  ```
    export AWS_DEFAULT_REGION=Your_AWS_REGION **(NOTE: NOT ALL REGIONS SUPPORT AWS TRANSCRIBE)**
    export AWS_ACCESS_KEY_ID=your_access_key
    export AWS_SECRET_ACCESS_KEY=your_secret_key
    export BUCKET_NAME=your_s3_bucket
  ```
3. Upload your audio_file to amazon s3
  `python transcript.py upload-audio-file <filepath>`

4. Start your transcription
  `python transcript.py start-transcription --language en-US --speakers <number of speakers> <filename>`

5. Check your transcription and download your transcription job.
  `python transcript.py check-job <filename> --filepath <desired output
  filepath>`

  The transcriptions are asyncrhonous so you will need to check to see if it is
  complete.

  If the transcription **IS NOT** complete, the status of of the transcription will
  be returned.

  If the transcription **IS** complete, the transcription will be returned as text.
