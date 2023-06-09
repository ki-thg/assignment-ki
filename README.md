# Mass Transit Billing

## Overview
The Public Transport Billing System is a command-line application that calculates the billing charges for public transport journeys based on the provided zone map and journey data. It applies daily and monthly caps to ensure fair and accurate billing.

## Prerequisites
- Python 3.9.16
- pytest 7.3.1

## Setup
1. Unzip file and save locally on your machine
2. Navigate to the project's root directory.

## Usage
1. Prepare the input files:
    - Create a `zone_map.csv` file containing the station-zone mappings.
    - Create a `journey_data.csv` file containing the journey records.
2. Run the billing system:
    ```shell
    python main.py zone_map.csv journey_data.csv output.csv
    ```
3. The billing system will calculate the charges and generate an output file with the billing results.

## Running Tests
2. Run the tests using pytest:
    ```shell
    python -m pytest
    ```

#### Kevin Irvani