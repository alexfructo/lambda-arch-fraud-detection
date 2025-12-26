import json
from datetime import datetime, timezone
from io import BytesIO

def write_silver(minio, bucket, event):
    date = datetime.now(timezone.utc)
    path = (
        f"transactions/scored/"
        f"year={date.year}/month={date.month}/day={date.day}/"
        f"{event.get('transaction', event).get('trans_num')}.json"
    )

    payload = json.dumps(event).encode("utf-8")
    data_stream = BytesIO(payload)

    minio.put_object(
        bucket_name=bucket,
        object_name=path,
        data=data_stream,
        length=len(payload),
        content_type="application/json"
    )
