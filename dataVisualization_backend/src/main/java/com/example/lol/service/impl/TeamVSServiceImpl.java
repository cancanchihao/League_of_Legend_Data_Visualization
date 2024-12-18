package com.example.lol.service.impl;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.example.lol.common.TeamVSResult;
import com.example.lol.mapper.TeamVSMapper;
import com.example.lol.pojo.TeamVS;
import com.example.lol.service.TeamVSService;

@Service
public class TeamVSServiceImpl extends ServiceImpl<TeamVSMapper, TeamVS> implements TeamVSService {

    @Autowired
    private TeamVSMapper teamVSMapper;

    @Override
    public String getWinRateBetweenTeams(String team1, String team2, String matchType) {
        String[] teams = new String[2];
        teams[0] = team1;
        teams[1] = team2;
        Arrays.sort(teams);
        LambdaQueryWrapper<TeamVS> lambdaQueryWrapper = new LambdaQueryWrapper<TeamVS>();
        lambdaQueryWrapper.eq(TeamVS::getMatchType, matchType).eq(TeamVS::getTeam1_name, teams[0])
                .eq(TeamVS::getTeam2_name, teams[1]);
        TeamVS selected = teamVSMapper.selectOne(lambdaQueryWrapper);
        if (selected == null) {
            return "-";
        }
        TeamVSResult teamVSResult = new TeamVSResult(selected.getMatches_won_1(), selected.getMatches_won_2());

        if (teams[0].equals(team1)) {
            return teamVSResult.getWinRate21();
        } else {
            return teamVSResult.getWinRate12();
        }
    }

    @Override
    public List<Object> getheatMapData(List<String> teams, String matchType) {
        int size = teams.size();

        List<Object> resultList = new ArrayList<>();

        for (int i = 0; i < size; i++) {
            for (int j = 0; j < size; j++) {
                if (i == j) {
                    resultList.add(new Object[] { i, j, "-" });
                } else {
                    String winRate = getWinRateBetweenTeams(teams.get(i), teams.get(j), matchType);
                    if (winRate.equals("-")) {
                        resultList.add(new Object[] { i, j, "-" });
                    } else {
                        String winRateBetweenTeams = String.format("%.2f",
                                Float.parseFloat(winRate));
                        resultList.add(new Object[] { i, j, Float.parseFloat(winRateBetweenTeams) });
                    }

                }

            }
        }
        return resultList;
    }

    @Override
    public int getWinCountBetweenTeams(String team1, String team2, String matchType) {

        String[] teams = new String[2];
        teams[0] = team1;
        teams[1] = team2;
        Arrays.sort(teams);
        LambdaQueryWrapper<TeamVS> lambdaQueryWrapper = new LambdaQueryWrapper<TeamVS>();
        lambdaQueryWrapper.eq(TeamVS::getMatchType, matchType).eq(TeamVS::getTeam1_name, teams[0])
                .eq(TeamVS::getTeam2_name, teams[1]);
        TeamVS selected = teamVSMapper.selectOne(lambdaQueryWrapper);
        if (selected == null) {
            return 0;
        }
        // 没有交换
        if (teams[0].equals(team1)) {
            return selected.getMatches_won_1();
        } else {
            return selected.getMatches_won_2();
        }

    }

}
