from openai import OpenAI
import google.generativeai as genai

#setting up API models
client = OpenAI(api_key='')
genai.configure(api_key='')
config = genai.GenerationConfig(temperature=0.0)
model = genai.GenerativeModel('gemini-pro', 
                              generation_config=config
                              )
#Comment out second argument for default temperature value, include for 0 temperature value
title = ""
conversation_history = []
subjects = 100
#number of AI subjects/repetitions
type = 0
#For ChatGPT 3.5-turbo type = 0, ChatGPT 4.0 type = 1, Gemini type = 2

def chat_with_gpt(prompt, model):
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
            model= model, 
            temperature=0,
            #This temperature parameter impacts the variance of responses. Valid Range: 0-2 where 0 is most determinastic and 2 is least determinastic. Comment out for default temperature value.
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=150
            #maximum amount of tokins that can be generated in the chat, this will limit the reponse to the number of tokens given, Integer Value.
        )
        add_to_history = response.choices[0].message.content
        conversation_history.append(prompt)
        conversation_history.append(add_to_history)
        #adds both the prompt and response to a variable saving conversation history
        return response.choices[0].message.content
    except Exception as e:
        print("Error:", e)
        return None

def chat_with_gemini(prompt):
    """
    Inputs a prompt to Gemini and returns the text response.

    Args:
        prompt (str): prompt being inputed for chat.

    Returns: 
        str: response given by AI
    """
    global conversation_history
    try:
        response = model.generate_content(prompt)
        text_response = response.text
        conversation_history.append(prompt)
        conversation_history.append(text_response)
        #adds both the prompt and response to a variable saving conversation history
        return text_response
    except Exception as e:
        print("Error:", e)
        return None

def conduct_experiment():
    """
    Creates all three prompts of the sequence and inputs them to the LLM. Adds data from each prompt to an individual text file for later analysis.

    Args: None

    Returns: None
    """
    global conversation_history
    prompt_1 = ""
    prompt_2_new_message = ""
    prompt_3_new_message = ""
    #Enter the three prompts depending on the order of the sequence.  
    for repetitions in range(subjects):
        conversation_history = []
        if type == 0:
            response_1 = chat_with_gpt(prompt_1, "gpt-3.5-turbo")
        elif type == 1:
            response_1 = chat_with_gpt(prompt_1, "gpt-4")
        else:
            response_1 = chat_with_gemini(prompt_1)
        prompt_2 = str(conversation_history) + " " + prompt_2_new_message
        print(prompt_2)
        if response_1:
            data = open("Data_1.txt", 'a')
            data.write(response_1 + '\n')
            data.close()
        else:
            print("Failed to get a response from GPT")
        #writes data in a text file and returns an error if there is no response
        conversation_history = []
        #resets conversation history variable for the next prompt
        if type == 0:
            response_2 = chat_with_gpt(prompt_2, "gpt-3.5-turbo")
        elif type == 1:
            response_2 = chat_with_gpt(prompt_2, "gpt-4")
        else:
            response_2 = chat_with_gemini(prompt_2)
        prompt_3 = str(conversation_history) + " " + prompt_3_new_message
        print(prompt_3)
        if response_2:
            data = open("Data_2.txt", 'a')
            data.write(response_2 + '\n')
            data.close()
        else:
            print("Failed to get a response from GPT")
        conversation_history = []
        if type == 0:
            response_3 = chat_with_gpt(prompt_3, "gpt-3.5-turbo")
        elif type == 1:
            response_3 = chat_with_gpt(prompt_3, "gpt-4")
        else:
            response_3 = chat_with_gemini(prompt_3)
        if response_3:
            data = open("Data_3.txt", 'a')
            data.write(response_3 + '\n')
            data.close()
        else:
            print("Failed to get a response from GPT")

def analyze(stakes, number, file):
    """
    Analyzes an individual data file and prints analysis into a seperate text file

    Args:
        stakes (int): The stakes of the game for this prompt in the sequence (ex. 100)
        number (int): This prompt's place in the order of the sequence (1, 2, or 3)
        file (str): The file the data was saved to that you wish to analyze

    Returns: None
    """
    strategy_a = 0
    strategy_b = 0
    error = 0
    stakes_vector = []
    stakes_responses = []
    repetitions = subjects
    with open(file) as data:
        for reps in range(repetitions):
            strategy = data.readline().strip()
            if strategy in {'a', "'a'", "A", "'A'", '[A]', '[a]', '["A"]', "['A']", "[A", "A]", "['a']", "['A'", "'A']", "[a", "a]", "['a'", "'a']"}:
                strategy_a += 1
                stakes_responses.append(1)
                stakes_vector.append(stakes)
            elif strategy in {'b', "'b'", "B", "'B'", '[B]', '[b]', '["B"]', "['B']", "[B", "B]", "['b']", "['B'", "'B']", "[b", "b]", "['b'", "'b']"}:
                strategy_b += 1
                stakes_responses.append(0)
                stakes_vector.append(stakes)
            else:
                error += 1
    total = strategy_a + strategy_b
    strategy_a_percent = strategy_a/total * 100
    strategy_b_percent = strategy_b/total * 100
    a_percent_string = str(strategy_a_percent)
    strategy_a_string = str(strategy_a)
    error_string = str(error)
    stakes_vector_string = str(stakes_vector)
    stakes_responses_string = str(stakes_responses)
    number_string = str(number)
    with open("results.txt", 'a') as findings:
        findings.write('\n' + title + '\n' + "Stakes " + number_string + " Results" + '\n' + "# of Strategy A: " + strategy_a_string + '\n' + "Percent of Strategy A: " + a_percent_string + '\n' + "Errors: " + error_string + '\n' + '\n' + stakes_vector_string + '\n' + '\n' + stakes_responses_string)

def main():
    conduct_experiment()
    analyze(100, 1, "Data_1.txt")
    analyze(400, 3, "Data_2.txt")
    analyze(200, 2, "Data_3.txt")
    #analyze data from each stake based on order

main()