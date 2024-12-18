package com.example.lol.common;

import com.example.lol.pojo.Player;

import lombok.Data;

@Data
public class BoxPlotResult {
    private String player;
    private int kills;
    private int deaths;
    private int assists;

    public BoxPlotResult(Player player) {
        this.player = player.getPlayer_name();
        this.kills = player.getKills();
        this.deaths = player.getDeaths();
        this.assists = player.getAssists();
    }
}
