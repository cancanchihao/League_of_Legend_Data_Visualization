package com.example.lol.pojo;

import com.baomidou.mybatisplus.annotation.TableName;

import lombok.Data;

@Data
@TableName("hero_distinct")
public class HeroDistinct {

    private String hero_name;
    private String matchType;
    private double pick_rate;
    private double ban_rate;
    private double win_rate;
}
