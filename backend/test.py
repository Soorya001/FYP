import requests
import os
import time 
import json

API_TOKEN = "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"
API_URL = "https://api-inference.huggingface.co/models/openai/whisper-medium"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()

dir_path = '/home/soorya/Desktop/mp3_files/'

f = open("text.json")
data = json.load(f)

total_words = 0
total_errors = 0

for path in os.listdir(dir_path):

    print("filename: ", path)

    text = query((dir_path + path))['text']
    # time.sleep(1)

    if path not in data.keys():
        continue

    word_count1 = len(text.split())
    word_count2 = len(data[path].split())

    total_words += (word_count2)

    total_errors += abs(word_count1 - word_count2)

    words1 = text.split()
    words2 = data[path].split()

    for i in range(min(word_count2, word_count1)):
        if (words1[i]).lower() != (words2[i]).lower():
            total_errors += 1


    # print(data[path], text, total_errors)
    print(total_words, total_errors)

print('total words: ', total_words)
print('total errors: ', total_errors)
print(total_errors/total_words)
