package com.example.lol.common;

import lombok.Data;

@Data
public class TeamVSResult {
    private int matchesWon1;
    private int matchesWon2;
    private int matches;
    private String winRate12;
    private String winRate21;

    public TeamVSResult(int matchesWon1, int matchesWon2) {
        this.matchesWon1 = matchesWon1;
        this.matchesWon2 = matchesWon2;
        this.matches = matchesWon1 + matchesWon2;
        this.winRate12 = String.format("%.2f", ((double) matchesWon1) / matches * 100.0);
        this.winRate21 = String.format("%.2f", ((double) matchesWon2) / matches * 100.0);
    }
}
