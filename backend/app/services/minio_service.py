"""MinIO object storage service for the YOLO11 backend."""

from __future__ import annotations

import io
import json
import logging
import time
import uuid
from pathlib import Path
from typing import Optional

from fastapi import UploadFile
from minio import Minio
from minio.error import S3Error

from app.config import settings
from app.utils.paths import Paths


logger = logging.getLogger(__name__)


class MinIOService:
    """Encapsulate MinIO bucket and object operations."""

    def __init__(self) -> None:
        endpoint = f"{settings.minio.host}:{settings.minio.port}"
        self.client = Minio(
            endpoint=endpoint,
            access_key=settings.minio.access_key,
            secret_key=settings.minio.secret_key,
            secure=settings.minio.secure,
        )
        self._ensure_buckets()

    def _ensure_buckets(self) -> None:
        buckets = [
            settings.minio.original_bucket,
            settings.minio.results_bucket,
            settings.minio.models_bucket,
        ]
        for bucket in buckets:
            try:
                if not self.client.bucket_exists(bucket):
                    self.client.make_bucket(bucket)
                    logger.info("Bucket 创建成功: %s", bucket)
                self._set_bucket_public_read(bucket)
            except Exception as exc:
                logger.warning("初始化 Bucket 失败: bucket=%s error=%s", bucket, exc)

    def _set_bucket_public_read(self, bucket_name: str) -> None:
        bucket_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": f"PublicRead{bucket_name}",
                    "Effect": "Allow",
                    "Principal": {"AWS": ["*"]},
                    "Action": ["s3:GetObject", "s3:GetObjectVersion"],
                    "Resource": f"arn:aws:s3:::{bucket_name}/*",
                }
            ],
        }
        try:
            self.client.set_bucket_policy(bucket_name, json.dumps(bucket_policy))
            logger.info("Bucket 已设置为公开读取: %s", bucket_name)
        except Exception as exc:
            logger.warning("设置 Bucket 公开读取失败: bucket=%s error=%s", bucket_name, exc)

    def upload_image(self, file: UploadFile, bucket_name: str) -> str:
        file_extension = file.filename.split(".")[-1] if "." in file.filename else "jpg"
        object_name = f"{uuid.uuid4().hex}.{file_extension}"
        file_content = file.file.read()
        self.client.put_object(
            bucket_name=bucket_name,
            object_name=object_name,
            data=io.BytesIO(file_content),
            length=len(file_content),
            content_type=file.content_type or "image/jpeg",
        )
        logger.info("图片上传成功: bucket=%s object=%s", bucket_name, object_name)
        return object_name

    async def upload_image_async(self, file: UploadFile, bucket_name: str) -> str:
        file_extension = file.filename.split(".")[-1] if "." in file.filename else "jpg"
        object_name = f"{uuid.uuid4().hex}.{file_extension}"
        file_content = await file.read()
        self.client.put_object(
            bucket_name=bucket_name,
            object_name=object_name,
            data=io.BytesIO(file_content),
            length=len(file_content),
            content_type=file.content_type or "image/jpeg",
        )
        logger.info("异步图片上传成功: bucket=%s object=%s", bucket_name, object_name)
        return object_name

    def upload_result_image(self, image_bytes: bytes, extension: str = "jpg") -> str:
        object_name = f"result_{uuid.uuid4().hex}.{extension}"
        self.client.put_object(
            bucket_name=settings.minio.results_bucket,
            object_name=object_name,
            data=io.BytesIO(image_bytes),
            length=len(image_bytes),
            content_type="image/jpeg",
        )
        logger.info("结果图片上传成功: object=%s", object_name)
        return object_name

    def upload_image_bytes(self, image_bytes: bytes, original_filename: str) -> str:
        file_extension = original_filename.split(".")[-1] if "." in original_filename else "jpg"
        object_name = f"{uuid.uuid4().hex}.{file_extension}"
        content_type = (
            f"image/{file_extension}"
            if file_extension in {"jpg", "jpeg", "png", "gif", "bmp", "tif", "tiff"}
            else "image/jpeg"
        )
        self.client.put_object(
            bucket_name=settings.minio.original_bucket,
            object_name=object_name,
            data=io.BytesIO(image_bytes),
            length=len(image_bytes),
            content_type=content_type,
        )
        logger.info("原始图片上传成功: object=%s", object_name)
        return object_name

    def get_presigned_url(
        self,
        bucket_name: str,
        object_name: str,
        expires: int = 3600,
    ) -> Optional[str]:
        try:
            return self.client.presigned_get_object(
                bucket_name=bucket_name,
                object_name=object_name,
                expires=expires,
            )
        except S3Error as exc:
            logger.warning(
                "生成预签名 URL 失败: bucket=%s object=%s error=%s",
                bucket_name,
                object_name,
                exc,
            )
            return None

    def get_public_url(self, bucket_name: str, object_name: str) -> str:
        scheme = "https" if settings.minio.secure else "http"
        return f"{scheme}://{settings.minio.host}:{settings.minio.port}/{bucket_name}/{object_name}"

    def delete_object(self, bucket_name: str, object_name: str) -> bool:
        try:
            self.client.remove_object(bucket_name, object_name)
            logger.info("对象删除成功: bucket=%s object=%s", bucket_name, object_name)
            return True
        except S3Error as exc:
            logger.warning("对象删除失败: bucket=%s object=%s error=%s", bucket_name, object_name, exc)
            return False

    def list_objects(self, bucket_name: str, prefix: str = "") -> list:
        try:
            return [obj.object_name for obj in self.client.list_objects(bucket_name, prefix=prefix)]
        except S3Error as exc:
            logger.warning("列出对象失败: bucket=%s prefix=%s error=%s", bucket_name, prefix, exc)
            return []

    def bucket_exists(self, bucket_name: str) -> bool:
        return self.client.bucket_exists(bucket_name)

    def upload_model_file(self, local_file_path: str, model_name: str) -> str:
        file_extension = local_file_path.split(".")[-1] if "." in local_file_path else "pt"
        object_name = f"{model_name}_{int(time.time())}.{file_extension}"
        file_content = Path(local_file_path).read_bytes()
        self.client.put_object(
            bucket_name=settings.minio.models_bucket,
            object_name=object_name,
            data=io.BytesIO(file_content),
            length=len(file_content),
            content_type="application/octet-stream",
        )
        logger.info("模型上传成功: object=%s", object_name)
        return object_name

    def download_model_file(self, object_name: str, local_save_path: str) -> bool:
        try:
            response = self.client.get_object(settings.minio.models_bucket, object_name)
            file_content = response.read()
            response.close()
            response.release_conn()

            local_path = Path(local_save_path)
            Paths.ensure_dir(local_path.parent)
            local_path.write_bytes(file_content)
            logger.info("模型下载成功: object=%s path=%s", object_name, local_save_path)
            return True
        except Exception as exc:
            logger.warning("下载模型失败: object=%s error=%s", object_name, exc)
            return False

    def list_models(self) -> list:
        return self.list_objects(settings.minio.models_bucket)

    def delete_model(self, object_name: str) -> bool:
        return self.delete_object(settings.minio.models_bucket, object_name)

    def get_latest_model(self, model_prefix: str = "rsod-yolo11n-best") -> Optional[str]:
        try:
            model_files = [
                model_name
                for model_name in self.list_models()
                if model_name.startswith(model_prefix)
                and not model_name.endswith("_metadata.json")
                and model_name.endswith(".pt")
            ]
            if not model_files:
                return None

            def parse_model_name(filename: str):
                try:
                    if "_v" in filename:
                        _, rest = filename.split("_v", 1)
                        version_str, timestamp_part = rest.split("_", 1)
                        timestamp = int(timestamp_part.split(".")[0])
                        major, minor, patch = map(int, version_str.split("."))
                        return (1, major, minor, patch, timestamp)
                    prefix, timestamp_part = filename.rsplit("_", 1)
                    if prefix and timestamp_part.split(".")[0].isdigit():
                        return (0, 0, 0, 0, int(timestamp_part.split(".")[0]))
                except Exception:
                    return (-1, 0, 0, 0, 0)
                return (-1, 0, 0, 0, 0)

            model_files.sort(key=parse_model_name, reverse=True)
            return model_files[0]
        except Exception as exc:
            logger.warning("获取最新模型失败: %s", exc)
            return None

    def get_model_metadata(self, model_object_name: str) -> Optional[dict]:
        try:
            metadata_name = model_object_name.replace(".pt", "_metadata.json")
            response = self.client.get_object(settings.minio.models_bucket, metadata_name)
            metadata_content = response.read().decode("utf-8")
            response.close()
            response.release_conn()
            return json.loads(metadata_content)
        except Exception as exc:
            logger.warning("获取模型元数据失败: object=%s error=%s", model_object_name, exc)
            return None

    def list_models_with_metadata(self, model_prefix: str = "rsod-yolo11n-best") -> list:
        try:
            model_files = [
                model_name
                for model_name in self.list_models()
                if model_name.startswith(model_prefix)
                and not model_name.endswith("_metadata.json")
                and model_name.endswith(".pt")
            ]
            return [
                {
                    "object_name": model_file,
                    "metadata": self.get_model_metadata(model_file),
                    "public_url": self.get_public_url(settings.minio.models_bucket, model_file),
                }
                for model_file in model_files
            ]
        except Exception as exc:
            logger.warning("列出模型失败: %s", exc)
            return []


minio_service = MinIOService()
