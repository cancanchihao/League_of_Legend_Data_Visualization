package com.example.lol.service;

import java.util.List;

import com.baomidou.mybatisplus.extension.service.IService;
import com.example.lol.common.CloudDiagram;
import com.example.lol.pojo.Hero;

public interface HeroService extends IService<Hero> {
    public List<CloudDiagram> getCloudDiagram(String matchType);

}
