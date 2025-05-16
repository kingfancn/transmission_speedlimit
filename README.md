# Transmission 自动限速脚本

基于 Tracker 的白名单机制，自动对非指定 Tracker 的种子进行上传/下载限速的Transmission管理工具

## 功能特性

- ✅ 智能限速 - 对非白名单Tracker的种子自动限制上传速度
- 🛡️ 状态检查 - 仅修改需要调整的限速设置，避免重复操作
- ⚡ 批量操作 - 支持一键取消所有种子的限速限制
- 🔒 安全认证 - 支持Transmission RPC认证机制
- 📊 状态反馈 - 实时显示操作进度和结果统计

## 快速开始

### 环境要求

- Python 3.6+
- Transmission客户端（需启用RPC）

### 安装依赖

```bash
pip install transmission-rpc

## 🚀 使用说明

### 快速命令指南

| 操作类型       | 命令                     | 效果说明                  |
|----------------|--------------------------|--------------------------|
| 应用限速规则   | `python script.py 1`     | 对非白名单Tracker种子限速  |
| 取消所有限速   | `python script.py 0`     | 完全移除所有限速设置       |

### 详细使用场景

#### 场景1：应用智能限速
```bash
# 对非白名单Tracker的种子自动限速（上传10KB/s，下载不限速）
python script.py 1

# 输出示例：
发现匹配种子 ID: 42, hash: A1B2C3D4E5 已应用限速设置
发现匹配种子 ID: 55, hash: F6G7H8I9J0 已应用限速设置
操作完成，共限速 2 个种子

### 配置更改
在代码中更改以下配置适配自己环境
# Transmission RPC 配置
RPC_HOST = '192.168.1.132'
RPC_PORT = 9091
RPC_USERNAME = 'admin'  # 如果没有认证，留空
RPC_PASSWORD = 'admin'

# 限速配置
DOWNLOAD_LIMIT = 0  # 单位：KB/s
UPLOAD_LIMIT = 10  # 单位：KB/s
TARGET_TRACKERS = [  # 目标Tracker白名单列表
    'm-team.cc', 'audiences.me', 'cinefiles.info'
    # 添加更多需要排除的Tracker...
]