# =============================================================================
# 配置文件模块
# =============================================================================
# 功能说明：
#   - 集中管理系统所有配置项
#   - 支持从环境变量读取配置
#   - 提供各服务的连接参数
#
# 使用方式：
#   from app.config import settings
#   settings.database.host  # 获取数据库主机
#   settings.minio.port    # 获取 MinIO 端口
#
# 环境变量说明：
#   - .env 文件中的配置会覆盖默认值
#   - 部署时可通过 Docker 环境变量或系统环境变量配置
# =============================================================================

# 导入 Pydantic BaseModel，用于数据验证和设置管理
from pydantic import BaseModel

# 导入类型提示 List，用于定义列表类型
from typing import List, Optional

# 导入 os 模块，用于读取操作系统环境变量
import os

from pathlib import Path

# 导入 dotenv 模块的 load_dotenv 函数，用于加载 .env 文件
from dotenv import load_dotenv

from app.utils.paths import Paths, find_project_root

# 获取 backend 目录路径（config.py 在 backend/app/ 下）
BACKEND_DIR = find_project_root(__file__)

# 加载 .env 文件到环境变量
# 使用 backend 目录下的 .env 文件
load_dotenv(BACKEND_DIR / ".env")


def _env_first(*names: str, default: Optional[str] = None) -> Optional[str]:
    """Return the first non-empty environment variable value."""
    for name in names:
        value = os.getenv(name)
        if value is not None and value != "":
            return value
    return default


def _resolve_backend_path(value: Optional[str], fallback: Path) -> str:
    """Resolve relative paths against the backend root for portability."""
    raw_value = value.strip() if value else ""
    if not raw_value:
        return str(fallback)

    candidate = Path(raw_value).expanduser()
    if not candidate.is_absolute():
        candidate = (BACKEND_DIR / candidate).resolve()
    else:
        candidate = candidate.resolve()
    return str(candidate)


def _minio_host_port() -> tuple[str, int]:
    endpoint = _env_first("MINIO_ENDPOINT", default="localhost:9000")
    default_host = "localhost"
    default_port = 9000
    if endpoint and ":" in endpoint:
        host_part, port_part = endpoint.rsplit(":", 1)
        try:
            default_port = int(port_part)
        except ValueError:
            default_port = 9000
        default_host = host_part or default_host

    host = _env_first("MINIO_HOST", default=default_host) or default_host
    port = int(_env_first("MINIO_PORT", default=str(default_port)) or default_port)
    return host, port


MINIO_HOST, MINIO_PORT = _minio_host_port()


class TargetClassConfig(BaseModel):
    """单个缺陷类别的展示配置。"""

    id: int
    name: str
    chinese_name: str
    description: str = ""


DEFAULT_TARGET_CATALOG = [
    TargetClassConfig(
        id=0,
        name="Crazing",
        chinese_name="龟裂",
        description="钢表面出现细密裂纹的缺陷。",
    ),
    TargetClassConfig(
        id=1,
        name="Inclusion",
        chinese_name="夹杂",
        description="钢表面或内部存在非金属夹杂物的缺陷。",
    ),
    TargetClassConfig(
        id=2,
        name="Patches",
        chinese_name="斑块",
        description="钢表面存在局部斑块状异常区域的缺陷。",
    ),
    TargetClassConfig(
        id=3,
        name="Pitted Surface",
        chinese_name="麻点",
        description="钢表面出现点状凹坑的缺陷。",
    ),
    TargetClassConfig(
        id=4,
        name="Rolled-in Scale",
        chinese_name="氧化皮压入",
        description="轧制过程中氧化皮压入钢表面的缺陷。",
    ),
    TargetClassConfig(
        id=5,
        name="Scratches",
        chinese_name="划伤",
        description="钢表面出现线状划痕的缺陷。",
    ),
]


# =============================================================================
# 数据库配置类
# =============================================================================
class DatabaseConfig(BaseModel):
    """
    PostgreSQL 数据库配置

    配置项：
        host: 数据库服务器地址，默认 localhost
        port: 数据库服务端口，默认 5432（PostgreSQL 标准端口）
        username: 数据库用户名，默认 rsod_user
        password: 数据库密码，默认 rsod_password
        database: 数据库名称，默认 rsod_platform
    """

    # 数据库主机地址，从环境变量 DB_HOST 读取，默认为 localhost
    host: str = os.getenv("DB_HOST", "localhost")

    # 数据库端口，从环境变量 DB_PORT 读取，转换为整数，默认为 5432
    port: int = int(os.getenv("DB_PORT", "5432"))

    # 数据库用户名，从环境变量 DB_USERNAME 读取，默认为 rsod_user
    username: str = _env_first("DB_USERNAME", "DB_USER", default="rsod_user") or "rsod_user"

    # 数据库密码，从环境变量 DB_PASSWORD 读取，默认为 rsod_password
    # 注意：生产环境应使用强密码并通过环境变量传入
    password: str = os.getenv("DB_PASSWORD", "rsod_password")

    # 数据库名称，从环境变量 DB_DATABASE 读取，默认为 rsod_platform
    database: str = _env_first("DB_DATABASE", "DB_NAME", default="rsod_db") or "rsod_db"


