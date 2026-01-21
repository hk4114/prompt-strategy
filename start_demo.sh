#!/bin/bash

# start_demo.sh
# 
# 用途：一键启动 Prompt Strategy Demo 项目（包含后端和前端）
# 使用方式：./start_demo.sh
#
# 该脚本会自动：
# 1. 检查必要环境 (Python, Node.js, npm)
# 2. 自动处理 Python 虚拟环境和依赖安装
# 3. 自动安装前端依赖
# 4. 同时启动后端 API 服务和前端开发服务器

set -e  # 遇到错误立即退出

# 定义颜色输出
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO] $1${NC}"
}

log_step() {
    echo -e "${BLUE}[STEP] $1${NC}"
}

log_error() {
    echo -e "${RED}[ERROR] $1${NC}"
}

# 检查命令是否存在
check_command() {
    if ! command -v "$1" &> /dev/null; then
        log_error "$1 未安装，请先安装 $1"
        exit 1
    fi
}

# 环境检查
log_step "正在检查运行环境..."
check_command python3
check_command node
check_command npm

log_info "环境检查通过！"

# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$SCRIPT_DIR"

# ==========================================
# 后端启动逻辑
# ==========================================
log_step "准备启动后端服务..."
cd "$PROJECT_ROOT/demo/backend"

# 检查并创建虚拟环境（推荐做法，避免污染全局环境）
if [ ! -d "venv" ]; then
    log_info "正在创建 Python 虚拟环境 (venv)..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 检查 pip 是否存在（虚拟环境中通常会有）
if ! command -v pip &> /dev/null; then
    log_error "虚拟环境中未找到 pip，请检查 Python 安装"
    exit 1
fi

log_info "正在安装/检查后端依赖..."
pip install -r requirements.txt

log_info "启动后端服务..."
# 后台启动后端服务
python run.py &
BACKEND_PID=$!
log_info "后端服务已在后台启动 (PID: $BACKEND_PID)"

# ==========================================
# 前端启动逻辑
# ==========================================
# 捕获退出信号，确保脚本退出（如 Ctrl+C）时关闭后端服务
cleanup() {
    log_info "正在关闭服务..."
    if kill -0 $BACKEND_PID 2>/dev/null; then
        kill $BACKEND_PID
        log_info "后端服务已停止"
    fi
    exit
}
trap cleanup EXIT INT TERM

# 等待几秒确保后端启动（可选）
sleep 2

log_step "准备启动前端服务..."
cd "$PROJECT_ROOT/demo/frontend"

if [ ! -d "node_modules" ]; then
    log_info "检测到首次运行，正在安装前端依赖..."
    npm install
else
    log_info "node_modules 已存在，跳过 npm install (如果遇到问题请手动执行 npm install)"
fi

log_info "启动前端开发服务器..."
npm run dev

# 注意：脚本会停留在 npm run dev 的执行界面
# 当用户按下 Ctrl+C 停止前端时，trap 会被触发从而关闭后端
