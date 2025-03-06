"""
OpenAI integration module for ROI Automation Dashboard.
This module handles sending data to the OpenAI API and processing the responses.
"""

import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from ai_prompt import data_analysis_prompt
from metric_definitions import METRIC_DEFINITIONS

# Load environment variables
load_dotenv()


class OpenAIAnalyzer:
    def __init__(self):
        """Initialize the OpenAI API client."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OpenAI API key not found. Please set it in the .env file."
            )

        # Initialize OpenAI client with just the API key to avoid proxy issues
        self.client = OpenAI(
            api_key=api_key,
        )
        self.model = "gpt-4o-mini"  # Use the most capable model available

    def generate_insights(self, data):
        """Generate insights from the processed data using OpenAI API."""
        customer_data, region_data = data
        try:
            # Use chat completion API to generate insights
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": data_analysis_prompt},
                    {
                        "role": "user",
                        "content": f"Here is the customer data to analyze: {customer_data} and here is the region data to analyze: {region_data}. Please analyze the data and find the most meaningful insights and please make sure you're using Q4 2024 as the most recent quarter. Make sure you're calculating % increases and decreases correctly. Here are the metric definitions which can you use to have more context about the data: {METRIC_DEFINITIONS}",
                    },
                ],
                temperature=0.1,  # Lower temperature for more consistent, analytical output
                max_tokens=2000,
            )

            # Extract the insights from the response
            insights = response.choices[0].message.content

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
        """Generate content specifically formatted for a PDF report."""
        try:
            customer_data, region_data = data
            # Use chat completion API to generate PDF content
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": data_analysis_prompt},
                    {
                        "role": "user",
                        "content": f"For the PDF report, here is the customer data to analyze: {customer_data} and here is the region data to analyze: {region_data}. Make sure you're calculating % increases and decreases correctly and please make sure you're using Q4 2024 as the most recent quarter. Here are the metric definitions which can you use to have more context about the data: {METRIC_DEFINITIONS}",
                    },
                ],
                temperature=0.1,
                max_tokens=2000,
            )

            # Extract the PDF content from the response
            pdf_content = response.choices[0].message.content

            return True, pdf_content

        except Exception as e:
            import traceback

            print("PDF ERROR: ", e)

            error_details = traceback.format_exc()
            return (
                False,
                f"Error generating PDF content with OpenAI API: {str(e)}\n{error_details}",
            )

    def generate_presentation_content(self, data):
        """Generate content specifically formatted for a PowerPoint presentation."""
        try:
            system_prompt = """
            You are an expert data analyst creating content for a PowerPoint presentation.
            
            The data you'll be analyzing contains healthcare operations metrics with these key dimensions:
            - dt_month: The month of the data
            - location_name: The name of the healthcare facility
            - region_name: The region where the facility is located
            
            Based on the data provided, create content for a slide deck with the following sections:
            
            1. Title Slide
            2. Executive Summary (key metrics and findings)
            3. Overall Performance (trends across all locations)
            4. Regional Analysis (performance by region)
            5. Location Spotlights (notable location performances)
            6. Areas of Concern (metrics that need attention)
            7. Success Stories (positive trends and achievements)
            8. Recommendations (specific action items)
            9. Next Steps
            
            For each slide, provide:
            - A clear title
            - Bullet points of content (2-5 points per slide)
            - Any notes or commentary for the presenter
            
            Format your response as a structured JSON object with each slide as a separate element.
            Keep the language professional, concise, and focused on business impact.
            """

            # Convert the data to a JSON string
            data_str = json.dumps(data)

            # Use chat completion API to generate presentation content
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {
                        "role": "user",
                        "content": f"Here is the data to analyze for the presentation: {data_str}",
                    },
                ],
                temperature=0.2,
                max_tokens=2500,
            )

            # Extract the presentation content from the response
            presentation_content = response.choices[0].message.content

            return True, presentation_content

        except Exception as e:
            import traceback

            error_details = traceback.format_exc()
            return (
                False,
                f"Error generating presentation content with OpenAI API: {str(e)}\n{error_details}",
            )
