package com.example.lol.pojo;

import com.baomidou.mybatisplus.annotation.TableName;

import lombok.Data;

@Data
@TableName("hero_chosen")
public class HeroChosen {
    private String player_name;
    private String player_team;
    private String player_region;
    private String matchType;
    private int matches_played;
    private int minutes_played;
    private int matches_won;
    private String hero_chosen_1;
    private String hero_chosen_2;
    private String hero_chosen_3;
    private String hero_chosen_4;
    private String hero_chosen_5;
    private String hero_chosen_6;
    private String hero_chosen_7;
    private String hero_chosen_8;
    private String hero_chosen_9;
    private String hero_chosen_10;

}
