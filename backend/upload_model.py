"""Upload v2 model to MinIO and register in DB."""
import io, json
from datetime import datetime
from pathlib import Path

from app.config import settings
from app.models.database import ModelVersion, SessionLocal
from app.services.minio_service import minio_service


def main():
    # 1. Check MinIO availability
    try:
        minio_service.client.list_buckets()
    except Exception:
        print("ERROR: MinIO not available. Start Docker first (docker compose up -d).")
        return

    # 2. Upload model + metadata
    base_name = "rsod-yolo11n-best_v2.0.0"
    object_name = minio_service.upload_model_file(settings.yolo_model_path, base_name)
    print(f"Uploaded: {object_name}")

    metadata = {
        "name": "rsod-yolo11n",
        "version": "2.0.0",
        "created_at": datetime.now().isoformat(),
        "metrics": {"mAP50": 0.876, "mAP50-95": 0.652},
        "config": {"epochs": 30, "batch": 4, "device": "0"},
    }
    md_bytes = json.dumps(metadata, ensure_ascii=False, indent=2).encode()
    meta_name = object_name.replace(".pt", "_metadata.json")
    minio_service.client.put_object(
        settings.minio.models_bucket,
        meta_name,
        data=io.BytesIO(md_bytes),
        length=len(md_bytes),
        content_type="application/json",
    )
    print(f"Uploaded: {meta_name}")

    # 3. Update local model_info.json
    info_path = Path(settings.yolo_model_path).parent / "model_info.json"
    try:
        info_path.write_text(
            json.dumps(
                {
                    "version": "2.0.0",
                    "object_name": object_name,
                    "loaded_at": datetime.now().isoformat(),
                    "metadata": metadata,
                },
                indent=2,
                ensure_ascii=False,
            )
        )
    except Exception as e:
        print(f"Warning: model_info.json update failed: {e}")

    # 4. INSERT model_versions via ORM
    with SessionLocal() as db:
        existing = (
            db.query(ModelVersion)
            .filter(ModelVersion.name == "rsod-yolo11n", ModelVersion.version == "2.0.0")
            .first()
        )
        if existing:
            existing.model_key = object_name
            existing.updated_at = datetime.now()
        else:
            db.add(ModelVersion(name="rsod-yolo11n", version="2.0.0", model_key=object_name, status="active"))
        db.commit()
    print("model_versions table updated.")

    print("Done. Restart backend to apply.")


if __name__ == "__main__":
    main()
