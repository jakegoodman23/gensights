data_analysis_prompt = """
You are an expert data analyst creating an executive summary PDF report. You are also an expert in surgical operations and should feel compelled to give recommendations based on the data.

The data you'll be analyzing contains healthcare surgical operations metrics with these key dimensions:
- dt_month: The month of the data
- location_name: The name of the healthcare facility
- region_name: The region where the facility is located
- qoq: The quarter over quarter change in the metric. Please use this to calculate the percentage change.

Based on the data provided, create a nicely formatted executive summary report with the following sections:

# Executive Summary Report

## Key Findings
[3-5 bullet points highlighting the most important discoveries]
Importance should be given to metrics where we see more than a 5% increase or decrease when compared to the previous quarter.
Priority should also be given to insights at the customer level but if there's anything beyond a 10% change at the region level, make sure to include that. 

## Regional Performance
[Summary of regional performance. How do the different regions compare against each other?]

## Recommendations
[3-5 specific, actionable recommendations based on the data. Remember, you're an expert in surgical operations and should feel compelled to give recommendations based on the data.]

Format your response using Markdown for proper PDF rendering.
Use headers, bullet points, and emphasis where appropriate.
Keep the language professional, concise, and focused on business impact.


Make sure you include the dates that are being compared with all the insights. For example, if we're saying the Case Volume is up 10% from last year, make sure you include the dates that are being compared. The most recent quarter, which is Q4 2024, is the most important and should be the main focus and be compared to past data.

If you have any insights from publically available sources as to how other hospitals are performing, make sure to include those as well and cite your sources (i.e. comparing against the industry average).
"""

meeting_notes_prompt = """
[These are the meeting notes from a meeting with the customer. You are an expert in the customer's business and should feel compelled to give recommendations based on the data.]


**Meeting Notes - Sacred Heart Hospital**  
**Date:** March 5, 2025  
**Customer:** Sacred Heart Hospital  
**Regions Covered:** Sacramento, Los Angeles  
**Executive Sponsor:** Dr. Bob Kelso  
**Attendees:** Dr. Bob Kelso, Julia Anderson (Interim OR Director, Sacramento), Dr. Todd Quinlan (Surgeon, LA), Michelle Martinez (OR Manager, LA), Alex Riley (Consultant)

### Discussion Points:

#### Staffing and Leadership Changes:
- Recent departure of OR Director at the Sacramento location; Julia Anderson stepping in as Interim Director.
- Concerns raised about increased stress and workload among Sacramento OR staff due to feeling short-staffed after leadership turnover.
- Dr. Kelso expressed urgency in filling the OR Director role permanently to stabilize operations and support staff morale.

#### Smart Scheduling Features:
- General excitement and optimism around upcoming smart scheduling feature rollout.
- Dr. Kelso anticipates significant improvements in OR efficiency and believes it could mitigate some staffing pressures.
- Julia Anderson emphasized the need for training sessions for Sacramento staff to effectively utilize new scheduling technology upon deployment.

#### Block Management Concerns:
- Dr. Todd Quinlan raised ongoing concerns from surgeons in Los Angeles around the current block management governance model.
- Surgeons question fairness, transparency, and efficiency of existing block allocation methods.
- Michelle Martinez agreed there's potential for improvement, expressed interest in exploring solutions from LT to optimize block scheduling governance.

#### Case Scheduling and Evening Overruns:
- Both Sacramento and Los Angeles teams noted continued challenges with surgical cases consistently running late into evenings.
- Staffing fatigue noted as a significant issue, impacting staff retention and satisfaction.
- Dr. Kelso requested insights and recommendations on better staffing models or adjustments to current scheduling practices to manage these late-running cases more effectively.

### Action Items:
1. Schedule demonstration session of LT Block Management solutions with LA team.
2. Provide recommendations for staffing adjustments or case scheduling improvements to alleviate evening overruns.
3. Coordinate smart scheduling training and implementation timeline for Sacramento OR staff.
"""

beckers_web_scrape = """

**Sacred Heart Hospital Explores Potential Acquisition by Behemoth Hospital; Major EHR Transition Anticipated**  
**Published on March 5, 2025 – Becker’s Hospital Review**

Sacred Heart Hospital, a prominent healthcare provider serving the Sacramento and Los Angeles regions, is currently in advanced discussions regarding a potential acquisition by Behemoth Hospital, a national leader in integrated healthcare systems.

This strategic move, if finalized, would significantly impact Sacred Heart Hospital’s current operational practices, most notably through a major shift in their Electronic Health Records (EHR) platform. Sacred Heart currently utilizes Lumon Industries as their primary EHR system; however, integration into Behemoth Hospital's network would necessitate transitioning to Monster's Inc, the EHR solution favored by Behemoth.

Dr. Bob Kelso, Executive Sponsor at Sacred Heart, acknowledged ongoing negotiations but declined to provide detailed comments on the specifics. Industry analysts suggest this shift could lead to substantial operational efficiencies and increased resource availability for Sacred Heart, albeit requiring extensive training and system adaptation from medical and administrative staff.

The potential transition to Monster's Inc could also impact existing technology partnerships and operational workflows at Sacred Heart. Staff preparedness and strategic integration planning are expected to be critical to a successful transition, minimizing disruption to patient care and clinical operations.

Both organizations have committed to keeping stakeholders informed as talks progress, emphasizing a shared goal of enhancing patient outcomes and operational performance through this strategic partnership.

"""
