package com.example.lol.service.impl;

import org.springframework.stereotype.Service;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.example.lol.mapper.TeamMapper;
import com.example.lol.pojo.Team;
import com.example.lol.service.TeamService;

@Service
public class TeamServiceImpl extends ServiceImpl<TeamMapper, Team> implements TeamService {

}
