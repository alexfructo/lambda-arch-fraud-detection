import json
from datetime import datetime, timezone
from io import BytesIO


def write_bronze(minio, bucket, event):
    date = datetime.now(timezone.utc)

    object_path = (
        f"transactions/raw/"
        f"year={date.year}/month={date.month:02d}/day={date.day:02d}/"
        f"{event['trans_num']}.json"
    )

    payload = json.dumps(event).encode("utf-8")
    payload_stream = BytesIO(payload)

    minio.put_object(
        bucket_name=bucket,
        object_name=object_path,
        data=payload_stream,
        length=len(payload),
        content_type="application/json"
    )
