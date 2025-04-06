import boto3
import constants as cnst
from os.path import basename, join
import uuid
import time
import os
import json

def extract_data_frm_transcript(transcript_file):
    with open(transcript_file, 'r') as file:
        data = json.load(file)
        return data["results"]["transcripts"][0]["transcript"]

def get_diarized_transcript(audio_path):
    run_id = str(uuid.uuid4())
    audio_key=basename(audio_path)
    s3 = boto3.resource('s3')
    bucketobj = s3.Bucket(cnst.bucket)
    bucketobj.upload_file(Key=audio_key, Filename=audio_path)
    transcribe = boto3.client('transcribe', cnst.region)
    job_name = f"job-{cnst.unique_id}-{run_id}"
    job_uri = "s3://rabbit-bucket-vivek/" + audio_key
    transcribe.start_transcription_job(
        TranscriptionJobName = job_name,
        Media = {
            'MediaFileUri': job_uri
        },
        OutputBucketName = cnst.bucket,
        OutputKey = cnst.unique_id + '/', 
        LanguageCode = 'en-US', 
        Settings = {
            'ShowSpeakerLabels': True,
            'MaxSpeakerLabels': 5
        }    
    )
    
    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName = job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
        print("Not ready yet...")
        time.sleep(5)
    print(status)
    
    transcript_file=join(cnst.base_dir, run_id+"_transcription.json")
    if os.path.exists(transcript_file):
        os.remove(transcript_file)
    bucketobj.download_file(Key=cnst.unique_id+"/"+f"{job_name}.json", 
                            Filename=transcript_file)
    return extract_data_frm_transcript(transcript_file)

def tts(text):
    run_id = str(uuid.uuid4())
    polly_client = boto3.client('polly', region_name='us-east-1')  # Corrected AWS region
    
    response = polly_client.synthesize_speech(
        Engine="neural",
        Text=text,
        OutputFormat='mp3',
        VoiceId='Joanna'  # Specify voice to use
    )

    audio_file = join(cnst.base_dir,run_id+'_output.mp3')
    with open(audio_file, 'wb') as file:
        file.write(response['AudioStream'].read())
        
    return audio_file