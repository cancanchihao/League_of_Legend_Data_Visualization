package com.example.lol.pojo;

import com.baomidou.mybatisplus.annotation.TableName;

import lombok.Data;

@Data
@TableName("player")
public class Player {
    private String player_name;
    private String team;
    private String region;
    private String matchType;
    private String position;
    private int kills;
    private int deaths;
    private int assists;
    private int CS;
    private int gold;
    private int damage;
    private int tanking;
    private int matches_played;
    private int matches_won;
    private double minutes_played;
    private int matches_lose;
    private double win_rate;
    private double kills_per_game;
    private double deaths_per_game;
    private double assists_per_game;
    private double CS_per_minute;
    private double gold_per_minute;
    private double damage_per_game;
    private double tanking_per_game;
    private double KDA;

}
