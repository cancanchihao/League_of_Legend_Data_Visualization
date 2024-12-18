package com.example.lol.common;

import com.example.lol.pojo.HeroDistinct;

import lombok.Data;

@Data
public class HeroData {

    private String name;
    private double banRate;
    private double pickRate;
    private double winRate;

    public HeroData(HeroDistinct heroDistinct) {
        this.name = heroDistinct.getHero_name();
        this.banRate = Math.round((heroDistinct.getBan_rate() * 100) * 100.0) / 100.0;
        this.pickRate = Math.round((heroDistinct.getPick_rate() * 100) * 100.0) / 100.0;
        this.winRate = Math.round((heroDistinct.getWin_rate() * 100) * 100.0) / 100.0;
    }
}
