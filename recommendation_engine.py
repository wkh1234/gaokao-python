import os
import json
from typing import List, Optional, Dict
from datetime import datetime
from dotenv import load_dotenv

from models import (
    UserProfile, School, Major, 
    RecommendationResponse, SchoolRecommendation, MajorRecommendation,
    MatchLevel, StudentCategory
)
from supabase_client import SupabaseClient

load_dotenv()

class RecommendationEngine:
    """基于规则和AI的高考志愿推荐引擎"""
    
    def __init__(self, supabase_client: SupabaseClient):
        self.supabase = supabase_client
        self._use_ai = os.getenv("OPENAI_API_KEY") is not None
    
    def calculate_admission_probability(self, user_score: int, school_min_score: int) -> int:
        """
        计算录取概率
        基于考生分数与学校最低录取分的差值
        """
        score_diff = user_score - school_min_score
        
        if score_diff >= 50:
            return min(98, 90 + score_diff // 5)
        elif score_diff >= 30:
            return 85 + (score_diff - 30) // 2
        elif score_diff >= 20:
            return 75 + (score_diff - 20) * 2
        elif score_diff >= 10:
            return 60 + (score_diff - 10) * 1.5
        elif score_diff >= 0:
            return 50 + score_diff
        elif score_diff >= -10:
            return 35 + (score_diff + 10) * 1.5
        elif score_diff >= -20:
            return 20 + (score_diff + 20)
        else:
            return max(5, 15 + score_diff)
    
    def get_match_level(self, probability: int) -> MatchLevel:
        """根据录取概率确定匹配级别"""
        if probability >= 70:
            return MatchLevel.SAFE
        elif probability >= 40:
            return MatchLevel.MEDIUM
        else:
            return MatchLevel.CHALLENGE
    
    def _generate_school_match_reason(self, school: School, user: UserProfile, probability: int) -> str:
        """生成学校匹配原因"""
        reasons = []
        
        if user.preferred_locations:
            if school.province in user.preferred_locations:
                reasons.append(f"学校位于您偏好的{school.province}地区")
        
        if user.preferred_categories:
            if school.category in user.preferred_categories:
                reasons.append(f"属于您喜欢的{school.category}类型")
        
        if probability >= 70:
            reasons.append(f"您的分数超出该校{user.score - school.min_score}分，录取概率较高")
        elif probability >= 40:
            reasons.append(f"您的分数略低于该校分数线，需要一定运气")
        
        if "985" in school.level or "211" in school.level:
            reasons.append(f"该校为{school.level}高校，学校实力雄厚")
        
        if not reasons:
            reasons.append("该校综合实力与您的分数较为匹配")
        
        return "；".join(reasons[:3])
    
    def _generate_school_advice(self, school: School, user: UserProfile, probability: int, match_level: MatchLevel) -> str:
        """生成填报建议"""
        if match_level == MatchLevel.SAFE:
            return f"建议将该校作为第一志愿填报，专业选择余地较大。可优先考虑{school.hot_majors[0] if school.hot_majors else '热门专业'}。"
        elif match_level == MatchLevel.MEDIUM:
            return f"建议将该校放在第二或第三志愿，专业选择时建议服从调剂以增加录取机会。"
        else:
            return f"建议将该校作为冲刺志愿，专业选择时建议选择相对冷门的专业，并服从调剂降低风险。"
    
    def _generate_major_match_reason(self, major: Major, user: UserProfile) -> List[str]:
        """生成专业匹配原因"""
        reasons = []
        
        if user.preferred_professions:
            for profession in user.preferred_professions:
                if profession in major.careers:
                    reasons.append(f"该专业可以从事您感兴趣的{profession}职业")
                    break
        
        if user.interests:
            interest_map = {
                "科技": ["计算机", "电子", "通信", "人工智能"],
                "金融": ["金融", "经济", "会计"],
                "医学": ["医学", "临床", "口腔", "药学"],
                "工程": ["工程", "机械", "土木", "电气"],
                "法律": ["法学", "法律"],
                "教育": ["教育", "师范"]
            }
            for interest in user.interests:
                if interest in interest_map:
                    for keyword in interest_map[interest]:
                        if keyword in major.name:
                            reasons.append(f"您对{interest}领域感兴趣，该专业非常适合")
                            break
        
        if not reasons:
            reasons.append(f"{major.hot_level}{major.category}专业，就业前景广阔")
        
        return reasons[:3]
    
    async def generate_recommendations(self, user_profile: UserProfile) -> RecommendationResponse:
        """生成智能推荐"""
        # 获取所有学校和专业
        all_schools = await self.supabase.get_schools(limit=100)
        all_majors = await self.supabase.get_majors(limit=50)
        
        # 计算每所学校的录取概率
        school_recommendations = []
        for school in all_schools:
            probability = self.calculate_admission_probability(user_profile.score, school.min_score)
            match_level = self.get_match_level(probability)
            
            reason = self._generate_school_match_reason(school, user_profile, probability)
            advice = self._generate_school_advice(school, user_profile, probability, match_level)
            
            school_recommendations.append(SchoolRecommendation(
                school=school,
                probability=probability,
                match_level=match_level,
                match_reason=reason,
                advice=advice
            ))
        
        # 按概率排序
        school_recommendations.sort(key=lambda x: x.probability, reverse=True)
        
        # 分类
        safe_schools = [s for s in school_recommendations if s.match_level == MatchLevel.SAFE][:10]
        medium_schools = [s for s in school_recommendations if s.match_level == MatchLevel.MEDIUM][:10]
        challenge_schools = [s for s in school_recommendations if s.match_level == MatchLevel.CHALLENGE][:10]
        
        # 专业推荐
        major_recommendations = []
        for major in all_majors:
            reasons = self._generate_major_match_reason(major, user_profile)
            
            # 计算匹配度分数
            match_score = 60 + len(reasons) * 10
            
            major_recommendations.append(MajorRecommendation(
                major=major,
                match_score=min(100, match_score),
                match_reasons=reasons,
                career_prospects=f"该专业毕业生就业前景广阔，主要就业方向包括：{', '.join(major.careers[:3])}等"
            ))
        
        # 按匹配度排序
        major_recommendations.sort(key=lambda x: x.match_score, reverse=True)
        recommended_majors = major_recommendations[:10]
        
        # 生成AI分析总结
        ai_analysis = self._generate_ai_analysis(user_profile, safe_schools, medium_schools, recommended_majors)
        
        return RecommendationResponse(
            user_profile=user_profile,
            safe_schools=safe_schools,
            medium_schools=medium_schools,
            challenge_schools=challenge_schools,
            recommended_majors=recommended_majors,
            ai_analysis=ai_analysis
        )
    
    def _generate_ai_analysis(self, user_profile: UserProfile, safe: List, medium: List, majors: List) -> str:
        """生成AI分析总结"""
        analysis_parts = []
        
        # 基本情况分析
        analysis_parts.append(f"您的分数为{user_profile.score}分（{user_profile.category.value}），")
        
        if safe:
            top_school = safe[0]
            analysis_parts.append(f"稳妥志愿可重点关注{top_school.school.name}（录取概率约{top_school.probability}%）。")
        
        if medium:
            analysis_parts.append(f"适当考虑{medium[0].school.name}作为冲击目标。")
        
        if majors:
            top_major = majors[0]
            analysis_parts.append(f"专业方面，{top_major.major.name}与您的兴趣较为匹配。")
        
        analysis_parts.append("建议综合考虑学校实力、地理位置、专业前景等因素，合理安排志愿顺序。")
        
        return "".join(analysis_parts)


class CrewAIRecommendationEngine(RecommendationEngine):
    """基于CrewAI的增强推荐引擎"""
    
    def __init__(self, supabase_client: SupabaseClient):
        super().__init__(supabase_client)
        self._use_ai = True
        self._init_crew()
    
    def _init_crew(self):
        """初始化CrewAI crew"""
        try:
            from crewai import Agent, Task, Crew
            from crewai_tools import SerpAPIWrapper
            
            # 创建工具
            search_tool = SerpAPIWrapper(
                serpapi_api_key=os.getenv("SERPAPI_KEY")
            ) if os.getenv("SERPAPI_KEY") else None
            
            # 创建代理
            self.school_expert = Agent(
                role="高考志愿规划专家",
                goal="根据考生分数和偏好推荐最合适的学校",
                backstory="你是一位有10年经验的高考志愿填报专家，熟悉全国各大高校的录取规则和专业特色。",
                tools=[search_tool] if search_tool else []
            )
            
            self.major_expert = Agent(
                role="专业选择顾问",
                goal="根据考生的兴趣和职业规划推荐最合适的专业",
                backstory="你是一位专业的职业规划师，精通各类专业的学习内容和就业前景。",
                tools=[search_tool] if search_tool else []
            )
            
            self.analyst = Agent(
                role="数据分析员",
                goal="分析录取数据，提供精准的概率计算",
                backstory="你是一位数据分析专家，擅长处理各类录取统计数据。",
                tools=[]
            )
            
            self.crew = Crew(
                agents=[self.school_expert, self.major_expert, self.analyst],
                verbose=True
            )
            
        except ImportError:
            print("CrewAI not installed, using fallback engine")
            self._use_ai = False
    
    async def generate_recommendations(self, user_profile: UserProfile) -> RecommendationResponse:
        """使用CrewAI生成增强推荐"""
        if not self._use_ai or not hasattr(self, 'crew'):
            return await super().generate_recommendations(user_profile)
        
        try:
            from crewai import Task
            
            # 创建任务
            school_task = Task(
                description=f"根据用户信息（分数:{user_profile.score}，类别:{user_profile.category.value}，省份:{user_profile.province}）分析推荐合适的学校",
                agent=self.school_expert,
                expected_output="JSON格式的学校推荐列表"
            )
            
            major_task = Task(
                description=f"根据用户偏好（兴趣:{user_profile.interests}，职业方向:{user_profile.preferred_professions}）推荐合适的专业",
                agent=self.major_expert,
                expected_output="JSON格式的专业推荐列表"
            )
            
            # 执行crew
            result = self.crew.kickoff(inputs={
                'user_score': user_profile.score,
                'user_category': user_profile.category.value,
                'user_province': user_profile.province,
                'interests': user_profile.interests,
                'preferred_professions': user_profile.preferred_professions
            })
            
            # 这里可以解析crew的输出并整合到推荐结果中
            # 暂时使用基础引擎的结果
            return await super().generate_recommendations(user_profile)
            
        except Exception as e:
            print(f"CrewAI error: {e}, falling back to basic engine")
            return await super().generate_recommendations(user_profile)
