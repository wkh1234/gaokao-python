from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import os
from dotenv import load_dotenv

from database_client import DatabaseClient

load_dotenv()

app = FastAPI(
    title="高考志愿推荐 API",
    description="高考志愿推荐系统",
    version="1.0.0"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化组件
db_client = DatabaseClient()

# 健康检查
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

# 获取学校列表
@app.get("/api/schools")
async def get_schools(
    province: Optional[str] = None,
    category: Optional[str] = None,
    min_score: Optional[int] = None,
    max_score: Optional[int] = None,
    limit: int = 50
):
    """获取学校列表，支持筛选"""
    try:
        schools = await db_client.get_schools(
            province=province,
            category=category,
            min_score=min_score,
            max_score=max_score,
            limit=limit
        )
        return schools
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 获取学校详情
@app.get("/api/schools/{school_id}")
async def get_school_detail(school_id: str):
    """获取学校详细信息"""
    try:
        school = await db_client.get_school_by_id(school_id)
        if not school:
            raise HTTPException(status_code=404, detail="学校不存在")
        return school
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 获取学校开设的专业
@app.get("/api/schools/{school_id}/majors")
async def get_school_majors(school_id: str):
    """获取学校开设的所有专业"""
    try:
        majors = await db_client.get_school_majors(school_id)
        return {"majors": majors}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 获取专业列表
@app.get("/api/majors")
async def get_majors(
    category: Optional[str] = None,
    hot_level: Optional[str] = None,
    limit: int = 50
):
    """获取专业列表，支持筛选"""
    try:
        majors = await db_client.get_majors(
            category=category,
            hot_level=hot_level,
            limit=limit
        )
        return majors
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 获取专业详情
@app.get("/api/majors/{major_id}")
async def get_major_detail(major_id: str):
    """获取专业详细信息"""
    try:
        major = await db_client.get_major_by_id(major_id)
        if not major:
            raise HTTPException(status_code=404, detail="专业不存在")
        return major
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 获取专业分数线
@app.get("/api/majors/{major_id}/score-lines")
async def get_major_score_lines(major_id: str, school_id: Optional[str] = None):
    """获取专业的历年分数线"""
    try:
        score_lines = await db_client.get_major_score_lines(major_id, school_id)
        return {"score_lines": score_lines}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 获取省份列表
@app.get("/api/provinces")
async def get_provinces():
    """获取所有省份"""
    try:
        provinces = await db_client.get_provinces()
        return {"provinces": provinces}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 获取专业类别列表
@app.get("/api/major-categories")
async def get_major_categories():
    """获取所有专业类别"""
    try:
        categories = await db_client.get_major_categories()
        return {"categories": categories}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 收藏操作
@app.post("/api/favorites")
async def add_favorite(item: dict):
    """添加收藏"""
    try:
        favorite = await db_client.add_favorite(item)
        return {"success": True, "data": favorite}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/favorites/{user_id}")
async def get_favorites(user_id: str):
    """获取用户收藏"""
    try:
        favorites = await db_client.get_favorites(user_id)
        return {"favorites": favorites}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/favorites/{favorite_id}")
async def remove_favorite(favorite_id: str):
    """删除收藏"""
    try:
        await db_client.remove_favorite(favorite_id)
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
