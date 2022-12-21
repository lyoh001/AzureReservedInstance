# VICGOV - Azure Reserved Instance
## 1. Introduction
### 1.1	Overview

There is a requirement from the business to further analyse the current cost model of Azure resources and purchase Azure reserved instances and enable hybrid benefit.

This document is intended to provide a high level overview of workflow on how the automation fetches payload in JSON via API and converts them into consumable data format for further analysis activity.

Included a step by step detailed analysis notebook around discovering and exploring the current consumption pattern. (ref: https://github.com/lyoh001/AzureReservedInstance/blob/main/notebook/notebook.ipynb)


## 2 Azure Reserved Instance Power BI Reports
- Description: Fetch and analyse the current cloud resource consumption pattern via Power BI and Notebook EDA and further predict the cost with ML Time Series. 
- Priority: 3
- Owners: Tier 0

## 3 Logical Architecture
### 3.1	Logical System Component Overview
![Figure 1: Logical Architecture Overview](./images/workflow.png)
1. Data gets pulled from Azure cost management REST API to 
Azure Machine learning workspace for EDA and model building.
1. Building EDA report and ML model via Azure ML workspace and Power BI report.
1. Notebook gets pushed to github repository.
1. The end users can consume PowerBI report from any devices.

![Figure 1: Powerbi Dashboard](./images/powerbi.png)

## 4 Power BI Report Link
Ref: [Interactive Power BI Dashboard Link](https://lyoh001.com/mlvmaudit)

## Used By
This project is used by the following teams:
- Cloud Hosting Platform