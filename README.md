# Note App
SnB.001

### 后续计划
会有两个版本：
1. Standalone版本，主要就是本地记录存取整理相关的；
2. Server版本，会增加AI推荐相关的内容。

## 项目描述
一个简单的笔记应用，支持用户注册、登录、笔记管理和标签管理功能。

## 安装步骤

### 后端

1. 导航到 `backend` 目录
2. 创建虚拟环境并安装依赖
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
3. 下载 MongoDB Community Server：
   https://www.mongodb.com/try/download/community 
   下载对应的安装程序
   
4. 导航到 `note_app` 目录,运行后端服务器
   ```bash
   python .\backend\app.py

### 前端
1. 导航到 frontend 目录
2. 创建虚拟环境并安装依赖
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
3. 运行前端应用
   ```bash
   python app.py
   
## 说明
使用 dash-mantine-components 需要注意：
### React 18 Issue
    Dash Mantine Components is based on REACT 18. You must set the env variable REACT_VERSION=18.2.0 before starting up the app.

    npm install react@18.2.0 react-dom@18.2.0
    
    如果安装失败可以尝试使用其他 npm 镜像源
    npm config set registry https://registry.npmmirror.com/
