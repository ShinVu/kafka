# KAFKA

A exercise project for practising with Kafka

## Installation

Requirements:

- Docker
- Visual studio remote container extensions

## Usage

In this small project, I simulate a streaming process where:

- Setting up Kafka with Kraft and Docker
- Setting up Dev environment with dev container extension
- Setting up Airflow with Docker
- Setting up Mysql with Docker
- Data is produced and simulated by Airflow DAG to kafka
- Data is consumed by consumer using Python Confluent-kafka, this data is then push to MySQL database

