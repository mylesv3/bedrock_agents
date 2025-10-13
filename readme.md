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