# =============================================================================
# MinIO 对象存储配置类
# =============================================================================
class MinIOConfig(BaseModel):
    """
    MinIO 对象存储配置

    MinIO 是一个高性能的分布式对象存储系统，兼容 Amazon S3 API
    用于存储图片、视频、模型文件等非结构化数据

    配置项：
        host: MinIO 服务器地址，默认 localhost
        port: MinIO API 端口，默认 9000
        access_key: 访问密钥（相当于用户名），默认 admin
        secret_key: 秘密密钥（相当于密码），默认 minio_password
        secure: 是否使用 HTTPS 连接，默认 false（开发环境用 HTTP）
        original_bucket: 原始图片存储桶名称
        results_bucket: 检测结果图片存储桶名称
        models_bucket: AI 模型文件存储桶名称
    """

    # MinIO 服务器主机地址
    host: str = MINIO_HOST

    # MinIO API 端口（不是 Console 端口）
    port: int = MINIO_PORT

    # 访问密钥（Access Key），用于身份验证
    access_key: str = os.getenv("MINIO_ACCESS_KEY", "admin")

    # 秘密密钥（Secret Key），用于身份验证
    # 注意：生产环境应使用强密码并通过环境变量传入
    secret_key: str = os.getenv("MINIO_SECRET_KEY", "minio_password")

    # 是否使用安全连接（HTTPS）
    # 从环境变量读取并转换为布尔值
    # 支持的值：true, 1, yes（不区分大小写）
    secure: bool = os.getenv("MINIO_SECURE", "false").lower() in ("true", "1", "yes")

    # 原始图片存储桶名称，用于保存上传的原始图片
    original_bucket: str = "rsod-original"

    # 检测结果图片存储桶名称，用于保存检测后的图片
    results_bucket: str = "rsod-results"

    # 模型文件存储桶名称，用于保存 AI 模型文件（设置为私有访问）
    models_bucket: str = "rsod-models"


# =============================================================================
# Redis 缓存配置类
# =============================================================================
class RedisConfig(BaseModel):
    """
    Redis 缓存配置

    Redis 是一个开源的内存数据结构存储系统，可用作数据库、缓存和消息队列
    用于缓存热点数据、会话管理、实时分析等场景

    配置项：
        host: Redis 服务器地址，默认 localhost
        port: Redis 服务端口，默认 6379
        password: Redis 访问密码，默认 redis_password
    """

    # Redis 服务器主机地址
    host: str = os.getenv("REDIS_HOST", "localhost")

    # Redis 服务端口
    port: int = int(os.getenv("REDIS_PORT", "6379"))

    # Redis 访问密码，用于身份验证
    # 注意：生产环境应使用强密码并通过环境变量传入
    password: str = os.getenv("REDIS_PASSWORD", "redis_password")


