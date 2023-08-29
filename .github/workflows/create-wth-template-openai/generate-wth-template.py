import os
import logging
import getopt
import argparse
import asyncio
import semantic_kernel as sk
import semantic_kernel.connectors.ai.open_ai as sk_oai
from plugins.UtilitiesPlugin.UtilitiesPlugin import UtilitiesPlugin
from semantic_kernel.core_skills.file_io_skill import FileIOSkill

plugins_directory = "./plugins"
what_the_hack_plugin_name = "WhatTheHack"
summarize_plugin_name = "SummarizeSkill"
utilities_plugin_name = "UtilitiesPlugin"
fileio_plugin_name = "FileIOSkill"

overview_function_name = "Overview"
challenge_function_name = "Challenge"
solution_function_name = "Solution"
coach_overview_function_name = "CoachOverview"
increment_suffix_number_function_name = "IncrementSuffixNumber"
set_overview_function_name = "SetOverview"
set_write_context_function_name = "SetWriteContext"
write_async_function_name = "writeAsync"

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION] [FILE]...",
        description="Create a new hackathon project from a template using OpenAI's API.")
    
    parser.add_argument("-c", "--number_of_challenges", help="Number of challenges to generate", type=int)
    parser.add_argument("-n", "--name_of_hack", help="Name of hackathon project", type=str)
    parser.add_argument("-d", "--description_of_hack", help="Description of hackathon project", type=str)
    parser.add_argument("-k", "--keywords", help="Keywords for hackathon project", type=str)
    parser.add_argument("-m", "--openai_model_name", help="OpenAI model name", type=str)
    parser.add_argument("-e", "--openai_endpoint_uri", help="OpenAI endpoint URI (should include API version query parameter)", type=str)
    parser.add_argument("-a", "--openai_api_key", help="OpenAI API key", type=str)
    parser.add_argument("-v", "--verbose", help="Verbose logging", action='store_true')
    return parser

def setup_kernel(openai_model_name, openai_endpoint_uri, openai_api_key):
    print("Setting up kernel")
    kernel = sk.Kernel()
    kernel.add_text_completion_service("WhatTheHack",
                                       sk_oai.AzureTextCompletion(
                                         openai_model_name,
                                         openai_endpoint_uri,
                                         openai_api_key
                                       ))
    return kernel

def import_plugins(kernel):
    print("Importing plugins")
    plugins = {}
    plugins[what_the_hack_plugin_name] = kernel.import_semantic_skill_from_directory(os.path.abspath(plugins_directory), what_the_hack_plugin_name)
    plugins[summarize_plugin_name] = kernel.import_semantic_skill_from_directory(os.path.abspath(plugins_directory), summarize_plugin_name)
    plugins[utilities_plugin_name] = kernel.import_skill(UtilitiesPlugin(), skill_name=utilities_plugin_name)
    plugins[fileio_plugin_name] = kernel.import_skill(FileIOSkill(), skill_name=fileio_plugin_name)

    return plugins

def setup_context(kernel, args):
    print("Setting up context")
    context = kernel.create_new_context()
    context["description_of_hack"] = args.description_of_hack
    context["number_of_challenges"] = str(args.number_of_challenges)
    context["keywords"] = args.keywords
    context["history"] = ""

    return context

async def run_chain(args, kernel, overview_function, challenge_function, solution_function, coach_overview_function, increment_suffix_number_function, set_overview_function, context):
    functions = [
        overview_function,
        set_overview_function,
        coach_overview_function,
    ]

    for i in range(0, args.number_of_challenges):
        functions.append(challenge_function)
        functions.append(solution_function)
        functions.append(increment_suffix_number_function)

    result = await kernel.run_async(*functions,
                                    input_context=context
                                    )
    print(result)

async def main(argv):
    parser = init_argparse()
    args = parser.parse_args(argv)

    logging_levels = [logging.WARNING, logging.INFO, logging.DEBUG]
    level = logging_levels[min(args.verbose, len(logging_levels) - 1)]

    logging.basicConfig(level=level, 
                        format='%(asctime)s %(levelname)s %(message)s')

    kernel = setup_kernel(args.openai_model_name, args.openai_endpoint_uri, args.openai_api_key)
    plugins = import_plugins(kernel)

    what_the_hack_plugin = plugins[what_the_hack_plugin_name]
    overview_function = what_the_hack_plugin[overview_function_name]
    challenge_function = what_the_hack_plugin[challenge_function_name]
    solution_function = what_the_hack_plugin[solution_function_name]
    coach_overview_function = what_the_hack_plugin[coach_overview_function_name]
    utilities_plugin = plugins[utilities_plugin_name]
    increment_suffix_number_function = utilities_plugin[increment_suffix_number_function_name]
    set_overview_function = utilities_plugin[set_overview_function_name]
    fileio_plugin = plugins[fileio_plugin_name]
    write_async_function = fileio_plugin[write_async_function_name]

    context = setup_context(kernel, args)

    print("**Overview**")
    result = await kernel.run_async(overview_function, input_context=context)
    print(result)

    context["overview"] = result["input"]

    print("**Challenge 01**")
    result = await kernel.run_async(challenge_function, input_context=context)
    print(result)

    # await run_chain(args, kernel, overview_function, challenge_function, solution_function, coach_overview_function, increment_suffix_number_function, set_overview_function, context)

    pass

if __name__ == "__main__":
    import sys
    asyncio.run(main(sys.argv[1:]))