package com.example.lol.controller;

import java.util.ArrayList;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.example.lol.common.BoxPlotResult;
import com.example.lol.common.PlayerCompResult;
import com.example.lol.common.Result;
import com.example.lol.common.ScatterDiagramResult;
import com.example.lol.pojo.Player;
import com.example.lol.service.PlayerService;

@CrossOrigin
@RestController
@RequestMapping("/player")
public class PlayerController {

    @Autowired
    private PlayerService playerService;

    @GetMapping("/getBoxPlot")
    public Result getBoxPlot(@RequestParam String matchType) {
        try {
            List<Player> players = playerService.lambdaQuery().eq(Player::getMatchType, matchType).list();
            List<BoxPlotResult> boxPlotResults = new ArrayList<BoxPlotResult>();
            for (int i = 0; i < players.size(); i++) {
                BoxPlotResult temp = new BoxPlotResult(players.get(i));
                boxPlotResults.add(temp);
            }
            return Result.suc(boxPlotResults, boxPlotResults.size());
        } catch (Exception e) {
            System.err.println(e.getMessage());
            return Result.fail("查询失败！");
        }
    }

    @GetMapping("/getScatterDiagram")
    public Result getScatterDiagram(@RequestParam String matchType) {
        try {
            List<Player> players = playerService.lambdaQuery().eq(Player::getMatchType, matchType).list();
            List<ScatterDiagramResult> scatterDiagramResults = new ArrayList<ScatterDiagramResult>();
            for (int i = 0; i < players.size(); i++) {
                ScatterDiagramResult temp = new ScatterDiagramResult(players.get(i));
                scatterDiagramResults.add(temp);
            }
            return Result.suc(scatterDiagramResults, scatterDiagramResults.size());
        } catch (Exception e) {
            System.err.println(e.getMessage());
            return Result.fail("查询失败！");
        }
    }

    @GetMapping("/getPlayerComp")
    public Result getPlayerComp(@RequestParam String matchType, @RequestParam String team1,
            @RequestParam String team2) {
        try {
            List<PlayerCompResult> playerCompResults = new ArrayList<PlayerCompResult>();
            List<Player> team1Players = playerService.lambdaQuery().eq(Player::getMatchType, matchType)
                    .eq(Player::getTeam, team1).orderByDesc(Player::getMatches_played).list();
            List<Player> team2Players = playerService.lambdaQuery().eq(Player::getMatchType, matchType)
                    .eq(Player::getTeam, team2).orderByDesc(Player::getMatches_played).list();
            String[] order = { "TOP", "JUG", "MID", "ADC", "SUP" };
            for (int i = 0; i < order.length; i++) {
                for (int j = 0; j < team1Players.size(); j++) {
                    if (team1Players.get(j).getPosition().equals(order[i])) {
                        playerCompResults.add(new PlayerCompResult(team1Players.get(j)));
                        break;
                    }
                }
                for (int k = 0; k < team2Players.size(); k++) {
                    if (team2Players.get(k).getPosition().equals(order[i])) {
                        playerCompResults.add(new PlayerCompResult(team2Players.get(k)));
                        break;
                    }
                }
            }

            return Result.suc(playerCompResults);
        } catch (Exception e) {
            System.err.println(e.getMessage());
            return Result.fail("查询失败！");
        }
    }
}
