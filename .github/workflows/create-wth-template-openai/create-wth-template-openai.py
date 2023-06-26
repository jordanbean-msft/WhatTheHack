import sys
import os
import json
import requests
import logging
import getopt
import argparse
import shutil

template_directory_name = "000-HowToHack"
openai_prompt_directory_name = "openai-prompts"

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION] [FILE]...",
        description="Create a new hackathon project from a template using OpenAI's API.")
    
    parser.add_argument("-c", "--number_of_challenges", help="Number of challenges to generate", type=int)
    parser.add_argument("-r", "--remove_existing_directory", help="Remove existing directory", action='store_true')
    parser.add_argument("-n", "--name_of_hack", help="Name of hackathon project", type=str)
    parser.add_argument("-p", "--path_to_hack", help="Path to hackathon project", type=str)
    parser.add_argument("-d", "--description_of_hack", help="Description of hackathon project", type=str)
    parser.add_argument("-k", "--keywords", help="Keywords for hackathon project", type=str)
    parser.add_argument("-e", "--openai_endpoint_uri", help="OpenAI endpoint URI (should include API version query parameter)", type=str)
    parser.add_argument("-a", "--openai_api_key", help="OpenAI API key", type=str)
    parser.add_argument("-v", "--verbose", help="Verbose logging", action='store_true')
    return parser

def get_openai_prompt_content(path_to_prompt_file) -> str:
    with open(path_to_prompt_file, "r") as file:
        promptText = file.read()
    return promptText

def generate_openai_message_array(system_content, user_prompt_content) -> list:
    message_array = [
      { 
        "role": "system", 
        "content": system_content
      }, 
      { 
        "role": "user", 
        "content": user_prompt_content
      }
    ]

    return message_array

def call_openai(message_array) -> str:
    data = { 
      "messages": message_array, 
      "max_tokens": 800, 
      "temperature": 0.7, 
      "top_p": 0.95, 
      "frequency_penalty": 0, 
      "presence_penalty": 0, 
      "stop": "Null" 
    }

    json_data = json.dumps(data)

    headers = { "Content-Type": "application/json", "api-key": f"{openai_api_key}" }

    request = requests.Request('POST', 
                               openai_endpoint_uri, 
                               headers=headers, 
                               data=json_data)
    prepared = request.prepare()

    s = requests.Session()
    openai_response = s.send(prepared)

    if(openai_response.status_code != 200):
        logging.error(f"OpenAI API call failed with status code: {openai_response.status_code}")
        logging.error(f"OpenAI API call failed with response: {openai_response.text}")
        logging.error(f"OpenAI API call failed with data: {openai_response.request.body}")

    json_data = json.loads(openai_response.text)

    content = json_data['choices'][0]['message']['content']

    return content

def create_directory_structure(delete_existing_directory):
    if delete_existing_directory:
        shutil.rmtree(root_path, 
                      ignore_errors=True)
    
    logging.info(f"Creating {root_path} directory...")
        
    # create the xxx-YetAnotherWth directory
    os.mkdir(root_path)

    logging.info(f"Creating {root_path}/Coach/Solutions directories...")
        
    # create the Coach & Coach/Solutions directories
    os.makedirs(f"{root_path}/Coach/Solutions")

    #add a file to allow git to store an "empty" directory
    open(f"{root_path}/Coach/Solutions/.gitkeep", 'w').close()

    # copying the Coach Lectures template file in the /Coach directory
    shutil.copy(f"{template_directory_name}/WTH-Lectures-Template.pptx", 
                f"{root_path}/Coach/Lectures.pptx")

    logging.info(f"Creating {root_path}/Student/Resources directories...")
        
    # create the Student & Student/Resources directories
    os.makedirs(f"{root_path}/Student/Resources")
    
    #add a file to allow git to store an "empty" directory
    open(f"{root_path}/Student/Resources/.gitkeep", 'w').close()


