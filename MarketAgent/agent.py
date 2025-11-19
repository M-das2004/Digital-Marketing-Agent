import os

try:
    from dotenv import load_dotenv
    load_dotenv()

    # Use a faster model for a complex sequential flow
    MODEL_NAME = os.environ.get("GOOGLE_GENAI_MODEL", "gemini-2.0-flash")
except ImportError:
    print("Warning: python-dotenv not installed. Ensure API key is set")
    MODEL_NAME = "gemini-2.0-flash"

from google.adk.agents import LlmAgent, SequentialAgent, BaseAgent
from google.adk.tools import google_search

# --- Updated Imports for New Agents ---
from .instructions import (
    PRODUCT_ANALYSIS_INSTRUCTION,
    MARKET_RESEARCH_INSTRUCTION,
    AUDIENCE_AGENT_INSTRUCTION, # NEW
    PLATFORM_AGENT_INSTRUCTION, # NEW
    CONCEPT_INSTRUCTION,
    IMAGE_GENERATION_AGENT_INSTRUCTION, # NEW
    AD_CREATIVE_INSTRUCTION,
    COST_ESTIMATION_INSTRUCTION,
    CAMPAIGN_AGENT_INSTRUCTION,
    CAMPAIGN_ORCHESTRATOR_INSTRUCTION
)

# --- Sub Agent 1: ProductAnalysisAgent ---
product_analysis_agent = LlmAgent(
    name="ProductAnalysisAgent",
    model=MODEL_NAME,
    instruction=PRODUCT_ANALYSIS_INSTRUCTION,
    tools=[google_search],
    output_key="product_analysis"
)

# --- Sub Agent 2: MarketResearchAgent ---
market_research_agent = LlmAgent(
    name="MarketResearchAgent",
    model=MODEL_NAME,
    instruction=MARKET_RESEARCH_INSTRUCTION,
    tools=[google_search],
    output_key="market_research_summary"
)

# --- NEW Sub Agent 3: AudienceAgent ---
audience_agent = LlmAgent(
    name="AudienceAgent",
    model=MODEL_NAME,
    instruction=AUDIENCE_AGENT_INSTRUCTION,
    tools=[google_search], # Used for general demographic/interest research
    output_key="audience_personas"
)

# --- NEW Sub Agent 4: PlatformAgent ---
platform_agent = LlmAgent(
    name="PlatformAgent",
    model=MODEL_NAME,
    instruction=PLATFORM_AGENT_INSTRUCTION,
    tools=[google_search], # Used for platform/benchmark research
    output_key="platform_recommendations"
)

# --- Sub Agent 5: ConceptAgent (Renumbered) ---
concept_agent = LlmAgent(
    name="ConceptAgent",
    model=MODEL_NAME,
    instruction=CONCEPT_INSTRUCTION,
    output_key="campaign_concepts"
)

# --- NEW Sub Agent 6: ImageGenerationAgent ---
image_generation_agent = LlmAgent(
    name="ImageGenerationAgent",
    model=MODEL_NAME,
    instruction=IMAGE_GENERATION_AGENT_INSTRUCTION,
    # No external tools needed, as it generates a specification based on context
    output_key="visual_asset_spec"
)

# --- Sub Agent 7: AdCreativeAgent (Renumbered) ---
ad_creative_agent = LlmAgent(
    name="AdCreativeAgent",
    model=MODEL_NAME,
    instruction=AD_CREATIVE_INSTRUCTION,
    output_key="ad_creative"
)

# --- Sub Agent 8: CostEstimationAgent (Renumbered) ---
cost_estimation_agent = LlmAgent(
    name="CostEstimationAgent",
    model=MODEL_NAME,
    instruction=COST_ESTIMATION_INSTRUCTION,
    output_key="cost_estimation"
)

# --- Sub Agent 9: CampaignAgent (Formatter) (Renumbered) ---
campaign_agent = LlmAgent(
    name="CampaignAgentFormatter",
    model=MODEL_NAME,
    instruction=CAMPAIGN_AGENT_INSTRUCTION,
    output_key="final_campaign_report"
)


#class SilentSequentialAgent(BaseAgent):
#    """Sequential agent that suppresses intermediate outputs and only yields final agent events.
#   
#   Behavior: Runs all sub-agents sequentially but only yields events from the last sub-agent.
#   This prevents the UI from displaying intermediate outputs while preserving all in-memory
#   state updates (so later agents still have access to earlier results).
#   """
#
#    async def _run_async_impl(self, ctx):
#        """Run all sub-agents; only yield events from the final one."""
#        for i, sub_agent in enumerate(self.sub_agents):
#            if i == len(self.sub_agents) - 1:
#                # Final sub-agent: forward all events to caller (UI)
#                async for event in sub_agent.run_async(ctx):
#                    yield event
#            else:
#                # Intermediate sub-agents: consume events but do not yield them
#                async for _ in sub_agent.run_async(ctx):
#                    pass
#
#    async def _run_live_impl(self, ctx):
#        """Run all sub-agents in live mode; only yield events from the final one."""
#        for i, sub_agent in enumerate(self.sub_agents):
#            if i == len(self.sub_agents) - 1:
#                async for event in sub_agent.run_live(ctx):
#                    yield event
#            else:
#                async for _ in sub_agent.run_live(ctx):
#                    pass


# --- Sequential Orchestrator ---
# Updated to include new agents in a logical marketing workflow
campaign_orchestrator = SequentialAgent(
    name="ContextualDigitalMarketingAssistant",
    description=CAMPAIGN_ORCHESTRATOR_INSTRUCTION,
    sub_agents=[
        product_analysis_agent,
        market_research_agent,
        audience_agent,            # NEW: Identify target customer
        platform_agent,            # NEW: Select channels based on audience
        concept_agent,             # Generate messaging
        image_generation_agent,    # NEW: Specify required visual asset
        ad_creative_agent,         # Generate text copy
        cost_estimation_agent,     # Budget based on platforms/assets
        campaign_agent,            # Compile report (FINAL - only this displays in UI)
    ]
)

root_agent = campaign_orchestrator
