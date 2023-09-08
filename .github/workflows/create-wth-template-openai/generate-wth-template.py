import os
import logging
import getopt
import argparse
import asyncio
import semantic_kernel as sk
import semantic_kernel.connectors.ai.open_ai as sk_oai
import semantic_kernel.connectors.memory.azure_cognitive_search as sk_m_azure
from semantic_kernel.planning.basic_planner import BasicPlanner
from plugins.UtilitiesPlugin.UtilitiesPlugin import UtilitiesPlugin
from semantic_kernel.core_skills.file_io_skill import FileIOSkill
from semantic_kernel.core_skills.text_memory_skill import TextMemorySkill

plugins_directory = "./plugins"
what_the_hack_plugin_name = "WhatTheHack"
summarize_plugin_name = "SummarizeSkill"
utilities_plugin_name = "UtilitiesPlugin"
fileio_plugin_name = "FileIOSkill"
text_memory_plugin_name = "TextMemorySkill"

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
    parser.add_argument("-b", "--openai_embedding_model_name", help="OpenAI embedding model name", type=str)
    parser.add_argument("-e", "--openai_endpoint_uri", help="OpenAI endpoint URI (should include API version query parameter)", type=str)
    parser.add_argument("-a", "--openai_api_key", help="OpenAI API key", type=str)
    parser.add_argument("-v", "--verbose", help="Verbose logging", action='store_true')
    return parser

def setup_kernel(openai_model_name, openai_embeddings_model_name, openai_endpoint_uri, openai_api_key):
    print("Setting up kernel")
    kernel = sk.Kernel()
    kernel.add_text_completion_service(service_id="OpenAI-Completion",
                                       service=sk_oai.AzureTextCompletion(
                                         deployment_name=openai_model_name,
                                         endpoint=openai_endpoint_uri,
                                         api_key=openai_api_key
                                       ))
    kernel.add_text_embedding_generation_service(service_id="OpenAI-Embedding",
                                                 service=sk_oai.AzureTextEmbedding(
                                                    deployment_name=openai_embeddings_model_name,
                                                    endpoint=openai_endpoint_uri,
                                                    api_key=openai_api_key
                                                 ))
    #kernel.register_memory_store(memory_store=sk_m_azure.AzureCognitiveSearchMemoryStore())        
    kernel.register_memory_store(memory_store=sk.memory.VolatileMemoryStore())        
    return kernel

def import_plugins(kernel):
    print("Importing plugins")

    plugins = {}
    plugins[what_the_hack_plugin_name] = kernel.import_semantic_skill_from_directory(os.path.abspath(plugins_directory), what_the_hack_plugin_name)
    plugins[summarize_plugin_name] = kernel.import_semantic_skill_from_directory(os.path.abspath(plugins_directory), summarize_plugin_name)
    plugins[utilities_plugin_name] = kernel.import_skill(UtilitiesPlugin(), skill_name=utilities_plugin_name)
    plugins[fileio_plugin_name] = kernel.import_skill(FileIOSkill(), skill_name=fileio_plugin_name)
    plugins[text_memory_plugin_name] = kernel.import_skill(TextMemorySkill(), skill_name=text_memory_plugin_name)

    return plugins

def setup_context(kernel, args):
    print("Setting up context")
    
    context = kernel.create_new_context()
    variables = sk.ContextVariables()
    
    variables["description_of_hack"] = args.description_of_hack
    variables["number_of_challenges"] = str(args.number_of_challenges)
    variables["keywords"] = args.keywords

    context["example_hackathon_challenge_document"] = """
## Introduction

When setting up an IoT device, it is important to understand how 'thingamajigs' work. Thingamajigs are a key part of every IoT device and ensure they are able to communicate properly with edge servers. Thingamajigs require IP addresses to be assigned to them by a server and thus must have unique MAC addresses. In this challenge, you will get hands on with a thingamajig and learn how one is configured.

## Description

In this challenge, you will properly configure the thingamajig for your IoT device so that it can communicate with the mother ship.

You can find a sample \`thingamajig.config\` file in the \`/ChallengeXX\` folder of the Resources.zip file provided by your coach. This is a good starting reference, but you will need to discover how to set exact settings.

Please configure the thingamajig with the following specifications:
- Use dynamic IP addresses
- Only trust the following whitelisted servers: "mothership", "IoTQueenBee" 
- Deny access to "IoTProxyShip"

You can view an architectural diagram of an IoT thingamajig here: [Thingamajig.PDF](/Student/Resources/Architecture.PDF?raw=true).

## Success Criteria

To complete this challenge successfully, you should be able to:
- Verify that the IoT device boots properly after its thingamajig is configured.
- Verify that the thingamajig can connect to the mothership.
- Demonstrate that the thingamajic will not connect to the IoTProxyShip

## Learning Resources

- [What is a Thingamajig?](https://www.bing.com/search?q=what+is+a+thingamajig)
- [10 Tips for Never Forgetting Your Thingamajic](https://www.youtube.com/watch?v=dQw4w9WgXcQ)
- [IoT & Thingamajigs: Together Forever](https://www.youtube.com/watch?v=yPYZpwSpKmA)

## Tips

- IoTDevices can fail from a broken heart if they are not together with their thingamajig. Your device will display a broken heart emoji on its screen if this happens.
- An IoTDevice can have one or more thingamajigs attached which allow them to connect to multiple networks.
""".strip()
    context[sk.core_skills.TextMemorySkill.COLLECTION_PARAM] = "exampleHack"
    context[sk.core_skills.TextMemorySkill.RELEVANCE_PARAM] = "0.8"

    variables["history"] = ""

    return context, variables

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

async def generate_and_execute_plan(kernel):
    planner = BasicPlanner()

    print("**Planning**")
    plan = await planner.create_plan_async(goal="Generate a hackathon overview, set of challenges, and solutions based upon the context provided.", kernel=kernel)
    print("**Generated Plan**")
    print(plan.generated_plan)

    print("**Executing Plan**")
    result = await planner.execute_plan_async(plan, kernel)
    print("Result")
    print(result)

async def main(argv):
    parser = init_argparse()
    args = parser.parse_args(argv)

    logging_levels = [logging.WARNING, logging.INFO, logging.DEBUG]
    level = logging_levels[min(args.verbose, len(logging_levels) - 1)]

    logging.basicConfig(level=level, 
                        format='%(asctime)s %(levelname)s %(message)s')

    kernel = setup_kernel(args.openai_model_name, args.openai_embedding_model_name, args.openai_endpoint_uri, args.openai_api_key)
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

    context, variables = setup_context(kernel, args)

    #await generate_and_execute_plan(kernel)

    print("**Overview**")
    result = await kernel.run_async(overview_function, input_context=context, input_vars=variables)
    print(result)

    variables["overview"] = result["input"]
    variables["input"] = ""

    print("**Challenge 01**")
    result = await kernel.run_async(challenge_function, input_context=context, input_vars=variables)
    print(result)
    variables["challenge"] = result["input"]

    print("**Solution 01**")
    result = await kernel.run_async(solution_function, input_context=context, input_vars=variables)
    print(result)

    # await run_chain(args, kernel, overview_function, challenge_function, solution_function, coach_overview_function, increment_suffix_number_function, set_overview_function, context)

    pass

if __name__ == "__main__":
    import sys
    asyncio.run(main(sys.argv[1:]))