def write_markdown_file(path_to_prompt_file, openai_user_prompt, path_to_markdown_file) -> str:
    openai_system_prompt = get_openai_prompt_content(f"{path_to_prompt_file}")

    message_array = generate_openai_message_array(f"{openai_system_prompt}", 
                                                  f"{openai_user_prompt}")

    openai_response = call_openai(message_array)

    with open(path_to_markdown_file, "w") as file_object:
        file_object.write(openai_response)

    return openai_response

def create_hack_description(number_of_challenges) -> str:
    openai_response = write_markdown_file(f"{path_to_openai_prompt_directory}/WTH-Overview-Prompt.txt", 
                                          f"Generate a overview page of the hack based upon the following description: {description_of_hack}. Generate {number_of_challenges} challenges. Use the following keywords to help guide which challenges to generate: {keywords}", 
                                          f"{root_path}/README.md")

    return openai_response

def create_challenge_markdown_file(full_path, prefix, suffix_number) -> str:
    openai_response = write_markdown_file(f"{path_to_openai_prompt_directory}/WTH-Challenge-Prompt.txt", 
                                          f"Generate a student challenge page of the hack based upon challenge {suffix_number} in following description: {openai_hack_description}.", 
                                          f"{full_path}/{prefix}-{suffix_number:02d}.md")

    return openai_response

def create_solution_markdown_file(full_path, prefix, suffix_number, challenge_response) -> str:
    openai_response = write_markdown_file(f"{path_to_openai_prompt_directory}/WTH-Solution-Prompt.txt", 
                                          f"Generate a coach's guide solution page. It should be the step-by-step solution guide based upon the following challenge description: {challenge_response}", 
                                          f"{full_path}/{prefix}-{suffix_number:02d}.md")

    return openai_response

def create_challenge_and_solution(challenge_number):
    logging.info(f"Creating {root_path}/Challenge-{challenge_number:02d}.md...")
    
    challenge_response = create_challenge_markdown_file(f"{root_path}/Student", 
                                                        "Challenge", 
                                                        challenge_number)

    logging.info(f"Creating {root_path}/Solution-{challenge_number:02d}.md...")

    create_solution_markdown_file(f"{root_path}/Coach", 
                                  "Solution", 
                                  challenge_number, 
                                  challenge_response)

def create_coach_guide_markdown_file(full_path, number_of_solutions) -> str:
    logging.info(f"Creating {full_path}/README.md...")

    openai_response = write_markdown_file(f"{path_to_openai_prompt_directory}/WTH-Coach-Overview-Prompt.txt", 
                                          f"Generate a coach's guide overview page of the hack based upon the following description: {openai_hack_description}", 
                                          f"{full_path}/README.md")

    return openai_response

def create_challenges_and_solutions(number_of_challenges):
    for challenge_number in range(0, number_of_challenges + 1):
        create_challenge_and_solution(challenge_number)

    create_coach_guide_markdown_file(f"{root_path}/Coach", 
                                     number_of_challenges)

def main(argv):
    parser = init_argparse()
    args = parser.parse_args(argv)

    logging_levels = [logging.WARNING, logging.INFO, logging.DEBUG]
    level = logging_levels[min(args.verbose, len(logging_levels) - 1)]

    logging.basicConfig(level=level, 
                        format='%(asctime)s %(levelname)s %(message)s')

    wth_directory_name = f"xxx-{args.name_of_hack}"

    global verbosity
    verbosity = args.verbose

    global root_path
    root_path = f"{args.path_to_hack}/{wth_directory_name}"

    path_to_template_directory = f"{args.path_to_hack}/{template_directory_name}"

    global path_to_openai_prompt_directory
    path_to_openai_prompt_directory = f"{path_to_template_directory}/{openai_prompt_directory_name}"

    global description_of_hack
    description_of_hack = f"{args.description_of_hack}"

    global keywords
    keywords = f"{args.keywords}"

    global openai_endpoint_uri
    openai_endpoint_uri = f"{args.openai_endpoint_uri}"

    global openai_api_key
    openai_api_key = f"{args.openai_api_key}"

    create_directory_structure(args.remove_existing_directory)

    global openai_hack_description
    openai_hack_description = create_hack_description(args.number_of_challenges)

    create_challenges_and_solutions(args.number_of_challenges)

if __name__ == "__main__":
    main(sys.argv[1:])