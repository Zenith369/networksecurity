from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logger.logging import logging
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.entity.config_entity import ModelTrainerConfig
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
        
        datatransformationconfig = DataTransformationConfig(training_pipeline_config=trainingpipelineconfig)
        data_transformation = DataTransformation(data_validation_artifact=datavalidationartifact,
                                                 data_transformation_config=datatransformationconfig)
        logging.info("Initiate data transformation")
        datatransformationartifact = data_transformation.initiate_data_transformation()
        logging.info("Data transformation completed")
        print(datatransformationartifact)

        logging.info("Model training started")
        modeltrainerconfig = ModelTrainerConfig(training_pipeline_config=trainingpipelineconfig)
        model_trainer = ModelTrainer(data_transformation_artifact=datatransformationartifact,
                                     model_trainer_config=modeltrainerconfig)
        modeltrainerartifact = model_trainer.initiate_model_trainer()
        logging.info("Model training completed")
        print(modeltrainerartifact)

    except Exception as e:
        raise NetworkSecurityException(e, sys)