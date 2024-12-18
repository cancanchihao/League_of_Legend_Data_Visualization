package com.example.lol.controller;

import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

import org.apache.tomcat.util.http.fileupload.IOUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.core.metadata.OrderItem;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.example.lol.common.BarDiagramResult;
import com.example.lol.common.CloudDiagram;
import com.example.lol.common.HeroCompResult;
import com.example.lol.common.HeroData;
import com.example.lol.common.Result;
import com.example.lol.pojo.HeroDistinct;
import com.example.lol.pojo.HeroVS;
import com.example.lol.service.HeroDistinctService;
import com.example.lol.service.HeroService;
import com.example.lol.service.HeroVSService;

import jakarta.servlet.http.HttpServletResponse;

@CrossOrigin
@RestController
@RequestMapping("/hero")
public class HeroController {

    @Autowired
    private HeroService heroService;

    @Autowired
    private HeroDistinctService heroDistinctService;

    @Autowired
    private HeroVSService heroVSService;

    private static final String rootPath = System.getProperty("user.dir") + "\\src\\main\\resources\\";

    @GetMapping("/getCloudDiagram")
    public Result getCloudDiagram(@RequestParam String matchType) {
        try {
            List<CloudDiagram> cloudDiagram = heroService.getCloudDiagram(matchType);
            Collections.sort(cloudDiagram);
            List<CloudDiagram> result = new ArrayList<>(cloudDiagram.subList(0, 30));
            return Result.suc(result, result.size());
        } catch (Exception e) {
            System.err.println(e.getMessage());
            return Result.fail("查询失败！");
        }
    }

    @GetMapping("/heroImg")
    public void getHeroImg(HttpServletResponse res, @RequestParam String heroName) {
        String fileName = heroName + ".png";
        File imgFile = new File(rootPath + "Image\\Heros\\" + fileName);

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

    @GetMapping("/getBarDiagram")
    public Result getBarDiagram(@RequestParam String matchType, @RequestParam long currentPage,
            @RequestParam String sortWay) {
        try {
            int pageSize = 8;
            long totalPage = 0;

            Page<HeroDistinct> page = Page.of(currentPage, pageSize);

            if (currentPage > 0) {

                if (!sortWay.isBlank()) {
                    page.addOrder(OrderItem.desc(sortWay));
                } else {
                    page.addOrder(OrderItem.desc("ban_rate"));
                }

                LambdaQueryWrapper<HeroDistinct> lambdaQueryWrapper = new LambdaQueryWrapper<HeroDistinct>()
                        .eq(HeroDistinct::getMatchType, matchType);

                Page<HeroDistinct> p = heroDistinctService.page(page, lambdaQueryWrapper);
                totalPage = p.getPages();
                BarDiagramResult barDiagramResult = new BarDiagramResult(totalPage);
                List<HeroDistinct> results = p.getRecords();
                for (int i = 0; i < results.size(); i++) {
                    barDiagramResult.getHerodatas().add(new HeroData(results.get(i)));
                }
                return Result.suc(barDiagramResult);

            } else {
                return Result.fail("页码不正确！");
            }
        } catch (Exception e) {
            System.err.println(e.getMessage());
            return Result.fail("查询失败");
        }

    }

    @GetMapping("/getHeroComp")
    public Result getHeroComp(@RequestParam String matchType, @RequestParam String hero1,
            @RequestParam String hero2) {
        try {
            List<HeroVS> heroVSs = heroVSService.getHeroComp(matchType, hero1, hero2);
            if (heroVSs.size() == 0) {
                List<HeroCompResult> heroCompResults = new ArrayList<HeroCompResult>();
                heroCompResults.add(new HeroCompResult(hero1));
                heroCompResults.add(new HeroCompResult(hero2));
                return Result.suc(heroCompResults);
            }
            List<HeroCompResult> heroCompResults = new ArrayList<HeroCompResult>();
            heroCompResults.add(new HeroCompResult(hero1, heroVSs.get(0)));
            heroCompResults.add(new HeroCompResult(hero2, heroVSs.get(0)));
            return Result.suc(heroCompResults);
        } catch (Exception e) {
            System.err.println(e.getMessage());
            return Result.fail("查询失败！");
        }
    }
}