package com.example.lol.service;

import java.util.List;

import com.baomidou.mybatisplus.extension.service.IService;
import com.example.lol.pojo.HeroVS;

public interface HeroVSService extends IService<HeroVS> {

    List<HeroVS> getHeroComp(String matchType, String hero1, String hero2);

}
