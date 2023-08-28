import os
import logging
import getopt
import argparse
import asyncio
import semantic_kernel as sk
import semantic_kernel.connectors.ai.open_ai as sk_oai

plugins_directory = "./plugins"
what_the_hack_plugin_name = "WhatTheHack"
summarize_plugin_name = "SummarizeSkill"
overview_function_name = "Overview"
challenge_function_name = "Challenge"
solution_function_name = "Solution"
coach_overview_function_name = "CoachOverview"

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

    return plugins

def setup_context(kernel, args):
    print("Setting up context")
    context = kernel.create_new_context()
    context["description_of_hack"] = args.description_of_hack
    context["number_of_challenges"] = str(args.number_of_challenges)
    context["keywords"] = args.keywords
    context["history"] = ""

    return context

async def main(argv):
    parser = init_argparse()
    args = parser.parse_args(argv)

    logging_levels = [logging.WARNING, logging.INFO, logging.DEBUG]
    level = logging_levels[min(args.verbose, len(logging_levels) - 1)]

    logging.basicConfig(level=level, 
                        format='%(asctime)s %(levelname)s %(message)s')

    kernel = setup_kernel(args.openai_model_name, args.openai_endpoint_uri, args.openai_api_key)
    plugins = import_plugins(kernel)

    whatTheHackPlugin = plugins[what_the_hack_plugin_name]
    overviewFunction = whatTheHackPlugin[overview_function_name]
    challengeFunction = whatTheHackPlugin[challenge_function_name]
    solutionFunction = whatTheHackPlugin[solution_function_name]
    coachOverviewFunction = whatTheHackPlugin[coach_overview_function_name]

    context = setup_context(kernel, args)
    
    print("**Overview**")

    context["input"] = context["description_of_hack"]

    result = await kernel.run_async(overviewFunction,
                                    input_context=context
                                    )
    
    context["overview"] = result["input"]

    print(result)

    print("**Challenge 1**")

    context2 = kernel.create_new_context()
    context2["overview"] = context["overview"]
    context2["suffix_number"] = "1"

    result2 = await kernel.run_async(challengeFunction,
                                    input_context=context2
                                    )
    print(result2)
    
    print("**Coach Overview**")

    result1 = await kernel.run_async(coachOverviewFunction,
                                    input_context=context
                                    )

    print(result1)
    
    print("**Solution 1**")
    result3 = await kernel.run_async(solutionFunction,
                                    input_context=context
                                    )
    print(result3)
    
    pass

if __name__ == "__main__":
    import sys
    asyncio.run(main(sys.argv[1:]))