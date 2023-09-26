import logging
import os
import semantic_kernel as sk
import semantic_kernel.connectors.ai.open_ai as sk_oai
import semantic_kernel.connectors.memory.azure_cognitive_search as sk_m_azure
from semantic_kernel.planning.basic_planner import BasicPlanner
from semantic_kernel.core_skills.file_io_skill import FileIOSkill
from semantic_kernel.core_skills.text_memory_skill import TextMemorySkill
from opencensus.ext.azure.log_exporter import AzureLogHandler

plugins_directory = "plugins"
what_the_hack_plugin_name = "WhatTheHack"
summarize_plugin_name = "SummarizeSkill"
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

def setup_kernel(openai_gpt_model_name, openai_embeddings_model_name, openai_endpoint_uri, openai_api_key, application_insights_connection_string):
    print("Setting up kernel")

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    
    logger.addHandler(AzureLogHandler(connection_string=application_insights_connection_string))

    kernel = sk.Kernel(log=logger)
    kernel.add_text_completion_service(service_id="OpenAI-Completion",
                                       service=sk_oai.AzureTextCompletion(
                                         deployment_name=openai_gpt_model_name,
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
    plugins[what_the_hack_plugin_name] = kernel.import_semantic_skill_from_directory(os.path.join(os.path.dirname(__file__), plugins_directory), what_the_hack_plugin_name)
    plugins[summarize_plugin_name] = kernel.import_semantic_skill_from_directory(os.path.join(os.path.dirname(__file__), plugins_directory), summarize_plugin_name)
    plugins[fileio_plugin_name] = kernel.import_skill(FileIOSkill(), skill_name=fileio_plugin_name)
    plugins[text_memory_plugin_name] = kernel.import_skill(TextMemorySkill(), skill_name=text_memory_plugin_name)

    return plugins

async def setup_context(kernel, args):
    print("Setting up context")
    
    context = kernel.create_new_context()
    variables = sk.ContextVariables()
    
    variables["description_of_hack"] = args.description_of_hack
    variables["number_of_challenges"] = str(args.number_of_challenges)
    variables["keywords"] = args.keywords

    with open(os.path.join(os.path.dirname(__file__), plugins_directory, what_the_hack_plugin_name, challenge_function_name, 'example-hackathon-challenge-document.txt'), 'r') as file:
        example_challenge_text = file.read()

    await kernel.memory.save_information_async(collection="hackathon", id="id1", text=example_challenge_text)

    context["example_hackathon_challenge_document"] = "Find an example challenge"
    context["example_hackathon_solution_document"] = "Find an example solution"
    context[sk.core_skills.TextMemorySkill.COLLECTION_PARAM] = "hackathon"
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