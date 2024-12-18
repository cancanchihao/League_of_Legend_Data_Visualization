package com.example.lol.common;

import com.example.lol.pojo.Team;

import lombok.Data;

@Data
public class TeamCompResult {

    private String name;
    private double baron;
    private double dragon;
    private double turts;
    private double KDA;
    private int winCount;

    public TeamCompResult(Team team, int winCount) {
        this.name = team.getTeam();
        this.baron = team.getBaron_per_game();
        this.dragon = team.getDra_per_game();
        this.turts = team.getTurts_per_game();
        this.KDA = team.getKDA();
        this.winCount = winCount;
    }

}
