package com.example.lol.common;

import com.example.lol.pojo.Hero;

import lombok.Data;

@Data
public class CloudDiagram implements Comparable<CloudDiagram> {
    private String name;
    private int value;

    public CloudDiagram(Hero hero) {
        this.name = hero.getHero_name();
        this.value = hero.getPick_count() + hero.getBan_count();
    }

    @Override
    public int compareTo(CloudDiagram o) {
        return o.getValue() - this.value;
    }
}
