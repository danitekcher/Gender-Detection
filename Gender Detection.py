import ollama
import sys

def namesfile(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            names_text = f.read()
            if not names_text.strip():
                print(f"Error")
                return
    except FileNotFoundError:
        print(f"Error The file not found")
        return
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return

    prompt = f"""
You are an expert name classifier. Your task is to classify the following list of names into 'male' and 'female' categories.
Some names might be unisex; place them in the category they are most commonly associated with.
Provide the output ONLY in the following format, with no extra text, explanations, or introductions:

male:
[name1]
[name2]
...

female:
[name3]
[name4]
...

Here is the list of names to classify:
---
{names_text}
---
"""
    try:
        client = ollama.Client(
            host='http://localhost:11434',
            proxies=None
        )

        response = client.chat(
            model='llama3.2',
            messages=[
                {
                    'role': 'user',
                    'content': prompt,
                },
            ],
            options={
                'temperature': 0.0
            }
        )

        classinames = response['message']['content']
        print(classinames.strip())

    except Exception as e:
        print(f"the procese failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    input_file = "namelist.txt"
    namesfile(input_file)
