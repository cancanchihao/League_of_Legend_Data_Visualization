package com.example.lol.common;

import java.util.ArrayList;
import java.util.List;

import com.example.lol.pojo.Player;

import lombok.Data;

@Data
public class PlayerCompResult {

    private String name;
    private List<Double> stats;

    public PlayerCompResult(Player player) {
        this.name = player.getPlayer_name();
        this.stats = new ArrayList<>();
        this.stats.add(player.getKDA());
        this.stats.add(player.getCS_per_minute());
        this.stats.add(player.getGold_per_minute());
        this.stats.add(player.getDamage_per_game());
        this.stats.add(player.getTanking_per_game());
    }
}