# =============================================================================
# 应用全局配置类
# =============================================================================
class Settings(BaseModel):
    """
    应用全局配置

    整合所有配置项，包括应用信息、CORS、YOLO 模型参数等

    配置项：
        app_name: 应用名称
        app_version: 应用版本号
        debug: 调试模式开关
        host: 服务监听地址
        port: 服务监听端口
        static_dir: 静态文件目录
        upload_dir: 上传文件存储目录
        result_dir: 检测结果文件目录
        database: 数据库配置（DatabaseConfig 实例）
        minio: MinIO 配置（MinIOConfig 实例）
        redis: Redis 配置（RedisConfig 实例）
        cors_origins: CORS 允许的来源列表
        yolo_model_path: YOLO 模型文件路径
        confidence_threshold: 目标检测置信度阈值
        iou_threshold: 非极大值抑制 IOU 阈值
    """

    # -------------------------------------------------------------------------
    # 应用基本信息
    # -------------------------------------------------------------------------

    # 应用名称，用于 API 文档标题
    app_name: str = os.getenv("APP_NAME", "RSOD Detection Platform")

    # 应用版本号
    app_version: str = os.getenv("APP_VERSION", "1.0.0")

    # 调试模式开关
    # True: 启用详细日志输出、服务重启自动加载代码变更
    # False: 生产模式，优化性能
    debug: bool = os.getenv("DEBUG", "true").lower() in ("true", "1", "yes")

    # 服务监听地址
    # 0.0.0.0: 监听所有网络接口（允许外部访问）
    # 127.0.0.1: 仅监听本地回环地址（仅本地访问）
    host: str = os.getenv("HOST", "0.0.0.0")

    # 服务监听端口
    port: int = int(os.getenv("PORT", "8000"))

    # 外部访问基址，用于构造 API 返回的可访问 URL
    public_base_url: str = os.getenv(
        "PUBLIC_BASE_URL",
        f"http://localhost:{os.getenv('PORT', '8000')}",
    )

    # -------------------------------------------------------------------------
    # 静态文件和目录配置
    # -------------------------------------------------------------------------

    # backend 根目录
    backend_root: str = str(BACKEND_DIR)

    # 数据目录
    data_root: str = _resolve_backend_path(os.getenv("DATA_ROOT"), Paths.data())

    # 训练集目录
    train_root: str = _resolve_backend_path(os.getenv("TRAIN_ROOT"), Paths.train_root())

    # 训练图片目录
    train_images_dir: str = _resolve_backend_path(
        os.getenv("TRAIN_IMAGES_DIR"),
        Paths.train_images(),
    )

    # 训练标签目录
    train_labels_dir: str = _resolve_backend_path(
        os.getenv("TRAIN_LABELS_DIR"),
        Paths.train_labels(),
    )

    # 静态文件目录，用于 serving 上传的图片等静态资源
    static_dir: str = _resolve_backend_path(os.getenv("STATIC_DIR"), Paths.static())

    # 上传文件存储目录，保存用户上传的原始图片
    upload_dir: str = _resolve_backend_path(os.getenv("UPLOAD_DIR"), Paths.uploads())

    # 检测结果文件目录，保存检测后的图片
    result_dir: str = _resolve_backend_path(os.getenv("RESULT_DIR"), Paths.results())

    # 模型目录
    models_dir: str = _resolve_backend_path(os.getenv("MODELS_DIR"), Paths.models())

    # 日志目录
    logs_dir: str = _resolve_backend_path(os.getenv("LOGS_DIR"), Paths.logs())

    # -------------------------------------------------------------------------
    # 服务配置实例
    # -------------------------------------------------------------------------

    # 数据库配置实例
    database: DatabaseConfig = DatabaseConfig()

    # MinIO 对象存储配置实例
    minio: MinIOConfig = MinIOConfig()

    # Redis 缓存配置实例
    redis: RedisConfig = RedisConfig()

    # -------------------------------------------------------------------------
    # CORS 跨域配置
    # -------------------------------------------------------------------------

    # CORS（跨域资源共享）允许的来源列表
    # 多个来源用逗号分隔
    # 开发环境通常包括前端开发服务器地址
    cors_origins: List[str] = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173,http://localhost:3000"
    ).split(",")

    # -------------------------------------------------------------------------
    # YOLO 目标检测模型配置
    # -------------------------------------------------------------------------

    # YOLO 模型文件路径，相对于项目根目录
    # 支持的模型：yolo11n.pt, yolo11s.pt, yolo11m.pt 等
    yolo_model_path: str = _resolve_backend_path(
        os.getenv("YOLO_MODEL_PATH"),
        Paths.models() / "yolo11n.pt",
    )

    # 目标检测置信度阈值
    # 只有检测框置信度 >= 此值的结果才会被保留
    # 范围：0.0 - 1.0，默认 0.5
    confidence_threshold: float = float(os.getenv("CONFIDENCE_THRESHOLD", "0.5"))

    # 非极大值抑制（Non-Maximum Suppression）IOU 阈值
    # 用于去除重叠的检测框，只保留最优的检测结果
    # 范围：0.0 - 1.0，默认 0.45
    iou_threshold: float = float(os.getenv("IOU_THRESHOLD", "0.45"))

    # -------------------------------------------------------------------------
    # DeepSeek AI 问答配置
    # -------------------------------------------------------------------------
    deepseek_api_key: str = os.getenv("DEEPSEEK_API_KEY", "")
    deepseek_api_base_url: str = os.getenv("DEEPSEEK_API_BASE_URL", "https://api.deepseek.com")
    deepseek_model: str = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
    deepseek_timeout: int = int(os.getenv("DEEPSEEK_TIMEOUT", "60"))

    # 允许上传的图片扩展名
    allowed_upload_extensions: List[str] = [
        ".jpg",
        ".jpeg",
        ".png",
        ".bmp",
        ".tif",
        ".tiff",
    ]

    # 允许上传的图片 MIME 类型
    allowed_upload_mime_types: List[str] = [
        "image/jpeg",
        "image/png",
        "image/bmp",
        "image/tiff",
        "image/x-tiff",
    ]

    # 当前项目统一使用的缺陷类别定义
    target_catalog: List[TargetClassConfig] = DEFAULT_TARGET_CATALOG

    @property
    def target_names(self) -> List[str]:
        return [target.name for target in self.target_catalog]

    def get_target_by_id(self, class_id: int) -> Optional[TargetClassConfig]:
        for target in self.target_catalog:
            if target.id == class_id:
                return target
        return None


# =============================================================================
# 全局配置实例
# =============================================================================
# 创建全局唯一的配置实例
# 在应用的任何地方都可以通过 import settings 访问配置
# 注意：应在应用启动时创建此实例，以确保所有配置正确加载
settings = Settings()
