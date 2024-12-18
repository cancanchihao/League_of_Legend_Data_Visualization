package com.example.lol.pojo;

import com.baomidou.mybatisplus.annotation.TableName;

import lombok.Data;

@Data
@TableName("hero_vs")
public class HeroVS {
    private String hero1_name;
    private String hero1_position;
    private String hero2_name;
    private String hero2_position;
    private String matchType;
    private int matches_played;
    private int minutes_played;
    private int matches_won_1;
    private int matches_won_2;
    private int hero1_kills;
    private int hero1_deaths;
    private int hero1_assists;
    private int hero1_CS;
    private int hero1_gold;
    private double hero1_damage;
    private double hero1_tanking;
    private int hero2_kills;
    private int hero2_deaths;
    private int hero2_assists;
    private int hero2_CS;
    private int hero2_gold;
    private double hero2_damage;
    private double hero2_tanking;

}
