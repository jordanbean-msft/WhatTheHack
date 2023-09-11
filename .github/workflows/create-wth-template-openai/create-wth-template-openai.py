import sys
import os
import logging
import argparse
import shutil
import asyncio
from what_the_hack_openai import *

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
    parser.add_argument("-m", "--openai_model_name", help="OpenAI model name", type=str)
    parser.add_argument("-b", "--openai_embedding_model_name", help="OpenAI embedding model name", type=str)
    parser.add_argument("-e", "--openai_endpoint_uri", help="OpenAI endpoint URI (should include API version query parameter)", type=str)
    parser.add_argument("-a", "--openai_api_key", help="OpenAI API key", type=str)
    parser.add_argument("-i", "--application_insights_key", help="Application Insights key", type=str)
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

async def call_openai(function, variables):
    result = await kernel.run_async(function, input_context=context, input_vars=variables)

    return result

def create_directory_structure(delete_existing_directory):
    if delete_existing_directory:
        shutil.rmtree(root_path, 
                      ignore_errors=True)
    
    logging.info(f"Creating {root_path} directory...")
        
    # create the xxx-YetAnotherWth directory
    os.makedirs(root_path)

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


async def write_markdown_file(function_name, variables, path_to_markdown_file):
    what_the_hack_plugin = plugins[what_the_hack_plugin_name]
    
    openai_response = await call_openai(what_the_hack_plugin[function_name],
                                        variables)

    with open(path_to_markdown_file, "w") as file_object:
        file_object.write(openai_response.result)

    return openai_response

async def create_hack_description(variables, number_of_challenges):
    openai_response = await write_markdown_file(overview_function_name,
                                                variables,
                                                f"{root_path}/README.md")
    
    variables["overview"] = openai_response["input"]
    variables["input"] = ""

    return openai_response

async def create_challenge_markdown_file(variables, full_path, prefix, suffix_number):
    openai_response = await write_markdown_file(challenge_function_name,
                                                variables,
                                                f"{full_path}/{prefix}-{suffix_number:02d}.md")

    return openai_response

async def create_solution_markdown_file(variables, full_path, prefix, suffix_number, challenge_response):
    variables["challenge"] = challenge_response["input"]

    openai_response = await write_markdown_file(solution_function_name,
                                                variables,
                                                f"{full_path}/{prefix}-{suffix_number:02d}.md")

    return openai_response

async def create_challenge_and_solution(variables, challenge_number):
    logging.info(f"Creating {root_path}/Challenge-{challenge_number:02d}.md...")

    variables["suffix_number"] = f"{challenge_number:02d}"
    
    challenge_response = await create_challenge_markdown_file(variables,
                                                              f"{root_path}/Student", 
                                                              "Challenge", 
                                                              challenge_number)

    logging.info(f"Creating {root_path}/Solution-{challenge_number:02d}.md...")

    await create_solution_markdown_file(variables,
                                        f"{root_path}/Coach", 
                                        "Solution", 
                                        challenge_number, 
                                        challenge_response)

async def create_coach_guide_markdown_file(variables, full_path, number_of_solutions):
    logging.info(f"Creating {full_path}/README.md...")

    openai_response = await write_markdown_file(coach_overview_function_name,
                                                variables,
                                                f"{full_path}/README.md")

    return openai_response

async def create_challenges_and_solutions(variables, number_of_challenges):

    for challenge_number in range(0, number_of_challenges + 1):
        await create_challenge_and_solution(variables, challenge_number)

    await create_coach_guide_markdown_file(variables, 
                                           f"{root_path}/Coach", 
                                           number_of_challenges)

async def main(argv):
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

    global kernel
    kernel = setup_kernel(args.openai_model_name, args.openai_embedding_model_name, args.openai_endpoint_uri, args.openai_api_key, args.application_insights_key)

    global plugins
    plugins = import_plugins(kernel)

    global context
    context, variables = await setup_context(kernel, args)
    
    global openai_hack_description
    openai_hack_description = await create_hack_description(variables, args.number_of_challenges)

    await create_challenges_and_solutions(variables, args.number_of_challenges)

if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))