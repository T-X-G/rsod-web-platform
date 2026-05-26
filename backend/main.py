from dotenv import load_dotenv
load_dotenv()  # 加载 .env 文件

from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from ultralytics import YOLO
from PIL import Image
import uvicorn
import uuid
import io
from pathlib import Path

from app.api import router as qa_router
from app.models import Base
from app.utils.database import engine

app = FastAPI(
    title="遥感目标智能检测平台",
    description="基于YOLO的遥感图像目标检测系统API",
    version="1.0.0"
)

# ==================== 加载 YOLO 模型 ====================
# 确保模型文件存在，如果不存在会自动下载（仅限官方模型）
MODEL_PATH = "models/yolo11n.pt"          # 可替换为你的 best.pt
try:
    model = YOLO(MODEL_PATH)
    print(f"✅ 模型加载成功: {MODEL_PATH}")
except Exception as e:
    print(f"⚠️ 模型加载失败: {e}，将使用占位模式（仅测试用）")
    model = None

# ==================== CORS 配置 ====================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # 生产环境应指定具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== 数据库初始化 ====================
Base.metadata.create_all(bind=engine)

# ==================== 注册路由 ====================
app.include_router(qa_router)

# ==================== 静态文件目录 ====================
STATIC_DIR = Path("static")
STATIC_DIR.mkdir(exist_ok=True)          # 如果目录不存在则创建
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# ==================== 健康检查 ====================
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "rsod-web-platform",
        "version": "1.0.0"
    }

# ==================== 根路径 ====================
@app.get("/")
async def root():
    return {"message": "欢迎使用遥感目标智能检测平台"}

# ==================== 单图检测接口 ====================
@app.post("/detection/single")
async def detect_single_image(
    file: UploadFile = File(...),
    model_name: str = Form("rsod-yolo11n")
):
    # 情况1：模型未加载
    if model is None:
        return {
            "success": False,
            "message": "模型服务未就绪，请检查后端模型文件"
        }

    try:
        # 1. 读取并转换上传的图片
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data)).convert("RGB")

        # 2. 执行推理
        results = model.predict(source=image, conf=0.5)
        result = results[0]

        # 3. 解析检测结果
        boxes = []
        if result.boxes is not None:
            for box in result.boxes:
                boxes.append({
                    "class_name": model.names[int(box.cls)],
                    "confidence": float(box.conf),
                })

        # 4. 生成标注图片并保存到 static 目录
        # 注意：result.plot() 返回 numpy 数组 (BGR 格式)
        import cv2
        annotated_img_bgr = result.plot()
        annotated_img_rgb = cv2.cvtColor(annotated_img_bgr, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(annotated_img_rgb)

        # 生成唯一文件名
        filename = f"result_{uuid.uuid4().hex}.jpg"
        filepath = STATIC_DIR / filename
        pil_img.save(filepath, quality=95)

        # 构造访问 URL（前端将通过代理或直接请求该地址）
        result_image_url = f"/static/{filename}"

        # 5. 返回结果
        return {
            "success": True,
            "data": {
                "total_objects": len(boxes),
                "detection_time": round(result.speed.get('inference', 0) / 1000, 2),
                "model_name": model_name,
                "boxes": boxes,
                "result_image_url": result_image_url
            }
        }

    except Exception as e:
        print(f"❌ 检测失败: {e}")
        return {
            "success": False,
            "message": f"检测失败: {str(e)}"
        }

# ==================== 启动入口 ====================
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True      # 开发模式自动重载，生产环境建议去掉
    )