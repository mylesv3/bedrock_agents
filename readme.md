# AI Workflow w/ AWS

## Overview
This lab is a multi-agent AI workflow built in AWS Bedrock, and it is deployed using API Gateway and Postman. This workflow acts as a travel advisor that contains three agents: a supervisor agent, an accommodation agent, and a restaurant agent. Based on the user input, the supervisor agent will know which other agent to invoke for a response (accommodation or restaurant).

<img width="970" height="591" alt="image" src="https://github.com/user-attachments/assets/31832dbc-6478-4647-b48e-7c38be71c5e1" />

### Skills Learned
 - Built and deployed multi-agent systems using AWS Bedrock and Lambda.
 - Designed and orchestrated agent workflows with task delegation.
 - Integrated API Gateway and S3 for data handling and endpoint management.

### Tools Used
 - AWS (Bedrock, Lambda, S3, API Gateway)
 - Postman
 - Python
 - Claude AI

## Restaurant Agent

<img width="706" height="491" alt="Screenshot 2025-10-13 073302" src="https://github.com/user-attachments/assets/3d9c6de6-b651-4f7a-bc76-a68dfb912f24" />

This agent in AWS Bedrock recommends a restaurant based on the user's preferences for fine dining and location


<img width="710" height="389" alt="Screenshot 2025-10-13 073342" src="https://github.com/user-attachments/assets/af1da8f5-e93f-41c5-996d-bb0ba115db8b" />

Agent group takes in two parameters (fine_dine and city)

## Accommodation Agent

<img width="693" height="504" alt="Screenshot 2025-10-13 074236" src="https://github.com/user-attachments/assets/3b7aeb3b-dd84-4cdc-9689-f7595292284f" />

This agent in AWS Bedrock recommends an accommodation option based on the user's preferences for hotels/airbnbs

<img width="713" height="403" alt="Screenshot 2025-10-13 074310" src="https://github.com/user-attachments/assets/85e0ed56-3d68-4b6f-ad3d-7ca85afb616d" />

<img width="708" height="460" alt="Screenshot 2025-10-13 074329" src="https://github.com/user-attachments/assets/1a7e1ebc-30d1-4c00-8b6d-a008762f4e3c" />

Accommodation Action Groups
