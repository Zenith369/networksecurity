from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logger.logging import logging
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig

import sys

if __name__ == "__main__":
    try:
        trainingpipelineconfig = TrainingPipelineConfig()
        
        dataingestionconfig = DataIngestionConfig(training_pipeline_config=trainingpipelineconfig)
        dataingestion = DataIngestion(data_ingestion_config=dataingestionconfig)
        logging.info("Initiate data ingestion")
        dataingestionartifact = dataingestion.initiate_data_ingestion()
        logging.info("Data ingestion completed")
        print(dataingestionartifact)
        data_validation_config = DataValidationConfig(training_pipeline_config=trainingpipelineconfig)
        data_validation = DataValidation(data_ingestion_artifact=dataingestionartifact,
                                        data_validation_config=data_validation_config)
        logging.info("Initiate data validation")
        datavalidationartifact = data_validation.initiate_data_validation()        
        logging.info("Data validation completed")
        print(datavalidationartifact)
    except Exception as e:
        raise NetworkSecurityException(e, sys)