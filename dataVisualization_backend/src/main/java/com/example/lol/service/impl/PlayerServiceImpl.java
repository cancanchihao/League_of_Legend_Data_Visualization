package com.example.lol.service.impl;

import org.springframework.stereotype.Service;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.example.lol.mapper.PlayerMapper;
import com.example.lol.pojo.Player;
import com.example.lol.service.PlayerService;

@Service
public class PlayerServiceImpl extends ServiceImpl<PlayerMapper, Player> implements PlayerService {

}
