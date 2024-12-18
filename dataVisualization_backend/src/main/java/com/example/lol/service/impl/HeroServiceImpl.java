package com.example.lol.service.impl;

import java.util.ArrayList;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.example.lol.common.CloudDiagram;
import com.example.lol.mapper.HeroMapper;
import com.example.lol.pojo.Hero;
import com.example.lol.service.HeroService;

@Service
public class HeroServiceImpl extends ServiceImpl<HeroMapper, Hero> implements HeroService {

    @Autowired
    private HeroMapper heroMapper;

    @Override
    public List<CloudDiagram> getCloudDiagram(String matchType) {
        List<Hero> heros = heroMapper.getCloudDiagram(matchType);
        List<CloudDiagram> cloudDiagram = new ArrayList<CloudDiagram>();
        for (int i = 0; i < heros.size(); i++) {
            CloudDiagram temp = new CloudDiagram(heros.get(i));
            cloudDiagram.add(temp);
        }
        return cloudDiagram;
    }

}
