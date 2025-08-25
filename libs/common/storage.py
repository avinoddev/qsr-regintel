# libs/common/storage.py
import os, json, mimetypes, hashlib
import boto3
from botocore.client import Config

S3_ENDPOINT = os.getenv("S3_ENDPOINT")
S3_PUBLIC_ENDPOINT = os.getenv("S3_PUBLIC_ENDPOINT")  # e.g. http://localhost:9000
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
S3_SECRET_KEY = os.getenv("S3_SECRET_KEY")
S3_BUCKET_RAW = os.getenv("S3_BUCKET_RAW", "raw-docs")
S3_BUCKET_PDF = os.getenv("S3_BUCKET_PDF", "rendered-pdfs")

def _client(endpoint_url: str):
    return boto3.client(
        "s3",
        endpoint_url=endpoint_url,
        aws_access_key_id=S3_ACCESS_KEY,
        aws_secret_access_key=S3_SECRET_KEY,
        config=Config(signature_version="s3v4"),
        region_name="us-east-1",
    )

def s3():
    return _client(S3_ENDPOINT)

def s3_public():
    # Use the public host for signing, so the presigned URL is valid when opened from your Mac
    return _client(S3_PUBLIC_ENDPOINT or S3_ENDPOINT)

def ensure_bucket(bucket: str):
    cli = s3()
    try:
        cli.head_bucket(Bucket=bucket)
    except Exception:
        cli.create_bucket(Bucket=bucket)

def put_bytes(bucket: str, key: str, data: bytes, content_type: str | None = None):
    extra = {}
    if content_type:
        extra["ContentType"] = content_type
    s3().put_object(Bucket=bucket, Key=key, Body=data, **extra)
    return key

def presign_get(bucket: str, key: str, expires: int = 3600) -> str:
    # internal presign (minio:9000)
    return s3().generate_presigned_url(
        "get_object", Params={"Bucket": bucket, "Key": key}, ExpiresIn=expires
    )

def presign_get_public(bucket: str, key: str, expires: int = 3600) -> str:
    # public presign (localhost:9000) – host is baked into the signature
    return s3_public().generate_presigned_url(
        "get_object", Params={"Bucket": bucket, "Key": key}, ExpiresIn=expires
    )

def get_sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def guess_ext(mime: str | None, url: str | None = None) -> str:
    if mime:
        ext = mimetypes.guess_extension(mime.split(";")[0].strip()) or ""
        if ext: return ext
    if url:
        mt, _ = mimetypes.guess_type(url)
        if mt:
            return mimetypes.guess_extension(mt) or ""
    return ""
