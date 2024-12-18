package com.example.lol.pojo;

import com.baomidou.mybatisplus.annotation.TableName;

import lombok.Data;

@Data
@TableName("team")
public class Team {
    private String team;
    private String region;
    private String matchType;
    private int Baron;
    private int Dra;
    private int Turts;
    private int kills;
    private int deaths;
    private int assists;
    private int CS;
    private int gold;
    private double damage;
    private double tanking;
    private int matches_played;
    private int matches_won;
    private double minutes_played;
    private int matches_lose;
    private double win_rate;
    private double Baron_per_game;
    private double Dra_per_game;
    private double Turts_per_game;
    private double kills_per_game;
    private double deaths_per_game;
    private double assists_per_game;
    private double CS_per_minute;
    private double gold_per_minute;
    private double damage_per_game;
    private double tanking_per_game;
    private double KDA;
}
