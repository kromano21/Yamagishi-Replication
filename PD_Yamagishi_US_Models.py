from openai import OpenAI
import os
import csv
import google.generativeai as genai

client = OpenAI(api_key='') #Insert API Key
conversation_history = []
subjects = 100

def chat_with_gpt(prompt):
    """
    Inputs a prompt to ChatGPT and returns the text response.

    Args:
        prompt (str): prompt being inputed for chat.
        model (str): code for model being used (Use "gpt-3.5-turbo" for 3.5 and "gpt-4" for 4.0).

    Returns: 
        str: response given by AI
    """
    global conversation_history
    try:
        response = client.chat.completions.create(
            model= "deepseek-reasoner", 
            #temperature=0, #Alter Temperature parameter here
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=150
        )
        reasoning_content = response.choices[0].message.reasoning_content
        reasoning_return = open("", 'a') #Save Reasoning Content here
        reasoning_return.write(reasoning_content + '\n \n \n')
        reasoning_return.close()
        add_to_history = response.choices[0].message.content
        conversation_history.append(prompt)
        conversation_history.append(add_to_history)
        return response.choices[0].message.content
    except Exception as e:
        print("Error:", e)

def chat_with_gemini(prompt):
    global model
    try:
        response = model.generate_content(prompt)
        text_response = response.text.strip()
        return text_response
    except Exception as e:
        print("Error:", e)
        return None
    
def get_ai_response(prompt):
    while True:
        response = chat_with_gpt(prompt)
        #response = chat_with_gemini(prompt)
        if response:
            return response
        else:
            print("Failed to get response from the AI 1")

def conduct_experiment(stakes_1, stakes_2, stakes_3, sequence, framing, temperature):
    global model
    global master_list
    global conversation_history

    genai.configure(api_key='') #Insert Your API Key
    config = genai.GenerationConfig(temperature=0.0)
    if temperature == 0:
        model = genai.GenerativeModel('gemini-1.5-pro', generation_config=config)
    else:
        model = genai.GenerativeModel('gemini-1.5-pro')
    
    prompt_1 = "" #Prompt 1
    prompt_2_new_message = "" #Prompt 2
    prompt_3_new_message = "" #Prompt 3
    #Enter the three prompts depending on the order of the sequence.  
    for repetitions in range(subjects):
        conversation_history = []
        individual_list = []
        response_1 = get_ai_response(prompt_1).strip()
        individual_list.append(stakes_1)
        if response_1 in {'a', "'a'", "A", "'A'", '[A]', '[a]', '["A"]', "['A']", "[A", "A]", "['a']", "['A'", "'A']", "[a", "a]", "['a'", "'a']"}:
            individual_list.append(1)
        elif response_1 in {'b', "'b'", "B", "'B'", '[B]', '[b]', '["B"]', "['B']", "[B", "B]", "['b']", "['B'", "'B']", "[b", "b]", "['b'", "'b']"}:
            individual_list.append(0)
        else:
            print("ERROR")
        individual_list.append("") #Insert model here
        individual_list.append(sequence)
        individual_list.append(1)
        individual_list.append(framing)
        individual_list.append(temperature)
        master_list.append(individual_list)
        prompt_2 = str(conversation_history) + " " + prompt_2_new_message
        print(prompt_2)
        conversation_history = []
        individual_list = []
        individual_list.append(stakes_2)
        response_2 = get_ai_response(prompt_2).strip()
        if response_2 in {'a', "'a'", "A", "'A'", '[A]', '[a]', '["A"]', "['A']", "[A", "A]", "['a']", "['A'", "'A']", "[a", "a]", "['a'", "'a']"}:
            individual_list.append(1)
        elif response_2 in {'b', "'b'", "B", "'B'", '[B]', '[b]', '["B"]', "['B']", "[B", "B]", "['b']", "['B'", "'B']", "[b", "b]", "['b'", "'b']"}:
            individual_list.append(0)
        else:
            print("ERROR")
        individual_list.append("") #Insert Model Here
        individual_list.append(sequence)
        individual_list.append(2)
        individual_list.append(framing)
        individual_list.append(temperature)
        master_list.append(individual_list)
        prompt_3 = str(conversation_history) + " " + prompt_3_new_message
        print(prompt_3)
        conversation_history = []
        individual_list = []
        individual_list.append(stakes_3)
        response_3 = get_ai_response(prompt_3).strip()
        if response_3 in {'a', "'a'", "A", "'A'", '[A]', '[a]', '["A"]', "['A']", "[A", "A]", "['a']", "['A'", "'A']", "[a", "a]", "['a'", "'a']"}:
            individual_list.append(1)
        elif response_3 in {'b', "'b'", "B", "'B'", '[B]', '[b]', '["B"]', "['B']", "[B", "B]", "['b']", "['B'", "'B']", "[b", "b]", "['b'", "'b']"}:
            individual_list.append(0)
        else:
            print("ERROR")
        individual_list.append("") #Insert Model Here
        individual_list.append(sequence)
        individual_list.append(3)
        individual_list.append(framing)
        individual_list.append(temperature)
        master_list.append(individual_list)

def main():
    global master_list
    master_list = []
    column_list = ["Stakes", "Response", "Model", "Sequence", "Order_in_Sequence", "Framing", "Temperature"]
    master_list.append(column_list)
    #conduct_experiment(100, 400, 200, 4, 3, 1)

    file_path = ""

    file_exists_one = os.path.isfile(file_path)

    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)

        if not file_exists_one:
            writer.writerow(master_list[0])
        
        writer.writerows(master_list[1:])

main()