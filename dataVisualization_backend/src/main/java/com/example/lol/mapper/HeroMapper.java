package com.example.lol.mapper;

import java.util.List;

import org.apache.ibatis.annotations.Select;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.example.lol.pojo.Hero;

public interface HeroMapper extends BaseMapper<Hero> {

    @Select("SELECT hero_name, SUM(pick_count) AS pick_count, SUM(ban_count) AS ban_count FROM hero WHERE matchType = #{matchType} GROUP BY hero_name")
    public List<Hero> getCloudDiagram(String matchType);

}
