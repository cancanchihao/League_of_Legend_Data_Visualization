package com.example.lol.common;

import java.util.ArrayList;
import java.util.List;

import lombok.Data;

@Data
public class BarDiagramResult {
    private long totalPage;
    private List<HeroData> herodatas;

    public BarDiagramResult(long totalPage) {
        this.totalPage = totalPage;
        this.herodatas = new ArrayList<>();
    }
}
