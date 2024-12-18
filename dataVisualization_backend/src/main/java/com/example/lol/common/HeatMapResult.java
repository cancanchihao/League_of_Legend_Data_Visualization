package com.example.lol.common;

import java.util.ArrayList;
import java.util.List;

import lombok.Data;

@Data
public class HeatMapResult {

    List<String> teams;

    List<Object> heatMapDatas;

    public HeatMapResult() {
        this.teams = new ArrayList<>();
        this.heatMapDatas = new ArrayList<>();
    }
}
