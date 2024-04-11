# CryptoPipe

## Introduction
CryptoPipe is a streamlined scheduler created out of necessity. Existing solutions, such as Airflow and Prefect, didn't meet my expectations, prompting me to design a bespoke scheduler tailored to my specific needs.

## Architecture
The scheduler is basically using apscheduler + FastAPI, no DAG management.  Users implement a job definition in a job registry and create it.
