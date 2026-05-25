# 智能检测页面布局优化计划

## 一、需求分析

### 当前问题
1. 顶部有4个功能卡片，其中「摄像头」「视频检测」不需要
2. 左右分栏布局拥挤，视觉体验差
3. 图片无法放大查看细节

### 修改需求
1. **模块删减**：保留「单图检测」「批量检测」，删除「摄像头」「视频检测」
2. **布局重构**：改为上下流式排版
3. **交互新增**：图片点击放大查看功能
4. **UI优化**：调整卡片样式、间距、阴影

### 禁止修改内容
- 业务逻辑和接口调用
- 文字内容
- 原有功能
- 核心代码结构

## 二、修改计划

### 1. 功能卡片删减
- 删除 `functionTabs` 数组中的「摄像头」「视频检测」对象

### 2. 布局重构
- 将 `main-content` 的 flex 布局改为 block
- 移除 `left-panel` 和 `right-panel` 的固定宽度限制
- 所有模块改为全屏宽度，上下排列
- 增加模块间距

### 3. 新增图片查看器
- 添加全屏弹窗式图片查看器组件
- 支持放大、缩小、拖拽操作
- 支持点击关闭按钮或空白区域关闭

### 4. UI样式优化
- 统一卡片样式、阴影、圆角
- 调整内边距和间距
- 保持工业简约科技风格

## 三、文件修改

### 修改文件：`frontend/src/views/DetectionPage.vue`

**结构调整**：
```
页面顶部
├── 页面标题区域（面包屑、标题、副标题）
├── 模型选择器（移到标题右侧）
└── 功能卡片栏（居中，2个卡片）

页面主体（上下流式）
├── 检测预览模块（全宽）
├── 检测模型+版本信息模块（全宽）
├── 识别清单模块（全宽）
├── AI诊断建议模块（全宽）
└── 操作按钮模块（全宽）
```

**新增交互**：
- 图片点击触发查看器
- 查看器支持缩放（滚轮）和拖拽

## 四、代码修改要点

### 1. 删除不需要的图标导入
- 删除 `Folder`（摄像头图标）
- 删除 `Monitor`（视频图标）

### 2. 修改 functionTabs 数组
```javascript
const functionTabs = [
  { key: "single", name: "单图检测", desc: "快速识别一张图片", icon: Picture, accept: "image/*", multiple: false },
  { key: "batch", name: "批量检测", desc: "一次处理多张图片", icon: Plus, accept: "image/*", multiple: true },
];
```

### 3. 新增图片查看器状态和方法
```javascript
const showImageViewer = ref(false);
const viewerImageUrl = ref("");
const viewerTitle = ref("");

const openImageViewer = (url, title) => {
  viewerImageUrl.value = url;
  viewerTitle.value = title;
  showImageViewer.value = true;
};

const closeImageViewer = () => {
  showImageViewer.value = false;
};
```

### 4. 修改布局样式
- `.function-tabs` 添加 `justify-content: center`
- `.main-content` 改为 `display: block`
- `.left-panel` 和 `.right-panel` 改为 `width: 100%`
- 添加模块间距类

## 五、注意事项

1. 保持所有业务逻辑不变
2. 保持文字内容不变
3. 响应式适配不同屏幕尺寸
4. 代码符合原有编码规范
