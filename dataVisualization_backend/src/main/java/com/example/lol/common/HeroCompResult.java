package com.example.lol.common;

import com.example.lol.pojo.HeroVS;

import lombok.Data;

@Data
public class HeroCompResult {

    private String name;
    private int winCount;
    private double KDA;
    private double gold;
    private double damage;
    private double tanking;

    public HeroCompResult(String heroName, HeroVS heroVS) {
        this.name = heroName;
        if (heroName.equals(heroVS.getHero1_name())) {
            this.winCount = heroVS.getMatches_won_1();
            if (heroVS.getHero1_deaths() == 0) {
                this.KDA = heroVS.getHero1_kills() + heroVS.getHero1_assists();
            } else {
                this.KDA = Math.round(
                        (heroVS.getHero1_kills() + heroVS.getHero1_assists()) / (double) heroVS.getHero1_deaths()
                                * 100.0)
                        / 100.0;
            }
            this.gold = Math.round(heroVS.getHero1_gold() / heroVS.getMinutes_played() * 100.0) / 100.0;
            this.damage = Math.round(heroVS.getHero1_damage() / heroVS.getMatches_played() * 100.0) / 100.0;
            this.tanking = Math.round(heroVS.getHero1_tanking() / heroVS.getMatches_played() * 100.0) / 100.0;
        } else {
            this.winCount = heroVS.getMatches_won_2();
            if (heroVS.getHero2_deaths() == 0) {
                this.KDA = heroVS.getHero2_kills() + heroVS.getHero2_assists();
            } else {
                this.KDA = Math.round(
                        (heroVS.getHero2_kills() + heroVS.getHero2_assists()) / (double) heroVS.getHero2_deaths()
                                * 100.0)
                        / 100.0;
            }
            this.gold = Math.round(heroVS.getHero2_gold() / heroVS.getMinutes_played() * 100.0) / 100.0;
            this.damage = Math.round(heroVS.getHero2_damage() / heroVS.getMatches_played() * 100.0) / 100.0;
            this.tanking = Math.round(heroVS.getHero2_tanking() / heroVS.getMatches_played() * 100.0) / 100.0;
        }
    }

    public HeroCompResult(String heroName) {
        this.name = heroName;
        this.winCount = 0;
        this.KDA = 0;
        this.gold = 0;
        this.damage = 0;
        this.tanking = 0;

    }

}
