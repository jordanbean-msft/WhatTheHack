import logging
import argparse
import asyncio
from what_the_hack_openai import *

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION] [FILE]...",
        description="Create a new hackathon project from a template using OpenAI's API.")
    
    parser.add_argument("-c", "--number_of_challenges", help="Number of challenges to generate", type=int)
    parser.add_argument("-n", "--name_of_hack", help="Name of hackathon project", type=str)
    parser.add_argument("-d", "--description_of_hack", help="Description of hackathon project", type=str)
    parser.add_argument("-k", "--keywords", help="Keywords for hackathon project", type=str)
    parser.add_argument("-m", "--openai_model_name", help="OpenAI model name", type=str)
    parser.add_argument("-b", "--openai_embedding_model_name", help="OpenAI embedding model name", type=str)
    parser.add_argument("-e", "--openai_endpoint_uri", help="OpenAI endpoint URI (should include API version query parameter)", type=str)
    parser.add_argument("-a", "--openai_api_key", help="OpenAI API key", type=str)
    parser.add_argument("-i", "--application_insights_key", help="Application Insights key", type=str)
    parser.add_argument("-v", "--verbose", help="Verbose logging", action='store_true')
    return parser

async def main(argv):
    parser = init_argparse()
    args = parser.parse_args(argv)

    logging_levels = [logging.WARNING, logging.INFO, logging.DEBUG]
    level = logging_levels[min(args.verbose, len(logging_levels) - 1)]

    logging.basicConfig(level=level, 
                        format='%(asctime)s %(levelname)s %(message)s')

    kernel = setup_kernel(args.openai_model_name, args.openai_embedding_model_name, args.openai_endpoint_uri, args.openai_api_key, args.application_insights_key)
    plugins = import_plugins(kernel)

    what_the_hack_plugin = plugins[what_the_hack_plugin_name]
    overview_function = what_the_hack_plugin[overview_function_name]
    challenge_function = what_the_hack_plugin[challenge_function_name]
    solution_function = what_the_hack_plugin[solution_function_name]
    coach_overview_function = what_the_hack_plugin[coach_overview_function_name]
    fileio_plugin = plugins[fileio_plugin_name]
    write_async_function = fileio_plugin[write_async_function_name]

    context, variables = await setup_context(kernel, args)

    #await generate_and_execute_plan(kernel)

    print("**Overview**")
    result1 = (await kernel.run_async(overview_function, input_context=context, input_vars=variables, input_str=args.description_of_hack))
    print(result1)

    variables["overview"] = result1["input"]
    variables["input"] = ""

    print("**Challenge 01**")

    variables["suffix_number"] = "01"

    result2 = await kernel.run_async(challenge_function, input_context=context, input_vars=variables)
    print(result2)
    variables["challenge"] = result2["input"]

    print("**Solution 01**")
    result3 = await kernel.run_async(solution_function, input_context=context, input_vars=variables)
    print(result3)

    print("**Challenge 02**")

    variables["suffix_number"] = "02"

    result4 = await kernel.run_async(challenge_function, input_context=context, input_vars=variables)
    print(result4)
    variables["challenge"] = result4["input"]

    print("**Solution 02**")
    result5 = await kernel.run_async(solution_function, input_context=context, input_vars=variables)
    print(result5)


    # await run_chain(args, kernel, overview_function, challenge_function, solution_function, coach_overview_function, increment_suffix_number_function, set_overview_function, context)

    pass

if __name__ == "__main__":
    import sys
    asyncio.run(main(sys.argv[1:]))