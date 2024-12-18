package com.example.lol.service.impl;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.example.lol.mapper.HeroVSMapper;
import com.example.lol.pojo.HeroVS;
import com.example.lol.service.HeroVSService;

@Service
public class HeroVSServiceImpl extends ServiceImpl<HeroVSMapper, HeroVS> implements HeroVSService {

    @Autowired
    private HeroVSMapper heroVSMapper;

    @Override
    public List<HeroVS> getHeroComp(String matchType, String hero1, String hero2) {

        LambdaQueryWrapper<HeroVS> lambdaQueryWrapper = new LambdaQueryWrapper<HeroVS>();

        lambdaQueryWrapper.eq(HeroVS::getMatchType, matchType)
                .and(lqw -> lqw.eq(HeroVS::getHero1_name, hero1).eq(HeroVS::getHero2_name, hero2)
                        .or(qw -> qw.eq(HeroVS::getHero1_name, hero2).eq(HeroVS::getHero2_name, hero1)))
                .orderByDesc(HeroVS::getMatches_played);
        // 此赛段hero1和hero2对位的情况 按照对位次数排序
        List<HeroVS> results = heroVSMapper.selectList(lambdaQueryWrapper);
        return results;
    }

}
