
def write_transactional(conn, event: dict):

    transaction = event.get("transaction", event)
    inference = event.get("inference", event)
    cursor = conn.cursor()

    sql = """
    INSERT INTO transactions_scored (
        transaction_id,
        request_id,
        fraud_probability,
        confidence,
        is_fraud,
        risk_level,
        recommended_action,
        xgboost_score,
        random_forest_score,
        ensemble_strategy,
        xgboost_version,
        random_forest_version,
        preprocessor_version,
        transaction_value,
        location_distance_km,
        processing_time_ms,
        status
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    data = (
        transaction["trans_num"],
        inference["metadata"]["request_id"],
        inference["ensemble"]["fraud_probability"],
        inference["ensemble"]["confidence"],
        inference["ensemble"]["is_fraud"],
        inference["ensemble"]["risk_level"],
        inference["ensemble"]["recommended_action"],
        inference["models"]["xgboost"],
        inference["models"]["random_forest"],
        inference["model"]["strategy"],
        inference["model"]["versions"]["xgboost"],
        inference["model"]["versions"]["random_forest"],
        inference["model"]["preprocessor_version"],
        inference["insights"]["transaction_value"],
        inference["insights"]["location_distance_km"],
        inference["processing"]["processing_time_ms"],
        inference["metadata"]["status"]
    )

    cursor.execute(sql, data)
    conn.commit()
    cursor.close()

