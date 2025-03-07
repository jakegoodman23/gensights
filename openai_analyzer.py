"""
OpenAI integration module for ROI Automation Dashboard.
This module handles sending data to the OpenAI API and processing the responses.
"""

import os
import json
from openai import OpenAI, AzureOpenAI
from dotenv import load_dotenv
from ai_prompt import data_analysis_prompt, meeting_notes_prompt, beckers_web_scrape
from metric_definitions import METRIC_DEFINITIONS

# Load environment variables
load_dotenv()


class OpenAIAnalyzer:
    def __init__(self):
        """Initialize the OpenAI API client."""

        self.api_key = os.getenv("OPENAI_API_KEY")
        self.azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.api_version = os.getenv("AZURE_OPENAI_API_VERSION")
        self.temperature = 0.25
        self.max_tokens = 2000
        self.model = "gpt-4o"
        self.client = AzureOpenAI(
            api_key=self.api_key,
            api_version=self.api_version,
            azure_endpoint=self.azure_endpoint,
        )

        self.cached_insights = None  # Cache to store insights
        self.meeting_insights = None  # Cache to store meeting-specific insights
        self.beckers_insights = None  # Cache to store Becker's web scrape insights

    def extract_meeting_insights(self):
        """Extract key insights and recommendations from the meeting notes."""
        # Check if we already have meeting insights cached
        if self.meeting_insights:
            return True, self.meeting_insights

        try:
            # Generate targeted insights from the meeting notes
            prompt = """
            You are an expert healthcare operations consultant reviewing meeting notes from a customer meeting.
            
            Please analyze these meeting notes and extract:
            1. Key concerns and pain points mentioned by the customer
            2. Important business context that should influence recommendations
            3. Specific requests or areas where the customer is seeking help
            4. Priorities that should be reflected in the executive summary
            
            Format your response with clear sections and bullet points.
            """

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": meeting_notes_prompt},
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )

            # Extract the meeting insights
            self.meeting_insights = response.choices[0].message.content
            return True, self.meeting_insights

        except Exception as e:
            import traceback

            error_details = traceback.format_exc()
            print("ERROR EXTRACTING MEETING INSIGHTS: ", error_details)
            return (
                False,
                f"Error extracting meeting insights: {str(e)}\n{error_details}",
            )

    def extract_beckers_insights(self):
        """Extract key insights from the Becker's web scrape data."""
        # Check if we already have Becker's insights cached
        if self.beckers_insights:
            return True, self.beckers_insights

        try:
            # Generate targeted insights from the Becker's web scrape
            prompt = """
            You are an expert healthcare business analyst reviewing an article from Becker's Hospital Review.
            
            Please analyze this article and extract:
            1. Key business changes that could impact operations (acquisition, EHR transition)
            2. Critical timeline considerations for the healthcare organization
            3. Strategic implications that should be reflected in recommendations
            4. High-priority issues that should be highlighted in an executive summary
            
            Format your response with clear sections and bullet points.
            """

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": beckers_web_scrape},
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )

            # Extract the Becker's insights
            self.beckers_insights = response.choices[0].message.content
            return True, self.beckers_insights

        except Exception as e:
            import traceback

            error_details = traceback.format_exc()
            print("ERROR EXTRACTING BECKER'S INSIGHTS: ", error_details)
            return (
                False,
                f"Error extracting Becker's insights: {str(e)}\n{error_details}",
            )

    def generate_insights(self, data):
        """Generate insights from the processed data using OpenAI API."""
        customer_data, region_data = data
        try:
            # Check if we already have insights cached
            if self.cached_insights:
                return True, self.cached_insights

            # First generate baseline insights from the data
            baseline_response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": data_analysis_prompt},
                    {
                        "role": "user",
                        "content": f"Here is the customer data to analyze: {customer_data} and here is the region data to analyze: {region_data}. Please create a complete executive summary with key findings, regional performance analysis, and recommendations. Make sure you're using Q4 2024 as the most recent quarter and calculating % increases and decreases correctly. All of the pct changes with the 'pct_qoq' suffixes are already in percentage point changes - do not multiply them by 100. Here are the metric definitions which can you use to have more context about the data: {METRIC_DEFINITIONS}",
                    },
                ],
                temperature=self.temperature,  # Lower temperature for more consistent, analytical output
                max_tokens=self.max_tokens,
            )

            # Extract the baseline insights
            baseline_insights = baseline_response.choices[0].message.content

            # Extract meeting-specific insights
            success_meeting, meeting_insights = self.extract_meeting_insights()
            if not success_meeting:
                meeting_insights = "Could not extract meeting insights. Proceeding with data insights only."

            # Extract insights from Becker's web scrape
            success_beckers, beckers_insights = self.extract_beckers_insights()
            if not success_beckers:
                beckers_insights = "Could not extract insights from Becker's article. Proceeding without this information."

            # Now, generate enhanced insights by combining data analysis with meeting notes and web scrape
            combined_prompt = """
            You are an expert consultant creating an executive summary report that integrates multiple sources of information:
            1. Data insights from operational metrics
            2. Meeting notes from customer conversations
            3. Industry news from Becker's Hospital Review
            
            Your task is to create a comprehensive executive summary that:
            1. Heavily prioritizes both the meeting notes AND the Becker's article information in the findings and recommendations. No need to include that this is heavily prioritized, just do it.
            2. Connects all three sources of information where relevant
            3. Makes specific recommendations that address both the customer's concerns from the meeting AND the strategic implications from the Becker's article
            4. Organizes information in a clear, business-focused format suitable for executives
            5. Be concise with the information, don't repeat yourself just to fill up space
            
            The meeting notes and Becker's article should be treated as high-priority context that shapes your analysis and recommendations. Don't mention anywhere in the report that this is highly prioritized
            """

            enhanced_response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": combined_prompt},
                    {
                        "role": "user",
                        "content": f"Here are the baseline data insights:\n\n{baseline_insights}\n\nHere are the meeting notes that should be heavily prioritized in the findings and recommendations:\n\n{meeting_notes_prompt}\n\nHere are the key insights extracted from the meeting notes:\n\n{meeting_insights}\n\nHere is important industry news from Becker's Hospital Review that should also be heavily prioritized:\n\n{beckers_web_scrape}\n\nHere are the key insights extracted from the Becker's article:\n\n{beckers_insights}\n\nPlease create an enhanced executive summary that heavily prioritizes BOTH the meeting notes AND the Becker's article information while incorporating relevant data insights. Format the response with clear sections for Key Findings, Regional Performance, and Recommendations using Markdown.",
                    },
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )

            # Extract the enhanced insights that prioritize meeting notes and Becker's information
            insights = enhanced_response.choices[0].message.content

            # Cache the insights for reuse
            self.cached_insights = insights

            return True, insights

        except Exception as e:
            import traceback

            error_details = traceback.format_exc()
            print("ERROR DETAILS: ", error_details)
            return (
                False,
                f"Error generating insights with OpenAI API: {str(e)}\n{error_details}",
            )

    def generate_pdf_content(self, data):
        """Generate content specifically formatted for a PDF report by reusing insights."""
        # If we already have insights from a previous call, use them
        if self.cached_insights:
            return True, self.cached_insights

        # Otherwise, generate new insights
        return self.generate_insights(data)
