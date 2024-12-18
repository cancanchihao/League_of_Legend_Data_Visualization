package com.example.lol.common;

import com.example.lol.pojo.Team;

import lombok.Data;

@Data
public class WinRateResult {
    private String team;
    private int matches_won;
    private int matches_lose;
    private double win_rate;

    public WinRateResult(Team team) {
        this.team = team.getTeam();
        this.matches_won = team.getMatches_won();
        this.matches_lose = team.getMatches_lose();
        this.win_rate = team.getWin_rate();
    }

}
