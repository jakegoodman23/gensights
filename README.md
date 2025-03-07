# GenSights Tool

**Important to note this is just a tool for demoing purposes! While it does make LLM calls all the data is synthetic and not pulling in from real sources**

A web application that uses AI to synthesize data from multiple sources and automatically generate insights, visualizations, and formatted reports. The application processes operational data, meeting notes, and industry news to identify trends, provide recommendations, and create executive-ready summaries.

## Background

Executive check-ins are hard to prepare for. Our Outcomes team has to spend a lot of time manually finding meaningful insights from our application and then trying to combine that with the customer's strategy to ensure we're presenting ourselves as a valuable transformational partner. This tool not only aims to automate some of that insight collection which will increase our team's scalability but also hopefully increases the overall quality of these check-ins by ensuring all of the important items are being touched on.

## Data Collection

All of the below data is synthetic data however it should closely resemble the structure that we'd be able to pull if this tool were productionalized.

### Metric Insights (Application Data)

While we have all of this data in our app, it's hard to quickly find the most meaningful insights (i.e. metrics that have moved significantly or ones that closely tie to the customer's strategic gaols). By having all of this data synthesized by an LLM, it can find those insights and also relate them to the other data sources.

### Meeting Notes (Notion)

Notion is a gold mine of valuable insights and one of those areas we wanted to focus on was past meeting notes with the customer that could easily be aggregated and analyzed by a LLM. This is a staple feature of an LLM and being able to combine it with other actionable data is where the value of this tool can really emerge. Additionally, this is just one aspect of Notion - obviously there's so much more insights in Notion that could be tied in (i.e. churn warfare, upcoming capabilities, surgical operations knowledge, etc.).

### Beckers Healthcare News (Aurora/Web)

We thought it'd be interesting to be able to tap into our already existing Aurora capabilities to do "deep research" on a customer and focus that specifically on Beckers news as an example since that stays pretty up-to-date. Being able to foil that into an Executive summary would really make sure we're demonstrating ourselves as a transformational partner and able to help them with more things than just adoption of our product.

## Executive Summary

The finished product. After making repeated calls to the LLM with all of the above information, we're left with some really valuable synthesized insights that combines everything together to make sure we're focusing on the right things with the customer. The output should be used to guide how the check-in presentations are constructed and maybe in the future, the output could be more customer facing as the capabilities and models improve.
