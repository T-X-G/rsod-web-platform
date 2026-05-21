# 钢材表面缺陷检测项目修改计划

## 一、项目背景

这是一个前后端分离的YOLO目标检测平台，后端用FastAPI，前端用Vue3，技术栈为YOLO11+FastAPI+Vue3。现需将原来的RSOD遥感4类目标检测（飞机、油罐、立交桥、操场），改成东北大学宋克臣团队的钢材表面缺陷6类检测。

## 二、修改需求

### 目标类别替换
将原有的4类遥感目标替换为以下6种钢材缺陷：

| ID | 英文名称 | 中文名称 | 描述 |
|---|---------|---------|------|
| 0 | crazing | 裂纹 | 钢材表面的裂纹类缺陷 |
| 1 | inclusion | 夹杂物 | 钢材中的非金属夹杂物缺陷 |
| 2 | patches | 斑点 | 钢材表面的斑点状缺陷 |
| 3 | pitted_surface | 麻面 | 钢材表面的麻点、凹坑类缺陷 |
| 4 | rolled_in_scale | 轧入氧化皮 | 钢材轧制过程中形成的氧化皮缺陷 |
| 5 | scratches | 划痕 | 钢材表面的划痕类缺陷 |

### 修改原则
1. 保持原有接口结构、返回格式不变，不影响其他逻辑
2. 保持和原有代码风格一致（注释格式、变量命名）
3. 将与类别相关的逻辑作出相应修改

## 三、修改文件清单

### 1. 后端文件

#### 文件1: `backend/app/api/detection.py`
- **位置**: 第423-428行（目标类别列表接口）
- **修改内容**: 将RSOD 4类目标替换为钢材表面缺陷6类
- **说明**: 修改 `get_target_list()` 函数中的 `targets` 列表

#### 文件2: `backend/app/services/detection_service.py`
- **位置1**: 第293-298行（`_init_class_names()` 方法）
- **修改内容**: 将类别名称映射字典从RSOD 4类替换为钢材缺陷6类

- **位置2**: 第310-316行（`get_class_chinese_name()` 方法）
- **修改内容**: 将中文名称映射字典从RSOD 4类替换为钢材缺陷6类

### 2. 前端文件（可选）

#### 文件3: `frontend/src/api/detection.js`
- **检查内容**: 确认接口调用路径是否正确（当前路径为 `/targets/list`，后端实际路径为 `/detection/targets/list`）
- **说明**: 如果前端调用路径与后端实际路径不一致，需要修改

## 四、修改步骤

### 步骤1: 修改后端API路由文件
修改 `backend/app/api/detection.py` 中的目标类别列表：

```python
# 原代码（第423-428行）
targets = [
    TargetItem(id=0, name="aircraft", chinese_name="飞机", description="固定翼飞机、直升机等"),
    TargetItem(id=1, name="oiltank", chinese_name="油罐", description="储油罐、化工罐等"),
    TargetItem(id=2, name="overpass", chinese_name="立交桥", description="各类立交桥"),
    TargetItem(id=3, name="playground", chinese_name="操场", description="运动场、操场等"),
]

# 修改后
targets = [
    TargetItem(id=0, name="crazing", chinese_name="裂纹", description="钢材表面的裂纹类缺陷"),
    TargetItem(id=1, name="inclusion", chinese_name="夹杂物", description="钢材中的非金属夹杂物缺陷"),
    TargetItem(id=2, name="patches", chinese_name="斑点", description="钢材表面的斑点状缺陷"),
    TargetItem(id=3, name="pitted_surface", chinese_name="麻面", description="钢材表面的麻点、凹坑类缺陷"),
    TargetItem(id=4, name="rolled_in_scale", chinese_name="轧入氧化皮", description="钢材轧制过程中形成的氧化皮缺陷"),
    TargetItem(id=5, name="scratches", chinese_name="划痕", description="钢材表面的划痕类缺陷"),
]
```

### 步骤2: 修改检测服务中的类别映射

修改 `backend/app/services/detection_service.py`：

**位置1**: `_init_class_names()` 方法（第293-298行）

```python
# 原代码
self.class_names = {
    0: "aircraft",    # 飞机
    1: "oiltank",     # 油罐
    2: "overpass",    # 立交桥
    3: "playground",  # 操场
}

# 修改后
self.class_names = {
    0: "crazing",            # 裂纹
    1: "inclusion",          # 夹杂物
    2: "patches",            # 斑点
    3: "pitted_surface",     # 麻面
    4: "rolled_in_scale",    # 轧入氧化皮
    5: "scratches",          # 划痕
}
```

**位置2**: `get_class_chinese_name()` 方法（第310-316行）

```python
# 原代码
chinese_names = {
    "aircraft": "飞机",
    "oiltank": "油罐",
    "overpass": "立交桥",
    "playground": "操场"
}

# 修改后
chinese_names = {
    "crazing": "裂纹",
    "inclusion": "夹杂物",
    "patches": "斑点",
    "pitted_surface": "麻面",
    "rolled_in_scale": "轧入氧化皮",
    "scratches": "划痕"
}
```

### 步骤3: 检查前端API调用路径

检查 `frontend/src/api/detection.js` 中的 `getTargetList()` 函数：

```javascript
// 原代码
export const getTargetList = () => {
  return request({
    url: "/targets/list",  // 这里需要确认是否正确
    method: "get",
  });
};
```

根据后端路由定义，正确路径应为 `/detection/targets/list`，如果不一致需要修改。

## 五、验证测试

修改完成后，建议进行以下验证：

1. **API接口测试**: 调用 `/api/detection/targets/list` 接口，确认返回6类钢材缺陷类别
2. **检测功能测试**: 上传测试图片进行检测，确认类别识别正确
3. **历史记录测试**: 确认历史记录中的类别名称显示正确

## 六、风险提示

1. **模型兼容性**: 确保后端加载的YOLO模型是针对钢材表面缺陷训练的模型（6类）
2. **数据迁移**: 如果数据库中存在旧的RSOD检测记录，可能需要清理或迁移
3. **前端兼容性**: 如果前端有硬编码的类别列表，需要同步修改

## 七、修改影响评估

| 文件 | 修改内容 | 影响范围 |
|-----|---------|---------|
| `backend/app/api/detection.py` | 目标类别列表 | API响应数据 |
| `backend/app/services/detection_service.py` | 类别名称映射 | 检测结果解析、中文名称转换 |
| `frontend/src/api/detection.js` | 接口路径（如需要） | 前端数据获取 |

修改完成后，API接口结构保持不变，仅类别数据发生变化，不会影响其他业务逻辑。
