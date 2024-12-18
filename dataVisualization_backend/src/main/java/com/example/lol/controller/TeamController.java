package com.example.lol.controller;

import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.ArrayList;
import java.util.List;

import org.apache.tomcat.util.http.fileupload.IOUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.example.lol.common.HeatMapResult;
import com.example.lol.common.Result;
import com.example.lol.common.TeamCompResult;
import com.example.lol.common.WinRateResult;
import com.example.lol.pojo.Team;
import com.example.lol.service.TeamService;
import com.example.lol.service.TeamVSService;

import jakarta.servlet.http.HttpServletResponse;

import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;

@CrossOrigin
@RestController
@RequestMapping("/team")
public class TeamController {

    @Autowired
    private TeamService teamService;
    @Autowired
    private TeamVSService teamVSService;

    private static final String rootPath = System.getProperty("user.dir") + "\\src\\main\\resources\\";

    @GetMapping("/getWinRate")
    public Result getWinRate(@RequestParam String matchType) {
        try {
            List<Team> teams = teamService.lambdaQuery().eq(Team::getMatchType, matchType)
                    .select(Team::getTeam, Team::getMatches_won, Team::getMatches_lose, Team::getWin_rate)
                    .orderByDesc(Team::getWin_rate).list();
            List<WinRateResult> results = new ArrayList<WinRateResult>();
            for (int i = 0; i < teams.size(); i++) {
                WinRateResult winRateResult = new WinRateResult(teams.get(i));
                winRateResult.setWin_rate(Math.round((winRateResult.getWin_rate() * 100) * 100.0) / 100.0);
                results.add(winRateResult);
            }
            return Result.suc(results, results.size());
        } catch (Exception e) {
            System.err.println(e.getMessage());
            return Result.fail("查询失败！");
        }
    }

    @GetMapping("/getHeatMap")
    public Result getHeatMap(@RequestParam String matchType) {
        try {
            List<Team> teams = teamService.lambdaQuery().eq(Team::getMatchType, matchType).select(Team::getTeam).list();
            HeatMapResult heatMapResult = new HeatMapResult();
            for (int i = 0; i < teams.size(); i++) {
                heatMapResult.getTeams().add(teams.get(i).getTeam());
            }
            heatMapResult.setHeatMapDatas(teamVSService.getheatMapData(heatMapResult.getTeams(), matchType));
            return Result.suc(heatMapResult, teams.size());
        } catch (Exception e) {
            System.err.println(e.getMessage());
            return Result.fail("查询失败！");
        }
    }

    @GetMapping("/teamImg")
    public void getHeroImg(HttpServletResponse res, @RequestParam String teamName, @RequestParam String matchType) {
        String fileName = teamName + ".png";
        File imgFile = new File(rootPath + "Image\\Teams\\" + matchType + "\\" + fileName);

        if (!imgFile.exists()) {
            res.setStatus(HttpServletResponse.SC_NOT_FOUND);
            return;
        }

        try (InputStream is = new FileInputStream(imgFile); OutputStream os = res.getOutputStream()) {
            res.setContentType("application/x-png");
            IOUtils.copy(is, os);
        } catch (Exception e) {
            System.err.println(e.getMessage());
            res.setStatus(HttpServletResponse.SC_INTERNAL_SERVER_ERROR);
        }
    }

    @GetMapping("/getTeamComp")
    public Result getTeamComp(@RequestParam String matchType, @RequestParam String team1, @RequestParam String team2) {

        try {
            List<TeamCompResult> teamCompResults = new ArrayList<TeamCompResult>();
            teamCompResults.add(new TeamCompResult(
                    teamService.lambdaQuery().eq(Team::getMatchType, matchType).eq(Team::getTeam, team1).one(),
                    teamVSService.getWinCountBetweenTeams(team1, team2, matchType)));
            teamCompResults.add(new TeamCompResult(
                    teamService.lambdaQuery().eq(Team::getMatchType, matchType).eq(Team::getTeam, team2).one(),
                    teamVSService.getWinCountBetweenTeams(team2, team1, matchType)));
            return Result.suc(teamCompResults);
        } catch (Exception e) {
            System.err.println(e.getMessage());
            return Result.fail("查询失败！");
        }

    }

}
