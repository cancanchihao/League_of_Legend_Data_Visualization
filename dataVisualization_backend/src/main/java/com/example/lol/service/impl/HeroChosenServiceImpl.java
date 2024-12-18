package com.example.lol.service.impl;

import org.springframework.stereotype.Service;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.example.lol.mapper.HeroChosenMapper;
import com.example.lol.pojo.HeroChosen;
import com.example.lol.service.HeroChosenService;

@Service
public class HeroChosenServiceImpl extends ServiceImpl<HeroChosenMapper, HeroChosen> implements HeroChosenService {

}
