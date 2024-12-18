package com.example.lol.pojo;

import com.baomidou.mybatisplus.annotation.TableName;

import lombok.Data;

@Data
@TableName("team_vs")
public class TeamVS {
    private String Team1_name;
    private String Team1_region;
    private String Team2_name;
    private String Team2_region;
    private String matchType;
    private int matches_played;
    private double minutes_played;
    private int matches_won_1;
    private int matches_won_2;
    private int Team1_Baron;
    private int Team1_Dra;
    private int Team1_Turts;
    private int Team1_kills;
    private int Team1_deaths;
    private int Team1_assists;
    private int Team1_CS;
    private int Team1_gold;
    private double Team1_damage;
    private double Team1_tanking;
    private int Team2_Baron;
    private int Team2_Dra;
    private int Team2_Turts;
    private int Team2_kills;
    private int Team2_deaths;
    private int Team2_assists;
    private int Team2_CS;
    private int Team2_gold;
    private double Team2_damage;
    private double Team2_tanking;

}
