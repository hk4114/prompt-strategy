# 提示词生成器

## 快速启动 (Quick Start)

项目提供了一键启动脚本，可自动安装依赖并同时启动前后端：

```bash
./start_demo.sh
```

## 手动启动 (Manual Start)

如果你需要分别启动或调试：

### 启动后端
```sh
cd demo/backend
pip install -r requirements.txt
python run.py
```

### 启动前端
```sh
cd demo/frontend
npm install
npm run dev
```

## to do list
- [x] 部署
- [x] 首页导航
- [x] 最小公式
- [ ] 复杂智能体
- [ ] MIPROv2 + DSPY 实现 APO（自动提示优化）