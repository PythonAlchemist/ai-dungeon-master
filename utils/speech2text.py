import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import torch
import librosa
from datasets import load_dataset
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor

LANG_ID = "en"
MODEL_ID = "jonatasgrosman/wav2vec2-large-xlsr-53-english"
SAMPLES = 10

Live = False
if Live:
    # Record Live Audio

    fs=44100
    duration = 3  # seconds
    print("Recording Audio")
    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1,dtype='float64', blocking=True)
    sd.play(myrecording, fs, blocking=True)
else:
    # Read Audio File
    fs, myrecording = wav.read("speech.wav")


# Transcribe Audio
test_dataset = load_dataset("common_voice", LANG_ID, split=f"test[:{SAMPLES}]")

processor = Wav2Vec2Processor.from_pretrained(MODEL_ID)
model = Wav2Vec2ForCTC.from_pretrained(MODEL_ID)

# Preprocessing the datasets.
# We need to read the audio files as arrays
def speech_file_to_array_fn(batch):
    speech_array, sampling_rate = librosa.load(batch["path"], sr=16_000)
    batch["speech"] = speech_array
    batch["sentence"] = batch["sentence"].upper()
    return batch

test_dataset = test_dataset.map(speech_file_to_array_fn)
inputs = processor(test_dataset["speech"], sampling_rate=16_000, return_tensors="pt", padding=True)

with torch.no_grad():
    logits = model(inputs.input_values, attention_mask=inputs.attention_mask).logits

predicted_ids = torch.argmax(logits, dim=-1)
predicted_sentences = processor.batch_decode(predicted_ids)

for i, predicted_sentence in enumerate(predicted_sentences):
    print("-" * 100)
    print("Reference:", test_dataset[i]["sentence"])
    print("Prediction:", predicted_sentence)



# from huggingsound import SpeechRecognitionModel

# model = SpeechRecognitionModel("jonatasgrosman/wav2vec2-large-xlsr-53-english")
# audio_paths = ["/path/to/file.mp3", "/path/to/another_file.wav"]

# transcriptions = model.transcribe(audio_paths)