package com.example.lol.service.impl;

import org.springframework.stereotype.Service;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.example.lol.mapper.HeroDistinctMapper;
import com.example.lol.pojo.HeroDistinct;
import com.example.lol.service.HeroDistinctService;

@Service
public class HeroDistinctServiceImpl extends ServiceImpl<HeroDistinctMapper, HeroDistinct>
        implements HeroDistinctService {

}
