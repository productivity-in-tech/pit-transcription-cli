"""
This is the Amazon S3 information from the project.
Any sensitive data is stored in the environment variables and not in this file.
"""
from pathlib import Path
from transcriptor import amazon

import typer
import boto3
import os

bucket = os.environ.get("BUCKET_NAME", True)
storage = boto3.client("s3")
transcribe=boto3.client('transcribe')

app = typer.Typer()

@app.command()
def upload_audio_file(filename):
    filepath = Path(filename)
    return storage.upload_file(filename, Bucket=bucket, Key=filepath.name)


@app.command()
def start_transcription(
        key: str,
        *,
        language: str='en-US',
        speakers: int=0
        storage=storage,
        transcribe=transcribe,
        bucket=bucket,
):
    transcribe_job_uri = f"{storage.meta.endpoint_url}/{bucket}/{key}"
    if speakers:
        settings = {
            "ShowSpeakerLabels": True,
            "MaxSpeakerLabels": 5,
            }
    else:
        settings = {}

    transcribe.start_transcription_job(
        TranscriptionJobName=key,
        Media={"MediaFileUri": transcribe_job_uri},
        MediaFormat=Path(key).suffix[1:],
        LanguageCode=language,
        Settings=settings,
    )
    return key


def check(key:str):
    job = transcribe.get_transcription_job(TranscriptionJobName=key)
    return job['TranscriptionJob']['TranscriptionJobStatus']


@app.command()
def check_job(key:str, filepath: str = 'results.txt'):
    if (status:=check(key)) != 'COMPLETED':
        return typer.echo(status)

    t = amazon.from_job(key)

    with open(filepath, 'w') as f:
        f.write(t.as_text())

    return typer.echo(f'Job Completed - Transcription copied to {filepath}')


def get_job(key:str):
    return transcribe.get_transcription_job(TranscriptionJobName=key)


if __name__ == "__main__":
    app()
