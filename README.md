# CryptoPipe

## Introduction
CryptoPipe is a streamlined scheduler created out of necessity. Existing solutions, such as Airflow and Prefect, didn't meet my expectations, prompting me to design a bespoke scheduler tailored to my specific needs.

## Architecture
Adhering to the conventional design of schedulers, CryptoPipe constructs a job scheduler using basic building blocks:
- **Task:** This represents the simplest form of defining an activity or a process to be executed.
- **Job:** This outlines how tasks are arranged and interact with each other.
- **Action:** Essentially a Task coupled with input parameters, indicating a specific instance of a task ready to be executed.
- **Execution:** This signifies a specific instance of a Job, incorporating input parameters and scheduling details, ready for execution.