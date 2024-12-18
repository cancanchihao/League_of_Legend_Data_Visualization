package com.example.lol.service;

import java.util.List;

import com.baomidou.mybatisplus.extension.service.IService;
import com.example.lol.pojo.TeamVS;

public interface TeamVSService extends IService<TeamVS> {

    public String getWinRateBetweenTeams(String team1, String team2, String matchType);

    public int getWinCountBetweenTeams(String team1, String team2, String matchType);

    public List<Object> getheatMapData(List<String> teams, String matchType);

}
