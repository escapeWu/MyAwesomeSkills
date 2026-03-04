# Skill: coinglass-liquidation-heatmap

## 1. 简介
专门用于访问 Coinglass 清算热力图页面，获取指定币种截图并上传到文件管理模块。

> 本 Skill 只负责“打开页面 -> 截图 -> 上传”，不做任何图像内容分析。

## 2. 核心指令
- **页面 URL**: `https://www.coinglass.com/zh/pro/futures/LiquidationHeatMap?coin={COIN}`
  - 默认币种为 `BTC`。
  - 切换币种示例: `?coin=ETH`, `?coin=SOL`。
- **上传接口**: `POST /api/files/upload`
- **鉴权方式**: `Authorization: Bearer <API_KEY>`

## 3. 操作流程
1. **初始化连接**
   - 必须使用 `profile="chrome"`。
   - 检查 Browser Relay 状态。如果未连接，提醒用户点击 Chrome 插件图标。

2. **页面导航**
   - 构造目标 URL（含 `?coin=` 参数）并调用 `browser:open`。

3. **骨架侦察 (`snapshot`)**
   - 调用 `browser:snapshot(refs: "aria")`。
   - 确认标题（例如 `Binance {COIN}/USDT 清算热力图`）已加载，确保数据渲染完成。
   - 识别图表容器的 `ref`（通常包含 `canvas` 元素）。

4. **精准截图 (`screenshot`)**
   - 调用 `browser:screenshot`。
   - 建议使用 `fullPage: false` 截取当前视口，或针对图表容器 `ref` 进行局部截图。

5. **生成上传文件名**
   - 文件名格式必须为：`coinglass-[coinpair]-yyyy-mm-dd-liquid`
   - `coinpair` 规则：将交易对转为去斜杠大写格式（如 `BTC/USDT -> BTCUSDT`）。
   - 日期规则：按 `yyyy-mm-dd` 生成（推荐使用当日 UTC 日期，保持一致）。
   - 上传时 `file` 的文件名必须使用该规范，不添加额外前后缀。

6. **上传截图**
   - 发起 `POST /api/files/upload`。
   - `Headers`:
     - `Authorization: Bearer <API_KEY>`
   - `Content-Type`: `multipart/form-data`
   - `FormData` 字段：
     - `file`: 截图文件（二进制）

## 4. 返回结构规范
返回结果必须是上传结果，不包含任何支撑阻力或流动性分析字段。推荐结构如下：

```json
{
  "coin": "BTC",
  "coinpair": "BTCUSDT",
  "filename": "coinglass-BTCUSDT-2026-03-04-liquid",
  "upload": {
    "key": "...",
    "url": "..."
  },
  "source_page": "https://www.coinglass.com/zh/pro/futures/LiquidationHeatMap?coin=BTC"
}
```

## 5. 失败处理
- **页面未加载到目标图表**：返回页面加载失败并提示重试。
- **上传失败**：返回 HTTP 状态码与错误信息，不执行任何分析回退。

## 6. 注意事项
- 不做图像内容分析，不输出“支撑/阻力/流动性磁石”等分析段落。
- 文件名规范必须固定为：`coinglass-[coinpair]-yyyy-mm-dd-liquid`。
- API Key 必须通过环境变量或运行环境注入，禁止在文档或代码中硬编码。
