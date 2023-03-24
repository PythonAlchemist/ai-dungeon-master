from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
from datasets import load_dataset
import torch
import sounddevice as sd

processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts")
vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")

text = "Hello everyone. My name is Matthew Mercer, voice actor and Dungeon Master for Critical Role and welcome to the first episode of the new series, Critical Role: The Legend of Vox Machina."
inputs = processor(text=text, return_tensors="pt")

# load xvector containing speaker's voice characteristics from a dataset
embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
speaker_embeddings = torch.tensor(embeddings_dataset[7305]["xvector"]).unsqueeze(0)
# speaker_embeddings = torch.tensor(embeddings_dataset[5000]["xvector"]).unsqueeze(0)

speech = model.generate_speech(inputs["input_ids"], speaker_embeddings, vocoder=vocoder)

sd.play(speech.numpy(), samplerate=16000, blocking=True)

# sf.write("speech.wav", speech.numpy(), samplerate=16000)
# #sph = AudioSegment.from_wav("speech.wav")
# sph = speech
# play(sph)