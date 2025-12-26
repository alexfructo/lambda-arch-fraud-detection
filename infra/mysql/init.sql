USE lambda_db;

CREATE TABLE IF NOT EXISTS transactions_scored (
  id BIGINT NOT NULL AUTO_INCREMENT,
  transaction_id VARCHAR(64) NOT NULL,
  request_id VARCHAR(64) NOT NULL,
  fraud_probability DECIMAL(6,5) NOT NULL,
  confidence DECIMAL(6,5) NOT NULL,
  is_fraud TINYINT(1) NOT NULL,
  risk_level VARCHAR(20) NOT NULL,
  recommended_action VARCHAR(50) NOT NULL,
  model_strategy VARCHAR(50) DEFAULT NULL,
  xgboost_version VARCHAR(20) DEFAULT NULL,
  random_forest_version VARCHAR(20) DEFAULT NULL,
  preprocessor_version VARCHAR(20) DEFAULT NULL,
  processing_time_ms DECIMAL(10,2) DEFAULT NULL,
  transaction_value DECIMAL(12,2) DEFAULT NULL,
  location_distance_km DECIMAL(10,2) DEFAULT NULL,
  random_forest_score DECIMAL(6,5) DEFAULT NULL,
  xgboost_score DECIMAL(6,5) DEFAULT NULL,
  ensemble_strategy VARCHAR(100) DEFAULT NULL,
  status VARCHAR(100) DEFAULT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

  PRIMARY KEY (id),
  KEY idx_transaction_id (transaction_id),
  KEY idx_is_fraud (is_fraud),
  KEY idx_created_at (created_at)
);
