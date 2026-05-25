/**
 * 缺陷检测库 Mock 数据（简化版）
 * - 每个缺陷包含 15 维工业化信息（部分字段可扩展）
 * - 图片使用本地静态资源：/defects/<slug>/<1..5>.jpg
 */

export interface DefectImage {
  id: number;
  url: string;
}

export interface DefectDetail {
  id: number;
  name: string;
  englishName: string;
  category: string;
  categoryColor: string;
  priority: "高优先级" | "中优先级" | "关键";

  // 核心属性
  description: string;
  causes: string[];
  impact: string[];
  performanceImpact: string;
  commonProcesses: string[];
  detectionDifficulty: string;
  preventionMeasures: string[];
  aiDetectionFocus: string;
  recommendedModels: string[];
  riskLevel: "低" | "中" | "高";

  // 图片和场景
  images: DefectImage[];
  industrialScenario: string;
  detectionSuggestions: string[];
}

export const defectsMockData: DefectDetail[] = [
  {
    id: 1,
    name: "裂纹",
    englishName: "Crazing",
    category: "表面缺陷类",
    categoryColor: "text-red-400 bg-red-500/20",
    priority: "高优先级",
    description:
      "钢材表面出现的线性或分支状断裂痕迹，是严重的结构缺陷，可能直接导致零件报废或使用中破裂",
    causes: [
      "热轧或锻造冷却速率不当",
      "材料内应力释放不充分",
      "加工或运输过程中的机械冲击",
    ],
    impact: ["降低抗拉强度和延展性", "削弱疲劳强度，易扩展为大裂纹"],
    performanceImpact: "显著降低力学性能，可能使寿命大幅缩短，不适合承重用途。",
    commonProcesses: ["热轧", "锻造", "焊接"],
    detectionDifficulty: "微细裂纹难以通过视觉检测，需要高分辨率或超声等手段。",
    preventionMeasures: ["优化热处理工艺", "增加退火消应力"],
    aiDetectionFocus: "裂纹方向性、边界对比度与宽度变化",
    recommendedModels: ["YOLOv8 Large", "YOLOv11m"],
    riskLevel: "高",
    images: [
      { id: 1, url: "/defects/crazing/1.png" },
      { id: 2, url: "/defects/crazing/2.png" },
      { id: 3, url: "/defects/crazing/3.png" },
      { id: 4, url: "/defects/crazing/4.png" },
      { id: 5, url: "/defects/crazing/5.png" },
    ],
    industrialScenario:
      "汽车曲轴、压力容器与锻件在热处理或焊接后可能出现裂纹，需要重点关注。",
    detectionSuggestions: [
      "使用侧光与高分辨率相机",
      "结合非破坏性检测（超声、X光）",
    ],
  },
  {
    id: 2,
    name: "斑点",
    englishName: "Patches",
    category: "表面缺陷类",
    categoryColor: "text-red-400 bg-red-500/20",
    priority: "高优先级",
    description: "表面色差或纹理异常，影响外观与防护性能。",
    causes: ["油污残留", "氧化不均", "储存环境潮湿"],
    impact: ["影响外观", "可能成为腐蚀起点"],
    performanceImpact: "主要影响外观，严重时影响耐腐蚀性。",
    commonProcesses: ["轧制", "酸洗", "表面处理"],
    detectionDifficulty: "色差与纹理差异幅度大，需自适应算法。",
    preventionMeasures: ["加强清洁", "改进酸洗钝化"],
    aiDetectionFocus: "色差区域轮廓与纹理对比",
    recommendedModels: ["YOLOv11n", "YOLOv8m"],
    riskLevel: "中",
    images: [
      { id: 1, url: "/defects/patches/1.png" },
      { id: 2, url: "/defects/patches/2.png" },
      { id: 3, url: "/defects/patches/3.png" },
      { id: 4, url: "/defects/patches/4.png" },
      { id: 5, url: "/defects/patches/5.png" },
    ],
    industrialScenario: "酸洗钝化、轧制与储存不当会引发斑点。",
    detectionSuggestions: ["使用偏光或多光谱相机", "建立基准样本库"],
  },
  {
    id: 3,
    name: "划痕",
    englishName: "Scratches",
    category: "表面缺陷类",
    categoryColor: "text-red-400 bg-red-500/20",
    priority: "高优先级",
    description: "线性划伤，通常由摩擦或碰撞产生，影响外观和防护层。",
    causes: ["运输摩擦", "堆放滑动", "加工接触"],
    impact: ["破坏防护层", "降低疲劳强度"],
    performanceImpact: "深划痕会降低疲劳强度并影响装配精度。",
    commonProcesses: ["包装运输", "机械加工"],
    detectionDifficulty: "方向多样且受反光影响，需多角度光照。",
    preventionMeasures: ["改进包装", "规范搬运流程"],
    aiDetectionFocus: "划痕连续性与方向一致性",
    recommendedModels: ["YOLOv11n", "YOLOv8-seg"],
    riskLevel: "中",
    images: [
      { id: 1, url: "/defects/scratches/1.png" },
      { id: 2, url: "/defects/scratches/2.png" },
      { id: 3, url: "/defects/scratches/3.png" },
      { id: 4, url: "/defects/scratches/4.png" },
      { id: 5, url: "/defects/scratches/5.png" },
    ],
    industrialScenario: "冲压、堆放与运输环节是划痕的常见来源。",
    detectionSuggestions: ["多方向照明", "高速相机捕捉细节"],
  },
  {
    id: 4,
    name: "麻面",
    englishName: "Pitted Surface",
    category: "表面状态类",
    categoryColor: "text-orange-400 bg-orange-500/20",
    priority: "中优先级",
    description: "表面粗糙、凹凸不平，影响光洁度和涂层附着。",
    causes: ["轧辊磨损", "酸洗参数不当", "抛光不足"],
    impact: ["降低涂层均匀性", "增加腐蚀风险"],
    performanceImpact: "可能降低防腐能力并影响外观质量。",
    commonProcesses: ["热轧", "酸洗", "抛光"],
    detectionDifficulty: "需统计区域粗糙度参数，光照影响大。",
    preventionMeasures: ["定期维护轧辊", "改进酸洗工艺"],
    aiDetectionFocus: "区域粗糙度与凹陷分布",
    recommendedModels: ["YOLOv11n", "自定义纹理模型"],
    riskLevel: "中",
    images: [
      { id: 1, url: "/defects/pitted surface/1.png" },
      { id: 2, url: "/defects/pitted surface/2.png" },
      { id: 3, url: "/defects/pitted surface/3.png" },
      { id: 4, url: "/defects/pitted surface/4.png" },
      { id: 5, url: "/defects/pitted surface/5.png" },
    ],
    industrialScenario: "轧辊维护不到位和酸洗不当会导致麻面。",
    detectionSuggestions: ["低角度斜光", "粗糙度参考库"],
  },
  {
    id: 5,
    name: "轧入氧化皮",
    englishName: "Rolled-in Scale",
    category: "表面状态类",
    categoryColor: "text-orange-400 bg-orange-500/20",
    priority: "中优先级",
    description: "高温氧化皮被压入表面，形成硬脆缺陷并可能脱落。",
    causes: ["除鳞不彻底", "轧辊污染", "温度控制不当"],
    impact: ["形成凹坑", "降低疲劳强度"],
    performanceImpact: "脱落后形成坑洞，局部疲劳强度显著下降。",
    commonProcesses: ["热轧", "除鳞"],
    detectionDifficulty: "形态不规则，与轧制纹理相似时难以区分。",
    preventionMeasures: ["升级除鳞设备", "严格温度控制"],
    aiDetectionFocus: "暗色不规则区域与纹理方向关系",
    recommendedModels: ["YOLOv8m", "YOLOv11l"],
    riskLevel: "中",
    images: [
      { id: 1, url: "/defects/rolled-in scale/1.png" },
      { id: 2, url: "/defects/rolled-in scale/2.png" },
      { id: 3, url: "/defects/rolled-in scale/3.png" },
      { id: 4, url: "/defects/rolled-in scale/4.png" },
      { id: 5, url: "/defects/rolled-in scale/5.png" },
    ],
    industrialScenario: "除鳞流程故障和轧辊污染是主要原因。",
    detectionSuggestions: ["多光谱成像", "及时检测除鳞效果"],
  },
  {
    id: 6,
    name: "夹杂物",
    englishName: "Inclusions",
    category: "内部缺陷类",
    categoryColor: "text-cyan-400 bg-cyan-500/20",
    priority: "关键",
    description: "钢材内部的非金属杂质，严重影响力学性能与寿命。",
    causes: ["脱氧不完全", "原材料杂质", "精炼不充分"],
    impact: ["降低疲劳强度", "影响冲击韧性"],
    performanceImpact: "显著降低疲劳和冲击性能，影响关键零件可靠性。",
    commonProcesses: ["冶炼", "精炼", "浇铸"],
    detectionDifficulty: "内部缺陷需超声、X光等无损检测手段。",
    preventionMeasures: ["改进精炼工艺", "采用真空冶炼（高端产品）"],
    aiDetectionFocus: "超声回波与X光图像特征",
    recommendedModels: ["超声波AI系统", "X光图像分析模型"],
    riskLevel: "高",
    images: [
      { id: 1, url: "/defects/inclusion/1.png" },
      { id: 2, url: "/defects/inclusion/2.png" },
      { id: 3, url: "/defects/inclusion/3.png" },
      { id: 4, url: "/defects/inclusion/4.png" },
      { id: 5, url: "/defects/inclusion/5.png" },
    ],
    industrialScenario: "承重轴、轴承钢等对夹杂物敏感，需严格控制与检测。",
    detectionSuggestions: ["全体积超声扫描", "建立夹杂物数据库"],
  },
];

export function getDefectById(id: number): DefectDetail | undefined {
  return defectsMockData.find((d) => d.id === id);
}

export function getCategories(): string[] {
  return Array.from(new Set(defectsMockData.map((d) => d.category)));
}

export function getDefectsByCategory(category: string): DefectDetail[] {
  return defectsMockData.filter((d) => d.category === category);
}

export function searchDefects(query: string): DefectDetail[] {
  const q = query.trim().toLowerCase();
  if (!q) return defectsMockData;
  return defectsMockData.filter(
    (d) =>
      d.name.toLowerCase().includes(q) ||
      d.englishName.toLowerCase().includes(q) ||
      d.description.toLowerCase().includes(q),
  );
}
