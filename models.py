from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class StudentCategory(str, Enum):
    LIBERAL_ARTS = "文科"
    SCIENCE = "理科"

class MatchLevel(str, Enum):
    SAFE = "稳妥"      # 录取概率 >= 70%
    MEDIUM = "适中"    # 40% <= 录取概率 < 70%
    CHALLENGE = "冲刺" # 录取概率 < 40%

# 学校模型
class School(BaseModel):
    id: str
    name: str
    province: str
    category: str  # 理工类/综合类/师范类等
    level: str  # 985/211/普通本科
    min_score: int  # 最低录取分
    max_score: int  # 最高录取分
    avg_score: Optional[int] = None  # 平均分
    enrollment_count: Optional[int] = None  # 招生人数
    hot_majors: Optional[List[str]] = []  # 热门专业
    location: Optional[str] = None  # 所在地
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

# 专业模型
class Major(BaseModel):
    id: str
    name: str
    category: str  # 理工类/文史类/经管类等
    degree: str  # 学位
    hot_level: str  # 热门程度
    avg_salary: str  # 平均薪资
    employment_rate: str  # 就业率
    difficulty: str  # 学习难度
    description: str  # 专业介绍
    careers: List[str] = []  # 就业方向
    subjects_required: Optional[List[str]] = []  # 选科要求
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

# 用户画像
class UserProfile(BaseModel):
    user_id: Optional[str] = None
    score: int = Field(..., ge=0, le=750, description="高考分数")
    category: StudentCategory  # 文科/理科
    province: str  # 所在省份
    rank: Optional[int] = None  # 省排名
    interests: Optional[List[str]] = []  # 兴趣爱好
    preferred_locations: Optional[List[str]] = []  # 偏好地区
    preferred_categories: Optional[List[str]] = []  # 偏好学校类别
    preferred_professions: Optional[List[str]] = []  # 偏好职业方向

# 推荐请求
class RecommendationRequest(BaseModel):
    user_profile: UserProfile
    include_safe: bool = True  # 包含稳妥推荐
    include_medium: bool = True  # 包含适中推荐
    include_challenge: bool = True  # 包含冲刺推荐
    max_schools_per_level: int = Field(default=10, ge=1, le=50)  # 每级最多学校数
    max_majors: int = Field(default=10, ge=1, le=50)  # 最多专业数

# 单个推荐结果
class SchoolRecommendation(BaseModel):
    school: School
    probability: int  # 录取概率 0-100
    match_level: MatchLevel
    match_reason: str  # 匹配原因
    advice: str  # 填报建议

class MajorRecommendation(BaseModel):
    major: Major
    match_score: float  # 匹配度 0-100
    match_reasons: List[str]  # 匹配原因
    career_prospects: str  # 职业前景

# 推荐响应
class RecommendationResponse(BaseModel):
    user_profile: UserProfile
    safe_schools: List[SchoolRecommendation] = []  # 稳妥推荐
    medium_schools: List[SchoolRecommendation] = []  # 适中推荐
    challenge_schools: List[SchoolRecommendation] = []  # 冲刺推荐
    recommended_majors: List[MajorRecommendation] = []  # 推荐专业
    ai_analysis: str  # AI分析总结
    generated_at: datetime = Field(default_factory=datetime.now)

# 收藏模型
class Favorite(BaseModel):
    id: str
    user_id: str
    item_id: str
    item_type: str  # school/major
    item_name: str
    created_at: datetime = Field(default_factory=datetime.now)

# 收藏请求
class FavoriteRequest(BaseModel):
    user_id: str
    item_id: str
    item_type: str
    item_name: str

# 概率计算请求
class ProbabilityRequest(BaseModel):
    user_score: int
    school_id: str
    province: Optional[str] = None  # 所在省份（用于省控线计算）

# 概率计算响应
class ProbabilityResponse(BaseModel):
    school_id: str
    school_name: str
    user_score: int
    school_min_score: int
    score_difference: int
    probability: int
    match_level: MatchLevel
    analysis: str
