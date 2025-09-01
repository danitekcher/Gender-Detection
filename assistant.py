import ollama
import csv

employees = []

def load_file(csv_file):
    global employees
    with open(csv_file, 'r', encoding='utf-8') as f:
        read = csv.reader(f)
        next(read)
        for row in read:
             if len(row) >= 2:
                 name = row[0].strip()
                 career = row[1].strip()
                 employees.append({'name': name, 'career': career})
     

def show_employees():
    return [f"{e['name']}_______{e['career']}" for e in employees]

def search_employee(name):
    for e in employees:
        if name.lower() == e['name'].lower():
            return f"{e['name']} --> {e['career']}"
    return f"No information found for {name}."

def gender_employee(name):
    # آماده کردن متن لیست کارمندان
    employees_text = "\n".join([f"{e['name']} - {e['career']}" for e in employees])
    
    # prompt به مدل
    prompt = f"""
    Here is our company employee list:
    {employees_text}
    
    Guess the gender of the employee named '{name}'.
    Answer only one word: 'male' or 'female'.
    """
    
    response = ollama.chat(
        model="llama3.2:3b",
        messages=[{'role': 'user', 'content': prompt}],
        options={'temperature': 0.0}
    )
    
    gender = response['message']['content'].strip().lower()
    return gender if gender in ['male', 'female'] else "unknown"

tools = [
    {
        "type": "function",
        "function": {
            "name": "show_employees",
            "description": "List all employees in the company",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_employee",
            "description": "Get career information about a person by their name",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Full name of the person"}
                },
                "required": ["name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "gender_employee",
            "description": "Get gender information about a person by their name",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Full name of the person"}
                },
                "required": ["name"]
            }
        }
    }
]

def process_with_tools(user_input):
    response = ollama.chat(
        model="llama3.2:3b",
        messages=[{"role": "user", "content": user_input}],
        tools=tools
    )

    message = response['message']
    tool_calls = message.get('tool_calls', [])

    if not tool_calls:
        return message.get('content', "No response.")

    outputs = []
    for call in tool_calls:
        func_name = call['function']['name']
        args = call['function'].get('arguments', {}) 

        if func_name == "show_employees":
            outputs.append("\n".join(show_employees()))
        elif func_name == "search_employee":
            name = args.get("name", "")
            outputs.append(search_employee(name))
        elif func_name == "gender_employee":
            name = args.get("name", "")
            outputs.append(gender_employee(name))
        else:
            outputs.append(f"Unknown tool: {func_name}")

    return "\n".join(outputs)

def main():
    csv_file = input("Enter CSV file path: ").strip()
    load_file(csv_file)

    while True:
        user_input = input("\nYour question (or type 'quit'): ").strip()
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("Goodbye! 😁")
            break

        response = process_with_tools(user_input)
        print("\nAI:", response)


if __name__ == "__main__":
    main()
