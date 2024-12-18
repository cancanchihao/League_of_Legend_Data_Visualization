package com.example.lol.pojo;

import com.baomidou.mybatisplus.annotation.TableName;

import lombok.Data;

@Data
@TableName("hero")
public class Hero {
    private String hero_name;
    private String position;
    private String matchType;
    private int pick_count;
    private int ban_count;
    private int win_count;
    private int matches_played;
    private double pick_rate;
    private double ban_rate;
    private double win_rate;

}
