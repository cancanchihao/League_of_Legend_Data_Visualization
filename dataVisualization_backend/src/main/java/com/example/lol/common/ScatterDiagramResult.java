package com.example.lol.common;

import com.example.lol.pojo.Player;

import lombok.Data;

@Data
public class ScatterDiagramResult {
    private String player;
    private double gold;
    private double CS;
    private double damage;
    private double tanking;

    public ScatterDiagramResult(Player player) {
        this.player = player.getPlayer_name();
        this.gold = player.getGold_per_minute();
        this.CS = player.getCS_per_minute();
        this.damage = player.getDamage_per_game();
        this.tanking = player.getTanking_per_game();
    }
}
