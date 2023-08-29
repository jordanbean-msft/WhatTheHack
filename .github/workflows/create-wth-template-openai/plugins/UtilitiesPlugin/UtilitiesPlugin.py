from semantic_kernel.skill_definition import (
    sk_function,
    sk_function_context_parameter
)
from semantic_kernel.orchestration.sk_context import SKContext

class UtilitiesPlugin:
    @sk_function(
        name="IncrementSuffixNumber"
    )
    @sk_function_context_parameter(
        name="suffix_number",
        description="The suffix number to increment."
    )
    def IncrementSuffixNumber(self, context: SKContext) -> str:
        context["suffix_number"] = str(int(context["suffix_number"]) + 1)
        
        return ""

    @sk_function(
        name="SetOverview"
    )
    @sk_function_context_parameter(
        name="input",
        description=""
    )
    @sk_function_context_parameter(
        name="overview",
        description=""
    )
    def SetOverview(self, context: SKContext) -> str:
        context["overview"] = context["input"]
        
        return ""